from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import socket
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXPERIMENT_ROOT))
import fixtures  # noqa: E402

SPEC = importlib.util.spec_from_file_location(
    "mneme_synthetic_hardening", EXPERIMENT_ROOT / "hardening.py"
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load hardening module")
HARDENING = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HARDENING)

RECORDED_AT = "2026-09-20T00:00:00Z"
QUERY = "lantern observatory"


class HardeningTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="mneme-hardening-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def preserve(self, label: str = "state"):
        base = self.root / label
        input_paths = fixtures.materialize(base / "incoming")
        archive = base / "archive"
        manifest = HARDENING.preserve_package(input_paths, archive, RECORDED_AT)
        return base, input_paths, archive, manifest

    def build(self, label: str = "state"):
        base, input_paths, archive, manifest = self.preserve(label)
        derived = base / "derived"
        result = HARDENING.build_derived(archive, derived, RECORDED_AT)
        return base, input_paths, archive, manifest, derived, result

    @staticmethod
    def records_by_id(result):
        return {
            record["source_id"]: record for record in result["messages"]["messages"]
        }

    @staticmethod
    def synthetic_item(source_id, raw):
        digest = hashlib.sha256(raw).hexdigest()
        return {
            "id": source_id,
            "sha256": digest,
            "provenance": {"event_id": f"prov-preserve-{source_id.lower()}"},
        }

    @staticmethod
    def deeply_nested_message(levels):
        chunks = [
            b"From: nested@example.test\n",
            b"To: archive@example.test\n",
            b"Date: Sat, 20 Sep 2026 00:00:00 +0000\n",
            b"Message-ID: <nested@example.test>\n",
            b"Subject: Deep synthetic MIME\n",
            b'Content-Type: multipart/mixed; boundary="b0"\n\n',
        ]
        for level in range(levels - 1):
            chunks.append(f"--b{level}\n".encode("ascii"))
            chunks.append(
                f'Content-Type: multipart/mixed; boundary="b{level + 1}"\n\n'.encode(
                    "ascii"
                )
            )
        chunks.extend(
            [
                f"--b{levels - 1}\n".encode("ascii"),
                b"Content-Type: text/plain; charset=utf-8\n\nbody\n",
            ]
        )
        for level in reversed(range(levels)):
            chunks.append(f"--b{level}--\n".encode("ascii"))
        return b"".join(chunks)

    def test_fixture_catalog_has_fixed_bytes_hashes_and_expected_truth(self) -> None:
        catalog = json.loads(
            (EXPERIMENT_ROOT / "fixture-catalog.json").read_text(encoding="utf-8")
        )
        self.assertEqual(1, catalog["catalog_version"])
        self.assertEqual(fixtures.catalog_rows(), catalog["fixtures"])
        self.assertEqual(14, len(fixtures.FIXTURES))
        for fixture in fixtures.FIXTURES:
            self.assertEqual(fixtures.EXPECTED_HASHES[fixture.fixture_id], fixture.sha256)
        self.assertIn(b"\r\n", fixtures.UNICODE_CRLF)
        self.assertNotIn(b"\r\n", fixtures.PLAIN_LF)

    def test_preservation_retains_every_occurrence_and_exact_bytes(self) -> None:
        _, input_paths, archive, manifest = self.preserve()
        self.assertEqual(14, len(manifest["source_items"]))
        for item in manifest["source_items"]:
            preserved = archive / item["relative_path"]
            self.assertEqual(input_paths[item["id"]].read_bytes(), preserved.read_bytes())
            self.assertEqual(fixtures.EXPECTED_HASHES[item["id"]], item["sha256"])
            self.assertEqual(len(preserved.read_bytes()), item["byte_count"])
        HARDENING.verify_archive(archive)

    def test_declared_parse_outcomes_and_warnings_match_catalog(self) -> None:
        *_, result = self.build()
        records = self.records_by_id(result)
        for fixture in fixtures.FIXTURES:
            with self.subTest(fixture=fixture.fixture_id):
                record = records[fixture.fixture_id]
                self.assertEqual(fixture.expected_status, record["status"])
                self.assertEqual(list(fixture.expected_warnings), record["warnings"])

    def test_encodings_unicode_and_headers_are_derived_deterministically(self) -> None:
        *_, result = self.build()
        records = self.records_by_id(result)
        self.assertIn("Résumé", records["EML-002"]["fields"]["subject"])
        self.assertIn("İzmir", records["EML-002"]["fields"]["subject"])
        qp_text = "\n".join(
            part.get("text", "") for part in records["EML-003"]["parts"]
        )
        b64_text = "\n".join(
            part.get("text", "") for part in records["EML-004"]["parts"]
        )
        self.assertIn("café lantern", qp_text)
        self.assertIn("blue lantern", b64_text)
        self.assertEqual("indexed_with_warnings", records["EML-009"]["status"])
        self.assertEqual("indexed_with_warnings", records["EML-012"]["status"])

    def test_duplicate_relations_preserve_all_source_occurrences(self) -> None:
        _, _, archive, manifest, _, result = self.build()
        duplicates = result["duplicates"]
        self.assertEqual(
            ["EML-001", "EML-005"],
            duplicates["exact_byte_duplicates"][0]["source_ids"],
        )
        self.assertEqual(
            ["EML-001", "EML-005", "EML-006"],
            duplicates["message_id_duplicates"][0]["source_ids"],
        )
        self.assertEqual(14, len(manifest["source_items"]))
        self.assertTrue((archive / "source-items" / "EML-001.eml").exists())
        self.assertTrue((archive / "source-items" / "EML-005.eml").exists())

    def test_attachments_use_derived_paths_and_are_never_named_from_source_paths(self) -> None:
        _, _, _, _, derived, result = self.build()
        record = self.records_by_id(result)["EML-007"]
        attachments = [part for part in record["parts"] if "artifact_path" in part]
        self.assertEqual(3, len(attachments))
        self.assertIn("unsafe-attachment-name", record["warnings"])
        self.assertIn("duplicate-attachment-name", record["warnings"])
        expected_hashes = {
            hashlib.sha256(fixtures.ATTACHMENT_TEXT).hexdigest(),
            hashlib.sha256(fixtures.ATTACHMENT_BINARY).hexdigest(),
            hashlib.sha256(b"unnamed synthetic attachment\n").hexdigest(),
        }
        self.assertEqual(expected_hashes, {part["sha256"] for part in attachments})
        for part in attachments:
            path = derived / part["artifact_path"]
            self.assertTrue(path.is_file())
            self.assertNotIn("..", part["artifact_path"])
            self.assertTrue(path.resolve().is_relative_to(derived.resolve()))

    def test_hostile_html_is_escaped_and_build_attempts_no_network(self) -> None:
        base, _, archive, _ = self.preserve()
        derived = base / "derived"
        with mock.patch.object(socket, "socket", side_effect=AssertionError("network forbidden")):
            result = HARDENING.build_derived(archive, derived, RECORDED_AT)
        record = self.records_by_id(result)["EML-008"]
        html_parts = [
            part for part in record["parts"] if part.get("display_mode") == "escaped-inert-text"
        ]
        self.assertEqual(1, len(html_parts))
        inert = (derived / html_parts[0]["artifact_path"]).read_text(encoding="utf-8")
        self.assertIn("&lt;script&gt;", inert)
        self.assertNotIn("<script>", inert)
        self.assertIn("tracker.example.test", inert)
        self.assertIn("html-inert", record["warnings"])

    def test_hostile_codec_alias_is_quarantined_without_crashing(self) -> None:
        raw = (
            b"From: codec@example.test\nTo: archive@example.test\n"
            b"Date: Sat, 20 Sep 2026 00:00:00 +0000\n"
            b"Message-ID: <codec@example.test>\nSubject: Hostile codec\n"
            b'Content-Type: text/plain; charset="hex"\n\n616263\n'
        )
        record, occurrences, artifacts = HARDENING._parse_source(
            self.synthetic_item("EML-900", raw), raw, RECORDED_AT
        )
        self.assertEqual("quarantined", record["status"])
        self.assertIn("not a text codec", record["failure"])
        self.assertEqual([], occurrences)
        self.assertEqual({}, artifacts)

    def test_extreme_mime_depth_is_iteratively_bounded_and_quarantined(self) -> None:
        raw = self.deeply_nested_message(350)
        self.assertLess(len(raw), HARDENING.MAX_SOURCE_BYTES)
        record, occurrences, artifacts = HARDENING._parse_source(
            self.synthetic_item("EML-901", raw), raw, RECORDED_AT
        )
        self.assertEqual("quarantined", record["status"])
        self.assertIn("MIME depth", record["failure"])
        self.assertEqual([], occurrences)
        self.assertEqual({}, artifacts)

    def test_attachment_classification_uses_repository_pinned_table(self) -> None:
        raw = (
            b"From: attachment@example.test\nTo: archive@example.test\n"
            b"Date: Sat, 20 Sep 2026 00:00:00 +0000\n"
            b"Message-ID: <attachment@example.test>\nSubject: Pinned MIME\n"
            b'Content-Type: multipart/mixed; boundary="pinned"\n\n'
            b"--pinned\nContent-Type: text/plain; charset=utf-8\n\nbody\n"
            b"--pinned\nContent-Type: application/octet-stream\n"
            b"Content-Disposition: attachment; filename=report.stl\n\nsolid\n"
            b"--pinned--\n"
        )
        record, _, _ = HARDENING._parse_source(
            self.synthetic_item("EML-902", raw), raw, RECORDED_AT
        )
        self.assertEqual("model/stl", HARDENING._pinned_attachment_type("report.stl"))
        self.assertIn("attachment-content-type-mismatch", record["warnings"])

    def test_quarantined_failures_create_no_trusted_index_or_artifacts(self) -> None:
        _, _, _, _, derived, result = self.build()
        records = self.records_by_id(result)
        quarantined = {
            source_id
            for source_id, record in records.items()
            if record["status"] == "quarantined"
        }
        self.assertEqual({"EML-010", "EML-011", "EML-013", "EML-014"}, quarantined)
        indexed_source_ids = {
            occurrence["source_id"]
            for rows in result["index"]["terms"].values()
            for occurrence in rows
        }
        self.assertTrue(quarantined.isdisjoint(indexed_source_ids))
        for source_id in quarantined:
            self.assertFalse((derived / "attachments" / source_id).exists())
            self.assertFalse((derived / "inert-html" / source_id).exists())
        self.assertIn("synthetic parser fault injection", records["EML-011"]["failure"])
        self.assertIn("invalid base64", records["EML-014"]["failure"])

    def test_clean_rebuild_find_citations_and_source_display_are_deterministic(self) -> None:
        base, _, archive, _, derived_a, _ = self.build()
        derived_b = base / "derived-b"
        HARDENING.build_derived(archive, derived_b, RECORDED_AT)
        self.assertEqual(HARDENING.tree_hashes(derived_a), HARDENING.tree_hashes(derived_b))
        first = HARDENING.deterministic_find(archive, derived_a, QUERY)
        second = HARDENING.deterministic_find(archive, derived_b, QUERY)
        self.assertEqual(first, second)
        self.assertGreaterEqual(len(first["results"]), 3)
        citation = first["results"][0]["citations"][0]["citation"]
        display = HARDENING.display_source(archive, derived_a, citation)
        self.assertEqual("escaped-inert-text-no-fetch", display["display_mode"])
        self.assertIn(display["source_id"], citation)
        self.assertIn(display["source_sha256"], citation)
        self.assertEqual("wholly-fictional-synthetic-fixture", display["provenance"]["source_kind"])

        unindexed = HARDENING._citation(
            display["source_id"], display["source_sha256"], "header:from:1"
        )
        with self.assertRaisesRegex(HARDENING.IntegrityError, "verified index occurrence"):
            HARDENING.display_source(archive, derived_a, unindexed)
        malformed = citation.rsplit("#", 1)[0] + "#header:subject:x"
        with self.assertRaisesRegex(HARDENING.ScopeError, "malformed"):
            HARDENING.display_source(archive, derived_a, malformed)

    def test_complete_export_restore_and_clean_rebuild_reconcile(self) -> None:
        base, _, archive, _, derived, _ = self.build()
        export_root = base / "export"
        HARDENING.export_bundle(archive, derived, export_root, RECORDED_AT)
        restored = HARDENING.restore_bundle(export_root, base / "restore")
        self.assertEqual(HARDENING.tree_hashes(archive), HARDENING.tree_hashes(restored["archive"]))
        self.assertEqual(HARDENING.tree_hashes(derived), HARDENING.tree_hashes(restored["derived"]))
        before = HARDENING.deterministic_find(archive, derived, QUERY)
        after = HARDENING.deterministic_find(restored["archive"], restored["derived"], QUERY)
        self.assertEqual(before, after)
        shutil.rmtree(restored["derived"])
        HARDENING.build_derived(restored["archive"], restored["derived"], RECORDED_AT)
        self.assertEqual(HARDENING.tree_hashes(derived), HARDENING.tree_hashes(restored["derived"]))

    def test_export_changed_member_fails_closed(self) -> None:
        base, _, archive, _, derived, _ = self.build()
        export_root = base / "export"
        HARDENING.export_bundle(archive, derived, export_root, RECORDED_AT)
        target = export_root / "README.txt"
        target.chmod(0o600)
        target.write_bytes(target.read_bytes() + b"changed")
        with self.assertRaisesRegex(HARDENING.IntegrityError, "missing, changed, or extra"):
            HARDENING.verify_export(export_root)

    def test_export_missing_member_fails_closed(self) -> None:
        base, _, archive, _, derived, _ = self.build()
        export_root = base / "export"
        HARDENING.export_bundle(archive, derived, export_root, RECORDED_AT)
        (export_root / "README.txt").unlink()
        with self.assertRaisesRegex(HARDENING.IntegrityError, "missing, changed, or extra"):
            HARDENING.verify_export(export_root)

    def test_export_extra_member_fails_closed(self) -> None:
        base, _, archive, _, derived, _ = self.build()
        export_root = base / "export"
        HARDENING.export_bundle(archive, derived, export_root, RECORDED_AT)
        (export_root / "unexpected.txt").write_text("unexpected", encoding="utf-8")
        with self.assertRaisesRegex(HARDENING.IntegrityError, "missing, changed, or extra"):
            HARDENING.verify_export(export_root)


if __name__ == "__main__":
    unittest.main()
