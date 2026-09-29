from __future__ import annotations

import hashlib
import html
import importlib.util
import json
import socket
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock


PROTOTYPE_ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("mneme_local_synthetic_prototype_4", PROTOTYPE_ROOT / "mneme.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load prototype 4")
MNEME = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MNEME)
P3 = MNEME.P3
HARDENING = MNEME.HARDENING
EML = P3.EML_FIXTURES
MBOX = P3.MBOX_FIXTURES

QUERY = "lantern observatory"
# With the batches below, "lantern observatory" matches these occurrences.
QUERY_IDS = ["EML-001", "EML-005", "EML-006", "EML-008", "EML-015", "EML-016", "EML-018", "EML-021", "EML-022"]
NON_QUARANTINED = [
    "EML-001", "EML-002", "EML-003", "EML-004", "EML-005", "EML-006", "EML-007", "EML-008",
    "EML-009", "EML-012", "EML-015", "EML-016", "EML-017", "EML-018", "EML-019", "EML-020",
    "EML-021", "EML-022", "EML-024",
]


def snapshot(root: Path):
    return [
        (p.relative_to(root).as_posix(), hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "dir")
        for p in sorted(root.rglob("*"))
    ]


def ids(result):
    return [row["source_id"] for row in result["results"]]


class DateClassificationTests(unittest.TestCase):
    def test_dates_are_normalized_to_utc_without_guessing(self) -> None:
        cases = {
            "Tue, 14 Oct 2025 09:30:00 +0000": ("valid", "2025-10-14T09:30:00Z"),
            "Wed, 15 Oct 2025 18:45:00 +0300": ("valid", "2025-10-15T15:45:00Z"),
            # Crosses UTC midnight: a local 15 October is a UTC 14 October.
            "Wed, 15 Oct 2025 01:30:00 +0300": ("valid", "2025-10-14T22:30:00Z"),
            "Wed, 15 Oct 2025 01:30:00 -0000": ("no-timezone", "2025-10-15T01:30:00Z"),
            "not-a-real-date": ("invalid", None),
            "": ("missing", None),
            None: ("missing", None),
        }
        for value, (status, utc) in cases.items():
            self.assertEqual({"date_status": status, "date_utc": utc}, MNEME.classify_date(value), value)

    def test_addresses_ignore_display_names_and_case(self) -> None:
        self.assertEqual(["mira.sol@example.test"], MNEME.addresses("Míra Sol <Mira.Sol@Example.Test>"))
        self.assertEqual(
            ["arin.vale@example.test", "nila.hart@example.test"],
            MNEME.addresses("Nila Hart <nila.hart@example.test>, arin.vale@example.test"),
        )
        self.assertEqual([], MNEME.addresses(None))
        self.assertEqual([], MNEME.addresses("undisclosed-recipients:;"))


class FindFilterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory(prefix="mneme-prototype-4-")
        cls.root = Path(cls.temporary.name)
        cls.state = cls.root / "state"
        inbox = MBOX.fixture("MBOX-001")
        damaged = MBOX.fixture("MBOX-004")
        batches = (
            ("base", EML.base_members(), "2026-09-20T12:00:00Z"),
            ("mixed", EML.increment_members() + ((inbox.filename, inbox.data),), "2026-09-28T09:00:00Z"),
            ("damaged", ((damaged.filename, damaged.data),), "2026-09-28T11:00:00Z"),
        )
        with mock.patch.object(socket, "socket", side_effect=AssertionError("network forbidden")):
            for name, members, recorded_at in batches:
                EML.materialize_files(cls.root / name, members)
                P3.ingest(cls.root / name, cls.state, recorded_at)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def find(self, query=None, **filters):
        return MNEME.find(self.state, query, **filters)

    # -- compatibility ----------------------------------------------------------

    def test_unfiltered_find_is_prototype_3_find_unchanged(self) -> None:
        for query in (QUERY, "north dome", "résumé", "no-such-term"):
            self.assertEqual(P3.find(self.state, query), self.find(query))
        self.assertEqual(QUERY_IDS, ids(self.find(QUERY)))

        def cli(module):
            output = StringIO()
            with redirect_stdout(output):
                self.assertEqual(0, module.main(["find", "--state", str(self.state), "--query", QUERY]))
            return output.getvalue()

        self.assertEqual(cli(P3), cli(MNEME))

    def test_filtered_results_keep_order_and_citations(self) -> None:
        unfiltered = {row["source_id"]: row for row in self.find(QUERY)["results"]}
        filtered = self.find(QUERY, family="mbox")
        self.assertEqual(["EML-018", "EML-021", "EML-022"], ids(filtered))
        for row in filtered["results"]:
            original = unfiltered[row["source_id"]]
            self.assertEqual(original, {k: v for k, v in row.items() if k != "facts"})
            for citation in row["citations"]:
                shown = P3.show(self.state, citation["citation"])
                self.assertEqual((citation["citation"], row["source_id"]), (shown["citation"], shown["source_id"]))

    # -- individual filters -------------------------------------------------------

    def test_family_and_mailbox(self) -> None:
        self.assertEqual(["EML-001", "EML-005", "EML-006", "EML-008", "EML-015", "EML-016"],
                         ids(self.find(QUERY, family="eml")))
        self.assertEqual(["EML-024"], ids(self.find(mailbox="damaged.mbox")))
        self.assertEqual(["EML-018", "EML-019", "EML-020", "EML-021", "EML-022"],
                         ids(self.find(mailbox="observatory-inbox.mbox")))
        self.assertEqual([], ids(self.find(family="eml", mailbox="damaged.mbox")))

    def test_attachment_filters_partition_the_candidates(self) -> None:
        with_attachment = ids(self.find(has_attachment=True))
        without = ids(self.find(has_attachment=False))
        self.assertEqual(["EML-007", "EML-019"], with_attachment)
        self.assertEqual(sorted(with_attachment + without), NON_QUARANTINED)
        self.assertFalse(set(with_attachment) & set(without))

    def test_status_filter_and_quarantine_exclusion(self) -> None:
        self.assertEqual(["EML-007", "EML-008", "EML-009", "EML-012"], ids(self.find(status="indexed_with_warnings")))
        self.assertEqual(NON_QUARANTINED, sorted(
            ids(self.find(status="indexed")) + ids(self.find(status="indexed_with_warnings"))))
        with self.assertRaisesRegex(HARDENING.ScopeError, "quarantined sources are never Find results"):
            self.find(status="quarantined")

    def test_address_filters_are_case_insensitive_and_ignore_display_names(self) -> None:
        # EML-003's sender is displayed as "Míra Sol" but has the same address.
        self.assertEqual(["EML-001", "EML-003", "EML-005", "EML-006", "EML-016", "EML-021"],
                         ids(self.find(sender="MIRA.SOL@example.test")))
        self.assertEqual(["EML-004", "EML-007", "EML-008", "EML-009", "EML-012", "EML-015", "EML-018",
                          "EML-020", "EML-022", "EML-024"], ids(self.find(recipient="mira.sol@example.test")))
        sender = set(ids(self.find(sender="mira.sol@example.test")))
        recipient = set(ids(self.find(recipient="mira.sol@example.test")))
        self.assertEqual(sorted(sender | recipient), ids(self.find(participant="mira.sol@example.test")))
        self.assertEqual([], ids(self.find(sender="nobody@example.test")))

    def test_date_range_is_inclusive_in_utc_and_reports_undated_candidates(self) -> None:
        # EML-002 is dated 18:45 +0300, which is 15:45 UTC on the same day.
        one_day = self.find(since="2025-10-15", until="2025-10-15")
        self.assertEqual(["EML-002"], ids(one_day))
        self.assertEqual("2025-10-15T15:45:00Z", one_day["results"][0]["facts"]["date_utc"])
        self.assertEqual(["EML-009"], one_day["filter_report"]["undated_candidates"])
        self.assertEqual(["EML-018", "EML-019", "EML-020", "EML-022", "EML-024"],
                         ids(self.find(since="2025-10-27", until="2025-10-28")))
        open_ended = ids(self.find(since="2025-10-27"))
        self.assertEqual(ids(self.find(since="2025-10-27", until="2025-10-28")), open_ended)
        # The invalid date is never guessed into a range, even an unbounded-looking one.
        self.assertNotIn("EML-009", ids(self.find(since="0001-01-01")))
        self.assertIn("EML-009", ids(self.find(sender="nila.hart@example.test")))

    # -- combinations and inspectability ------------------------------------------

    def test_combined_filters_report_each_step(self) -> None:
        result = self.find(QUERY, participant="arin.vale@example.test", since="2025-10-14", until="2025-10-14")
        self.assertEqual(["EML-001", "EML-005", "EML-006", "EML-016"], ids(result))
        report = result["filter_report"]
        self.assertEqual(len(QUERY_IDS), report["candidates"])
        self.assertEqual(["participant", "date"], [step["filter"] for step in report["steps"]])
        self.assertEqual(report["candidates"] - len(result["results"]),
                         sum(step["removed"] for step in report["steps"]))
        self.assertEqual(len(result["results"]), report["steps"][-1]["remaining"])
        self.assertEqual({"date": {"since": "2025-10-14", "until": "2025-10-14"},
                          "participant": "arin.vale@example.test"}, result["filters"])
        for row in result["results"]:
            facts = row["facts"]
            self.assertTrue(facts["date_utc"].startswith("2025-10-14"))
            self.assertIn("arin.vale@example.test", facts["senders"] + facts["recipients"])

    def test_filter_only_listing_cites_subjects_that_resolve(self) -> None:
        listing = self.find(mailbox="observatory-inbox.mbox")
        self.assertIsNone(listing["query"])
        self.assertNotIn("normalized_terms", listing)
        for row in listing["results"]:
            self.assertEqual(1, len(row["citations"]))
            citation = row["citations"][0]
            self.assertTrue(citation["citation"].endswith("#header:subject:1"))
            shown = P3.show(self.state, citation["citation"])
            self.assertEqual(row["source_id"], shown["source_id"])
            self.assertEqual(html.escape(citation["text"], quote=True), shown["display"])

    def test_find_is_read_only_and_repeatable(self) -> None:
        before = snapshot(self.state)
        first = self.find(QUERY, has_attachment=False, since="2025-10-01")
        self.assertEqual(first, self.find(QUERY, has_attachment=False, since="2025-10-01"))
        self.assertEqual(before, snapshot(self.state))
        P3.verify_state(self.state)

    # -- validation and CLI --------------------------------------------------------

    def test_invalid_filters_stop_before_reading_state(self) -> None:
        bad = (
            ({"since": "2025-13-01"}, "calendar day"),
            ({"since": "15/10/2025"}, "YYYY-MM-DD"),
            ({"since": "2025-10-20", "until": "2025-10-19"}, "later than"),
            ({"sender": "Mira Sol"}, "one address"),
            ({"family": "pst"}, "family"),
            ({"mailbox": "../inbox.mbox"}, "mailbox"),
        )
        with mock.patch.object(P3, "current_generation", side_effect=AssertionError("state read")):
            for filters, message in bad:
                with self.assertRaisesRegex(HARDENING.ScopeError, message):
                    self.find(QUERY, **filters)
            with self.assertRaisesRegex(HARDENING.ScopeError, "needs a query"):
                self.find()

    def test_cli_filters_and_delegation(self) -> None:
        output = StringIO()
        with redirect_stdout(output):
            status = MNEME.main(["find", "--state", str(self.state), "--from", "rowan.pike@example.test",
                                 "--has-attachment"])
        self.assertEqual(0, status)
        self.assertEqual([], ids(json.loads(output.getvalue())))
        output = StringIO()
        with redirect_stdout(output):
            status = MNEME.main(["find", "--state", str(self.state), "--from", "rowan.pike@example.test"])
        self.assertEqual(["EML-008", "EML-020"], ids(json.loads(output.getvalue())))
        errors = StringIO()
        with redirect_stderr(errors), redirect_stdout(StringIO()):
            self.assertEqual(2, MNEME.main(["find", "--state", str(self.state), "--since", "tomorrow"]))
        self.assertIn("YYYY-MM-DD", errors.getvalue())
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(0, MNEME.main(["verify", "--state", str(self.state)]))
        self.assertTrue(json.loads(output.getvalue())["verified"])


if __name__ == "__main__":
    unittest.main()
