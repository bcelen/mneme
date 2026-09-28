from __future__ import annotations

import hashlib
import importlib.util
import json
import mailbox
import socket
import tempfile
import types
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from typing import Dict, Tuple
from unittest import mock


PROTOTYPE_ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS_ROOT = PROTOTYPE_ROOT.parent


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MNEME = _load("mneme_local_synthetic_prototype_3", PROTOTYPE_ROOT / "mneme.py")
PROTOTYPE_2 = _load(
    "mneme_local_synthetic_prototype_2_for_comparison",
    EXPERIMENTS_ROOT / "mneme-local-prototype-2" / "mneme.py",
)
HARDENING = MNEME.HARDENING
MBOXRD = MNEME.MBOXRD
FIXTURES = MNEME.MBOX_FIXTURES
EML = MNEME.EML_FIXTURES
CORPUS = EML.CORPUS

FIRST_AT = "2026-09-20T12:00:00Z"
SECOND_AT = "2026-09-28T09:00:00Z"
THIRD_AT = "2026-09-28T10:00:00Z"
FOURTH_AT = "2026-09-28T11:00:00Z"
QUERY = "lantern observatory"
INBOX = FIXTURES.fixture("MBOX-001")
APPENDED = FIXTURES.fixture("MBOX-002")
CHANGED = FIXTURES.fixture("MBOX-003")
DAMAGED = FIXTURES.fixture("MBOX-004")
INBOX_OFFSETS = [0, 398, 1083, 1651, 2075]

# Accepted prototype-1 evidence (experiments/mneme-local-prototype-1/RESULTS.md).
ACCEPTED_DERIVED_MEMBERS = {
    "duplicates.json": "2a63201c9cc2cef10cd0eace5449d0fc030f2913cf325a2bc6831ffb50776335",
    "index.json": "0961bd45b5ef4cefe573cab596db5d11dd42539f6076250a811bfebafc21a729",
    "messages.json": "c8b7c67fa9763dae936eb3378a09b284c130899960146d4e9cb88fcf6e54cfe6",
}
ACCEPTED_FIND_IDS = ["EML-001", "EML-005", "EML-006", "EML-008"]
STABLE_FIELDS = ("citation", "display", "display_mode", "source_id", "source_sha256")


def snapshot(root: Path) -> Tuple[Tuple[str, ...], Dict[str, str]]:
    """Every path under root plus file digests; detects leftover empty directories."""

    paths = []
    digests = {}
    for candidate in sorted(root.rglob("*")):
        relative = candidate.relative_to(root).as_posix()
        paths.append(relative)
        if candidate.is_file():
            digests[relative] = hashlib.sha256(candidate.read_bytes()).hexdigest()
    return tuple(paths), digests


def segments_of(data: bytes):
    return [
        (segment, data[segment.offset : segment.offset + segment.length])
        for segment in MBOXRD.segment_container(data)
    ]


