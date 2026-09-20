from __future__ import annotations

import hashlib
import os
import sys
import tempfile
import unittest
from pathlib import Path


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXPERIMENT_ROOT))
import fixtures  # noqa: E402
import hardening  # noqa: E402
import isolation  # noqa: E402


RECORDED_AT = "2026-09-20T00:00:00Z"


def synthetic_item(source_id: str, raw: bytes):
    return {
        "byte_count": len(raw),
        "content_type": "message/rfc822",
        "id": source_id,
        "input_name": f"{source_id}.eml",
        "relative_path": f"source-items/{source_id}.eml",
        "sha256": hashlib.sha256(raw).hexdigest(),
        "provenance": {
            "event": "preserve",
            "event_id": f"prov-preserve-{source_id.lower()}",
            "recorded_at": RECORDED_AT,
            "source_kind": "wholly-fictional-synthetic-fixture",
            "tool": {"name": hardening.TOOL_NAME, "version": hardening.TOOL_VERSION},
        },
    }


def controlled_message(mode: str, body: bytes = b"synthetic body\n") -> bytes:
    return (
        b"From: isolation@example.test\n"
        b"To: archive@example.test\n"
        b"Date: Sat, 20 Sep 2026 00:00:00 +0000\n"
        b"Message-ID: <isolation-" + mode.encode("ascii") + b"@example.test>\n"
        b"Subject: Synthetic isolation " + mode.encode("ascii") + b"\n"
        b"X-Mneme-Synthetic-Isolation: " + mode.encode("ascii") + b"\n"
        b"Content-Type: text/plain; charset=utf-8\n\n" + body
    )


class ParserIsolationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="mneme-isolation-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def test_hostile_input_is_process_isolated_and_parser_failure_is_quarantined(self) -> None:
        raw = (
            b"From: hostile@example.test\n"
            b"To: archive@example.test\n"
            b"Date: Sat, 20 Sep 2026 00:00:00 +0000\n"
            b"Message-ID: <hostile@example.test>\n"
            b"Subject: Hostile synthetic header\n"
            b"X-Mneme-Synthetic-Failure: parser\n"
            b"X-Oversized-Header: " + (b"A" * 64_000) + b"\n\nbody\x00\xff\n"
        )
        result = isolation.run_isolated_parse(
            synthetic_item("EML-900", raw), raw, RECORDED_AT
        )
        self.assertEqual("quarantined", result.record["status"])
        self.assertIn("synthetic parser fault injection", result.record["failure"])
        self.assertEqual({}, result.artifacts)
        self.assertEqual([], result.occurrences)
        self.assertNotEqual(os.getpid(), result.evidence.worker_pid)
        self.assertEqual("completed", result.evidence.termination)
        self.assertTrue(result.evidence.temporary_root_removed)
        self.assertFalse(Path(result.evidence.temporary_root).exists())

    def test_oversized_input_fails_before_worker_launch(self) -> None:
        raw = b"X" * (hardening.MAX_SOURCE_BYTES + 1)
        result = isolation.run_isolated_parse(
            synthetic_item("EML-901", raw), raw, RECORDED_AT
        )
        self.assertEqual("quarantined", result.record["status"])
        self.assertIn("exceeds limit", result.record["failure"])
        self.assertEqual("preflight-size-limit", result.evidence.termination)
        self.assertIsNone(result.evidence.worker_pid)
        self.assertEqual({}, result.artifacts)

    def test_wall_or_cpu_time_limit_quarantines_and_cleans_up(self) -> None:
        raw = controlled_message("timeout")
        result = isolation.run_isolated_parse(
            synthetic_item("EML-902", raw), raw, RECORDED_AT
        )
        self.assertEqual("quarantined", result.record["status"])
        self.assertIn("time limit exceeded", result.record["failure"])
        self.assertIn(
            result.evidence.termination,
            {"wall-time-limit", "worker-exit"},
        )
        self.assertTrue(result.evidence.temporary_root_removed)
        self.assertFalse(Path(result.evidence.temporary_root).exists())

    def test_data_memory_limit_quarantines_and_cleans_up(self) -> None:
        raw = controlled_message("memory")
        result = isolation.run_isolated_parse(
            synthetic_item("EML-903", raw), raw, RECORDED_AT
        )
        self.assertEqual("quarantined", result.record["status"])
        self.assertIn("memory limit exceeded", result.record["failure"])
        self.assertIn(
            result.evidence.termination,
            {"memory-limit", "completed"},
        )
        self.assertGreater(
            result.evidence.peak_resident_bytes, isolation.MEMORY_LIMIT_BYTES
        )
        self.assertTrue(result.evidence.temporary_root_removed)
        self.assertFalse(Path(result.evidence.temporary_root).exists())

    def test_excessive_depth_parser_failure_and_rebuild_are_deterministic(self) -> None:
        incoming = fixtures.materialize(self.root / "incoming")
        archive = self.root / "archive"
        hardening.preserve_package(incoming, archive, RECORDED_AT)
        evidence = []

        def parser(item, raw, recorded_at):
            result = isolation.run_isolated_parse(item, raw, recorded_at)
            evidence.append(result.evidence)
            return result.parser_tuple()

        derived_a = self.root / "derived-a"
        derived_b = self.root / "derived-b"
        first = hardening.build_derived(
            archive, derived_a, RECORDED_AT, parse_source=parser
        )
        second = hardening.build_derived(
            archive, derived_b, RECORDED_AT, parse_source=parser
        )
        self.assertEqual(
            hardening.tree_hashes(derived_a), hardening.tree_hashes(derived_b)
        )
        self.assertEqual(first, second)
        records = {
            row["source_id"]: row for row in first["messages"]["messages"]
        }
        self.assertEqual("quarantined", records["EML-013"]["status"])
        self.assertIn("MIME depth", records["EML-013"]["failure"])
        self.assertEqual("quarantined", records["EML-011"]["status"])
        self.assertIn("parser fault", records["EML-011"]["failure"])
        indexed_source_ids = {
            occurrence["source_id"]
            for rows in first["index"]["terms"].values()
            for occurrence in rows
        }
        self.assertNotIn("EML-011", indexed_source_ids)
        self.assertNotIn("EML-013", indexed_source_ids)
        self.assertFalse((derived_a / "attachments" / "EML-011").exists())
        self.assertFalse((derived_a / "attachments" / "EML-013").exists())
        self.assertEqual(28, len(evidence))
        self.assertTrue(all(row.temporary_root_removed for row in evidence))
        self.assertTrue(
            all(
                row.temporary_root is not None
                and not Path(row.temporary_root).exists()
                for row in evidence
            )
        )


if __name__ == "__main__":
    unittest.main()
