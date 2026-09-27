#!/usr/bin/env python3
"""Local Mneme prototype 2: incremental synthetic EML ingestion with stable identity."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple


PROTOTYPE_ROOT = Path(__file__).resolve().parent
HARDENING_ROOT = PROTOTYPE_ROOT.parent / "synthetic-hardening-1"
for _root in (PROTOTYPE_ROOT, HARDENING_ROOT):
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))

import hardening as HARDENING  # noqa: E402
import increment_fixtures as INCREMENT  # noqa: E402
import isolation as ISOLATION  # noqa: E402


PROTOTYPE_NAME = "mneme-local-synthetic-prototype"
PROTOTYPE_VERSION = "2"
IDENTITY_CONVENTION = "mneme-occurrence-identity-v1"
ARCHIVE_PACKAGE_ID = "pkg-mneme-local-synthetic-archive"
SOURCE_KIND = "wholly-fictional-synthetic-fixture"
SOURCE_KEY_PREFIX = "synthetic-eml:"
MAX_SOURCE_ORDINAL = 999  # The accepted citation grammar allows EML-000..EML-999.
CURRENT_NAME = "CURRENT"
GENERATIONS_NAME = "generations"
STAGING_PREFIX = ".stage-"
TIMESTAMP_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
INCOMING_NAME_PATTERN = re.compile(r"^[0-9a-z][0-9a-z._-]{0,95}\.eml$")
SOURCE_ID_PATTERN = re.compile(r"^EML-(?P<ordinal>[0-9]{3})$")
GENERATION_PATTERN = re.compile(r"^generation-(?P<ordinal>[0-9]{4})$")
BATCH_PATTERN = re.compile(r"^batch-(?P<ordinal>[0-9]{4})$")


# ---------------------------------------------------------------------------
# Naming and small helpers


def _validate_recorded_at(recorded_at: str) -> None:
    if TIMESTAMP_PATTERN.fullmatch(recorded_at) is None:
        raise HARDENING.ScopeError("recorded-at must be UTC YYYY-MM-DDTHH:MM:SSZ")


def source_key_for(filename: str) -> str:
    return f"{SOURCE_KEY_PREFIX}{filename}"


def source_id_for(ordinal: int) -> str:
    if ordinal < 1 or ordinal > MAX_SOURCE_ORDINAL:
        raise HARDENING.ScopeError(
            f"source ordinal {ordinal} is outside the citation-compatible range "
            f"1..{MAX_SOURCE_ORDINAL}"
        )
    return f"EML-{ordinal:03d}"


def _generation_name(ordinal: int) -> str:
    return f"generation-{ordinal:04d}"


def _batch_id(ordinal: int) -> str:
    return f"batch-{ordinal:04d}"


def _require_new_path(path: Path, label: str) -> None:
    if path.exists() or path.is_symlink():
        raise HARDENING.ScopeError(f"{label} already exists: {path}")
    parent = path.parent
    if parent.is_symlink() or not parent.is_dir():
        raise HARDENING.ScopeError(
            f"{label} parent must be an existing non-symlink directory: {parent}"
        )


# ---------------------------------------------------------------------------
# Incoming batch


def _read_regular_file(path: Path) -> bytes:
    """Read one incoming member without following symlinks."""

    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(str(path), flags)
    except OSError as error:
        raise HARDENING.ScopeError(
            f"incoming member must be a regular non-symlink file: {path.name}"
        ) from error
    try:
        status = os.fstat(descriptor)
        if not stat.S_ISREG(status.st_mode):
            raise HARDENING.ScopeError(
                f"incoming member must be a regular non-symlink file: {path.name}"
            )
        if status.st_nlink != 1:
            raise HARDENING.ScopeError(
                f"incoming member must not be hard-linked: {path.name}"
            )
        if status.st_size > HARDENING.MAX_SOURCE_BYTES:
            raise HARDENING.ScopeError(
                f"incoming member exceeds {HARDENING.MAX_SOURCE_BYTES} bytes: {path.name}"
            )
        with os.fdopen(descriptor, "rb") as handle:
            descriptor = -1
            data = handle.read(HARDENING.MAX_SOURCE_BYTES + 1)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    if len(data) != status.st_size:
        raise HARDENING.ScopeError(f"incoming member changed while reading: {path.name}")
    return data


def read_incoming_batch(incoming_root: Path) -> List[Dict[str, Any]]:
    """Return the incoming batch sorted by source key, restricted to reviewed bytes."""

    if incoming_root.is_symlink() or not incoming_root.is_dir():
        raise HARDENING.ScopeError(
            f"incoming root must be a non-symlink directory: {incoming_root}"
        )
    allowlist = INCREMENT.reviewed_sha256_allowlist()
    members: List[Dict[str, Any]] = []
    for candidate in sorted(incoming_root.iterdir(), key=lambda path: path.name):
        name = candidate.name
        if INCOMING_NAME_PATTERN.fullmatch(name) is None:
            raise HARDENING.ScopeError(f"incoming member name is not supported: {name!r}")
        data = _read_regular_file(candidate)
        digest = hashlib.sha256(data).hexdigest()
        if digest not in allowlist:
            raise HARDENING.ScopeError(
                f"incoming member is not a reviewed synthetic fixture: {name}"
            )
        members.append(
            {
                "byte_count": len(data),
                "data": data,
                "input_name": name,
                "sha256": digest,
                "source_key": source_key_for(name),
            }
        )
    if not members:
        raise HARDENING.ScopeError("incoming batch is empty")
    members.sort(key=lambda member: member["source_key"])
    return members


# ---------------------------------------------------------------------------
# Manifest identity extension


def _verify_identity_extension(manifest: Mapping[str, Any]) -> None:
    """Check the occurrence-identity fields layered on the accepted v1 manifest."""

    if manifest.get("identity_convention") != IDENTITY_CONVENTION:
        raise HARDENING.IntegrityError("unsupported source identity convention")
    package = manifest["source_package"]
    if package.get("id") != ARCHIVE_PACKAGE_ID:
        raise HARDENING.IntegrityError("source package identity is unexpected")
    items = manifest["source_items"]
    batches = manifest.get("ingest_batches")
    if not isinstance(batches, list) or not batches:
        raise HARDENING.IntegrityError("ingest batch ledger is missing")

    seen_keys = set()
    for ordinal, item in enumerate(items, start=1):
        expected_id = source_id_for(ordinal)
        if item.get("id") != expected_id:
            raise HARDENING.IntegrityError(
                f"source IDs must be contiguous archive assignments; expected {expected_id}"
            )
        if item.get("relative_path") != f"source-items/{expected_id}.eml":
            raise HARDENING.IntegrityError(f"source path is not ID-derived: {expected_id}")
        key = item.get("source_key")
        name = item.get("input_name")
        if (
            not isinstance(name, str)
            or INCOMING_NAME_PATTERN.fullmatch(name) is None
            or key != source_key_for(name)
        ):
            raise HARDENING.IntegrityError(f"source key is malformed: {expected_id}")
        if key in seen_keys:
            raise HARDENING.IntegrityError(f"source key is bound twice: {key}")
        seen_keys.add(key)
        provenance = item.get("provenance")
        if (
            not isinstance(provenance, dict)
            or provenance.get("event_id") != f"prov-preserve-{expected_id.lower()}"
            or provenance.get("source_kind") != SOURCE_KIND
        ):
            raise HARDENING.IntegrityError(f"preservation provenance is malformed: {expected_id}")

    position = 0
    for ordinal, batch in enumerate(batches, start=1):
        if not isinstance(batch, dict) or batch.get("batch_id") != _batch_id(ordinal):
            raise HARDENING.IntegrityError("ingest batch IDs must be contiguous")
        recorded_at = batch.get("recorded_at")
        if not isinstance(recorded_at, str) or TIMESTAMP_PATTERN.fullmatch(recorded_at) is None:
            raise HARDENING.IntegrityError(f"ingest batch time is malformed: {batch['batch_id']}")
        members = batch.get("source_ids")
        if not isinstance(members, list) or not members:
            raise HARDENING.IntegrityError(f"ingest batch is empty: {batch['batch_id']}")
        expected = [item["id"] for item in items[position : position + len(members)]]
        if members != expected:
            raise HARDENING.IntegrityError(
                f"ingest batch does not own a contiguous ID range: {batch['batch_id']}"
            )
        for item in items[position : position + len(members)]:
            if item.get("ingest_batch") != batch["batch_id"]:
                raise HARDENING.IntegrityError(f"source batch link is wrong: {item['id']}")
            if item["provenance"].get("recorded_at") != recorded_at:
                raise HARDENING.IntegrityError(f"source batch time is wrong: {item['id']}")
        position += len(members)
    if position != len(items):
        raise HARDENING.IntegrityError("ingest batches do not cover every source item")


def verify_extends(previous: Mapping[str, Any], current: Mapping[str, Any]) -> None:
    """Require the current manifest to append exactly one batch to the previous one."""

    old_items = previous["source_items"]
    old_batches = previous["ingest_batches"]
    if current["source_items"][: len(old_items)] != old_items:
        raise HARDENING.IntegrityError("existing source items changed between generations")
    if current["ingest_batches"][: len(old_batches)] != old_batches:
        raise HARDENING.IntegrityError("existing ingest batches changed between generations")
    if len(current["ingest_batches"]) != len(old_batches) + 1:
        raise HARDENING.IntegrityError("a generation must append exactly one ingest batch")


def verify_generation(generation_root: Path) -> Dict[str, Any]:
    """Verify one published or staged generation and return its source manifest."""

    if generation_root.is_symlink() or not generation_root.is_dir():
        raise HARDENING.IntegrityError(
            f"generation must be a non-symlink directory: {generation_root}"
        )
    children = {candidate.name for candidate in generation_root.iterdir()}
    if children != {"archive", "derived"}:
        raise HARDENING.IntegrityError(
            "generation must contain exactly archive and derived directories"
        )
    archive = generation_root / "archive"
    derived = generation_root / "derived"
    manifest = HARDENING.verify_archive(archive)
    _verify_identity_extension(manifest)
    derived_manifest = HARDENING.verify_derived(archive, derived)
    if derived_manifest.get("recorded_at") != manifest["ingest_batches"][-1]["recorded_at"]:
        raise HARDENING.IntegrityError("derived state is not bound to the latest ingest batch")
    return manifest


# ---------------------------------------------------------------------------
# State layout: <state>/CURRENT names one directory under <state>/generations/


def _read_current_name(state_root: Path) -> str:
    current_path = state_root / CURRENT_NAME
    HARDENING._require_regular(current_path, "current-generation pointer")
    try:
        text = current_path.read_text(encoding="ascii")
    except (OSError, UnicodeError) as error:
        raise HARDENING.IntegrityError("current-generation pointer is unreadable") from error
    name = text[:-1] if text.endswith("\n") else ""
    if GENERATION_PATTERN.fullmatch(name) is None:
        raise HARDENING.IntegrityError("current-generation pointer is malformed")
    return name


def _published_generations(state_root: Path) -> List[str]:
    if state_root.is_symlink() or not state_root.is_dir():
        raise HARDENING.IntegrityError(f"state root must be a non-symlink directory: {state_root}")
    if {candidate.name for candidate in state_root.iterdir()} != {
        CURRENT_NAME,
        GENERATIONS_NAME,
    }:
        raise HARDENING.IntegrityError(
            "state root must contain exactly CURRENT and generations"
        )
    generations_root = state_root / GENERATIONS_NAME
    if generations_root.is_symlink() or not generations_root.is_dir():
        raise HARDENING.IntegrityError("generations must be a non-symlink directory")
    names = sorted(candidate.name for candidate in generations_root.iterdir())
    staging = [name for name in names if name.startswith(STAGING_PREFIX)]
    if staging:
        raise HARDENING.IntegrityError(
            f"interrupted staging is present and must be inspected: {staging}"
        )
    expected = [_generation_name(ordinal) for ordinal in range(1, len(names) + 1)]
    if names != expected:
        raise HARDENING.IntegrityError("published generations must be contiguous")
    if _read_current_name(state_root) != names[-1]:
        raise HARDENING.IntegrityError(
            "CURRENT does not name the latest generation; an interrupted publication "
            "must be inspected"
        )
    return names


def current_generation(state_root: Path) -> Tuple[str, Path, Dict[str, Any]]:
    names = _published_generations(state_root)
    root = state_root / GENERATIONS_NAME / names[-1]
    return names[-1], root, verify_generation(root)


def verify_state(state_root: Path) -> Dict[str, Any]:
    """Verify every retained generation and the append-only chain between them."""

    names = _published_generations(state_root)
    previous: Optional[Dict[str, Any]] = None
    generations = []
    for name in names:
        root = state_root / GENERATIONS_NAME / name
        manifest = verify_generation(root)
        if previous is None:
            if len(manifest["ingest_batches"]) != 1:
                raise HARDENING.IntegrityError("the first generation must hold one batch")
        else:
            verify_extends(previous, manifest)
        previous = manifest
        generations.append(
            {
                "derived_tree_sha256": HARDENING.tree_digest(root / "derived"),
                "generation": name,
                "source_count": len(manifest["source_items"]),
                "source_manifest_sha256": HARDENING.sha256_path(
                    root / "archive" / "manifest.json"
                ),
            }
        )
    return {"current": names[-1], "generations": generations, "verified": True}


def _write_current(state_root: Path, generation_name: str) -> None:
    HARDENING._atomic_write(
        state_root / CURRENT_NAME, f"{generation_name}\n".encode("ascii"), mode=0o600
    )


# ---------------------------------------------------------------------------
# Planning, staging, and publication


def plan_batch(
    previous: Optional[Mapping[str, Any]], batch: Sequence[Mapping[str, Any]]
) -> Dict[str, Any]:
    """Classify incoming members against existing identity before any staging."""

    existing = list(previous["source_items"]) if previous else []
    by_key = {item["source_key"]: item for item in existing}
    already_preserved: Dict[str, str] = {}
    new_members: List[Mapping[str, Any]] = []
    for member in batch:
        known = by_key.get(member["source_key"])
        if known is None:
            new_members.append(member)
            continue
        if known["sha256"] != member["sha256"] or known["byte_count"] != member["byte_count"]:
            raise HARDENING.IntegrityError(
                f"source key {member['source_key']} is already bound to {known['id']} "
                "with different bytes; changed source bytes are rejected"
            )
        already_preserved[member["source_key"]] = known["id"]
    assignments = [
        (source_id_for(len(existing) + offset), member)
        for offset, member in enumerate(new_members, start=1)
    ]
    return {"already_preserved": already_preserved, "assignments": assignments}


def _parse_at_preservation_time(item: Mapping[str, Any], raw: bytes, recorded_at: str):
    """Derive each source with the logical time of its own ingest batch."""

    return ISOLATION.isolated_parser(item, raw, item["provenance"]["recorded_at"])


def _build_generation(
    staged: Path,
    previous_root: Optional[Path],
    previous: Optional[Mapping[str, Any]],
    assignments: Sequence[Tuple[str, Mapping[str, Any]]],
    recorded_at: str,
) -> Dict[str, Any]:
    archive = staged / "archive"
    derived = staged / "derived"
    archive.mkdir(mode=0o700)
    items: List[Dict[str, Any]] = []
    batches: List[Dict[str, Any]] = []
    if previous is not None and previous_root is not None:
        for item in previous["source_items"]:
            raw = HARDENING._contained(previous_root / "archive", item["relative_path"]).read_bytes()
            if hashlib.sha256(raw).hexdigest() != item["sha256"]:
                raise HARDENING.IntegrityError(f"existing source changed: {item['id']}")
            HARDENING._atomic_write(archive / item["relative_path"], raw, mode=0o400)
            items.append(dict(item))
        batches = [dict(batch) for batch in previous["ingest_batches"]]

    batch_id = _batch_id(len(batches) + 1)
    for source_id, member in assignments:
        relative_path = f"source-items/{source_id}.eml"
        HARDENING._atomic_write(archive / relative_path, member["data"], mode=0o400)
        if (archive / relative_path).read_bytes() != member["data"]:
            raise HARDENING.IntegrityError(f"preserved bytes differ: {source_id}")
        items.append(
            {
                "byte_count": member["byte_count"],
                "content_type": "message/rfc822",
                "id": source_id,
                "ingest_batch": batch_id,
                "input_name": member["input_name"],
                "provenance": {
                    "event": "preserve",
                    "event_id": f"prov-preserve-{source_id.lower()}",
                    "recorded_at": recorded_at,
                    "source_kind": SOURCE_KIND,
                    "tool": {"name": PROTOTYPE_NAME, "version": PROTOTYPE_VERSION},
                },
                "relative_path": relative_path,
                "sha256": member["sha256"],
                "source_key": member["source_key"],
            }
        )
    batches.append(
        {
            "batch_id": batch_id,
            "recorded_at": recorded_at,
            "source_ids": [source_id for source_id, _ in assignments],
        }
    )
    manifest: Dict[str, Any] = {
        "hash_algorithm": "sha256",
        "identity_convention": IDENTITY_CONVENTION,
        "ingest_batches": batches,
        "manifest_version": 1,
        "source_items": items,
        "source_package": {
            "id": ARCHIVE_PACKAGE_ID,
            "members": [item["id"] for item in items],
            "source_family": "synthetic-eml",
        },
    }
    HARDENING._write_json(archive / "manifest.json", manifest, mode=0o400)
    rebuild_derived(archive, derived)
    staged_manifest = verify_generation(staged)
    if previous is not None:
        verify_extends(previous, staged_manifest)
    return staged_manifest


def rebuild_derived(archive: Path, derived: Path) -> Dict[str, Any]:
    """Deterministic full derivation from the archive, in stable source-ID order."""

    manifest = HARDENING.verify_archive(archive)
    _verify_identity_extension(manifest)
    return HARDENING.build_derived(
        archive,
        derived,
        manifest["ingest_batches"][-1]["recorded_at"],
        parse_source=_parse_at_preservation_time,
    )


def _duplicate_links(
    manifest: Mapping[str, Any], new_ids: Sequence[str]
) -> Dict[str, List[str]]:
    by_hash: Dict[str, List[str]] = {}
    for item in manifest["source_items"]:
        by_hash.setdefault(item["sha256"], []).append(item["id"])
    by_id = {item["id"]: item for item in manifest["source_items"]}
    return {
        source_id: [other for other in by_hash[by_id[source_id]["sha256"]] if other != source_id]
        for source_id in new_ids
        if len(by_hash[by_id[source_id]["sha256"]]) > 1
    }


def _generation_summary(generation_root: Path, manifest: Mapping[str, Any]) -> Dict[str, Any]:
    messages = HARDENING._load_json(generation_root / "derived" / "messages.json")["messages"]
    return {
        "derived_tree_sha256": HARDENING.tree_digest(generation_root / "derived"),
        "source_count": len(manifest["source_items"]),
        "source_manifest_sha256": HARDENING.sha256_path(
            generation_root / "archive" / "manifest.json"
        ),
        "status_counts": dict(sorted(Counter(record["status"] for record in messages).items())),
    }


def ingest(incoming_root: Path, state_root: Path, recorded_at: str) -> Dict[str, Any]:
    """Preserve new synthetic occurrences and publish one new verified generation."""

    _validate_recorded_at(recorded_at)
    batch = read_incoming_batch(incoming_root)
    creating = not (state_root.exists() or state_root.is_symlink())
    if creating:
        _require_new_path(state_root, "state root")
        previous_name, previous_root, previous = None, None, None
    else:
        previous_name, previous_root, previous = current_generation(state_root)

    plan = plan_batch(previous, batch)
    result: Dict[str, Any] = {
        "already_preserved": plan["already_preserved"],
        "prototype": {"name": PROTOTYPE_NAME, "version": PROTOTYPE_VERSION},
    }
    if not plan["assignments"]:
        # Only reachable with an existing state: a new state treats every member as new.
        result.update(
            {
                "generation": previous_name,
                "new_occurrences": {},
                "published": False,
                **_generation_summary(previous_root, previous),
            }
        )
        return result

    generation_ordinal = 1 if previous_name is None else int(previous_name.split("-")[1]) + 1
    generation_name = _generation_name(generation_ordinal)
    if creating:
        stage_root = Path(
            tempfile.mkdtemp(prefix=f".{state_root.name}.mneme-stage-", dir=str(state_root.parent))
        )
        staged = stage_root / GENERATIONS_NAME / generation_name
        staged.mkdir(parents=True, mode=0o700)
    else:
        stage_root = Path(
            tempfile.mkdtemp(prefix=STAGING_PREFIX, dir=str(state_root / GENERATIONS_NAME))
        )
        staged = stage_root
    stage_root.chmod(0o700)

    published_generation: Optional[Path] = None
    try:
        manifest = _build_generation(
            staged, previous_root, previous, plan["assignments"], recorded_at
        )
        if previous_root is not None:
            HARDENING.verify_archive(previous_root / "archive")
        summary = _generation_summary(staged, manifest)
        if creating:
            _write_current(stage_root, generation_name)
            if state_root.exists() or state_root.is_symlink():
                raise HARDENING.ScopeError(f"state root appeared during ingest: {state_root}")
            os.rename(stage_root, state_root)
        else:
            target = state_root / GENERATIONS_NAME / generation_name
            if target.exists() or target.is_symlink():
                raise HARDENING.IntegrityError(f"generation appeared during ingest: {target}")
            os.rename(staged, target)
            published_generation = target
            _write_current(state_root, generation_name)
            published_generation = None
    except BaseException:
        if published_generation is not None and published_generation.exists():
            shutil.rmtree(published_generation)
        if stage_root.exists():
            shutil.rmtree(stage_root)
        raise

    assignments = plan["assignments"]
    new_ids = [source_id for source_id, _ in assignments]
    result.update(
        {
            "batch_id": manifest["ingest_batches"][-1]["batch_id"],
            "exact_byte_duplicate_of": _duplicate_links(manifest, new_ids),
            "generation": generation_name,
            "new_occurrences": {
                source_id: member["source_key"] for source_id, member in assignments
            },
            "published": True,
            **summary,
        }
    )
    return result


# ---------------------------------------------------------------------------
# Read paths


def rebuild(state_root: Path, output_root: Path) -> Dict[str, Any]:
    """Rebuild current derived state from its archive and prove byte identity."""

    generation_name, generation_root, _ = current_generation(state_root)
    _require_new_path(output_root, "rebuild output")
    stage_root = Path(
        tempfile.mkdtemp(prefix=f".{output_root.name}.mneme-stage-", dir=str(output_root.parent))
    )
    stage_root.chmod(0o700)
    try:
        staged = stage_root / "derived"
        rebuild_derived(generation_root / "archive", staged)
        current_hashes = HARDENING.tree_hashes(generation_root / "derived")
        rebuilt_hashes = HARDENING.tree_hashes(staged)
        if rebuilt_hashes != current_hashes:
            raise HARDENING.IntegrityError(
                "rebuilt derived state differs from the current verified state"
            )
        result = {
            "derived_file_hashes": rebuilt_hashes,
            "derived_tree_sha256": HARDENING.tree_digest(staged),
            "generation": generation_name,
            "rebuild_equal": True,
            "source_manifest_sha256": HARDENING.sha256_path(
                generation_root / "archive" / "manifest.json"
            ),
        }
        if output_root.exists() or output_root.is_symlink():
            raise HARDENING.ScopeError(f"rebuild output appeared during rebuild: {output_root}")
        os.rename(staged, output_root)
        return result
    finally:
        if stage_root.exists():
            shutil.rmtree(stage_root)


def find(state_root: Path, query: str) -> Dict[str, Any]:
    _, generation_root, _ = current_generation(state_root)
    return HARDENING.deterministic_find(
        generation_root / "archive", generation_root / "derived", query
    )


def show(state_root: Path, citation: str) -> Dict[str, Any]:
    _, generation_root, _ = current_generation(state_root)
    return HARDENING.display_source(
        generation_root / "archive", generation_root / "derived", citation
    )


# ---------------------------------------------------------------------------
# CLI


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

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("--state", type=Path, required=True)

    find_parser = subparsers.add_parser("find")
    find_parser.add_argument("--state", type=Path, required=True)
    find_parser.add_argument("--query", required=True)

    show_parser = subparsers.add_parser("show")
    show_parser.add_argument("--state", type=Path, required=True)
    show_parser.add_argument("--citation", required=True)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        if arguments.command == "ingest":
            result = ingest(arguments.incoming, arguments.state, arguments.recorded_at)
        elif arguments.command == "rebuild":
            result = rebuild(arguments.state, arguments.output)
        elif arguments.command == "verify":
            result = verify_state(arguments.state)
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
