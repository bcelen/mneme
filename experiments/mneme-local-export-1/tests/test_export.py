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
SPEC = importlib.util.spec_from_file_location("mneme_local_export_1", EXPERIMENT_ROOT / "mneme_export.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load the export experiment")
EXPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPORT)
P3 = EXPORT.P3
HARDENING = EXPORT.HARDENING
EML = P3.EML_FIXTURES
MBOX = P3.MBOX_FIXTURES
QUERY = "lantern observatory"


def snapshot(root: Path):
    return [
        (p.relative_to(root).as_posix(), hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "dir")
        for p in sorted(root.rglob("*"))
    ]


def ingest(incoming: Path, state: Path, recorded_at: str):
    with mock.patch.object(socket, "socket", side_effect=AssertionError("network forbidden")):
        return P3.ingest(incoming, state, recorded_at)


class ExportRestoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory(prefix="mneme-export-1-")
        cls.root = Path(cls.temporary.name)
        cls.state = cls.root / "state"
        inbox, appended, damaged = (MBOX.fixture(f) for f in ("MBOX-001", "MBOX-002", "MBOX-004"))
        cls.batches = []
        for name, members, at in (
            ("base", EML.base_members(), "2026-09-20T12:00:00Z"),
            ("mixed", EML.increment_members() + ((inbox.filename, inbox.data),), "2026-09-28T09:00:00Z"),
            ("damaged", ((damaged.filename, damaged.data),), "2026-09-28T11:00:00Z"),
            ("appended", ((appended.filename, appended.data),), "2026-09-28T12:00:00Z"),
        ):
            EML.materialize_files(cls.root / name, members)
            cls.batches.append((cls.root / name, at))
        for incoming, at in cls.batches:
            ingest(incoming, cls.state, at)
        cls.export = cls.root / "export"
        cls.report = EXPORT.export_state(cls.state, cls.export)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def setUp(self) -> None:
        self.work = Path(tempfile.mkdtemp(prefix="case-", dir=str(self.root)))
        self.addCleanup(shutil.rmtree, self.work)

    def copy_export(self) -> Path:
        target = self.work / "export-copy"
        shutil.copytree(self.export, target)
        return target

    # -- layout and independence -------------------------------------------------

    def test_export_layout_is_complete_and_self_describing(self) -> None:
        self.assertTrue(self.report["complete"])
        self.assertEqual("generation-0004", self.report["current_generation"])
        self.assertEqual(["generation-0001", "generation-0002", "generation-0003", "generation-0004"],
                         self.report["generations"])
        self.assertEqual(snapshot(self.state), [
            (path[len("state/"):], digest) for path, digest in snapshot(self.export)
            if path.startswith("state/")
        ])
        self.assertIn("sha256sum -c SHA256SUMS", (self.export / "README.txt").read_text())

    def test_sha256sums_verifies_every_file_independently(self) -> None:
        lines = (self.export / "SHA256SUMS").read_text().splitlines()
        listed = {}
        for line in lines:
            digest, path = line.split("  ", 1)
            listed[path] = digest
        on_disk = {
            p.relative_to(self.export).as_posix()
            for p in self.export.rglob("*") if p.is_file()
        } - {"SHA256SUMS", "EXPORT-MANIFEST.json"}
        self.assertEqual(on_disk, set(listed))
        for path, digest in listed.items():
            self.assertEqual(digest, hashlib.sha256((self.export / path).read_bytes()).hexdigest(), path)

    def test_containers_are_reconstructed_byte_for_byte(self) -> None:
        expected = {
            "containers/obs-0001-observatory-inbox.mbox": MBOX.fixture("MBOX-001").data,
            "containers/obs-0002-damaged.mbox": MBOX.fixture("MBOX-004").data,
            "containers/obs-0003-observatory-inbox.mbox": MBOX.fixture("MBOX-002").data,
        }
        self.assertEqual(sorted(expected), self.report["container_files"])
        for path, data in expected.items():
            self.assertEqual(data, (self.export / path).read_bytes())

    def test_export_is_repeatable_and_read_only(self) -> None:
        before = snapshot(self.state)
        second = self.work / "second-export"
        EXPORT.export_state(self.state, second)
        self.assertEqual(snapshot(self.export), snapshot(second))
        self.assertEqual(before, snapshot(self.state))

    # -- restore ----------------------------------------------------------------

    def test_restore_reproduces_state_find_citations_and_rebuild(self) -> None:
        restored = self.work / "restored"
        result = EXPORT.restore_export(self.export, restored)
        self.assertTrue(result["restored"])
        self.assertEqual(snapshot(self.state), snapshot(restored))
        P3.verify_state(restored)
        found = P3.find(self.state, QUERY)
        self.assertEqual(found, P3.find(restored, QUERY))
        for row in found["results"]:
            for citation in row["citations"]:
                self.assertEqual(P3.show(self.state, citation["citation"]),
                                 P3.show(restored, citation["citation"]))
        rebuilt = P3.rebuild(restored, self.work / "rebuilt")
        self.assertTrue(rebuilt["rebuild_equal"])
        self.assertEqual(P3.rebuild(self.state, self.work / "rebuilt-original")["derived_tree_sha256"],
                         rebuilt["derived_tree_sha256"])

    def test_ingest_continues_identically_after_restore(self) -> None:
        original = self.work / "original"
        restored = self.work / "restored"
        shutil.copytree(self.state, original)
        EXPORT.restore_export(self.export, restored)
        copy = self.work / "copy-batch"
        EML.materialize_files(copy, ((("observatory-inbox-copy.mbox"), MBOX.fixture("MBOX-001").data),))
        first = ingest(copy, original, "2026-10-05T09:00:00Z")
        second = ingest(copy, restored, "2026-10-05T09:00:00Z")
        self.assertEqual(first, second)
        self.assertEqual(snapshot(original), snapshot(restored))

    # -- failure handling -------------------------------------------------------

    def test_failed_export_publishes_nothing(self) -> None:
        target = self.work / "failed-export"
        with mock.patch.object(EXPORT, "verify_export", side_effect=HARDENING.IntegrityError("injected")):
            with self.assertRaisesRegex(HARDENING.IntegrityError, "injected"):
                EXPORT.export_state(self.state, target)
        self.assertFalse(target.exists())
        self.assertEqual([], list(self.work.glob(".*mneme-stage-*")))

    def test_altered_exports_are_rejected_with_named_files(self) -> None:
        cases = {
            "changed": lambda e: (e / "state/generations/generation-0004/archive/source-items/EML-018.mboxrd"),
            "missing": lambda e: (e / "containers/obs-0002-damaged.mbox"),
            "extra": lambda e: (e / "state/generations/generation-0004/archive/stray.txt"),
        }
        for kind, locate in cases.items():
            altered = self.copy_export()
            path = locate(altered)
            if kind == "changed":
                path.chmod(0o600)
                path.write_bytes(path.read_bytes().replace(b"rota", b"ROTA", 1))
            elif kind == "missing":
                path.unlink()
            else:
                path.write_bytes(b"not part of the export\n")
            relative = path.relative_to(altered).as_posix()
            with self.assertRaisesRegex(HARDENING.IntegrityError, f"{kind}=\\[[^]]*{relative}"):
                EXPORT.verify_export(altered)
            with self.assertRaises(HARDENING.IntegrityError):
                EXPORT.restore_export(altered, self.work / f"restore-{kind}")
            self.assertFalse((self.work / f"restore-{kind}").exists())
            shutil.rmtree(altered)

    def test_container_edit_with_rewritten_hashes_is_still_rejected(self) -> None:
        altered = self.copy_export()
        container = altered / "containers/obs-0001-observatory-inbox.mbox"
        container.chmod(0o600)
        container.write_bytes(container.read_bytes().replace(b"settled", b"changed"))
        manifest_path = altered / "EXPORT-MANIFEST.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["members"] = HARDENING.tree_hashes(altered, exclude=EXPORT.SELF_DESCRIBING)
        manifest_path.chmod(0o600)
        HARDENING._write_json(manifest_path, manifest)
        sums = altered / "SHA256SUMS"
        sums.chmod(0o600)
        sums.write_bytes(EXPORT._sums_text(manifest["members"]))
        with self.assertRaisesRegex(HARDENING.IntegrityError, "differs from its segments"):
            EXPORT.verify_export(altered)

    def test_tampered_checksum_file_is_rejected(self) -> None:
        altered = self.copy_export()
        sums = altered / "SHA256SUMS"
        sums.chmod(0o600)
        sums.write_bytes(sums.read_bytes().replace(b"  README.txt", b"  README.TXT"))
        with self.assertRaisesRegex(HARDENING.IntegrityError, "SHA256SUMS disagrees"):
            EXPORT.verify_export(altered)

    def test_stale_current_and_diverged_exports_are_distinguished(self) -> None:
        self.assertEqual("current", EXPORT.verify_export(self.export, self.state)["relation_to_state"])
        live = self.work / "live"
        shutil.copytree(self.state, live)
        batch = self.work / "later"
        EML.materialize_files(batch, (("observatory-inbox-copy.mbox", MBOX.fixture("MBOX-001").data),))
        ingest(batch, live, "2026-10-05T09:00:00Z")
        stale = EXPORT.verify_export(self.export, live)
        self.assertEqual(("stale", 1), (stale["relation_to_state"], stale["generations_behind"]))
        other = self.work / "other"
        ingest(self.batches[0][0], other, "2026-09-21T12:00:00Z")
        self.assertEqual("diverged", EXPORT.verify_export(self.export, other)["relation_to_state"])

    def test_state_with_interrupted_ingest_is_not_exported(self) -> None:
        live = self.work / "live"
        shutil.copytree(self.state, live)
        (live / "generations" / ".stage-leftover").mkdir()
        with self.assertRaisesRegex(HARDENING.IntegrityError, "run recover first"):
            EXPORT.export_state(live, self.work / "refused")
        self.assertFalse((self.work / "refused").exists())

    def test_cli(self) -> None:
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(0, EXPORT.main(["verify-export", "--export", str(self.export),
                                             "--against-state", str(self.state)]))
        self.assertEqual("current", json.loads(output.getvalue())["relation_to_state"])
        errors = StringIO()
        with redirect_stderr(errors), redirect_stdout(StringIO()):
            self.assertEqual(2, EXPORT.main(["restore", "--export", str(self.export),
                                             "--output", str(self.state)]))
        self.assertIn("already exists", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
