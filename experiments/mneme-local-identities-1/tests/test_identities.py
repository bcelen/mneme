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
SPEC = importlib.util.spec_from_file_location("mneme_local_identities_1", EXPERIMENT_ROOT / "mneme_identities.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load the identities experiment")
IDS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(IDS)
P3 = IDS.P3
HARDENING = IDS.HARDENING
EML = P3.EML_FIXTURES
MBOX = P3.MBOX_FIXTURES
MIRA = "mira.sol@example.test"
# Occurrences that involve Mira (worked out from the fixtures, see RESULTS.md).
MIRA_AS_SENDER = ["EML-001", "EML-003", "EML-005", "EML-006", "EML-016", "EML-021"]
MIRA_AS_RECIPIENT = ["EML-004", "EML-007", "EML-008", "EML-009", "EML-012", "EML-015", "EML-018",
                     "EML-020", "EML-022", "EML-024"]


def snapshot(root: Path):
    return [
        (p.relative_to(root).as_posix(), hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "dir")
        for p in sorted(root.rglob("*"))
    ]


class AddressParsingTests(unittest.TestCase):
    def test_addresses_are_normalized_and_names_kept_as_evidence(self) -> None:
        self.assertEqual(
            [("Míra Sol", "mira.sol@example.test"), ("", "arin.vale@example.test")],
            IDS._named_addresses("Míra Sol <Mira.Sol@Example.TEST>, ARIN.VALE@example.test"),
        )
        self.assertEqual([], IDS._named_addresses("undisclosed-recipients:;"))
        self.assertEqual([], IDS._named_addresses(None))


class AddressIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory(prefix="mneme-identities-1-")
        cls.root = Path(cls.temporary.name)
        cls.state = cls.root / "state"
        inbox, damaged = MBOX.fixture("MBOX-001"), MBOX.fixture("MBOX-004")
        batches = (
            ("base", EML.base_members(), "2026-09-20T12:00:00Z"),
            ("mixed", EML.increment_members() + ((inbox.filename, inbox.data),), "2026-09-28T09:00:00Z"),
            ("damaged", ((damaged.filename, damaged.data),), "2026-09-28T11:00:00Z"),
        )
        with mock.patch.object(socket, "socket", side_effect=AssertionError("network forbidden")):
            for name, members, at in batches:
                EML.materialize_files(cls.root / name, members)
                P3.ingest(cls.root / name, cls.state, at)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def test_identities_are_addresses_and_never_people(self) -> None:
        result = IDS.identities(self.state)
        self.assertIn("not a person", result["note"])
        self.assertEqual(
            ["arin.vale@example.test", "jose.nunez@example.test", "mira.sol@example.test",
             "nila.hart@example.test", "rowan.pike@example.test", "zoe.akin@example.test"],
            [i["address"] for i in result["identities"]],
        )
        # 19 non-quarantined occurrences, each with exactly one sender and one recipient.
        self.assertEqual(19, sum(i["as_sender"] for i in result["identities"]))
        self.assertEqual(19, sum(i["as_recipient"] for i in result["identities"]))

    def test_summary_counts_dates_duplicates_and_display_names(self) -> None:
        mira = next(i for i in IDS.identities(self.state)["identities"] if i["address"] == MIRA)
        self.assertEqual(
            {
                "address": MIRA,
                "as_recipient": 10,
                "as_sender": 6,
                # EML-001, EML-005, EML-016 share bytes, as do EML-018 and EML-022.
                "distinct_source_hashes": 13,
                "display_names": ["Mira Sol", "Míra Sol"],
                "families": {"eml": 11, "mbox": 5},
                "first_seen_utc": "2025-10-14T09:30:00Z",
                "last_seen_utc": "2025-10-28T09:00:00Z",
                "occurrences": 16,
                "undated_occurrences": 1,
            },
            mira,
        )
        zoe = next(i for i in IDS.identities(self.state)["identities"] if i["address"] == "zoe.akin@example.test")
        self.assertEqual((["Zoë Akın"], "2025-10-15T15:45:00Z", "2025-10-15T15:45:00Z"),
                         (zoe["display_names"], zoe["first_seen_utc"], zoe["last_seen_utc"]))

    def test_identity_detail_lists_roles_correspondents_and_resolving_citations(self) -> None:
        detail = IDS.identity(self.state, "Mira.Sol@Example.Test")
        rows = {row["source_id"]: row for row in detail["occurrence_list"]}
        self.assertEqual(sorted(MIRA_AS_SENDER + MIRA_AS_RECIPIENT), list(rows))
        self.assertEqual(MIRA_AS_SENDER, sorted(s for s, r in rows.items() if r["roles"] == ["sender"]))
        self.assertEqual(MIRA_AS_RECIPIENT, sorted(s for s, r in rows.items() if r["roles"] == ["recipient"]))
        self.assertEqual(["Míra Sol"], rows["EML-003"]["display_names"])
        self.assertEqual(("invalid", None), (rows["EML-009"]["date_status"], rows["EML-009"]["date_utc"]))
        self.assertEqual(
            [
                {"address": "arin.vale@example.test", "received_from": 4, "sent_to": 5},
                {"address": "nila.hart@example.test", "received_from": 4, "sent_to": 1},
                {"address": "rowan.pike@example.test", "received_from": 2, "sent_to": 0},
            ],
            detail["correspondents"],
        )
        for row in detail["occurrence_list"]:
            shown = P3.show(self.state, row["citation"])
            self.assertEqual((row["source_id"], row["source_sha256"]), (shown["source_id"], shown["source_sha256"]))

    def test_quarantined_occurrences_never_count(self) -> None:
        cited = {row["source_id"] for row in IDS.identity(self.state, "nila.hart@example.test")["occurrence_list"]}
        # damaged.mbox records EML-025..EML-029 are Nila's but quarantined; only the survivor counts.
        self.assertIn("EML-024", cited)
        self.assertFalse(cited & {"EML-023", "EML-025", "EML-026", "EML-027", "EML-028", "EML-029"})

    def test_read_only_deterministic_and_validated(self) -> None:
        before = snapshot(self.state)
        self.assertEqual(IDS.identities(self.state), IDS.identities(self.state))
        self.assertEqual(IDS.identity(self.state, MIRA), IDS.identity(self.state, MIRA))
        self.assertEqual(before, snapshot(self.state))
        with self.assertRaisesRegex(HARDENING.ScopeError, "one address"):
            IDS.identity(self.state, "Mira Sol")
        with self.assertRaisesRegex(HARDENING.ScopeError, "no non-quarantined occurrence"):
            IDS.identity(self.state, "nobody@example.test")

    def test_cli(self) -> None:
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(0, IDS.main(["identity", "--state", str(self.state), "--address", MIRA]))
        self.assertEqual(16, json.loads(output.getvalue())["occurrences"])
        errors = StringIO()
        with redirect_stderr(errors), redirect_stdout(StringIO()):
            self.assertEqual(2, IDS.main(["identity", "--state", str(self.state), "--address", "x"]))
        self.assertIn("one address", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
