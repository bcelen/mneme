from __future__ import annotations

import hashlib
import importlib.util
import json
import socket
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("mneme_local_threads_1", EXPERIMENT_ROOT / "mneme_threads.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load the threading experiment")
THREADS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(THREADS)
P3 = THREADS.P3
HARDENING = THREADS.HARDENING
FIXTURES = THREADS.THREAD_FIXTURES
EML = P3.EML_FIXTURES


def shape(subtree):
    """Compact tree: (message_id, [source ids], missing, [children])."""

    return (
        subtree["message_id"],
        [o["source_id"] for o in subtree["occurrences"]],
        subtree["missing_from_archive"],
        [shape(child) for child in subtree["children"]],
    )


def snapshot(root: Path):
    return [
        (p.relative_to(root).as_posix(), hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "dir")
        for p in sorted(root.rglob("*"))
    ]


class MessageIdTests(unittest.TestCase):
    def test_only_bracketed_ids_are_extracted_in_order(self) -> None:
        self.assertEqual(["<a@x.test>", "<b@x.test>"], THREADS.message_ids("<A@X.test>\n <b@x.test> junk"))
        self.assertEqual([], THREADS.message_ids("not a message id"))
        self.assertEqual([], THREADS.message_ids(None))

    def test_fixture_hashes_are_pinned_and_synthetic(self) -> None:
        for fixture in FIXTURES.THREAD_FIXTURES:
            self.assertEqual(FIXTURES.EXPECTED_HASHES[fixture.fixture_id], fixture.sha256)
            text = fixture.data.decode("utf-8")
            addresses = {p.split(">")[0] for p in text.split("<")[1:] if "@" in p.split(">")[0]}
            self.assertTrue(all(a.endswith("example.test") for a in addresses), fixture.fixture_id)


class ThreadingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory(prefix="mneme-threads-1-")
        cls.root = Path(cls.temporary.name)
        cls.state = cls.root / "state"
        EML.materialize_files(cls.root / "base", EML.base_members())
        EML.materialize_files(cls.root / "threads", FIXTURES.members())
        with mock.patch.object(socket, "socket", side_effect=AssertionError("network forbidden")):
            THREADS.ingest(cls.root / "base", cls.state, "2026-09-20T12:00:00Z")
            cls.ingested = THREADS.ingest(cls.root / "threads", cls.state, "2026-10-05T09:00:00Z")
        cls.result = THREADS.build_threads(cls.state)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def thread(self, source_id):
        return THREADS.thread_of(self.state, source_id)

    def test_thread_fixtures_need_the_scoped_allowlist(self) -> None:
        self.assertEqual(
            {"EML-015": "synthetic-eml:31-dome-repair-plan.eml",
             "EML-023": "synthetic-mbox:thread-replies.mbox#offset=0"},
            {k: v for k, v in self.ingested["new_occurrences"].items() if k in ("EML-015", "EML-023")},
        )
        with self.assertRaisesRegex(HARDENING.ScopeError, "not a reviewed synthetic"):
            P3.ingest(self.root / "threads", self.root / "plain-state", "2026-10-05T09:00:00Z")
        self.assertFalse((self.root / "plain-state").exists())

    def test_reply_chain_with_missing_parent_and_cross_family_reply(self) -> None:
        dome = self.thread("EML-023")
        self.assertEqual("thread:<dome-repair-301@example.test>", dome["thread_id"])
        self.assertEqual(5, dome["occurrence_count"])
        self.assertEqual(
            ("<dome-repair-301@example.test>", ["EML-015"], False, [
                ("<dome-repair-302@example.test>", ["EML-016"], False, [
                    ("<dome-repair-303@example.test>", ["EML-017"], False, []),  # folded References
                    ("<dome-repair-305@example.test>", ["EML-023"], False, []),  # the MBOX reply
                ]),
                ("<dome-repair-399@example.test>", [], True, [
                    ("<dome-repair-304@example.test>", ["EML-018"], False, []),
                ]),
            ]),
            shape(dome["root"]),
        )
        self.assertEqual(["<dome-repair-399@example.test>"], self.result["missing_messages"])

    def test_subjects_and_malformed_references_never_create_links(self) -> None:
        for source_id in ("EML-019", "EML-022"):  # malformed references; shared subject only
            alone = self.thread(source_id)
            self.assertEqual(1, alone["occurrence_count"], source_id)
            self.assertEqual([], alone["root"]["children"])
        self.assertEqual(["EML-019"], self.result["unparseable_reference_headers"])

    def test_reply_loop_is_refused_deterministically_and_reported(self) -> None:
        loop = self.thread("EML-020")
        self.assertEqual(
            ("<loop-b-308@example.test>", ["EML-021"], False, [("<loop-a-307@example.test>", ["EML-020"], False, [])]),
            shape(loop["root"]),
        )
        self.assertEqual(
            [{"node": "<loop-b-308@example.test>", "rejected_parent": "<loop-a-307@example.test>",
              "source_id": "EML-021"}],
            self.result["cycles_refused"],
        )

    def test_shared_message_id_is_one_node_and_missing_id_is_its_own_thread(self) -> None:
        anchor = self.thread("EML-005")
        self.assertEqual(("<duplicate-anchor@example.test>", ["EML-001", "EML-005", "EML-006"], False, []),
                         shape(anchor["root"]))
        no_id = self.thread("EML-009")  # the malformed-header fixture has no Message-ID
        self.assertEqual((None, ["EML-009"], False, []), shape(no_id["root"]))
        self.assertEqual("thread:occurrence:EML-009", no_id["thread_id"])

    def test_conversation_list_ordering_and_counts(self) -> None:
        listed = THREADS.conversations(self.state)
        self.assertEqual(
            ["thread:<duplicate-anchor@example.test>", "thread:<dome-repair-301@example.test>",
             "thread:<loop-b-308@example.test>"],
            [t["thread_id"] for t in listed["threads"]],
        )
        everything = THREADS.conversations(self.state, include_singletons=True)
        self.assertEqual(12, len(everything["threads"]))
        listed_ids = sorted(o for t in everything["threads"] for o in _all_ids(t["root"]))
        # Every non-quarantined occurrence is in exactly one thread.
        _, generation, _ = P3.current_generation(self.state)
        records = json.loads((generation / "derived" / "messages.json").read_text())["messages"]
        self.assertEqual(sorted(r["source_id"] for r in records if r["status"] != "quarantined"), listed_ids)

    def test_citations_resolve_and_threading_is_read_only(self) -> None:
        before = snapshot(self.state)
        dome = self.thread("EML-015")
        self.assertEqual(dome, self.thread("EML-015"))
        for occurrence in _all_occurrences(dome["root"]):
            shown = P3.show(self.state, occurrence["citation"])
            self.assertEqual(occurrence["source_id"], shown["source_id"])
        self.assertEqual(before, snapshot(self.state))
        with self.assertRaisesRegex(HARDENING.ScopeError, "no non-quarantined occurrence"):
            self.thread("EML-010")

    def test_cli(self) -> None:
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(0, THREADS.main(["thread", "--state", str(self.state), "--source-id", "EML-017"]))
        self.assertEqual("thread:<dome-repair-301@example.test>", json.loads(output.getvalue())["thread_id"])
        errors = StringIO()
        with redirect_stderr(errors), redirect_stdout(StringIO()):
            self.assertEqual(2, THREADS.main(["thread", "--state", str(self.state), "--source-id", "EML-999"]))


def _all_occurrences(subtree):
    found = list(subtree["occurrences"])
    for child in subtree["children"]:
        found.extend(_all_occurrences(child))
    return found


def _all_ids(subtree):
    return [o["source_id"] for o in _all_occurrences(subtree)]


if __name__ == "__main__":
    unittest.main()
