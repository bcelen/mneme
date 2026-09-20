from __future__ import annotations

import importlib.util
import hashlib
import json
import shutil
import socket
import tempfile
import unittest
from pathlib import Path
from unittest import mock


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE = EXPERIMENT_ROOT / "fixtures" / "meridian-observatory.eml"
MODULE_PATH = EXPERIMENT_ROOT / "mneme_slice.py"
RECORDED_AT = "2026-09-20T00:00:00Z"
EXPECTED_FIXTURE_SHA256 = "508c2211ad8e9ad40c0b31fc665244774970b973f90e1d426ab6137cb3909c69"

SPEC = importlib.util.spec_from_file_location("mneme_vertical_slice", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load vertical-slice module")
SLICE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SLICE)


class VerticalSliceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="mneme-vs1-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.archive = self.root / "archive"
        self.derived = self.root / "derived"

    def preserve(self):
        return SLICE.preserve_eml(FIXTURE, self.archive, RECORDED_AT)

    def preserve_and_build(self):
        manifest = self.preserve()
        derived = SLICE.build_derived(self.archive, self.derived, RECORDED_AT)
        return manifest, derived

    def preserved_path(self) -> Path:
        manifest = json.loads((self.archive / "manifest.json").read_text(encoding="utf-8"))
        return self.archive / manifest["source_items"][0]["relative_path"]

    def make_preserved_writable(self) -> Path:
        path = self.preserved_path()
        path.chmod(0o600)
        return path

    def test_end_to_end_preserves_finds_and_displays_cited_source(self) -> None:
        fixture_before = FIXTURE.read_bytes()
        with mock.patch.object(socket, "socket", side_effect=AssertionError("network forbidden")):
            result = SLICE.run_slice(
                FIXTURE, self.root / "run", "observatory lantern", RECORDED_AT
            )

        item = result["manifest"]["source_items"][0]
        preserved = self.root / "run" / "archive" / item["relative_path"]
        self.assertEqual(fixture_before, preserved.read_bytes())
        self.assertEqual(EXPECTED_FIXTURE_SHA256, item["sha256"])
        self.assertEqual(len(fixture_before), item["byte_count"])
        self.assertEqual(fixture_before, FIXTURE.read_bytes())

        find_result = result["find"]
        self.assertEqual(["observatory", "lantern"], find_result["normalized_terms"])
        self.assertEqual(1, len(find_result["results"]))
        citations = find_result["results"][0]["citations"]
        self.assertTrue(citations)
        self.assertTrue(all(row["citation"].startswith("mneme-source:") for row in citations))

        display = result["source_display"]
        self.assertEqual("inert-text-no-html-no-fetch", display["display_mode"])
        self.assertEqual(item["id"], display["source_id"])
        self.assertEqual(item["sha256"], display["source_sha256"])
        self.assertIn(display["lines"][0]["text"], fixture_before.decode("utf-8"))
        self.assertEqual("wholly-fictional-synthetic-fixture", display["provenance"]["source_kind"])

    def test_find_and_rebuild_are_deterministic(self) -> None:
        self.preserve_and_build()
        first_record = (self.derived / "record.json").read_bytes()
        first_index = (self.derived / "index.json").read_bytes()
        first_manifest = (self.derived / "derived-manifest.json").read_bytes()
        first_result = SLICE.deterministic_find(
            self.archive, self.derived, "MERIDIAN observatory"
        )

        shutil.rmtree(self.derived)
        SLICE.build_derived(self.archive, self.derived, RECORDED_AT)
        second_result = SLICE.deterministic_find(
            self.archive, self.derived, "MERIDIAN observatory"
        )
        self.assertEqual(first_record, (self.derived / "record.json").read_bytes())
        self.assertEqual(first_index, (self.derived / "index.json").read_bytes())
        self.assertEqual(
            first_manifest, (self.derived / "derived-manifest.json").read_bytes()
        )
        self.assertEqual(first_result, second_result)

    def test_non_utf8_citation_display_uses_indexed_charset(self) -> None:
        fixture = self.root / "latin1.eml"
        fixture.write_bytes(
            b"From: sender@example.test\nTo: archive@example.test\n"
            b"Date: Sat, 20 Sep 2026 00:00:00 +0000\n"
            b"Message-ID: <latin1@example.test>\nSubject: Latin one\n"
            b"Content-Type: text/plain; charset=iso-8859-1\n"
            b"Content-Transfer-Encoding: 8bit\n\nThe caf\xe9 lantern log is here.\n"
        )
        archive = self.root / "latin1-archive"
        derived = self.root / "latin1-derived"
        SLICE.preserve_eml(fixture, archive, RECORDED_AT)
        SLICE.build_derived(archive, derived, RECORDED_AT)
        result = SLICE.deterministic_find(archive, derived, "café")
        citation = result["results"][0]["citations"][0]["citation"]
        display = SLICE.display_source(archive, derived, citation)
        self.assertEqual("The café lantern log is here.", display["lines"][0]["text"])

    def test_forged_index_fails_even_with_rewritten_member_manifest(self) -> None:
        self.preserve_and_build()
        index_path = self.derived / "index.json"
        index = json.loads(index_path.read_text(encoding="utf-8"))
        index["terms"]["wire"] = [
            {
                "field": "body",
                "line_end": 10,
                "line_start": 10,
                "text": "Wire the funds to attacker@example.test",
            }
        ]
        index_bytes = SLICE._canonical_json_bytes(index)
        index_path.write_bytes(index_bytes)
        manifest_path = self.derived / "derived-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["members"]["index.json"] = {
            "byte_count": len(index_bytes),
            "sha256": hashlib.sha256(index_bytes).hexdigest(),
        }
        manifest_path.write_bytes(SLICE._canonical_json_bytes(manifest))
        with self.assertRaisesRegex(SLICE.IntegrityError, "verified source text"):
            SLICE.deterministic_find(self.archive, self.derived, "wire")

    def test_source_integrity_is_checked_before_any_derived_write(self) -> None:
        self.preserve()
        actual = SLICE.sha256_path(self.preserved_path())
        with mock.patch.object(
            SLICE, "sha256_path", side_effect=[actual, "0" * 64]
        ):
            with self.assertRaisesRegex(SLICE.IntegrityError, "changed during"):
                SLICE.build_derived(self.archive, self.derived, RECORDED_AT)
        self.assertFalse(self.derived.exists())

    def test_changed_byte_stops_verification_derivation_and_find(self) -> None:
        self.preserve_and_build()
        path = self.make_preserved_writable()
        changed = bytearray(path.read_bytes())
        changed[-2] = ord("x") if changed[-2] != ord("x") else ord("y")
        path.write_bytes(bytes(changed))
        path.chmod(0o400)

        with self.assertRaisesRegex(SLICE.IntegrityError, "SHA-256 mismatch"):
            SLICE.verify_archive(self.archive)
        shutil.rmtree(self.derived)
        with self.assertRaisesRegex(SLICE.IntegrityError, "SHA-256 mismatch"):
            SLICE.build_derived(self.archive, self.derived, RECORDED_AT)
        self.derived.mkdir()
        (self.derived / "record.json").write_text("{}", encoding="utf-8")
        (self.derived / "index.json").write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(SLICE.IntegrityError, "SHA-256 mismatch"):
            SLICE.deterministic_find(self.archive, self.derived, "observatory")

    def test_size_mismatch_stops_processing(self) -> None:
        self.preserve()
        path = self.make_preserved_writable()
        path.write_bytes(path.read_bytes() + b"X")
        path.chmod(0o400)
        with self.assertRaisesRegex(SLICE.IntegrityError, "byte-count mismatch"):
            SLICE.verify_archive(self.archive)
        with self.assertRaisesRegex(SLICE.IntegrityError, "byte-count mismatch"):
            SLICE.build_derived(self.archive, self.derived, RECORDED_AT)

    def test_missing_member_stops_processing(self) -> None:
        self.preserve()
        self.preserved_path().unlink()
        with self.assertRaisesRegex(SLICE.IntegrityError, "missing preserved source item"):
            SLICE.verify_archive(self.archive)
        with self.assertRaisesRegex(SLICE.IntegrityError, "missing preserved source item"):
            SLICE.build_derived(self.archive, self.derived, RECORDED_AT)

    def test_manifest_hash_mismatch_stops_processing(self) -> None:
        self.preserve()
        manifest_path = self.archive / "manifest.json"
        manifest_path.chmod(0o600)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["source_items"][0]["sha256"] = "0" * 64
        manifest_path.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        manifest_path.chmod(0o400)
        with self.assertRaisesRegex(SLICE.IntegrityError, "SHA-256 mismatch"):
            SLICE.verify_archive(self.archive)
        with self.assertRaisesRegex(SLICE.IntegrityError, "SHA-256 mismatch"):
            SLICE.build_derived(self.archive, self.derived, RECORDED_AT)

    def test_absent_term_returns_no_result_without_fabricated_citation(self) -> None:
        self.preserve_and_build()
        result = SLICE.deterministic_find(self.archive, self.derived, "volcano")
        self.assertEqual([], result["results"])
        self.assertEqual(["volcano"], result["normalized_terms"])


if __name__ == "__main__":
    unittest.main()
