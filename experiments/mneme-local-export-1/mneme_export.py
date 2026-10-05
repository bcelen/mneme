#!/usr/bin/env python3
"""Application-independent export, verification, and restore of prototype-3 state.

An export is a plain directory that can be inspected and verified without
Mneme: an exact copy of every published generation, every observed MBOX
container reconstructed as an ordinary ``.mbox`` file, a ``SHA256SUMS`` file
for standard checksum tools, a README, and a JSON manifest. It contains no
timestamps, so exporting the same state twice produces identical bytes.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence


EXPERIMENT_ROOT = Path(__file__).resolve().parent
PROTOTYPE_3_PATH = EXPERIMENT_ROOT.parent / "mneme-local-prototype-3" / "mneme.py"


def _load_prototype_3():
    name = "mneme_local_synthetic_prototype_3"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, PROTOTYPE_3_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {PROTOTYPE_3_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


P3 = _load_prototype_3()
HARDENING = P3.HARDENING

EXPORT_FORMAT = "mneme-local-synthetic-export"
EXPORT_VERSION = 1
MANIFEST_NAME = "EXPORT-MANIFEST.json"
SUMS_NAME = "SHA256SUMS"
README_NAME = "README.txt"
SELF_DESCRIBING = (MANIFEST_NAME, SUMS_NAME)

README_TEXT = """Mneme local synthetic export, format version 1

This directory is readable and verifiable without Mneme.

  state/                  Exact copy of every published generation.
    CURRENT               Name of the current generation.
    generations/<gen>/archive/manifest.json
                          Source manifest (JSON): every preserved source item
                          with its ID, source key, byte count, SHA-256,
                          provenance, and, for MBOX segments, container and
                          byte span; plus ingest batches and container
                          observations.
    generations/<gen>/archive/source-items/
                          Preserved source bytes. *.eml files are messages;
                          *.mboxrd files are exact mbox segments.
    generations/<gen>/derived/
                          Derived index and records. Rebuildable from the
                          archive; included for convenience.
  containers/             Each observed mbox container of the current
                          generation, reassembled byte-for-byte from its
                          preserved segments. Open with any mbox reader.
  SHA256SUMS              SHA-256 of every file except itself and
                          EXPORT-MANIFEST.json.
  EXPORT-MANIFEST.json    Export metadata and the same per-file hashes.

Independent verification from this directory:

  Linux:  sha256sum -c SHA256SUMS
  macOS:  shasum -a 256 -c SHA256SUMS
