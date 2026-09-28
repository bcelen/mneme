#!/usr/bin/env python3
"""Local Mneme prototype 3: mixed synthetic EML and mboxrd ingestion with stable identity."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import stat
import sys
import tempfile
from collections import Counter
from email import policy
from email.parser import BytesParser
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple


PROTOTYPE_ROOT = Path(__file__).resolve().parent
EXPERIMENTS_ROOT = PROTOTYPE_ROOT.parent
for _root in (
    PROTOTYPE_ROOT,
    EXPERIMENTS_ROOT / "mneme-local-prototype-2",
    EXPERIMENTS_ROOT / "synthetic-hardening-1",
):
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))

import hardening as HARDENING  # noqa: E402
import increment_fixtures as EML_FIXTURES  # noqa: E402
import isolation as ISOLATION  # noqa: E402
import mbox_fixtures as MBOX_FIXTURES  # noqa: E402
import mboxrd as MBOXRD  # noqa: E402


PROTOTYPE_NAME = "mneme-local-synthetic-prototype"
PROTOTYPE_VERSION = "3"
IDENTITY_CONVENTION = "mneme-occurrence-identity-v2"
ARCHIVE_PACKAGE_ID = "pkg-mneme-local-synthetic-archive"
SOURCE_KIND = "wholly-fictional-synthetic-fixture"
EML_KEY_PREFIX = "synthetic-eml:"
MBOX_KEY_PREFIX = "synthetic-mbox:"
MBOX_CONTENT_TYPE = "application/x-mneme-mboxrd-segment"
MAX_CONTAINER_BYTES = 1024 * 1024
MAX_SOURCE_ORDINAL = 999  # The accepted citation grammar allows EML-000..EML-999.
CURRENT_NAME = "CURRENT"
GENERATIONS_NAME = "generations"
STAGING_PREFIX = ".stage-"
TIMESTAMP_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
INCOMING_NAME_PATTERN = re.compile(r"^[0-9a-z][0-9a-z._-]{0,95}\.(?P<suffix>eml|mbox)$")
MBOX_KEY_PATTERN = re.compile(
    r"^synthetic-mbox:(?P<name>[0-9a-z][0-9a-z._-]{0,95}\.mbox)#offset=(?P<offset>0|[1-9][0-9]*)$"
)
GENERATION_PATTERN = re.compile(r"^generation-(?P<ordinal>[0-9]{4})$")


# ---------------------------------------------------------------------------
# Naming helpers


def _validate_recorded_at(recorded_at: str) -> None:
    if TIMESTAMP_PATTERN.fullmatch(recorded_at) is None:
        raise HARDENING.ScopeError("recorded-at must be UTC YYYY-MM-DDTHH:MM:SSZ")


def eml_source_key(filename: str) -> str:
    return f"{EML_KEY_PREFIX}{filename}"


def container_key(filename: str) -> str:
    return f"{MBOX_KEY_PREFIX}{filename}"


def mbox_source_key(filename: str, offset: int) -> str:
    return f"{container_key(filename)}#offset={offset}"


def source_id_for(ordinal: int) -> str:
    if ordinal < 1 or ordinal > MAX_SOURCE_ORDINAL:
        raise HARDENING.ScopeError(
            f"source ordinal {ordinal} is outside the citation-compatible range "
            f"1..{MAX_SOURCE_ORDINAL}"
        )
    return f"EML-{ordinal:03d}"


def _relative_path(source_id: str, family: str) -> str:
    return f"source-items/{source_id}.{'eml' if family == 'eml' else 'mboxrd'}"


def _generation_name(ordinal: int) -> str:
    return f"generation-{ordinal:04d}"


def _batch_id(ordinal: int) -> str:
    return f"batch-{ordinal:04d}"


def _observation_id(ordinal: int) -> str:
    return f"obs-{ordinal:04d}"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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


def reviewed_allowlist() -> Dict[str, str]:
    """Map every reviewed synthetic input digest to its family."""

    allowlist = {digest: "eml" for digest in EML_FIXTURES.reviewed_sha256_allowlist()}
    for digest in MBOX_FIXTURES.EXPECTED_HASHES.values():
        allowlist[digest] = "mbox"
    return allowlist


def _read_regular_file(path: Path, limit: int) -> bytes:
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
            raise HARDENING.ScopeError(f"incoming member must not be hard-linked: {path.name}")
        if status.st_size > limit:
            raise HARDENING.ScopeError(f"incoming member exceeds {limit} bytes: {path.name}")
        with os.fdopen(descriptor, "rb") as handle:
            descriptor = -1
            data = handle.read(limit + 1)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    if len(data) != status.st_size:
        raise HARDENING.ScopeError(f"incoming member changed while reading: {path.name}")
    return data


def read_incoming_batch(incoming_root: Path) -> Dict[str, List[Dict[str, Any]]]:
    """Read and segment one incoming batch; every input must be reviewed synthetic bytes."""

    if incoming_root.is_symlink() or not incoming_root.is_dir():
        raise HARDENING.ScopeError(
            f"incoming root must be a non-symlink directory: {incoming_root}"
        )
    allowlist = reviewed_allowlist()
    occurrences: List[Dict[str, Any]] = []
    containers: List[Dict[str, Any]] = []
    for candidate in sorted(incoming_root.iterdir(), key=lambda path: path.name):
        name = candidate.name
        match = INCOMING_NAME_PATTERN.fullmatch(name)
        if match is None:
            raise HARDENING.ScopeError(f"incoming member name is not supported: {name!r}")
        family = match.group("suffix")
        limit = HARDENING.MAX_SOURCE_BYTES if family == "eml" else MAX_CONTAINER_BYTES
        data = _read_regular_file(candidate, limit)
        digest = _sha256(data)
        if allowlist.get(digest) != family:
            raise HARDENING.ScopeError(
                f"incoming member is not a reviewed synthetic {family} fixture: {name}"
            )
        if family == "eml":
            occurrences.append(
                {
                    "byte_count": len(data),
                    "data": data,
                    "family": "eml",
                    "input_name": name,
                    "sha256": digest,
                    "sort": (eml_source_key(name), 0),
                    "source_key": eml_source_key(name),
                }
            )
            continue
        segments = MBOXRD.segment_container(data)
        if not segments:
            raise HARDENING.ScopeError(f"mbox container is empty: {name}")
        keys = []
        for segment in segments:
            segment_bytes = data[segment.offset : segment.offset + segment.length]
            key = mbox_source_key(name, segment.offset)
            keys.append(key)
            occurrences.append(
                {
                    "byte_count": segment.length,
                    "container": {"format": "mboxrd", "key": container_key(name), "name": name},
                    "data": segment_bytes,
                    "family": "mbox",
                    "sha256": _sha256(segment_bytes),
                    "sort": (container_key(name), segment.offset),
                    "source_key": key,
                    "span": segment.as_span(),
                }
            )
        containers.append(
            {
                "byte_count": len(data),
                "container_key": container_key(name),
                "name": name,
                "segment_keys": keys,
                "sha256": digest,
            }
        )
    if not occurrences:
        raise HARDENING.ScopeError("incoming batch is empty")
    occurrences.sort(key=lambda occurrence: occurrence["sort"])
    return {"containers": containers, "occurrences": occurrences}


# ---------------------------------------------------------------------------
# Planning


def plan_batch(
    previous: Optional[Mapping[str, Any]], batch: Mapping[str, Sequence[Mapping[str, Any]]]
) -> Dict[str, Any]:
    """Classify the batch against existing identity before any staging or parsing."""

    existing = list(previous["source_items"]) if previous else []
    by_key = {item["source_key"]: item for item in existing}
    already_preserved: Dict[str, str] = {}
    new_occurrences: List[Mapping[str, Any]] = []
    for occurrence in batch["occurrences"]:
        known = by_key.get(occurrence["source_key"])
        if known is None:
            new_occurrences.append(occurrence)
            continue
        if known["sha256"] != occurrence["sha256"] or known["byte_count"] != occurrence["byte_count"]:
            raise HARDENING.IntegrityError(
                f"source key {occurrence['source_key']} is already bound to {known['id']} "
                "with different bytes; changed source bytes are rejected"
            )
        if occurrence["family"] == "mbox" and known.get("span") != occurrence["span"]:
            raise HARDENING.IntegrityError(
                f"source key {occurrence['source_key']} is already bound to {known['id']} "
                "with a different boundary context; changed source bytes are rejected"
            )
        already_preserved[occurrence["source_key"]] = known["id"]

    assignments = [
        (source_id_for(len(existing) + offset), occurrence)
        for offset, occurrence in enumerate(new_occurrences, start=1)
    ]
    ids_by_key = {item["source_key"]: item["id"] for item in existing}
    ids_by_key.update({occurrence["source_key"]: source_id for source_id, occurrence in assignments})
    observed = {
        (observation["container_key"], observation["sha256"])
        for observation in (previous or {}).get("container_observations", [])
    }
    new_observations = [
        {**container, "segment_ids": [ids_by_key[key] for key in container["segment_keys"]]}
        for container in batch["containers"]
        if (container["container_key"], container["sha256"]) not in observed
    ]
    return {
        "already_preserved": already_preserved,
        "assignments": assignments,
        "observations": new_observations,
    }


# ---------------------------------------------------------------------------
# Manifest identity extension


def _verify_items(items: Sequence[Mapping[str, Any]]) -> None:
    seen_keys = set()
    for ordinal, item in enumerate(items, start=1):
        expected_id = source_id_for(ordinal)
        if item.get("id") != expected_id:
            raise HARDENING.IntegrityError(
                f"source IDs must be contiguous archive assignments; expected {expected_id}"
            )
        family = item.get("source_family")
        if family not in {"eml", "mbox"}:
            raise HARDENING.IntegrityError(f"source family is unsupported: {expected_id}")
        if item.get("relative_path") != _relative_path(expected_id, family):
            raise HARDENING.IntegrityError(f"source path is not ID-derived: {expected_id}")
        key = item.get("source_key")
        if family == "eml":
            name = item.get("input_name")
            if (
                not isinstance(name, str)
                or INCOMING_NAME_PATTERN.fullmatch(name) is None
                or not name.endswith(".eml")
                or key != eml_source_key(name)
                or item.get("content_type") != "message/rfc822"
            ):
                raise HARDENING.IntegrityError(f"EML source key is malformed: {expected_id}")
        else:
            match = MBOX_KEY_PATTERN.fullmatch(key) if isinstance(key, str) else None
            container = item.get("container")
            span = item.get("span")
            if (
                match is None
                or container != {"format": "mboxrd", "key": container_key(match.group("name")),
                                 "name": match.group("name")}
                or not isinstance(span, dict)
                or span.get("offset") != int(match.group("offset"))
                or span.get("length") != item.get("byte_count")
                or item.get("content_type") != MBOX_CONTENT_TYPE
            ):
                raise HARDENING.IntegrityError(f"MBOX source key or span is malformed: {expected_id}")
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


def _verify_observations(
    archive_root: Path, items: Sequence[Mapping[str, Any]], observations: Sequence[Mapping[str, Any]]
) -> Dict[str, str]:
    """Reassemble every observed container from preserved segments and re-segment it."""

    by_id = {item["id"]: item for item in items}
    seen = set()
    observation_batch: Dict[str, str] = {}
    for ordinal, observation in enumerate(observations, start=1):
        observation_id = _observation_id(ordinal)
        if observation.get("observation_id") != observation_id:
            raise HARDENING.IntegrityError("container observation IDs must be contiguous")
        name = observation.get("name")
        if (
            not isinstance(name, str)
            or INCOMING_NAME_PATTERN.fullmatch(name) is None
            or not name.endswith(".mbox")
            or observation.get("container_key") != container_key(name)
            or observation.get("format") != "mboxrd"
        ):
            raise HARDENING.IntegrityError(f"container observation is malformed: {observation_id}")
        identity = (observation["container_key"], observation.get("sha256"))
        if identity in seen:
            raise HARDENING.IntegrityError(f"container observation is duplicated: {observation_id}")
        seen.add(identity)
        segment_ids = observation.get("segment_ids")
        if not isinstance(segment_ids, list) or not segment_ids:
            raise HARDENING.IntegrityError(f"container observation has no segments: {observation_id}")
        pieces = []
        for segment_id in segment_ids:
            item = by_id.get(segment_id)
            if item is None or item.get("container", {}).get("key") != observation["container_key"]:
                raise HARDENING.IntegrityError(
                    f"container observation refers to a foreign segment: {observation_id}"
                )
            pieces.append(HARDENING._contained(archive_root, item["relative_path"]).read_bytes())
        data = b"".join(pieces)
        if len(data) != observation.get("byte_count") or _sha256(data) != observation.get("sha256"):
            raise HARDENING.IntegrityError(
                f"preserved segments do not reassemble the observed container: {observation_id}"
            )
        expected_spans = [segment.as_span() for segment in MBOXRD.segment_container(data)]
        if [by_id[segment_id]["span"] for segment_id in segment_ids] != expected_spans:
            raise HARDENING.IntegrityError(
                f"recorded boundaries disagree with the container bytes: {observation_id}"
            )
        observation_batch[observation_id] = str(observation.get("batch_id"))
    return observation_batch


def _verify_identity_extension(archive_root: Path, manifest: Mapping[str, Any]) -> None:
    if manifest.get("identity_convention") != IDENTITY_CONVENTION:
        raise HARDENING.IntegrityError("unsupported source identity convention")
    if manifest["source_package"].get("id") != ARCHIVE_PACKAGE_ID:
        raise HARDENING.IntegrityError("source package identity is unexpected")
    items = manifest["source_items"]
    batches = manifest.get("ingest_batches")
    observations = manifest.get("container_observations")
    if not isinstance(batches, list) or not batches or not isinstance(observations, list):
        raise HARDENING.IntegrityError("ingest batch or container ledger is missing")
    _verify_items(items)
    observation_batch = _verify_observations(archive_root, items, observations)

    position = 0
    observation_position = 0
    for ordinal, batch in enumerate(batches, start=1):
        batch_id = _batch_id(ordinal)
        if not isinstance(batch, dict) or batch.get("batch_id") != batch_id:
            raise HARDENING.IntegrityError("ingest batch IDs must be contiguous")
        recorded_at = batch.get("recorded_at")
        if not isinstance(recorded_at, str) or TIMESTAMP_PATTERN.fullmatch(recorded_at) is None:
            raise HARDENING.IntegrityError(f"ingest batch time is malformed: {batch_id}")
        members = batch.get("source_ids")
        batch_observations = batch.get("container_observations")
        if not isinstance(members, list) or not isinstance(batch_observations, list):
            raise HARDENING.IntegrityError(f"ingest batch is malformed: {batch_id}")
        if not members and not batch_observations:
            raise HARDENING.IntegrityError(f"ingest batch records nothing: {batch_id}")
        if members != [item["id"] for item in items[position : position + len(members)]]:
            raise HARDENING.IntegrityError(f"ingest batch does not own a contiguous ID range: {batch_id}")
        expected_observations = [
            _observation_id(n)
            for n in range(observation_position + 1, observation_position + len(batch_observations) + 1)
        ]
        if batch_observations != expected_observations or any(
            observation_batch.get(observation_id) != batch_id for observation_id in batch_observations
        ):
            raise HARDENING.IntegrityError(f"ingest batch container ledger is wrong: {batch_id}")
        for item in items[position : position + len(members)]:
            if item.get("ingest_batch") != batch_id:
                raise HARDENING.IntegrityError(f"source batch link is wrong: {item['id']}")
            if item["provenance"].get("recorded_at") != recorded_at:
                raise HARDENING.IntegrityError(f"source batch time is wrong: {item['id']}")
            if item["source_family"] == "mbox" and not any(
                item["id"] in observations[int(observation_id.split("-")[1]) - 1]["segment_ids"]
                for observation_id in batch_observations
            ):
                raise HARDENING.IntegrityError(
                    f"MBOX segment is not covered by its batch's container observation: {item['id']}"
                )
        position += len(members)
        observation_position += len(batch_observations)
    if position != len(items) or observation_position != len(observations):
        raise HARDENING.IntegrityError("ingest batches do not cover every source item and observation")


def verify_extends(previous: Mapping[str, Any], current: Mapping[str, Any]) -> None:
    """Require the current manifest to append exactly one batch to the previous one."""

    for field in ("source_items", "ingest_batches", "container_observations"):
        old = previous[field]
        if current[field][: len(old)] != old:
            raise HARDENING.IntegrityError(f"existing {field} changed between generations")
    if len(current["ingest_batches"]) != len(previous["ingest_batches"]) + 1:
        raise HARDENING.IntegrityError("a generation must append exactly one ingest batch")


def verify_generation(generation_root: Path) -> Dict[str, Any]:
    """Verify one published or staged generation and return its source manifest."""

    if generation_root.is_symlink() or not generation_root.is_dir():
        raise HARDENING.IntegrityError(f"generation must be a non-symlink directory: {generation_root}")
    if {candidate.name for candidate in generation_root.iterdir()} != {"archive", "derived"}:
        raise HARDENING.IntegrityError("generation must contain exactly archive and derived directories")
    archive = generation_root / "archive"
    derived = generation_root / "derived"
    manifest = HARDENING.verify_archive(archive)
    _verify_identity_extension(archive, manifest)
    derived_manifest = HARDENING.verify_derived(archive, derived)
    if derived_manifest.get("recorded_at") != manifest["ingest_batches"][-1]["recorded_at"]:
        raise HARDENING.IntegrityError("derived state is not bound to the latest ingest batch")
    records = HARDENING._load_json(derived / "messages.json")["messages"]
    families = {item["id"]: item["source_family"] for item in manifest["source_items"]}
    if [record.get("source_id") for record in records] != list(families):
        raise HARDENING.IntegrityError("derived records are not in source-ID order")
    for record in records:
        is_mbox = families[record["source_id"]] == "mbox"
        rule = record.get("mbox", {}).get("rule") if isinstance(record.get("mbox"), dict) else None
        if is_mbox != (rule is not None) or (is_mbox and rule != MBOXRD.MBOX_RULE):
            raise HARDENING.IntegrityError(
                f"derived MBOX record has a stale or missing rule: {record['source_id']}"
            )
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


def _state_layout(state_root: Path) -> Tuple[List[str], List[str]]:
    """Return published generation names and unpublished leftovers from interruption."""

    if state_root.is_symlink() or not state_root.is_dir():
        raise HARDENING.IntegrityError(f"state root must be a non-symlink directory: {state_root}")
    if {candidate.name for candidate in state_root.iterdir()} != {CURRENT_NAME, GENERATIONS_NAME}:
        raise HARDENING.IntegrityError("state root must contain exactly CURRENT and generations")
    generations_root = state_root / GENERATIONS_NAME
    if generations_root.is_symlink() or not generations_root.is_dir():
        raise HARDENING.IntegrityError("generations must be a non-symlink directory")
    current = _read_current_name(state_root)
    current_ordinal = int(current.split("-")[1])
    published: List[str] = []
    leftovers: List[str] = []
    for candidate in sorted(generations_root.iterdir(), key=lambda path: path.name):
        name = candidate.name
        if candidate.is_symlink() or not candidate.is_dir():
            raise HARDENING.IntegrityError(f"generations contains a non-directory: {name}")
        match = GENERATION_PATTERN.fullmatch(name)
        if match and int(match.group("ordinal")) <= current_ordinal:
            published.append(name)
        elif match or name.startswith(STAGING_PREFIX):
            leftovers.append(name)
        else:
            raise HARDENING.IntegrityError(f"generations contains an unexpected entry: {name}")
    if published != [_generation_name(n) for n in range(1, current_ordinal + 1)]:
        raise HARDENING.IntegrityError("published generations must be contiguous up to CURRENT")
    return published, leftovers


def current_generation(state_root: Path) -> Tuple[str, Path, Dict[str, Any]]:
    """Resolve and verify the published generation named by CURRENT."""

    published, _ = _state_layout(state_root)
    root = state_root / GENERATIONS_NAME / published[-1]
    return published[-1], root, verify_generation(root)


def verify_state(state_root: Path) -> Dict[str, Any]:
    """Verify every retained generation and the append-only chain between them."""

    published, leftovers = _state_layout(state_root)
    previous: Optional[Dict[str, Any]] = None
    generations = []
    for name in published:
        root = state_root / GENERATIONS_NAME / name
        manifest = verify_generation(root)
        if previous is None:
            if len(manifest["ingest_batches"]) != 1:
                raise HARDENING.IntegrityError("the first generation must hold one batch")
        else:
            verify_extends(previous, manifest)
        previous = manifest
        generations.append({"generation": name, **_generation_summary(root, manifest)})
    return {
        "current": published[-1],
        "generations": generations,
        "unpublished_leftovers": leftovers,
        "verified": True,
    }


def recover(state_root: Path) -> Dict[str, Any]:
    """Remove unpublished leftovers of an interrupted ingest after verifying CURRENT."""

    current_generation(state_root)
    _, leftovers = _state_layout(state_root)
    for name in leftovers:
        shutil.rmtree(state_root / GENERATIONS_NAME / name)
    return {"current": _read_current_name(state_root), "removed": leftovers}


def _write_current(state_root: Path, generation_name: str) -> None:
    HARDENING._atomic_write(
        state_root / CURRENT_NAME, f"{generation_name}\n".encode("ascii"), mode=0o600
    )


# ---------------------------------------------------------------------------
# Derivation


def _derive_provenance(item: Mapping[str, Any], recorded_at: str) -> Dict[str, Any]:
    return {
        "event": "derive",
        "event_id": f"prov-derive-{item['id'].lower()}",
        "input_event_id": item["provenance"]["event_id"],
        "recorded_at": recorded_at,
        "rule": HARDENING.PROCESSING_RULE,
        "tool": {"name": HARDENING.TOOL_NAME, "version": HARDENING.TOOL_VERSION},
    }


def _parse_occurrence(item: Mapping[str, Any], raw: bytes, recorded_at: str):
    """Derive one occurrence at the logical time of its own ingest batch."""

    batch_time = item["provenance"]["recorded_at"]
    if item["source_family"] == "eml":
        return ISOLATION.isolated_parser(item, raw, batch_time)

    span = item["span"]
    mbox_record: Dict[str, Any] = {
        "container_key": item["container"]["key"],
        "defects": MBOXRD.segment_defects(raw, span["kind"], span["starts_after_blank_line"]),
        "length": span["length"],
        "offset": span["offset"],
        "rule": MBOXRD.MBOX_RULE,
    }
    if mbox_record["defects"]:
        record = {
            "failure": "mbox segment defect: " + ",".join(mbox_record["defects"]),
            "isolation": {"mode": "not-parsed"},
            "mbox": mbox_record,
            "provenance": _derive_provenance(item, batch_time),
            "source_id": item["id"],
            "source_sha256": item["sha256"],
            "status": "quarantined",
            "warnings": [],
        }
        return record, [], {}

    message = MBOXRD.unescape_record(raw)
    mbox_record["message_byte_count"] = len(message)
    mbox_record["message_sha256"] = _sha256(message)
    parse_item = {**item, "byte_count": len(message), "sha256": mbox_record["message_sha256"]}
    record, occurrences, artifacts = ISOLATION.isolated_parser(parse_item, message, batch_time)
    # Citations and duplicate relations bind to the preserved segment bytes.
    record["source_sha256"] = item["sha256"]
    record["mbox"] = mbox_record
    for occurrence in occurrences:
        occurrence["source_sha256"] = item["sha256"]
    return record, occurrences, artifacts


def rebuild_derived(archive: Path, derived: Path) -> Dict[str, Any]:
    """Deterministic full derivation from the archive, in stable source-ID order."""

    manifest = HARDENING.verify_archive(archive)
    _verify_identity_extension(archive, manifest)
    return HARDENING.build_derived(
        archive,
        derived,
        manifest["ingest_batches"][-1]["recorded_at"],
        parse_source=_parse_occurrence,
    )


# ---------------------------------------------------------------------------
# Staging and publication


def _new_item(
    source_id: str, occurrence: Mapping[str, Any], batch_id: str, recorded_at: str
) -> Dict[str, Any]:
    family = occurrence["family"]
    item: Dict[str, Any] = {
        "byte_count": occurrence["byte_count"],
        "content_type": "message/rfc822" if family == "eml" else MBOX_CONTENT_TYPE,
        "id": source_id,
        "ingest_batch": batch_id,
        "provenance": {
            "event": "preserve",
            "event_id": f"prov-preserve-{source_id.lower()}",
            "recorded_at": recorded_at,
            "source_kind": SOURCE_KIND,
            "tool": {"name": PROTOTYPE_NAME, "version": PROTOTYPE_VERSION},
        },
        "relative_path": _relative_path(source_id, family),
        "sha256": occurrence["sha256"],
        "source_family": family,
        "source_key": occurrence["source_key"],
    }
    if family == "eml":
        item["input_name"] = occurrence["input_name"]
    else:
        item["container"] = dict(occurrence["container"])
        item["span"] = dict(occurrence["span"])
    return item


def _build_generation(
    staged: Path,
    previous_root: Optional[Path],
    previous: Optional[Mapping[str, Any]],
    plan: Mapping[str, Any],
    recorded_at: str,
) -> Dict[str, Any]:
    archive = staged / "archive"
    archive.mkdir(mode=0o700)
    items: List[Dict[str, Any]] = []
    batches: List[Dict[str, Any]] = []
    observations: List[Dict[str, Any]] = []
    if previous is not None and previous_root is not None:
        for item in previous["source_items"]:
            raw = HARDENING._contained(previous_root / "archive", item["relative_path"]).read_bytes()
            if _sha256(raw) != item["sha256"]:
                raise HARDENING.IntegrityError(f"existing source changed: {item['id']}")
            HARDENING._atomic_write(archive / item["relative_path"], raw, mode=0o400)
            items.append(dict(item))
        batches = [dict(batch) for batch in previous["ingest_batches"]]
        observations = [dict(observation) for observation in previous["container_observations"]]

    batch_id = _batch_id(len(batches) + 1)
    for source_id, occurrence in plan["assignments"]:
        item = _new_item(source_id, occurrence, batch_id, recorded_at)
        HARDENING._atomic_write(archive / item["relative_path"], occurrence["data"], mode=0o400)
        if (archive / item["relative_path"]).read_bytes() != occurrence["data"]:
            raise HARDENING.IntegrityError(f"preserved bytes differ: {source_id}")
        items.append(item)
    new_observation_ids = []
    for observation in plan["observations"]:
        observation_id = _observation_id(len(observations) + 1)
        new_observation_ids.append(observation_id)
        observations.append(
            {
                "batch_id": batch_id,
                "byte_count": observation["byte_count"],
                "container_key": observation["container_key"],
                "format": "mboxrd",
                "name": observation["name"],
                "observation_id": observation_id,
                "segment_ids": list(observation["segment_ids"]),
                "sha256": observation["sha256"],
            }
        )
    batches.append(
        {
            "batch_id": batch_id,
            "container_observations": new_observation_ids,
            "recorded_at": recorded_at,
            "source_ids": [source_id for source_id, _ in plan["assignments"]],
        }
    )
    manifest: Dict[str, Any] = {
        "container_observations": observations,
        "hash_algorithm": "sha256",
        "identity_convention": IDENTITY_CONVENTION,
        "ingest_batches": batches,
        "manifest_version": 1,
        "source_items": items,
        "source_package": {
            "id": ARCHIVE_PACKAGE_ID,
            "members": [item["id"] for item in items],
            "source_family": "synthetic-eml-and-mboxrd",
        },
    }
    HARDENING._write_json(archive / "manifest.json", manifest, mode=0o400)
    rebuild_derived(archive, staged / "derived")
    staged_manifest = verify_generation(staged)
    if previous is not None:
        verify_extends(previous, staged_manifest)
    return staged_manifest


def _generation_summary(generation_root: Path, manifest: Mapping[str, Any]) -> Dict[str, Any]:
    records = HARDENING._load_json(generation_root / "derived" / "messages.json")["messages"]
    return {
        "container_observation_count": len(manifest["container_observations"]),
        "derived_tree_sha256": HARDENING.tree_digest(generation_root / "derived"),
        "family_counts": dict(sorted(Counter(i["source_family"] for i in manifest["source_items"]).items())),
        "source_count": len(manifest["source_items"]),
        "source_manifest_sha256": HARDENING.sha256_path(generation_root / "archive" / "manifest.json"),
        "status_counts": dict(sorted(Counter(record["status"] for record in records).items())),
    }


def _occurrence_report(
    generation_root: Path, manifest: Mapping[str, Any], new_ids: Sequence[str]
) -> Dict[str, Any]:
    records = {
        record["source_id"]: record
        for record in HARDENING._load_json(generation_root / "derived" / "messages.json")["messages"]
    }
    by_hash: Dict[str, List[str]] = {}
    for item in manifest["source_items"]:
        by_hash.setdefault(item["sha256"], []).append(item["id"])
    by_id = {item["id"]: item for item in manifest["source_items"]}
    return {
        "exact_byte_duplicate_of": {
            source_id: [other for other in by_hash[by_id[source_id]["sha256"]] if other != source_id]
            for source_id in new_ids
            if len(by_hash[by_id[source_id]["sha256"]]) > 1
        },
        "quarantined": {
            source_id: records[source_id]["failure"]
            for source_id in new_ids
            if records[source_id]["status"] == "quarantined"
        },
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
        _, leftovers = _state_layout(state_root)
        if leftovers:
            raise HARDENING.IntegrityError(
                f"unpublished leftovers from an interrupted ingest are present: {leftovers}; "
                "run recover first"
            )
        previous_name, previous_root, previous = current_generation(state_root)

    plan = plan_batch(previous, batch)
    result: Dict[str, Any] = {
        "already_preserved": plan["already_preserved"],
        "prototype": {"name": PROTOTYPE_NAME, "version": PROTOTYPE_VERSION},
    }
    if not plan["assignments"] and not plan["observations"]:
        # Only reachable with an existing state: a new state treats every member as new.
        result.update(
            {
                "generation": previous_name,
                "new_container_observations": [],
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
        stage_root = Path(tempfile.mkdtemp(prefix=STAGING_PREFIX, dir=str(state_root / GENERATIONS_NAME)))
        staged = stage_root
    stage_root.chmod(0o700)

    renamed: Optional[Path] = None
    try:
        manifest = _build_generation(staged, previous_root, previous, plan, recorded_at)
        if previous_root is not None:
            HARDENING.verify_archive(previous_root / "archive")
        new_ids = [source_id for source_id, _ in plan["assignments"]]
        summary = _generation_summary(staged, manifest)
        report = _occurrence_report(staged, manifest, new_ids)
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
            renamed = target
            _write_current(state_root, generation_name)
            renamed = None
    except BaseException:
        if renamed is not None and renamed.exists():
            shutil.rmtree(renamed)
        if stage_root.exists():
            shutil.rmtree(stage_root)
        raise

    result.update(
        {
            "batch_id": manifest["ingest_batches"][-1]["batch_id"],
            "generation": generation_name,
            "new_container_observations": manifest["ingest_batches"][-1]["container_observations"],
            "new_occurrences": {
                source_id: occurrence["source_key"] for source_id, occurrence in plan["assignments"]
            },
            "published": True,
            **report,
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
            raise HARDENING.IntegrityError("rebuilt derived state differs from the current verified state")
        result = {
            "derived_file_hashes": rebuilt_hashes,
            "derived_tree_sha256": HARDENING.tree_digest(staged),
            "generation": generation_name,
            "rebuild_equal": True,
            "source_manifest_sha256": HARDENING.sha256_path(generation_root / "archive" / "manifest.json"),
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
    return HARDENING.deterministic_find(generation_root / "archive", generation_root / "derived", query)


def _display_mbox(
    archive: Path, derived: Path, item: Mapping[str, Any], citation: str, locator: str
) -> Dict[str, Any]:
    """Mirror the engine's citation display over the unescaped message of one segment."""

    raw = HARDENING._contained(archive, item["relative_path"]).read_bytes()
    if _sha256(raw) != item["sha256"]:
        raise HARDENING.IntegrityError("preserved segment changed")
    span = item["span"]
    if MBOXRD.segment_defects(raw, span["kind"], span["starts_after_blank_line"]):
        raise HARDENING.IntegrityError("quarantined MBOX segment has no citable text")
    message = BytesParser(policy=policy.default).parsebytes(MBOXRD.unescape_record(raw))
    occurrence = HARDENING._indexed_occurrence(derived, item["id"], item["sha256"], locator)
    if locator.startswith("header:"):
        components = locator.split(":")
        if len(components) != 3 or not components[2].isdigit():
            raise HARDENING.ScopeError("header citation locator is malformed")
        _, header_name, ordinal_text = components
        values = HARDENING._header_values(message, header_name)
        ordinal = int(ordinal_text)
        if ordinal < 1 or ordinal > len(values):
            raise HARDENING.ScopeError("header citation ordinal is outside the source")
        source_text = HARDENING._derived_header_value(message, header_name, values[ordinal - 1])
    elif locator.startswith("mime:"):
        part = HARDENING._part_by_locator(message, locator[len("mime:"):])
        if part.get_content_maintype() != "text":
            raise HARDENING.IntegrityError("indexed citation refers to a non-text MIME part")
        source_text = HARDENING._decode_text(part, HARDENING._decode_payload(part), [])
    else:
        raise HARDENING.ScopeError("citation locator type is unsupported")
    if occurrence["text"] != source_text:
        raise HARDENING.IntegrityError("indexed text differs from the unescaped MBOX source")
    return {
        "citation": citation,
        "display": html.escape(source_text, quote=True),
        "display_mode": "escaped-inert-text-no-fetch",
        "provenance": item["provenance"],
        "source_id": item["id"],
        "source_sha256": item["sha256"],
        "source_span": {
            "container_key": item["container"]["key"],
            "length": span["length"],
            "offset": span["offset"],
            "transform": "mboxrd-unescape",
        },
    }


def show(state_root: Path, citation: str) -> Dict[str, Any]:
    _, generation_root, manifest = current_generation(state_root)
    archive = generation_root / "archive"
    derived = generation_root / "derived"
    match = HARDENING.CITATION_PATTERN.fullmatch(citation)
    if match is None:
        raise HARDENING.ScopeError("citation format is unsupported")
    items = {item["id"]: item for item in manifest["source_items"]}
    item = items.get(match.group("source_id"))
    if item is None:
        raise HARDENING.IntegrityError("citation source is not in the archive")
    if item["source_family"] == "eml":
        return HARDENING.display_source(archive, derived, citation)
    if match.group("digest") != item["sha256"]:
        raise HARDENING.IntegrityError("citation digest does not match the source")
    return _display_mbox(archive, derived, item, citation, match.group("locator"))


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
    for name in ("verify", "recover"):
        subparsers.add_parser(name).add_argument("--state", type=Path, required=True)
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
        elif arguments.command == "recover":
            result = recover(arguments.state)
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
