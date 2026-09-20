from __future__ import annotations

import importlib.util
import json
import socket
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock


PROTOTYPE_ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "mneme_local_synthetic_prototype", PROTOTYPE_ROOT / "mneme.py"
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load local prototype")
MNEME = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MNEME)


RECORDED_AT = "2026-09-20T12:00:00Z"
QUERY = "lantern observatory"


class LocalPrototypeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="mneme-local-prototype-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.incoming = self.root / "incoming"
        self.state = self.root / "state"
        MNEME.CORPUS.materialize(self.incoming)

    def ingest(self):
        with mock.patch.object(
            socket, "socket", side_effect=AssertionError("network forbidden")
        ):
            return MNEME.ingest(self.incoming, self.state, RECORDED_AT)

    def test_ingests_all_synthetic_eml_and_preserves_exact_bytes(self) -> None:
        result = self.ingest()
        self.assertEqual(14, result["source_count"])
        self.assertEqual(
            {"indexed": 6, "indexed_with_warnings": 4, "quarantined": 4},
            result["status_counts"],
        )
        manifest = MNEME.HARDENING.verify_archive(self.state / "archive")
        messages = json.loads(
            (self.state / "derived" / "messages.json").read_text(encoding="utf-8")
        )["messages"]
        self.assertEqual(
            {"one-source-per-process"},
            {record["isolation"]["mode"] for record in messages},
        )
        for item in manifest["source_items"]:
            fixture = next(
                fixture
                for fixture in MNEME.CORPUS.FIXTURES
                if fixture.fixture_id == item["id"]
            )
            preserved = self.state / "archive" / item["relative_path"]
            self.assertEqual(fixture.data, preserved.read_bytes())
            self.assertEqual(fixture.sha256, item["sha256"])
            self.assertEqual(len(fixture.data), item["byte_count"])

    def test_rebuild_is_byte_identical_and_leaves_current_state_unchanged(self) -> None:
        self.ingest()
        before = MNEME.HARDENING.tree_hashes(self.state / "derived")
        rebuilt = self.root / "rebuilt-derived"
        result = MNEME.rebuild(self.state, rebuilt)
        self.assertTrue(result["rebuild_equal"])
        self.assertEqual(before, MNEME.HARDENING.tree_hashes(rebuilt))
        self.assertEqual(before, MNEME.HARDENING.tree_hashes(self.state / "derived"))

    def test_find_and_selected_source_display_are_verified_and_repeatable(self) -> None:
        self.ingest()
        first = MNEME.find(self.state, QUERY)
        second = MNEME.find(self.state, QUERY)
        self.assertEqual(first, second)
        self.assertGreaterEqual(len(first["results"]), 3)
        citation = first["results"][0]["citations"][0]["citation"]
        displayed = MNEME.show(self.state, citation)
        self.assertEqual(citation, displayed["citation"])
        self.assertEqual("escaped-inert-text-no-fetch", displayed["display_mode"])
        self.assertIn(displayed["source_id"], citation)
        self.assertIn(displayed["source_sha256"], citation)
        self.assertEqual(
            "wholly-fictional-synthetic-fixture",
            displayed["provenance"]["source_kind"],
        )

    def test_changed_or_incomplete_incoming_corpus_fails_without_state(self) -> None:
        missing = self.incoming / MNEME.CORPUS.FIXTURES[-1].filename
        missing.unlink()
        with self.assertRaisesRegex(
            MNEME.HARDENING.ScopeError, "reviewed inventory"
        ):
            MNEME.ingest(self.incoming, self.state, RECORDED_AT)
        self.assertFalse(self.state.exists())
        self.assertEqual([], list(self.root.glob(".state.mneme-stage-*")))

    def test_cli_find_returns_the_same_deterministic_result(self) -> None:
        self.ingest()
        output = StringIO()
        with redirect_stdout(output):
            status = MNEME.main(
                ["find", "--state", str(self.state), "--query", QUERY]
            )
        self.assertEqual(0, status)
        self.assertEqual(MNEME.find(self.state, QUERY), json.loads(output.getvalue()))


if __name__ == "__main__":
    unittest.main()
