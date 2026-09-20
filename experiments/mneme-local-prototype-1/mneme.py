#!/usr/bin/env python3
"""Small local Mneme prototype over the corrected synthetic EML engine."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence, Tuple


PROTOTYPE_ROOT = Path(__file__).resolve().parent
HARDENING_ROOT = PROTOTYPE_ROOT.parent / "synthetic-hardening-1"
if str(HARDENING_ROOT) not in sys.path:
    sys.path.insert(0, str(HARDENING_ROOT))

import fixtures as CORPUS  # noqa: E402
import hardening as HARDENING  # noqa: E402
import isolation as ISOLATION  # noqa: E402


PROTOTYPE_NAME = "mneme-local-synthetic-prototype"
PROTOTYPE_VERSION = "1"
TIMESTAMP_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def _validate_recorded_at(recorded_at: str) -> None:
    if TIMESTAMP_PATTERN.fullmatch(recorded_at) is None:
        raise HARDENING.ScopeError("recorded-at must be UTC YYYY-MM-DDTHH:MM:SSZ")


def _require_new_path(path: Path, label: str) -> None:
    if path.exists() or path.is_symlink():
        raise HARDENING.ScopeError(f"{label} already exists: {path}")
    parent = path.parent
    if parent.is_symlink() or not parent.is_dir():
        raise HARDENING.ScopeError(
            f"{label} parent must be an existing non-symlink directory: {parent}"
        )


def _incoming_paths(incoming_root: Path) -> Dict[str, Path]:
    if incoming_root.is_symlink() or not incoming_root.is_dir():
        raise HARDENING.ScopeError(
            f"incoming root must be a non-symlink directory: {incoming_root}"
        )
    expected_by_name = {fixture.filename: fixture for fixture in CORPUS.FIXTURES}
    actual_names = {candidate.name for candidate in incoming_root.iterdir()}
    if actual_names != set(expected_by_name):
        missing = sorted(set(expected_by_name) - actual_names)
        extra = sorted(actual_names - set(expected_by_name))
        raise HARDENING.ScopeError(
            f"incoming corpus differs from the reviewed inventory; missing={missing}, extra={extra}"
        )
    paths: Dict[str, Path] = {}
    for filename in sorted(expected_by_name):
        fixture = expected_by_name[filename]
        candidate = incoming_root / filename
        status = candidate.lstat()
        if stat.S_ISLNK(status.st_mode) or not stat.S_ISREG(status.st_mode):
            raise HARDENING.ScopeError(
                f"incoming member must be a regular non-symlink file: {filename}"
            )
        paths[fixture.fixture_id] = candidate
    return paths


def _state_paths(state_root: Path) -> Tuple[Path, Path]:
    if state_root.is_symlink() or not state_root.is_dir():
        raise HARDENING.IntegrityError(
            f"state root must be a non-symlink directory: {state_root}"
        )
    children = {candidate.name: candidate for candidate in state_root.iterdir()}
    if set(children) != {"archive", "derived"}:
        raise HARDENING.IntegrityError(
            "state root must contain exactly archive and derived directories"
        )
    archive = children["archive"]
    derived = children["derived"]
    if archive.is_symlink() or derived.is_symlink():
        raise HARDENING.IntegrityError("state directories must not be symlinks")
    HARDENING.verify_archive(archive)
    HARDENING.verify_derived(archive, derived)
    return archive, derived


def _new_staging_directory(target: Path) -> Path:
    _require_new_path(target, "target")
    staging = Path(
        tempfile.mkdtemp(prefix=f".{target.name}.mneme-stage-", dir=str(target.parent))
    )
    staging.chmod(0o700)
    return staging


def _publish_staging(staging: Path, target: Path) -> None:
    if target.exists() or target.is_symlink():
        raise HARDENING.ScopeError(f"target appeared during operation: {target}")
    os.rename(staging, target)


def _source_summary(manifest: Mapping[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {
        str(item["id"]): {
            "byte_count": int(item["byte_count"]),
            "sha256": str(item["sha256"]),
        }
        for item in manifest["source_items"]
    }


def ingest(
    incoming_root: Path, state_root: Path, recorded_at: str
) -> Dict[str, Any]:
    """Preserve and index the exact reviewed synthetic corpus as one local state."""

    _validate_recorded_at(recorded_at)
    input_paths = _incoming_paths(incoming_root)
    staging = _new_staging_directory(state_root)
    try:
        archive = staging / "archive"
        derived = staging / "derived"
        source_manifest = HARDENING.preserve_package(
            input_paths, archive, recorded_at
        )
        derived_result = HARDENING.build_derived(
            archive, derived, recorded_at, parse_source=ISOLATION.isolated_parser
        )
        HARDENING.verify_archive(archive)
        HARDENING.verify_derived(archive, derived)
        status_counts = Counter(
            record["status"] for record in derived_result["messages"]["messages"]
        )
        result = {
            "derived_tree_sha256": HARDENING.tree_digest(derived),
            "prototype": {"name": PROTOTYPE_NAME, "version": PROTOTYPE_VERSION},
            "source_count": len(source_manifest["source_items"]),
            "source_items": _source_summary(source_manifest),
            "source_manifest_sha256": HARDENING.sha256_path(
                archive / "manifest.json"
            ),
            "status_counts": dict(sorted(status_counts.items())),
        }
        _publish_staging(staging, state_root)
        return result
    except BaseException:
        if staging.exists():
            shutil.rmtree(staging)
        raise


def rebuild(state_root: Path, output_root: Path) -> Dict[str, Any]:
    """Rebuild derived state beside the current state and prove byte identity."""

    archive, derived = _state_paths(state_root)
    current_manifest = HARDENING.verify_derived(archive, derived)
    recorded_at = current_manifest.get("recorded_at")
    if not isinstance(recorded_at, str):
        raise HARDENING.IntegrityError("derived manifest lacks recorded-at")
    staging = _new_staging_directory(output_root)
    staging.rmdir()
    try:
        HARDENING.build_derived(
            archive, staging, recorded_at, parse_source=ISOLATION.isolated_parser
        )
        current_hashes = HARDENING.tree_hashes(derived)
        rebuilt_hashes = HARDENING.tree_hashes(staging)
        if rebuilt_hashes != current_hashes:
            raise HARDENING.IntegrityError(
                "rebuilt derived state differs from the current verified state"
            )
        result = {
            "derived_file_hashes": rebuilt_hashes,
            "derived_tree_sha256": HARDENING.tree_digest(staging),
            "rebuild_equal": True,
            "source_manifest_sha256": HARDENING.sha256_path(
                archive / "manifest.json"
            ),
        }
        _publish_staging(staging, output_root)
        return result
    except BaseException:
        if staging.exists():
            shutil.rmtree(staging)
        raise


def find(state_root: Path, query: str) -> Dict[str, Any]:
    """Run deterministic Find against verified local state."""

    archive, derived = _state_paths(state_root)
    return HARDENING.deterministic_find(archive, derived, query)


def show(state_root: Path, citation: str) -> Dict[str, Any]:
    """Display one cited source occurrence as inert, verified text."""

    archive, derived = _state_paths(state_root)
    return HARDENING.display_source(archive, derived, citation)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser("ingest")
    ingest_parser.add_argument("--incoming", type=Path, required=True)
    ingest_parser.add_argument("--state", type=Path, required=True)
    ingest_parser.add_argument("--recorded-at", required=True)

    rebuild_parser = subparsers.add_parser("rebuild")
    rebuild_parser.add_argument("--state", type=Path, required=True)
    rebuild_parser.add_argument("--output", type=Path, required=True)

    find_parser = subparsers.add_parser("find")
    find_parser.add_argument("--state", type=Path, required=True)
    find_parser.add_argument("--query", required=True)

    show_parser = subparsers.add_parser("show")
    show_parser.add_argument("--state", type=Path, required=True)
    show_parser.add_argument("--citation", required=True)
    return parser


def main(argv: Sequence[str] = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        if arguments.command == "ingest":
            result = ingest(arguments.incoming, arguments.state, arguments.recorded_at)
        elif arguments.command == "rebuild":
            result = rebuild(arguments.state, arguments.output)
        elif arguments.command == "find":
            result = find(arguments.state, arguments.query)
        elif arguments.command == "show":
            result = show(arguments.state, arguments.citation)
        else:
            raise HARDENING.ScopeError(f"unsupported command: {arguments.command}")
    except HARDENING.ExperimentError as error:
        print(f"STOPPED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