"""


def _require_new_path(path: Path, label: str) -> None:
    if path.exists() or path.is_symlink():
        raise HARDENING.ScopeError(f"{label} already exists: {path}")
    if path.parent.is_symlink() or not path.parent.is_dir():
        raise HARDENING.ScopeError(f"{label} parent must be an existing non-symlink directory")


def _stage_beside(target: Path) -> Path:
    stage = Path(tempfile.mkdtemp(prefix=f".{target.name}.mneme-stage-", dir=str(target.parent)))
    stage.chmod(0o700)
    return stage


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sums_text(members: Mapping[str, Mapping[str, Any]]) -> bytes:
    return "".join(f"{members[path]['sha256']}  {path}\n" for path in sorted(members)).encode("utf-8")


def _reconstruct_containers(generation_root: Path, manifest: Mapping[str, Any]) -> Dict[str, bytes]:
    items = {item["id"]: item for item in manifest["source_items"]}
    containers: Dict[str, bytes] = {}
    for observation in manifest["container_observations"]:
        data = b"".join(
            HARDENING._contained(generation_root / "archive", items[source_id]["relative_path"]).read_bytes()
            for source_id in observation["segment_ids"]
        )
        if len(data) != observation["byte_count"] or _sha256(data) != observation["sha256"]:
            raise HARDENING.IntegrityError(
                f"container does not reassemble: {observation['observation_id']}"
            )
        containers[f"containers/{observation['observation_id']}-{observation['name']}"] = data
    return containers


# ---------------------------------------------------------------------------
# Export


def export_state(state_root: Path, export_root: Path) -> Dict[str, Any]:
    """Write a complete, verified export; a failure publishes nothing."""

    verified = P3.verify_state(state_root)
    if verified["unpublished_leftovers"]:
        raise HARDENING.IntegrityError(
            f"state has unpublished leftovers {verified['unpublished_leftovers']}; run recover first"
        )
    _require_new_path(export_root, "export")
    stage = _stage_beside(export_root)
    try:
        shutil.copytree(state_root, stage / "state", symlinks=False)
        current_name, generation_root, manifest = P3.current_generation(stage / "state")
        for relative_path, data in _reconstruct_containers(generation_root, manifest).items():
            HARDENING._atomic_write(stage / relative_path, data, mode=0o400)
        HARDENING._atomic_write(stage / README_NAME, README_TEXT.encode("utf-8"), mode=0o400)
        members = HARDENING.tree_hashes(stage)
        HARDENING._atomic_write(stage / SUMS_NAME, _sums_text(members), mode=0o400)
        export_manifest = {
            "container_files": {
                f"containers/{o['observation_id']}-{o['name']}": {
                    "byte_count": o["byte_count"],
                    "container_key": o["container_key"],
                    "observation_id": o["observation_id"],
                    "sha256": o["sha256"],
                }
                for o in manifest["container_observations"]
            },
            "current_generation": current_name,
            "derived_tree_sha256": HARDENING.tree_digest(generation_root / "derived"),
            "export_format": EXPORT_FORMAT,
            "export_version": EXPORT_VERSION,
            "generations": [g["generation"] for g in verified["generations"]],
            "members": members,
            "source_count": len(manifest["source_items"]),
            "source_manifest_sha256": HARDENING.sha256_path(generation_root / "archive" / "manifest.json"),
        }
        HARDENING._write_json(stage / MANIFEST_NAME, export_manifest, mode=0o400)
        report = verify_export(stage)
        if export_root.exists() or export_root.is_symlink():
            raise HARDENING.ScopeError(f"export appeared during export: {export_root}")
        os.rename(stage, export_root)
    except BaseException:
        if stage.exists():
            shutil.rmtree(stage)
        raise
    return {**report, "export_sha256sums_sha256": HARDENING.sha256_path(export_root / SUMS_NAME)}


# ---------------------------------------------------------------------------
# Verification


def _chain_digests(state_root: Path, generations: Sequence[str]) -> List[str]:
    return [
        HARDENING.sha256_path(state_root / "generations" / name / "archive" / "manifest.json")
        for name in generations
    ]


def verify_export(export_root: Path, against_state: Optional[Path] = None) -> Dict[str, Any]:
    """Verify an export completely; name every missing, extra, or changed file."""

    if export_root.is_symlink() or not export_root.is_dir():
        raise HARDENING.IntegrityError(f"export must be a non-symlink directory: {export_root}")
    manifest_path = export_root / MANIFEST_NAME
    HARDENING._require_regular(manifest_path, "export manifest")
    manifest = HARDENING._load_json(manifest_path)
    if manifest.get("export_format") != EXPORT_FORMAT or manifest.get("export_version") != EXPORT_VERSION:
        raise HARDENING.IntegrityError("unsupported export format or version")
    listed = manifest.get("members")
    if not isinstance(listed, dict):
        raise HARDENING.IntegrityError("export manifest member map is missing")
    actual = HARDENING.tree_hashes(export_root, exclude=SELF_DESCRIBING)
    missing = sorted(set(listed) - set(actual))
    extra = sorted(set(actual) - set(listed))
    changed = sorted(path for path in set(listed) & set(actual) if listed[path] != actual[path])
    if missing or extra or changed:
        raise HARDENING.IntegrityError(
            f"export is incomplete or altered; missing={missing}, extra={extra}, changed={changed}"
        )
    sums_path = export_root / SUMS_NAME
    HARDENING._require_regular(sums_path, "checksum file")
    if sums_path.read_bytes() != _sums_text(listed):
        raise HARDENING.IntegrityError("SHA256SUMS disagrees with the export manifest")

    state = export_root / "state"
    chain = P3.verify_state(state)
    if chain["unpublished_leftovers"]:
        raise HARDENING.IntegrityError("exported state contains unpublished leftovers")
    current_name, generation_root, source_manifest = P3.current_generation(state)
    if (
        chain["current"] != manifest.get("current_generation")
        or [g["generation"] for g in chain["generations"]] != manifest.get("generations")
        or HARDENING.sha256_path(generation_root / "archive" / "manifest.json")
        != manifest.get("source_manifest_sha256")
        or HARDENING.tree_digest(generation_root / "derived") != manifest.get("derived_tree_sha256")
    ):
        raise HARDENING.IntegrityError("export manifest disagrees with the exported state")
    containers = _reconstruct_containers(generation_root, source_manifest)
    if set(containers) != set(manifest.get("container_files", {})):
        raise HARDENING.IntegrityError("exported containers do not match the observations")
    for relative_path, data in containers.items():
        if (export_root / relative_path).read_bytes() != data:
            raise HARDENING.IntegrityError(f"exported container differs from its segments: {relative_path}")

    report: Dict[str, Any] = {
        "complete": True,
        "container_files": sorted(containers),
        "current_generation": current_name,
        "generations": manifest["generations"],
        "member_count": len(listed),
        "source_count": manifest["source_count"],
        "source_manifest_sha256": manifest["source_manifest_sha256"],
    }
    if against_state is not None:
        live = P3.verify_state(against_state)
        live_names = [g["generation"] for g in live["generations"]]
        exported_names = manifest["generations"]
        exported_chain = _chain_digests(state, exported_names)
        if live_names[: len(exported_names)] == exported_names and _chain_digests(
            against_state, exported_names
        ) == exported_chain:
            report["relation_to_state"] = "current" if live_names == exported_names else "stale"
            report["generations_behind"] = len(live_names) - len(exported_names)
        else:
            report["relation_to_state"] = "diverged"
    return report


# ---------------------------------------------------------------------------
# Restore


def restore_export(export_root: Path, restore_root: Path) -> Dict[str, Any]:
    """Restore a verified export into a new state directory; a failure publishes nothing."""

    report = verify_export(export_root)
    _require_new_path(restore_root, "restore target")
    stage = _stage_beside(restore_root)
    try:
        staged = stage / "state"
        shutil.copytree(export_root / "state", staged, symlinks=False)
        restored = P3.verify_state(staged)
        exported = {
            path[len("state/"):]: value
            for path, value in HARDENING._load_json(export_root / MANIFEST_NAME)["members"].items()
            if path.startswith("state/")
        }
        if HARDENING.tree_hashes(staged) != exported:
            raise HARDENING.IntegrityError("restored state differs from the exported state")
        if restore_root.exists() or restore_root.is_symlink():
            raise HARDENING.ScopeError(f"restore target appeared during restore: {restore_root}")
        os.rename(staged, restore_root)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return {
        "current_generation": restored["current"],
        "generations": [g["generation"] for g in restored["generations"]],
        "restored": True,
        "source_manifest_sha256": report["source_manifest_sha256"],
    }


# ---------------------------------------------------------------------------
# CLI


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    export_parser = commands.add_parser("export")
    export_parser.add_argument("--state", type=Path, required=True)
    export_parser.add_argument("--output", type=Path, required=True)
    verify_parser = commands.add_parser("verify-export")
    verify_parser.add_argument("--export", type=Path, required=True)
    verify_parser.add_argument("--against-state", type=Path)
    restore_parser = commands.add_parser("restore")
    restore_parser.add_argument("--export", type=Path, required=True)
    restore_parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args(argv)
    try:
        if arguments.command == "export":
            result = export_state(arguments.state, arguments.output)
        elif arguments.command == "verify-export":
            result = verify_export(arguments.export, arguments.against_state)
        else:
            result = restore_export(arguments.export, arguments.output)
    except HARDENING.ExperimentError as error:
        print(f"STOPPED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