class MboxrdFormatTests(unittest.TestCase):
    """Pure segmentation and escaping checks; no archive state."""

    def test_fixture_hashes_are_pinned_and_synthetic(self) -> None:
        for fixture in FIXTURES.MBOX_FIXTURES:
            self.assertEqual(FIXTURES.EXPECTED_HASHES[fixture.fixture_id], fixture.sha256)
            text = fixture.data.decode("utf-8")
            addresses = {part.split(">")[0] for part in text.split("<")[1:] if "@" in part.split(">")[0]}
            self.assertTrue(addresses)
            self.assertTrue(all(address.endswith("example.test") for address in addresses))

    def test_segments_tile_every_container_byte_exactly_once(self) -> None:
        for fixture in FIXTURES.MBOX_FIXTURES:
            segments = MBOXRD.segment_container(fixture.data)
            self.assertEqual(0, segments[0].offset)
            for before, after in zip(segments, segments[1:]):
                self.assertEqual(before.offset + before.length, after.offset)
            self.assertEqual(len(fixture.data), segments[-1].offset + segments[-1].length)
            self.assertEqual(fixture.data, b"".join(piece for _, piece in segments_of(fixture.data)))
        self.assertEqual(INBOX_OFFSETS, [s.offset for s in MBOXRD.segment_container(INBOX.data)])
        self.assertEqual([], MBOXRD.segment_container(b""))

    def test_boundaries_agree_with_the_standard_library_mailbox(self) -> None:
        with tempfile.TemporaryDirectory(prefix="mneme-mbox-oracle-") as directory:
            for fixture in FIXTURES.MBOX_FIXTURES:
                path = Path(directory) / f"{fixture.fixture_id}.mbox"
                path.write_bytes(fixture.data)
                box = mailbox.mbox(str(path), create=False)
                try:
                    standard = [box.get_bytes(key, from_=True) for key in box.keys()]
                finally:
                    box.close()
                records = [piece for segment, piece in segments_of(fixture.data) if segment.kind == "record"]
                self.assertEqual(len(standard), len(records), fixture.fixture_id)
                for theirs, ours in zip(standard, records):
                    # The standard library trims the separator line and keeps mboxrd escaping.
                    self.assertTrue(ours.startswith(theirs), fixture.fixture_id)
                    self.assertLessEqual(len(ours) - len(theirs), 1)
        # The standard library silently drops the damaged container's preamble.
        self.assertEqual("preamble", MBOXRD.segment_container(DAMAGED.data)[0].kind)

    def test_mboxrd_unescaping_matches_the_literal_fixture(self) -> None:
        self.assertEqual(FIXTURES.QUOTED_FROM_MESSAGE, MBOXRD.unescape_record(FIXTURES.QUOTED_FROM_RECORD))
        envelope = MBOXRD.envelope_line(FIXTURES.QUOTED_FROM_RECORD)
        self.assertEqual(
            FIXTURES.QUOTED_FROM_RECORD, MBOXRD.build_record(envelope, FIXTURES.QUOTED_FROM_MESSAGE)
        )
        unescaped = MBOXRD.unescape_record(FIXTURES.QUOTED_FROM_RECORD)
        self.assertIn(b"\nFrom the north dome", unescaped)
        self.assertIn(b"\n>From the archive", unescaped)
        self.assertIn(b"\n>>From three levels down", unescaped)
        self.assertIn(b"\n>Fromage stays quoted.", unescaped)
        self.assertIn(b"\n From with a leading space", unescaped)
        for (_, record), message in zip(segments_of(INBOX.data), FIXTURES.INBOX_MESSAGES):
            self.assertEqual(message, MBOXRD.unescape_record(record))

    def test_malformed_records_are_classified(self) -> None:
        defects = [
            tuple(MBOXRD.segment_defects(piece, segment.kind, segment.starts_after_blank_line))
            for segment, piece in segments_of(DAMAGED.data)
        ]
        self.assertEqual(list(FIXTURES.MALFORMED_EXPECTED_DEFECTS), defects)
        self.assertEqual(["empty-record"], MBOXRD.segment_defects(
            b"From a@example.test Mon Oct 27 08:00:00 2025\n\n", "record", True))
        with self.assertRaises(ValueError):
            MBOXRD.unescape_record(segments_of(DAMAGED.data)[-1][1])


class MboxIngestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="mneme-prototype-3-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.state = self.root / "state"
        self.counter = 0

    def batch(self, *members) -> Path:
        self.counter += 1
        path = self.root / f"incoming-{self.counter}"
        EML.materialize_files(path, members)
        return path

    def base(self) -> Path:
        return self.batch(*EML.base_members())

    def mbox(self, fixture, name: str = None) -> Path:
        return self.batch((name or fixture.filename, fixture.data))

    def ingest(self, incoming: Path, recorded_at: str, state: Path = None):
        with mock.patch.object(socket, "socket", side_effect=AssertionError("network forbidden")):
            return MNEME.ingest(incoming, state or self.state, recorded_at)

    def generation(self, name: str) -> Path:
        return self.state / "generations" / name

    def manifest(self, name: str):
        return HARDENING.verify_archive(self.generation(name) / "archive")

    def records(self, name: str):
        path = self.generation(name) / "derived" / "messages.json"
        return {record["source_id"]: record for record in json.loads(path.read_text())["messages"]}

    def citations(self, found):
        return [c["citation"] for row in found["results"] for c in row["citations"]]

    def assert_no_leftovers(self) -> None:
        self.assertEqual([], sorted(p.name for p in self.root.glob(".*mneme-stage-*")))
        generations = self.state / "generations"
        if generations.exists():
            self.assertEqual([], sorted(p.name for p in generations.glob(".stage-*")))

    # -- byte preservation, boundaries, identity ------------------------------

    def test_mbox_segments_are_preserved_exactly_with_boundaries_and_ids(self) -> None:
        self.ingest(self.base(), FIRST_AT)
        result = self.ingest(self.mbox(INBOX), SECOND_AT)
        expected_ids = [f"EML-{n:03d}" for n in range(15, 20)]
        self.assertEqual(
            {sid: f"synthetic-mbox:observatory-inbox.mbox#offset={off}"
             for sid, off in zip(expected_ids, INBOX_OFFSETS)},
            result["new_occurrences"],
        )
        manifest = self.manifest("generation-0002")
        items = {item["id"]: item for item in manifest["source_items"]}
        archive = self.generation("generation-0002") / "archive"
        pieces = []
        for source_id, (segment, piece) in zip(expected_ids, segments_of(INBOX.data)):
            item = items[source_id]
            preserved = (archive / item["relative_path"]).read_bytes()
            self.assertEqual(piece, preserved)
            self.assertEqual(f"source-items/{source_id}.mboxrd", item["relative_path"])
            self.assertEqual(segment.as_span(), item["span"])
            self.assertEqual(hashlib.sha256(piece).hexdigest(), item["sha256"])
            self.assertEqual("mbox", item["source_family"])
            self.assertEqual(0o400, (archive / item["relative_path"]).stat().st_mode & 0o777)
            pieces.append(preserved)
        self.assertEqual(INBOX.data, b"".join(pieces))
        self.assertEqual(
            [{"batch_id": "batch-0002", "byte_count": len(INBOX.data),
              "container_key": "synthetic-mbox:observatory-inbox.mbox", "format": "mboxrd",
              "name": "observatory-inbox.mbox", "observation_id": "obs-0001",
              "segment_ids": expected_ids, "sha256": INBOX.sha256}],
            manifest["container_observations"],
        )
        # Every EML identity from generation 1 is unchanged.
        first = self.manifest("generation-0001")
        self.assertEqual(first["source_items"], manifest["source_items"][:14])
        records = self.records("generation-0002")
        for source_id, message in zip(expected_ids, FIXTURES.INBOX_MESSAGES):
            self.assertEqual(hashlib.sha256(message).hexdigest(), records[source_id]["mbox"]["message_sha256"])
            self.assertEqual("one-source-per-process", records[source_id]["isolation"]["mode"])

    def test_mixed_eml_and_mbox_batch_keeps_accepted_eml_identity(self) -> None:
        mixed = self.batch(*EML.base_members(), (INBOX.filename, INBOX.data))
        result = self.ingest(mixed, FIRST_AT)
        self.assertEqual({"eml": 14, "mbox": 5}, result["family_counts"])
        items = self.manifest("generation-0001")["source_items"]
        for item, fixture in zip(items, CORPUS.FIXTURES):
            self.assertEqual(fixture.fixture_id, item["id"])
            self.assertEqual(f"synthetic-eml:{fixture.filename}", item["source_key"])
        self.assertEqual(["mbox"] * 5, [item["source_family"] for item in items[14:]])

        accepted_state = self.root / "prototype-2-state"
        PROTOTYPE_2.ingest(self.base(), accepted_state, FIRST_AT)
        accepted = PROTOTYPE_2.find(accepted_state, QUERY)
        found = MNEME.find(self.state, QUERY)
        self.assertEqual(accepted["results"], found["results"][:4])
        for citation in self.citations(accepted):
            theirs = PROTOTYPE_2.show(accepted_state, citation)
            ours = MNEME.show(self.state, citation)
            self.assertEqual({f: theirs[f] for f in STABLE_FIELDS}, {f: ours[f] for f in STABLE_FIELDS})

    def test_eml_only_generation_reproduces_accepted_derived_members(self) -> None:
        self.ingest(self.base(), FIRST_AT)
        derived = self.generation("generation-0001") / "derived"
        for member, digest in ACCEPTED_DERIVED_MEMBERS.items():
            self.assertEqual(digest, HARDENING.sha256_path(derived / member), member)
        self.assertEqual(ACCEPTED_FIND_IDS, [r["source_id"] for r in MNEME.find(self.state, QUERY)["results"]])

    # -- idempotency ----------------------------------------------------------

    def test_reingestion_is_idempotent_and_appends_only_new_records(self) -> None:
        self.ingest(self.base(), FIRST_AT)
        self.ingest(self.mbox(INBOX), SECOND_AT)
        before = snapshot(self.state)
        again = self.ingest(self.mbox(INBOX), THIRD_AT)
        self.assertFalse(again["published"])
        self.assertEqual(5, len(again["already_preserved"]))
        self.assertEqual(before, snapshot(self.state))

        appended = self.ingest(self.mbox(APPENDED), THIRD_AT)
        self.assertEqual({"EML-020": "synthetic-mbox:observatory-inbox.mbox#offset=2473"},
                         appended["new_occurrences"])
        self.assertEqual(["obs-0002"], appended["new_container_observations"])
        observation = self.manifest("generation-0003")["container_observations"][1]
        self.assertEqual([f"EML-{n:03d}" for n in range(15, 21)], observation["segment_ids"])

        after_append = snapshot(self.state)
        for fixture in (APPENDED, INBOX):  # both observations are already recorded
            result = self.ingest(self.mbox(fixture), FOURTH_AT)
            self.assertFalse(result["published"])
        self.assertEqual(after_append, snapshot(self.state))
        MNEME.verify_state(self.state)

    # -- duplicates -----------------------------------------------------------

    def test_duplicates_are_distinct_occurrences_and_message_id_is_not_identity(self) -> None:
        self.ingest(self.base(), FIRST_AT)
        self.ingest(self.mbox(INBOX), SECOND_AT)
        items = {i["id"]: i for i in self.manifest("generation-0002")["source_items"]}
        # Records 1 and 5 of the mailbox are byte-identical at different offsets.
        self.assertEqual(items["EML-015"]["sha256"], items["EML-019"]["sha256"])
        self.assertNotEqual(items["EML-015"]["source_key"], items["EML-019"]["source_key"])

        copy = self.ingest(self.mbox(INBOX, "observatory-inbox-copy.mbox"), THIRD_AT)
        self.assertEqual([f"EML-{n:03d}" for n in range(20, 25)], sorted(copy["new_occurrences"]))
        self.assertEqual(["obs-0002"], copy["new_container_observations"])
        self.assertEqual(["EML-017"], copy["exact_byte_duplicate_of"]["EML-022"])

        duplicates = json.loads((self.generation("generation-0003") / "derived" / "duplicates.json").read_text())
        exact = {tuple(group["source_ids"]) for group in duplicates["exact_byte_duplicates"]}
        self.assertIn(("EML-015", "EML-019", "EML-020", "EML-024"), exact)
        self.assertIn(("EML-001", "EML-005"), exact)
        anchors = [g for g in duplicates["message_id_duplicates"]
                   if g["message_id"] == "<duplicate-anchor@example.test>"]
        self.assertEqual(1, len(anchors))
        self.assertEqual(["EML-001", "EML-005", "EML-006", "EML-018", "EML-023"], anchors[0]["source_ids"])
        # Same Message-ID, different bytes: a distinct occurrence, not an exact duplicate.
        self.assertNotEqual(items["EML-001"]["sha256"], items["EML-018"]["sha256"])

    # -- changed-source rejection --------------------------------------------

    def test_changed_bytes_at_an_existing_offset_are_rejected_before_staging(self) -> None:
        self.ingest(self.base(), FIRST_AT)
        self.ingest(self.mbox(INBOX), SECOND_AT)
        before = snapshot(self.state)
        # The changed mailbox arrives alongside an otherwise acceptable new EML.
        rejected = self.batch((CHANGED.filename, CHANGED.data), EML.increment_members()[0])
        with mock.patch.object(MNEME.ISOLATION, "isolated_parser", side_effect=AssertionError("parsed")), \
                mock.patch.object(MNEME.tempfile, "mkdtemp", side_effect=AssertionError("staged")):
            with self.assertRaisesRegex(HARDENING.IntegrityError, "offset=398 is already bound to EML-016"):
                self.ingest(rejected, THIRD_AT)
        self.assertEqual(before, snapshot(self.state))

    def test_unreviewed_container_bytes_are_out_of_scope(self) -> None:
        unreviewed = self.batch(("other.mbox", INBOX.data + b"From x@example.test Mon Oct 27 08:00:00 2025\n\n"))
        with self.assertRaisesRegex(HARDENING.ScopeError, "not a reviewed synthetic mbox fixture"):
            self.ingest(unreviewed, FIRST_AT)
        renamed = self.batch(("inbox.eml", INBOX.data))
        with self.assertRaisesRegex(HARDENING.ScopeError, "not a reviewed synthetic eml fixture"):
            self.ingest(renamed, FIRST_AT)
        self.assertFalse(self.state.exists())

    # -- malformed input ------------------------------------------------------

    def test_malformed_and_unsafe_records_are_preserved_and_quarantined(self) -> None:
        self.ingest(self.base(), FIRST_AT)
        result = self.ingest(self.mbox(DAMAGED), SECOND_AT)
        ids = [f"EML-{n:03d}" for n in range(15, 22)]
        self.assertEqual(ids, sorted(result["new_occurrences"]))
        expected = {
            sid: "mbox segment defect: " + ",".join(defects)
            for sid, defects in zip(ids, FIXTURES.MALFORMED_EXPECTED_DEFECTS) if defects
        }
        self.assertEqual(expected, result["quarantined"])
        records = self.records("generation-0002")
        self.assertEqual("indexed", records["EML-016"]["status"])
        # Every byte, including the preamble and the truncated tail, is preserved.
        archive = self.generation("generation-0002") / "archive"
        items = {i["id"]: i for i in self.manifest("generation-0002")["source_items"]}
        self.assertEqual(DAMAGED.data, b"".join((archive / items[s]["relative_path"]).read_bytes() for s in ids))
        index = json.loads((self.generation("generation-0002") / "derived" / "index.json").read_text())
        cited = {row["source_id"] for rows in index["terms"].values() for row in rows}
        self.assertTrue(cited.isdisjoint(expected))
        survivor = MNEME.find(self.state, "neighbours")
        self.assertEqual(["EML-016"], [row["source_id"] for row in survivor["results"]])
        quarantined = f"mneme-source:EML-019@sha256:{items['EML-019']['sha256']}#header:subject:1"
        with self.assertRaises(HARDENING.IntegrityError):
            MNEME.show(self.state, quarantined)

    # -- deterministic rebuild -------------------------------------------------

    def test_full_rebuild_is_deterministic_across_mixed_sources(self) -> None:
        self.ingest(self.base(), FIRST_AT)
        self.ingest(self.batch((INBOX.filename, INBOX.data), (DAMAGED.filename, DAMAGED.data)), SECOND_AT)
        self.ingest(self.mbox(APPENDED), THIRD_AT)
        derived = self.generation("generation-0003") / "derived"
        records = json.loads((derived / "messages.json").read_text())["messages"]
        self.assertEqual([f"EML-{n:03d}" for n in range(1, 28)], [r["source_id"] for r in records])
        # damaged.mbox sorts before observatory-inbox.mbox within the batch.
        items = self.manifest("generation-0003")["source_items"]
        self.assertEqual("synthetic-mbox:damaged.mbox#offset=0", items[14]["source_key"])
        self.assertEqual("synthetic-mbox:observatory-inbox.mbox#offset=0", items[21]["source_key"])

        rebuilt = MNEME.rebuild(self.state, self.root / "rebuilt")
        self.assertTrue(rebuilt["rebuild_equal"])
        self.assertEqual(HARDENING.tree_hashes(derived), HARDENING.tree_hashes(self.root / "rebuilt"))

        other = self.root / "other-state"
        self.ingest(self.batch(*reversed(EML.base_members())), FIRST_AT, other)
        self.ingest(self.batch((DAMAGED.filename, DAMAGED.data), (INBOX.filename, INBOX.data)), SECOND_AT, other)
        self.ingest(self.mbox(APPENDED), THIRD_AT, other)
        self.assertEqual(snapshot(self.state), snapshot(other))
        self.assert_no_leftovers()

    # -- Find and citation stability -------------------------------------------

    def test_existing_find_results_and_citations_are_stable(self) -> None:
        self.ingest(self.base(), FIRST_AT)
        before = MNEME.find(self.state, QUERY)
        before_shown = {c: MNEME.show(self.state, c) for c in self.citations(before)}

        self.ingest(self.mbox(INBOX), SECOND_AT)
        middle = MNEME.find(self.state, QUERY)
        self.assertEqual(before["results"], middle["results"][:4])
        self.assertEqual(["EML-015", "EML-018", "EML-019"], [r["source_id"] for r in middle["results"][4:]])
        middle_shown = {c: MNEME.show(self.state, c) for c in self.citations(middle)}

        self.ingest(self.batch((DAMAGED.filename, DAMAGED.data)), THIRD_AT)
        self.ingest(self.mbox(APPENDED), FOURTH_AT)
        after = MNEME.find(self.state, QUERY)
        self.assertEqual(middle["results"], after["results"][: len(middle["results"])])
        for citation, shown in {**before_shown, **middle_shown}.items():
            self.assertEqual(shown, MNEME.show(self.state, citation))

    def test_mbox_citation_displays_unescaped_inert_text_with_span(self) -> None:
        self.ingest(self.mbox(INBOX), FIRST_AT)
        found = MNEME.find(self.state, "north dome")
        self.assertEqual(["EML-003"], [r["source_id"] for r in found["results"]])
        citation = found["results"][0]["citations"][0]["citation"]
        shown = MNEME.show(self.state, citation)
        self.assertTrue(shown["display"].startswith("Observers wrote:\nFrom the north dome"))
        self.assertIn("\n&gt;From the archive", shown["display"])
        self.assertEqual(
            {"container_key": "synthetic-mbox:observatory-inbox.mbox", "length": 568,
             "offset": 1083, "transform": "mboxrd-unescape"},
            shown["source_span"],
        )
        forged = citation.replace(shown["source_sha256"], "0" * 64)
        with self.assertRaisesRegex(HARDENING.IntegrityError, "digest"):
            MNEME.show(self.state, forged)

    # -- staging, rollback, interruption --------------------------------------

    def test_failed_first_ingest_leaves_no_state(self) -> None:
        with mock.patch.object(MNEME, "rebuild_derived", side_effect=HARDENING.IntegrityError("injected")):
            with self.assertRaisesRegex(HARDENING.IntegrityError, "injected"):
                self.ingest(self.batch((INBOX.filename, INBOX.data)), FIRST_AT)
        self.assertFalse(self.state.exists())
        self.assert_no_leftovers()

    def test_failures_roll_back_and_leave_the_previous_generation_usable(self) -> None:
        self.ingest(self.base(), FIRST_AT)
        before = snapshot(self.state)
        found = MNEME.find(self.state, QUERY)

        real_parser = MNEME.ISOLATION.isolated_parser

        def fail_on_mbox(item, raw, recorded_at):
            if item.get("source_family") == "mbox":
                raise HARDENING.IntegrityError("injected mbox parser failure")
            return real_parser(item, raw, recorded_at)

        with mock.patch.object(MNEME.ISOLATION, "isolated_parser", side_effect=fail_on_mbox):
            with self.assertRaisesRegex(HARDENING.IntegrityError, "injected mbox parser"):
                self.ingest(self.mbox(INBOX), SECOND_AT)
        self.assertEqual(before, snapshot(self.state))
        self.assertEqual(found, MNEME.find(self.state, QUERY))

        with mock.patch.object(MNEME, "_write_current", side_effect=OSError("injected pointer")):
            with self.assertRaisesRegex(OSError, "injected pointer"):
                self.ingest(self.mbox(INBOX), SECOND_AT)
        self.assertEqual(before, snapshot(self.state))
        self.assert_no_leftovers()
        self.assertEqual("generation-0002", self.ingest(self.mbox(INBOX), SECOND_AT)["generation"])

    def test_interrupted_staging_keeps_current_usable_until_recovered(self) -> None:
        self.ingest(self.base(), FIRST_AT)
        before = snapshot(self.state)
        found = MNEME.find(self.state, QUERY)
        # Simulate a crash: the prototype's own cleanup cannot run, as if the process died.
        # Only this module's shutil is replaced, so the parser's temporary cleanup still runs.
        no_cleanup = types.SimpleNamespace(rmtree=lambda *args, **kwargs: None)
        crashes = (
            ("_write_current", "generation-0002"),  # renamed into place, CURRENT not replaced
            ("rebuild_derived", ".stage-"),  # crashed while staging
        )
        for target, leftover in crashes:
            with mock.patch.object(MNEME, "shutil", no_cleanup), \
                    mock.patch.object(MNEME, target, side_effect=RuntimeError("simulated crash")):
                with self.assertRaisesRegex(RuntimeError, "simulated crash"):
                    self.ingest(self.mbox(INBOX), SECOND_AT)
            verified = MNEME.verify_state(self.state)
            self.assertEqual("generation-0001", verified["current"])
            self.assertEqual(1, len(verified["unpublished_leftovers"]))
            self.assertTrue(verified["unpublished_leftovers"][0].startswith(leftover))
            self.assertEqual("generation-0001\n", (self.state / "CURRENT").read_text())
            self.assertEqual(found, MNEME.find(self.state, QUERY))
            with self.assertRaisesRegex(HARDENING.IntegrityError, "run recover"):
                self.ingest(self.mbox(INBOX), SECOND_AT)
            self.assertEqual(verified["unpublished_leftovers"], MNEME.recover(self.state)["removed"])
            self.assertEqual(before, snapshot(self.state))

        self.ingest(self.mbox(INBOX), SECOND_AT)
        clean = self.root / "clean-state"
        self.ingest(self.base(), FIRST_AT, clean)
        self.ingest(self.mbox(INBOX), SECOND_AT, clean)
        self.assertEqual(snapshot(clean), snapshot(self.state))

    def test_tampered_segment_blocks_reads_and_ingest(self) -> None:
        self.ingest(self.mbox(INBOX), FIRST_AT)
        preserved = self.generation("generation-0001") / "archive" / "source-items" / "EML-002.mboxrd"
        preserved.chmod(0o600)
        preserved.write_bytes(preserved.read_bytes().replace(b"The rota table", b"The rota TABLE"))
        with self.assertRaisesRegex(HARDENING.IntegrityError, "SHA-256 mismatch"):
            MNEME.find(self.state, QUERY)
        with self.assertRaises(HARDENING.IntegrityError):
            self.ingest(self.mbox(APPENDED), SECOND_AT)

    def test_recorded_boundaries_are_rederived_from_preserved_bytes(self) -> None:
        self.ingest(self.mbox(INBOX), FIRST_AT)
        archive = self.generation("generation-0001") / "archive"
        manifest = HARDENING.verify_archive(archive)
        MNEME._verify_identity_extension(archive, manifest)
        forged = json.loads(json.dumps(manifest))
        forged["source_items"][2]["span"]["starts_after_blank_line"] = False
        with self.assertRaisesRegex(HARDENING.IntegrityError, "boundaries disagree"):
            MNEME._verify_identity_extension(archive, forged)
        forged = json.loads(json.dumps(manifest))
        forged["container_observations"][0]["segment_ids"] = ["EML-002", "EML-001", "EML-003",
                                                              "EML-004", "EML-005"]
        with self.assertRaisesRegex(HARDENING.IntegrityError, "reassemble"):
            MNEME._verify_identity_extension(archive, forged)

    # -- CLI -------------------------------------------------------------------

    def test_cli_ingest_and_changed_source_rejection(self) -> None:
        output = StringIO()
        with redirect_stdout(output), mock.patch.object(
            socket, "socket", side_effect=AssertionError("network forbidden")
        ):
            status = MNEME.main(["ingest", "--incoming", str(self.mbox(INBOX)),
                                 "--state", str(self.state), "--recorded-at", FIRST_AT])
        self.assertEqual(0, status)
        self.assertEqual(["obs-0001"], json.loads(output.getvalue())["new_container_observations"])
        errors = StringIO()
        with redirect_stderr(errors), redirect_stdout(StringIO()):
            status = MNEME.main(["ingest", "--incoming", str(self.mbox(CHANGED)),
                                 "--state", str(self.state), "--recorded-at", SECOND_AT])
        self.assertEqual(2, status)
        self.assertIn("changed source bytes are rejected", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
