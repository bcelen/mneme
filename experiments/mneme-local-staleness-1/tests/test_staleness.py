from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import socket
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("mneme_local_staleness_1", EXPERIMENT_ROOT / "mneme_staleness.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load the staleness experiment")
STALE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(STALE)
P3 = STALE.P3
HARDENING = STALE.HARDENING
EML = P3.EML_FIXTURES
MBOX = P3.MBOX_FIXTURES
QUERY = "lantern observatory"
OLD_MBOX_RULE = "synthetic-mboxrd-segmentation-v0"
MBOX_IDS = [f"EML-{n:03d}" for n in range(15, 27)]  # damaged.mbox 015-021, inbox 022-026


def snapshot(root: Path):
    return [
        (p.relative_to(root).as_posix(), hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "dir")
        for p in sorted(root.rglob("*"))
    ]


def component(report, name):
    return next(c for c in report["components"] if c["component"] == name)


class StalenessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory(prefix="mneme-staleness-1-")
        cls.root = Path(cls.temporary.name)
        inbox, damaged = MBOX.fixture("MBOX-001"), MBOX.fixture("MBOX-004")
        EML.materialize_files(cls.root / "base", EML.base_members())
        EML.materialize_files(cls.root / "mail", ((inbox.filename, inbox.data), (damaged.filename, damaged.data)))
        cls.current = cls.root / "current-state"
        cls.stale = cls.root / "stale-state"
        with mock.patch.object(socket, "socket", side_effect=AssertionError("network forbidden")):
            for state, rule in ((cls.current, P3.MBOXRD.MBOX_RULE), (cls.stale, OLD_MBOX_RULE)):
                with mock.patch.object(P3.MBOXRD, "MBOX_RULE", rule):
                    P3.ingest(cls.root / "base", state, "2026-09-20T12:00:00Z")
                    P3.ingest(cls.root / "mail", state, "2026-09-28T09:00:00Z")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def setUp(self) -> None:
        self.work = Path(tempfile.mkdtemp(prefix="case-", dir=str(self.root)))
        self.addCleanup(shutil.rmtree, self.work)

    def test_current_state_reports_no_stale_component(self) -> None:
        report = STALE.check_staleness(self.current)
        self.assertEqual("current", report["status"])
        self.assertEqual([], report["stale_components"])
        self.assertEqual(
            ["engine-rule", "engine-tool", "isolation-profile", "mbox-rule"],
            [c["component"] for c in report["components"]],
        )
        self.assertEqual([[]] * 4, [c["stale_source_ids"] for c in report["components"]])
        self.assertEqual(P3.find(self.current, QUERY), STALE.guarded_find(self.current, QUERY))

    def test_old_mbox_rule_is_reported_with_exactly_the_affected_records(self) -> None:
        with self.assertRaisesRegex(HARDENING.IntegrityError, "stale or missing rule"):
            P3.find(self.stale, QUERY)  # prototype 3 refuses, without explanation
        report = STALE.check_staleness(self.stale)
        self.assertEqual("stale", report["status"])
        self.assertEqual(["mbox-rule"], report["stale_components"])
        mbox = component(report, "mbox-rule")
        self.assertEqual([OLD_MBOX_RULE], mbox["recorded"])
        self.assertEqual(MBOX_IDS, mbox["stale_source_ids"])
        for name in ("engine-rule", "engine-tool", "isolation-profile"):
            self.assertEqual((False, []), (component(report, name)["stale"],
                                           component(report, name)["stale_source_ids"]), name)
        with self.assertRaisesRegex(HARDENING.IntegrityError, r"stale \(mbox-rule\).*rederive"):
            STALE.guarded_find(self.stale, QUERY)

    def test_engine_rule_change_marks_every_record_stale(self) -> None:
        with mock.patch.object(HARDENING, "PROCESSING_RULE", "synthetic-eml-hardening-v3"):
            report = STALE.check_staleness(self.current)
            with self.assertRaisesRegex(HARDENING.IntegrityError, "stale or unknown"):
                P3.find(self.current, QUERY)
        engine = component(report, "engine-rule")
        self.assertTrue(engine["stale"])
        self.assertEqual(26, len(engine["stale_source_ids"]))
        self.assertIn("engine-rule", report["stale_components"])

    def test_isolation_profile_change_affects_only_parsed_records(self) -> None:
        with mock.patch.dict(P3.ISOLATION.LIMIT_PROFILE, {"wall_seconds": 5.0}):
            report = STALE.check_staleness(self.current)
        isolation = component(report, "isolation-profile")
        self.assertTrue(isolation["stale"])
        records = json.loads((self.current / "generations/generation-0002/derived/messages.json").read_text())
        parsed = sorted(r["source_id"] for r in records["messages"]
                        if r.get("isolation", {}).get("mode") == "one-source-per-process")
        self.assertEqual(parsed, isolation["stale_source_ids"])
        self.assertNotIn("EML-019", parsed)  # a damaged-segment quarantine is never parsed

    def test_corrupt_derived_state_is_not_called_stale(self) -> None:
        state = self.work / "state"
        shutil.copytree(self.current, state)
        index = state / "generations/generation-0002/derived/index.json"
        index.chmod(0o600)
        index.write_bytes(index.read_bytes().replace(b"lantern", b"lantren", 1))
        report = STALE.check_staleness(state)
        self.assertEqual("corrupt", report["status"])
        self.assertEqual(["derived member missing, extra, or changed: index.json"], report["integrity_problems"])
        with self.assertRaisesRegex(HARDENING.IntegrityError, "corrupt"):
            STALE.guarded_find(state, QUERY)

    def test_rederive_produces_current_derived_state_and_a_complete_report(self) -> None:
        before = snapshot(self.stale)
        output = self.work / "rederived"
        report = STALE.rederive(self.stale, output)
        self.assertEqual(before, snapshot(self.stale))  # the state itself is untouched
        self.assertEqual("stale", report["previous_status"])
        self.assertFalse(report["published_into_state"])
        self.assertEqual(STALE.current_rules(), report["rules"])
        self.assertEqual(["derived-manifest.json", "messages.json"], report["comparison_with_current"]["changed"])
        self.assertEqual([], report["comparison_with_current"]["added"] + report["comparison_with_current"]["removed"])
        self.assertEqual(
            # Four accepted EML quarantines, then damaged.mbox (EML-015..021) minus its survivor EML-016.
            {"EML-010", "EML-011", "EML-013", "EML-014", "EML-015", "EML-017", "EML-018", "EML-019",
             "EML-020", "EML-021"},
            set(report["failures"]),
        )
        self.assertEqual(json.loads((output / "REBUILD-REPORT.json").read_text()), report)
        archive = self.stale / "generations/generation-0002/archive"
        HARDENING.verify_derived(archive, output / "derived")
        # Rebuilding the stale archive under current rules equals the state built under them.
        self.assertEqual(HARDENING.tree_hashes(self.current / "generations/generation-0002/derived"),
                         HARDENING.tree_hashes(output / "derived"))

    def test_rederive_is_deterministic_and_publishes_nothing_on_failure(self) -> None:
        first = STALE.rederive(self.stale, self.work / "first")
        second = STALE.rederive(self.stale, self.work / "second")
        self.assertEqual(first, second)
        with mock.patch.object(P3, "rebuild_derived", side_effect=HARDENING.IntegrityError("injected")):
            with self.assertRaisesRegex(HARDENING.IntegrityError, "injected"):
                STALE.rederive(self.stale, self.work / "failed")
        self.assertFalse((self.work / "failed").exists())
        self.assertEqual([], list(self.work.glob(".*mneme-stage-*")))
        with self.assertRaisesRegex(HARDENING.ScopeError, "already exists"):
            STALE.rederive(self.stale, self.work / "first")

    def test_cli_exit_codes(self) -> None:
        for state, expected in ((self.current, 0), (self.stale, 3)):
            with redirect_stdout(StringIO()):
                self.assertEqual(expected, STALE.main(["check", "--state", str(state)]))
        errors = StringIO()
        with redirect_stderr(errors), redirect_stdout(StringIO()):
            self.assertEqual(2, STALE.main(["find", "--state", str(self.stale), "--query", QUERY]))
        self.assertIn("rederive", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
