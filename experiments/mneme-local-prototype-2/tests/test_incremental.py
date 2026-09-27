from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import socket
import tempfile
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


MNEME = _load("mneme_local_synthetic_prototype_2", PROTOTYPE_ROOT / "mneme.py")
ACCEPTED = _load(
    "mneme_local_synthetic_prototype_1",
    EXPERIMENTS_ROOT / "mneme-local-prototype-1" / "mneme.py",
)
HARDENING = MNEME.HARDENING
INCREMENT = MNEME.INCREMENT
CORPUS = INCREMENT.CORPUS

FIRST_AT = "2026-09-20T12:00:00Z"
SECOND_AT = "2026-09-27T12:00:00Z"
QUERY = "lantern observatory"

# Accepted prototype-1 evidence (experiments/mneme-local-prototype-1/RESULTS.md).
ACCEPTED_DERIVED_MEMBERS = {
    "duplicates.json": "2a63201c9cc2cef10cd0eace5449d0fc030f2913cf325a2bc6831ffb50776335",
    "index.json": "0961bd45b5ef4cefe573cab596db5d11dd42539f6076250a811bfebafc21a729",
    "messages.json": "c8b7c67fa9763dae936eb3378a09b284c130899960146d4e9cb88fcf6e54cfe6",
}
ACCEPTED_FIND_IDS = ["EML-001", "EML-005", "EML-006", "EML-008"]


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


class IncrementalIngestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="mneme-prototype-2-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.state = self.root / "state"
        self.base = self.root / "base"
        INCREMENT.materialize_files(self.base, INCREMENT.base_members())

    def batch(self, name: str, members) -> Path:
        path = self.root / name
        INCREMENT.materialize_files(path, members)
        return path

    def increment(self) -> Path:
        # Includes one already-preserved member to exercise a mixed batch.
        return self.batch(
            "increment", INCREMENT.increment_members() + (INCREMENT.base_members()[0],)
        )

    def ingest(self, incoming: Path, recorded_at: str = FIRST_AT, state: Path = None):
        with mock.patch.object(
            socket, "socket", side_effect=AssertionError("network forbidden")
        ):
            return MNEME.ingest(incoming, state or self.state, recorded_at)

    def generation(self, name: str) -> Path:
        return self.state / "generations" / name

    def manifest(self, name: str):
        return HARDENING.verify_archive(self.generation(name) / "archive")

    def assert_no_staging_leftovers(self) -> None:
        self.assertEqual([], sorted(p.name for p in self.root.glob(".*mneme-stage-*")))
        generations = self.state / "generations"
        if generations.exists():
            self.assertEqual([], sorted(p.name for p in generations.glob(".stage-*")))

    # -- identity -----------------------------------------------------------

    def test_first_ingest_assigns_immutable_ids_in_source_key_order(self) -> None:
        # Materialize in reverse order so directory creation order cannot matter.
        reversed_batch = self.batch("reversed", tuple(reversed(INCREMENT.base_members())))
        result = self.ingest(reversed_batch)
        self.assertTrue(result["published"])
        self.assertEqual("generation-0001", result["generation"])
        self.assertEqual("generation-0001\n", (self.state / "CURRENT").read_text())
        manifest = self.manifest("generation-0001")
        self.assertEqual("mneme-occurrence-identity-v1", manifest["identity_convention"])
        for item, fixture in zip(manifest["source_items"], CORPUS.FIXTURES):
            self.assertEqual(fixture.fixture_id, item["id"])
            self.assertEqual(f"synthetic-eml:{fixture.filename}", item["source_key"])
            self.assertEqual(f"source-items/{fixture.fixture_id}.eml", item["relative_path"])
            self.assertEqual("batch-0001", item["ingest_batch"])
            preserved = self.generation("generation-0001") / "archive" / item["relative_path"]
            self.assertEqual(fixture.data, preserved.read_bytes())
            self.assertEqual(0o400, preserved.stat().st_mode & 0o777)
        self.assertEqual(
            {"indexed": 6, "indexed_with_warnings": 4, "quarantined": 4},
            result["status_counts"],
        )

    def test_source_ids_stop_at_the_citation_compatible_limit(self) -> None:
        self.assertEqual("EML-999", MNEME.source_id_for(999))
        with self.assertRaisesRegex(HARDENING.ScopeError, "citation-compatible"):
            MNEME.source_id_for(1000)

    # -- stability against the accepted prototype ---------------------------

    def test_first_generation_matches_accepted_find_citations_and_derived_members(self) -> None:
        self.ingest(self.base)
        derived = self.generation("generation-0001") / "derived"
        for member, digest in ACCEPTED_DERIVED_MEMBERS.items():
            self.assertEqual(digest, HARDENING.sha256_path(derived / member), member)

        accepted_state = self.root / "accepted-state"
        ACCEPTED.ingest(self.base, accepted_state, FIRST_AT)
        accepted_find = ACCEPTED.find(accepted_state, QUERY)
        found = MNEME.find(self.state, QUERY)
        self.assertEqual(accepted_find, found)
        self.assertEqual(ACCEPTED_FIND_IDS, [row["source_id"] for row in found["results"]])
        self.assertEqual(
            HARDENING.tree_hashes(accepted_state / "derived", exclude=("derived-manifest.json",)),
            HARDENING.tree_hashes(derived, exclude=("derived-manifest.json",)),
        )
        for row in found["results"]:
            for citation in row["citations"]:
                ours = MNEME.show(self.state, citation["citation"])
                theirs = ACCEPTED.show(accepted_state, citation["citation"])
                for field in ("citation", "display", "display_mode", "source_id", "source_sha256"):
                    self.assertEqual(theirs[field], ours[field])

    def test_existing_find_results_and_citations_stay_stable_after_increment(self) -> None:
        self.ingest(self.base)
        before = MNEME.find(self.state, QUERY)
        before_other = MNEME.find(self.state, "résumé")
        shown = {
            citation["citation"]: MNEME.show(self.state, citation["citation"])
            for row in before["results"]
            for citation in row["citations"]
        }

        self.ingest(self.increment(), SECOND_AT)
        after = MNEME.find(self.state, QUERY)
        old_ids = {row["source_id"] for row in before["results"]}
        self.assertEqual(
            before["results"], [row for row in after["results"] if row["source_id"] in old_ids]
        )
        self.assertEqual(
            ["EML-015", "EML-016"],
            [row["source_id"] for row in after["results"] if row["source_id"] not in old_ids],
        )
        self.assertEqual(before_other, MNEME.find(self.state, "résumé"))
        for citation, displayed in shown.items():
            self.assertEqual(displayed, MNEME.show(self.state, citation))
        # Each generation keeps the accepted state shape readable by prototype 1.
        self.assertEqual(after, ACCEPTED.find(self.generation("generation-0002"), QUERY))

    # -- idempotency ----------------------------------------------------------

    def test_reingesting_the_same_batch_is_an_exact_no_op(self) -> None:
        self.ingest(self.base)
        before = snapshot(self.state)
        again = self.ingest(self.batch("again", INCREMENT.base_members()), SECOND_AT)
        self.assertFalse(again["published"])
        self.assertEqual({}, again["new_occurrences"])
        self.assertEqual(14, len(again["already_preserved"]))
        self.assertEqual("generation-0001", again["generation"])
        self.assertEqual(before, snapshot(self.state))

        self.ingest(self.increment(), SECOND_AT)
        after_increment = snapshot(self.state)
        repeat = self.ingest(self.batch("repeat", INCREMENT.increment_members()), SECOND_AT)
        self.assertFalse(repeat["published"])
        self.assertEqual(after_increment, snapshot(self.state))

    def test_incremental_batch_appends_without_rewriting_existing_identity(self) -> None:
        self.ingest(self.base)
        result = self.ingest(self.increment(), SECOND_AT)
        self.assertEqual("generation-0002", result["generation"])
        self.assertEqual("batch-0002", result["batch_id"])
        self.assertEqual(
            {"synthetic-eml:01-plain-lf-7bit.eml": "EML-001"}, result["already_preserved"]
        )
        self.assertEqual(
            {
                "EML-015": "synthetic-eml:15-lantern-follow-up.eml",
                "EML-016": "synthetic-eml:16-resent-plain-lf-7bit.eml",
                "EML-017": "synthetic-eml:17-dome-maintenance.eml",
            },
            result["new_occurrences"],
        )
        first = self.manifest("generation-0001")
        second = self.manifest("generation-0002")
        self.assertEqual(first["source_items"], second["source_items"][:14])
        self.assertEqual(first["ingest_batches"], second["ingest_batches"][:1])
        self.assertEqual(
            {"batch_id": "batch-0002", "recorded_at": SECOND_AT,
             "source_ids": ["EML-015", "EML-016", "EML-017"]},
            second["ingest_batches"][1],
        )
        verified = MNEME.verify_state(self.state)
        self.assertEqual("generation-0002", verified["current"])
        self.assertEqual([14, 17], [row["source_count"] for row in verified["generations"]])

    # -- duplicates and changed bytes ----------------------------------------

    def test_exact_byte_duplicate_is_a_distinct_occurrence(self) -> None:
        self.ingest(self.base)
        result = self.ingest(self.increment(), SECOND_AT)
        self.assertEqual({"EML-016": ["EML-001", "EML-005"]}, result["exact_byte_duplicate_of"])
        items = {item["id"]: item for item in self.manifest("generation-0002")["source_items"]}
        self.assertEqual(items["EML-001"]["sha256"], items["EML-016"]["sha256"])
        self.assertNotEqual(items["EML-001"]["source_key"], items["EML-016"]["source_key"])
        archive = self.generation("generation-0002") / "archive"
        self.assertEqual(
            (archive / "source-items/EML-001.eml").read_bytes(),
            (archive / "source-items/EML-016.eml").read_bytes(),
        )
        duplicates = json.loads(
            (self.generation("generation-0002") / "derived" / "duplicates.json").read_text()
        )
        self.assertIn(
            {"sha256": items["EML-001"]["sha256"], "source_ids": ["EML-001", "EML-005", "EML-016"]},
            duplicates["exact_byte_duplicates"],
        )
        citation = (
            "mneme-source:EML-016@sha256:" + items["EML-016"]["sha256"] + "#header:subject:1"
        )
        displayed = MNEME.show(self.state, citation)
        self.assertEqual("North observatory lantern schedule", displayed["display"])
        self.assertEqual("EML-016", displayed["source_id"])

    def test_changed_bytes_for_an_existing_source_key_are_rejected_before_staging(self) -> None:
        self.ingest(self.base)
        variant = next(f for f in CORPUS.FIXTURES if f.fixture_id == "EML-006")
        conflicting = self.batch(
            "conflicting",
            (
                ("01-plain-lf-7bit.eml", variant.data),
                INCREMENT.increment_members()[0],
            ),
        )
        before = snapshot(self.state)
        with mock.patch.object(
            MNEME.ISOLATION, "isolated_parser", side_effect=AssertionError("parsed")
        ), mock.patch.object(
            MNEME.tempfile, "mkdtemp", side_effect=AssertionError("staged")
        ):
            with self.assertRaisesRegex(HARDENING.IntegrityError, "already bound to EML-001"):
                self.ingest(conflicting, SECOND_AT)
        self.assertEqual(before, snapshot(self.state))
        self.assertEqual("generation-0001\n", (self.state / "CURRENT").read_text())

    def test_unreviewed_or_unsafe_incoming_members_are_rejected(self) -> None:
        self.ingest(self.base)
        before = snapshot(self.state)
        unreviewed = self.batch("unreviewed", (("20-unknown.eml", b"Subject: x\n\nnot reviewed\n"),))
        with self.assertRaisesRegex(HARDENING.ScopeError, "not a reviewed synthetic fixture"):
            self.ingest(unreviewed, SECOND_AT)

        linked = self.root / "linked"
        linked.mkdir()
        os.symlink(self.base / CORPUS.FIXTURES[0].filename, linked / "21-link.eml")
        with self.assertRaisesRegex(HARDENING.ScopeError, "regular non-symlink"):
            self.ingest(linked, SECOND_AT)

        badly_named = self.batch("badly-named", ((".hidden.eml", b""),))
        with self.assertRaisesRegex(HARDENING.ScopeError, "name is not supported"):
            self.ingest(badly_named, SECOND_AT)
        self.assertEqual(before, snapshot(self.state))

    # -- rebuild ----------------------------------------------------------------

    def test_full_rebuild_is_deterministic_in_source_id_order(self) -> None:
        self.ingest(self.base)
        self.ingest(self.increment(), SECOND_AT)
        derived = self.generation("generation-0002") / "derived"
        messages = json.loads((derived / "messages.json").read_text())["messages"]
        ids = [record["source_id"] for record in messages]
        self.assertEqual([f"EML-{n:03d}" for n in range(1, 18)], ids)
        # Each source is derived at the logical time of its own ingest batch.
        self.assertEqual(
            {FIRST_AT}, {r["provenance"]["recorded_at"] for r in messages[:14]}
        )
        self.assertEqual(
            {SECOND_AT}, {r["provenance"]["recorded_at"] for r in messages[14:]}
        )

        rebuilt = MNEME.rebuild(self.state, self.root / "rebuilt")
        self.assertTrue(rebuilt["rebuild_equal"])
        self.assertEqual(HARDENING.tree_hashes(derived), HARDENING.tree_hashes(self.root / "rebuilt"))

        # An independent state built from the same batches is byte-identical overall.
        other_state = self.root / "other-state"
        self.ingest(self.batch("base-2", tuple(reversed(INCREMENT.base_members()))),
                    FIRST_AT, other_state)
        self.ingest(self.batch("increment-2", tuple(reversed(INCREMENT.increment_members()))),
                    SECOND_AT, other_state)
        self.assertEqual(snapshot(self.state), snapshot(other_state))
        self.assert_no_staging_leftovers()

    # -- staged publication and rollback ------------------------------------

    def test_failed_first_ingest_leaves_no_state(self) -> None:
        with mock.patch.object(
            MNEME, "verify_generation", side_effect=HARDENING.IntegrityError("injected")
        ):
            with self.assertRaisesRegex(HARDENING.IntegrityError, "injected"):
                self.ingest(self.base)
        self.assertFalse(self.state.exists())
        self.assert_no_staging_leftovers()

    def test_failure_before_or_during_publication_rolls_back(self) -> None:
        self.ingest(self.base)
        before = snapshot(self.state)

        with mock.patch.object(
            MNEME, "rebuild_derived", side_effect=HARDENING.IntegrityError("injected derive")
        ):
            with self.assertRaisesRegex(HARDENING.IntegrityError, "injected derive"):
                self.ingest(self.increment(), SECOND_AT)
        self.assertEqual(before, snapshot(self.state))
        self.assert_no_staging_leftovers()

        # The new generation directory is renamed into place, then CURRENT fails.
        with mock.patch.object(MNEME, "_write_current", side_effect=OSError("injected pointer")):
            with self.assertRaisesRegex(OSError, "injected pointer"):
                self.ingest(self.batch("increment-b", INCREMENT.increment_members()), SECOND_AT)
        self.assertEqual(before, snapshot(self.state))
        self.assertFalse(self.generation("generation-0002").exists())
        self.assert_no_staging_leftovers()

        # The rolled-back batch can then be ingested normally.
        result = self.ingest(self.batch("increment-c", INCREMENT.increment_members()), SECOND_AT)
        self.assertEqual("generation-0002", result["generation"])
        MNEME.verify_state(self.state)

    def test_tampered_current_archive_blocks_ingest_and_reads(self) -> None:
        self.ingest(self.base)
        preserved = self.generation("generation-0001") / "archive" / "source-items" / "EML-002.eml"
        preserved.chmod(0o600)
        preserved.write_bytes(preserved.read_bytes() + b"tampered\n")
        with self.assertRaisesRegex(HARDENING.IntegrityError, "size mismatch|SHA-256 mismatch"):
            self.ingest(self.increment(), SECOND_AT)
        with self.assertRaises(HARDENING.IntegrityError):
            MNEME.find(self.state, QUERY)
        self.assertFalse(self.generation("generation-0002").exists())

    def test_interrupted_publication_fails_closed(self) -> None:
        self.ingest(self.base)
        (self.state / "generations" / ".stage-leftover").mkdir()
        with self.assertRaisesRegex(HARDENING.IntegrityError, "interrupted staging"):
            MNEME.find(self.state, QUERY)

    # -- CLI -------------------------------------------------------------------

    def test_cli_reports_ingest_and_rejection(self) -> None:
        output = StringIO()
        with redirect_stdout(output), mock.patch.object(
            socket, "socket", side_effect=AssertionError("network forbidden")
        ):
            status = MNEME.main(
                ["ingest", "--incoming", str(self.base), "--state", str(self.state),
                 "--recorded-at", FIRST_AT]
            )
        self.assertEqual(0, status)
        self.assertEqual("generation-0001", json.loads(output.getvalue())["generation"])

        variant = next(f for f in CORPUS.FIXTURES if f.fixture_id == "EML-006")
        conflicting = self.batch("conflicting", (("01-plain-lf-7bit.eml", variant.data),))
        errors = StringIO()
        with redirect_stderr(errors), redirect_stdout(StringIO()):
            status = MNEME.main(
                ["ingest", "--incoming", str(conflicting), "--state", str(self.state),
                 "--recorded-at", SECOND_AT]
            )
        self.assertEqual(2, status)
        self.assertIn("changed source bytes are rejected", errors.getvalue())


class IncrementFixtureTests(unittest.TestCase):
    def test_increment_fixture_hashes_are_pinned_and_synthetic(self) -> None:
        for fixture in INCREMENT.INCREMENT_FIXTURES:
            self.assertEqual(INCREMENT.EXPECTED_HASHES[fixture.fixture_id], fixture.sha256)
            text = fixture.data.decode("utf-8")
            addresses = {part.split(">")[0] for part in text.split("<")[1:]}
            self.assertTrue(all(address.endswith("example.test") for address in addresses))


if __name__ == "__main__":
    unittest.main()
