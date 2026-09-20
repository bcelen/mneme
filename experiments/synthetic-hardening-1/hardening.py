#!/usr/bin/env python3
"""Local, synthetic-only Mneme preservation and retrieval hardening experiment."""

from __future__ import annotations

import argparse
import base64
import binascii
import codecs
import hashlib
import html
import json
import os
import quopri
import re
import shutil
import stat
import sys
import tempfile
import unicodedata
from collections import Counter, defaultdict
from email import policy
from email.header import decode_header, make_header
from email.message import Message
from email.parser import BytesParser
from email.utils import parsedate_to_datetime
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Dict, Iterator, List, Mapping, MutableMapping, Sequence, Tuple

import fixtures


TOOL_NAME = "mneme-synthetic-hardening"
TOOL_VERSION = "1"
PROCESSING_RULE = "synthetic-eml-hardening-v2"
MAX_SOURCE_BYTES = 128 * 1024
MAX_MIME_DEPTH = 4
PINNED_ATTACHMENT_MIME_TYPES = {
    ".bin": "application/octet-stream",
    ".csv": "text/csv",
    ".eml": "message/rfc822",
    ".gif": "image/gif",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".json": "application/json",
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".stl": "model/stl",
    ".txt": "text/plain",
    ".zip": "application/zip",
}
TOKEN_PATTERN = re.compile(r"[a-z0-9]+(?:[-'][a-z0-9]+)*")
CITATION_PATTERN = re.compile(
    r"^mneme-source:(?P<source_id>EML-[0-9]{3})@sha256:"
    r"(?P<digest>[0-9a-f]{64})#(?P<locator>[a-z0-9:.-]+)$"
)
FATAL_DEFECTS = {
    "CloseBoundaryNotFoundDefect",
    "StartBoundaryNotFoundDefect",
    "MultipartInvariantViolationDefect",
}


class ExperimentError(RuntimeError):
    """Base stop condition."""


class IntegrityError(ExperimentError):
    """Integrity or manifest verification failed."""


class ScopeError(ExperimentError):
    """Operation left the approved experiment boundary."""


class ControlledParserFailure(ExperimentError):
    """A synthetic fixture triggered a controlled parser failure."""


ParseSource = Callable[
    [Mapping[str, Any], bytes, str],
    Tuple[Dict[str, Any], List[Dict[str, Any]], Dict[str, bytes]],
]


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(64 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _canonical_bytes(value: Mapping[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode(
        "utf-8"
    )


def _atomic_write(path: Path, data: bytes, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", dir=str(path.parent)
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary_path, mode)
        os.replace(temporary_path, path)
    except BaseException:
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass
        raise


def _write_json(path: Path, value: Mapping[str, Any], mode: int = 0o600) -> None:
    _atomic_write(path, _canonical_bytes(value), mode=mode)


def _load_json(path: Path) -> Dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise IntegrityError(f"cannot read valid JSON from {path}: {error}") from error
    if not isinstance(value, dict):
        raise IntegrityError(f"JSON root must be an object: {path}")
    return value


def _require_regular(path: Path, label: str) -> os.stat_result:
    try:
        status = path.lstat()
    except FileNotFoundError as error:
        raise IntegrityError(f"missing {label}: {path}") from error
    if stat.S_ISLNK(status.st_mode) or not stat.S_ISREG(status.st_mode):
        raise IntegrityError(f"{label} must be a regular non-symlink file: {path}")
    return status


def _contained(root: Path, relative_path: str) -> Path:
    member = PurePosixPath(relative_path)
    if member.is_absolute() or ".." in member.parts:
        raise IntegrityError(f"unsafe relative path: {relative_path}")
    candidate = root.joinpath(*member.parts)
    try:
        candidate.resolve().relative_to(root.resolve())
    except (OSError, ValueError) as error:
        raise IntegrityError(f"path escapes root: {relative_path}") from error
    return candidate


def tree_hashes(root: Path, exclude: Sequence[str] = ()) -> Dict[str, Dict[str, Any]]:
    excluded = set(exclude)
    result: Dict[str, Dict[str, Any]] = {}
    for candidate in sorted(root.rglob("*")):
        if candidate.is_symlink():
            raise IntegrityError(f"tree contains symlink: {candidate}")
        if candidate.is_file():
            relative = candidate.relative_to(root).as_posix()
            if relative not in excluded:
                result[relative] = {
                    "byte_count": candidate.stat().st_size,
                    "sha256": sha256_path(candidate),
                }
    return result


def tree_digest(root: Path) -> str:
    return hashlib.sha256(_canonical_bytes(tree_hashes(root))).hexdigest()


def preserve_package(
    input_paths: Mapping[str, Path], archive_root: Path, recorded_at: str
) -> Dict[str, Any]:
    if archive_root.exists():
        raise ScopeError(f"archive root already exists: {archive_root}")
    if set(input_paths) != {fixture.fixture_id for fixture in fixtures.FIXTURES}:
        raise ScopeError("input package does not match the reviewed fixture inventory")
    archive_root.mkdir(parents=True, mode=0o700)

    items: List[Dict[str, Any]] = []
    for fixture in fixtures.FIXTURES:
        input_path = input_paths[fixture.fixture_id]
        status = _require_regular(input_path, "synthetic fixture")
        if status.st_size > MAX_SOURCE_BYTES:
            raise ScopeError(f"fixture exceeds {MAX_SOURCE_BYTES} bytes: {fixture.fixture_id}")
        source_bytes = input_path.read_bytes()
        digest = hashlib.sha256(source_bytes).hexdigest()
        if digest != fixtures.EXPECTED_HASHES[fixture.fixture_id]:
            raise IntegrityError(f"fixture hash disagrees with reviewed catalog: {fixture.fixture_id}")
        relative_path = f"source-items/{fixture.fixture_id}.eml"
        preserved_path = archive_root / relative_path
        _atomic_write(preserved_path, source_bytes, mode=0o400)
        if preserved_path.read_bytes() != source_bytes:
            raise IntegrityError(f"preserved bytes differ: {fixture.fixture_id}")
        items.append(
            {
                "byte_count": len(source_bytes),
                "content_type": "message/rfc822",
                "id": fixture.fixture_id,
                "input_name": fixture.filename,
                "relative_path": relative_path,
                "sha256": digest,
                "provenance": {
                    "event": "preserve",
                    "event_id": f"prov-preserve-{fixture.fixture_id.lower()}",
                    "recorded_at": recorded_at,
                    "source_kind": "wholly-fictional-synthetic-fixture",
                    "tool": {"name": TOOL_NAME, "version": TOOL_VERSION},
                },
            }
        )
    manifest: Dict[str, Any] = {
        "hash_algorithm": "sha256",
        "manifest_version": 1,
        "source_package": {
            "id": "pkg-synthetic-hardening-001",
            "members": [item["id"] for item in items],
            "source_family": "synthetic-eml",
        },
        "source_items": items,
    }
    _write_json(archive_root / "manifest.json", manifest, mode=0o400)
    verify_archive(archive_root)
    return manifest


def verify_archive(archive_root: Path) -> Dict[str, Any]:
    if archive_root.is_symlink() or not archive_root.is_dir():
        raise IntegrityError(f"archive root is not a non-symlink directory: {archive_root}")
    manifest_path = archive_root / "manifest.json"
    _require_regular(manifest_path, "source manifest")
    manifest = _load_json(manifest_path)
    if manifest.get("manifest_version") != 1 or manifest.get("hash_algorithm") != "sha256":
        raise IntegrityError("unsupported source manifest convention")
    items = manifest.get("source_items")
    package = manifest.get("source_package")
    if not isinstance(items, list) or not isinstance(package, dict):
        raise IntegrityError("source manifest structure is incomplete")
    ids = [item.get("id") for item in items if isinstance(item, dict)]
    if len(ids) != len(items) or package.get("members") != ids:
        raise IntegrityError("source-package membership is inconsistent")
    if ids != sorted(ids) or len(ids) != len(set(ids)):
        raise IntegrityError("source IDs must be sorted and unique")

    expected_members = set()
    for item in items:
        required = {"id", "relative_path", "byte_count", "sha256", "provenance"}
        if not required.issubset(item):
            raise IntegrityError(f"incomplete source item: {item.get('id')}")
        relative_path = item["relative_path"]
        preserved_path = _contained(archive_root, relative_path)
        status = _require_regular(preserved_path, "preserved source")
        expected_members.add(relative_path)
        if status.st_size != item["byte_count"]:
            raise IntegrityError(f"source size mismatch: {item['id']}")
        if sha256_path(preserved_path) != item["sha256"]:
            raise IntegrityError(f"source SHA-256 mismatch: {item['id']}")

    actual_members = set()
    for candidate in archive_root.rglob("*"):
        if candidate.is_symlink():
            raise IntegrityError(f"archive contains symlink: {candidate}")
        if candidate.is_file() and candidate != manifest_path:
            actual_members.add(candidate.relative_to(archive_root).as_posix())
    if actual_members != expected_members:
        raise IntegrityError("source archive has missing or extra members")
    return manifest


def _normalize_tokens(text: str) -> List[str]:
    return TOKEN_PATTERN.findall(unicodedata.normalize("NFKC", text).casefold())


def _mime_depth(message: Message) -> int:
    maximum = 0
    pending = [(message, 1)]
    while pending:
        part, depth = pending.pop()
        maximum = max(maximum, depth)
        if maximum > MAX_MIME_DEPTH:
            return maximum
        if part.is_multipart():
            payload = part.get_payload()
            if isinstance(payload, list):
                pending.extend((child, depth + 1) for child in payload)
    return maximum


def _leaf_parts(message: Message, prefix: Tuple[int, ...] = ()) -> Iterator[Tuple[str, Message]]:
    if message.is_multipart():
        payload = message.get_payload()
        if not isinstance(payload, list):
            raise ControlledParserFailure("multipart payload is not a list")
        for index, part in enumerate(payload, start=1):
            yield from _leaf_parts(part, prefix + (index,))
    else:
        locator = ".".join(str(value) for value in (prefix or (1,)))
        yield locator, message


def _defect_names(message: Message) -> List[str]:
    names = []
    for part in message.walk():
        names.extend(type(defect).__name__ for defect in part.defects)
    return sorted(set(names))


def _decode_payload(part: Message) -> bytes:
    transfer_encoding = (part.get("Content-Transfer-Encoding") or "7bit").strip().lower()
    raw_payload = part.get_payload(decode=False)
    if isinstance(raw_payload, list):
        raise ControlledParserFailure("leaf MIME part has list payload")
    if raw_payload is None:
        payload_text = ""
    elif isinstance(raw_payload, str):
        payload_text = raw_payload
    else:
        payload_text = bytes(raw_payload).decode("ascii", errors="surrogateescape")

    if transfer_encoding == "base64":
        compact = re.sub(r"\s+", "", payload_text)
        try:
            return base64.b64decode(compact.encode("ascii"), validate=True)
        except (UnicodeEncodeError, binascii.Error) as error:
            raise ControlledParserFailure("invalid base64 transfer encoding") from error
    if transfer_encoding == "quoted-printable":
        try:
            return quopri.decodestring(payload_text.encode("ascii"))
        except UnicodeEncodeError as error:
            raise ControlledParserFailure("non-ASCII quoted-printable source") from error
    if transfer_encoding not in {"7bit", "8bit", "binary"}:
        raise ControlledParserFailure(f"unsupported transfer encoding: {transfer_encoding}")
    decoded = part.get_payload(decode=True)
    if decoded is not None:
        return decoded
    return payload_text.encode("utf-8", errors="surrogateescape")


def _decode_text(part: Message, payload: bytes, warnings: List[str]) -> str:
    charset = part.get_content_charset() or "us-ascii"
    try:
        codecs.lookup(charset)
    except LookupError:
        warnings.append(f"unknown-charset:{charset.lower()}")
        return payload.decode("utf-8", errors="replace")
    try:
        return payload.decode(charset, errors="strict")
    except LookupError as error:
        raise ControlledParserFailure(
            f"charset is not a text codec: {charset.lower()}"
        ) from error
    except UnicodeDecodeError:
        warnings.append(f"decode-replacement:{charset.lower()}")
        return payload.decode(charset, errors="replace")


def _header_values(message: Message, name: str) -> List[str]:
    return [str(value) for key, value in message.raw_items() if key.lower() == name.lower()]


def _decode_header_value(value: str) -> str:
    value = value.encode("utf-8", errors="surrogateescape").decode("utf-8", errors="replace")
    try:
        return str(make_header(decode_header(value)))
    except (LookupError, UnicodeError, ValueError):
        return value


def _derived_header_value(message: Message, name: str, raw_value: str) -> str:
    try:
        structured = message.get(name)
        if structured is not None:
            return str(structured)
    except (TypeError, ValueError, UnicodeError, OverflowError):
        pass
    return _decode_header_value(raw_value)


def _safe_attachment_name(original: str | None, locator: str) -> str:
    if not original:
        return f"attachment-{locator.replace('.', '-')}.bin"
    normalized = original.replace("\\", "/")
    basename = PurePosixPath(normalized).name
    cleaned = re.sub(r"[^A-Za-z0-9._-]", "_", basename).lstrip(".")
    return cleaned or f"attachment-{locator.replace('.', '-')}.bin"


def _pinned_attachment_type(filename: str) -> str | None:
    return PINNED_ATTACHMENT_MIME_TYPES.get(PurePosixPath(filename).suffix.casefold())


def _citation(source_id: str, digest: str, locator: str) -> str:
    return f"mneme-source:{source_id}@sha256:{digest}#{locator}"


def _parse_source(
    item: Mapping[str, Any], raw: bytes, recorded_at: str
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], Dict[str, bytes]]:
    base_record: Dict[str, Any] = {
        "source_id": item["id"],
        "source_sha256": item["sha256"],
        "provenance": {
            "event": "derive",
            "event_id": f"prov-derive-{item['id'].lower()}",
            "input_event_id": item["provenance"]["event_id"],
            "recorded_at": recorded_at,
            "rule": PROCESSING_RULE,
            "tool": {"name": TOOL_NAME, "version": TOOL_VERSION},
        },
    }
    try:
        message = BytesParser(policy=policy.default).parsebytes(raw)
        failure_values = _header_values(message, "X-Mneme-Synthetic-Failure")
        if failure_values and failure_values[0].strip().lower() == "parser":
            raise ControlledParserFailure("synthetic parser fault injection")
        depth = _mime_depth(message)
        if depth > MAX_MIME_DEPTH:
            raise ControlledParserFailure(
                f"MIME depth {depth} exceeds limit {MAX_MIME_DEPTH}"
            )
        defects = _defect_names(message)
        fatal = [name for name in defects if name in FATAL_DEFECTS]
        if fatal:
            raise ControlledParserFailure("fatal parser defect: " + ",".join(fatal))

        warnings: List[str] = []
        fields: Dict[str, str | None] = {}
        header_names = {
            "from": "From",
            "to": "To",
            "date": "Date",
            "message_id": "Message-ID",
            "subject": "Subject",
        }
        for field_name, header_name in header_names.items():
            values = _header_values(message, header_name)
            fields[field_name] = (
                _derived_header_value(message, header_name, values[0]) if values else None
            )
            if not values:
                warnings.append(f"missing-header:{field_name.replace('_', '-')}")
            if len(values) > 1:
                warnings.append(f"duplicate-header:{field_name.replace('_', '-')}")
        raw_header_values = [value for _, value in message.raw_items()]
        if any("=?" in value and "?=" not in value for value in raw_header_values):
            warnings.append("malformed-encoded-word")
        if fields["date"]:
            try:
                parsedate_to_datetime(str(fields["date"]))
            except (TypeError, ValueError, OverflowError):
                warnings.append("invalid-date")

        occurrences: List[Dict[str, Any]] = []
        if fields["subject"]:
            occurrences.append(
                {
                    "field": "subject",
                    "locator": "header:subject:1",
                    "source_id": item["id"],
                    "source_sha256": item["sha256"],
                    "text": fields["subject"],
                }
            )

        pending_artifacts: Dict[str, bytes] = {}
        part_records: List[Dict[str, Any]] = []
        attachment_names: List[str] = []
        for locator, part in _leaf_parts(message):
            payload = _decode_payload(part)
            content_type = part.get_content_type().lower()
            disposition = part.get_content_disposition()
            original_filename = part.get_filename()
            is_attachment = disposition == "attachment" or original_filename is not None
            part_record: Dict[str, Any] = {
                "byte_count": len(payload),
                "content_type": content_type,
                "disposition": disposition,
                "locator": f"mime:{locator}",
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
            if is_attachment:
                safe_name = _safe_attachment_name(original_filename, locator)
                if original_filename and safe_name != original_filename:
                    warnings.append("unsafe-attachment-name")
                attachment_names.append(safe_name.casefold())
                guessed_type = _pinned_attachment_type(safe_name)
                if guessed_type and guessed_type != content_type:
                    warnings.append("attachment-content-type-mismatch")
                relative_path = f"attachments/{item['id']}/part-{locator.replace('.', '-')}.bin"
                pending_artifacts[relative_path] = payload
                part_record.update(
                    {
                        "artifact_path": relative_path,
                        "original_filename": original_filename,
                        "safe_display_name": safe_name,
                    }
                )
            elif content_type == "text/html":
                text = _decode_text(part, payload, warnings)
                escaped = html.escape(text, quote=True).encode("utf-8")
                relative_path = f"inert-html/{item['id']}/part-{locator.replace('.', '-')}.txt"
                pending_artifacts[relative_path] = escaped
                part_record.update(
                    {"artifact_path": relative_path, "display_mode": "escaped-inert-text"}
                )
                warnings.append("html-inert")
            elif content_type == "text/plain":
                text = _decode_text(part, payload, warnings)
                part_record["text"] = text
                occurrences.append(
                    {
                        "field": "body",
                        "locator": f"mime:{locator}",
                        "source_id": item["id"],
                        "source_sha256": item["sha256"],
                        "text": text,
                    }
                )
            part_records.append(part_record)

        if any(count > 1 for count in Counter(attachment_names).values()):
            warnings.append("duplicate-attachment-name")
        warnings = sorted(set(warnings))
        record = {
            **base_record,
            "fields": fields,
            "mime_depth": depth,
            "parser_defects": defects,
            "parts": part_records,
            "status": "indexed_with_warnings" if warnings else "indexed",
            "warnings": warnings,
        }
        return record, occurrences, pending_artifacts
    except (ControlledParserFailure, UnicodeError, ValueError, TypeError) as error:
        record = {
            **base_record,
            "failure": str(error),
            "status": "quarantined",
            "warnings": [],
        }
        return record, [], {}


def _duplicate_relations(records: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    by_hash: MutableMapping[str, List[str]] = defaultdict(list)
    by_message_id: MutableMapping[str, List[Tuple[str, str]]] = defaultdict(list)
    for record in records:
        by_hash[str(record["source_sha256"])].append(str(record["source_id"]))
        fields = record.get("fields")
        if record.get("status") != "quarantined" and isinstance(fields, dict):
            message_id = fields.get("message_id")
            if message_id:
                by_message_id[str(message_id).strip().casefold()].append(
                    (str(record["source_id"]), str(record["source_sha256"]))
                )
    exact = [
        {"sha256": digest, "source_ids": sorted(source_ids)}
        for digest, source_ids in sorted(by_hash.items())
        if len(source_ids) > 1
    ]
    message_id = []
    for value, rows in sorted(by_message_id.items()):
        if len(rows) > 1 and len({digest for _, digest in rows}) > 1:
            message_id.append(
                {
                    "message_id": value,
                    "source_ids": sorted(source_id for source_id, _ in rows),
                }
            )
    return {"exact_byte_duplicates": exact, "message_id_duplicates": message_id}


def build_derived(
    archive_root: Path,
    derived_root: Path,
    recorded_at: str,
    parse_source: ParseSource | None = None,
) -> Dict[str, Any]:
    manifest = verify_archive(archive_root)
    if derived_root.exists():
        raise ScopeError(f"derived root already exists: {derived_root}")
    source_parser = parse_source or _parse_source

    records: List[Dict[str, Any]] = []
    occurrences: MutableMapping[str, List[Dict[str, Any]]] = defaultdict(list)
    artifacts: Dict[str, bytes] = {}
    for item in manifest["source_items"]:
        preserved_path = _contained(archive_root, item["relative_path"])
        raw = preserved_path.read_bytes()
        before = hashlib.sha256(raw).hexdigest()
        record, source_occurrences, pending_artifacts = source_parser(
            item, raw, recorded_at
        )
        if sha256_path(preserved_path) != before:
            raise IntegrityError(f"source changed during parsing: {item['id']}")
        records.append(record)
        for occurrence in source_occurrences:
            for token in sorted(set(_normalize_tokens(str(occurrence["text"])))):
                occurrences[token].append(occurrence)
        for relative_path, payload in pending_artifacts.items():
            if relative_path in artifacts:
                raise IntegrityError(f"duplicate derived artifact path: {relative_path}")
            artifacts[relative_path] = payload

    for rows in occurrences.values():
        rows.sort(
            key=lambda row: (
                row["source_id"], row["locator"], row["field"], row["text"]
            )
        )
    index: Dict[str, Any] = {
        "generation": PROCESSING_RULE,
        "normalization": "Unicode NFKC, casefold, ASCII alphanumeric/hyphen/apostrophe tokens",
        "terms": {token: occurrences[token] for token in sorted(occurrences)},
    }
    messages = {"generation": PROCESSING_RULE, "messages": records}
    duplicates = {
        "generation": PROCESSING_RULE,
        **_duplicate_relations(records),
    }

    derived_root.mkdir(parents=True, mode=0o700)
    _write_json(derived_root / "messages.json", messages)
    _write_json(derived_root / "index.json", index)
    _write_json(derived_root / "duplicates.json", duplicates)
    for relative_path in sorted(artifacts):
        _atomic_write(derived_root / relative_path, artifacts[relative_path])

    member_hashes = tree_hashes(derived_root)
    derived_manifest: Dict[str, Any] = {
        "derived_manifest_version": 1,
        "generation": PROCESSING_RULE,
        "members": member_hashes,
        "recorded_at": recorded_at,
        "source_manifest_sha256": sha256_path(archive_root / "manifest.json"),
    }
    _write_json(derived_root / "derived-manifest.json", derived_manifest)
    verify_derived(archive_root, derived_root)
    return {
        "duplicates": duplicates,
        "index": index,
        "messages": messages,
        "derived_manifest": derived_manifest,
    }


def verify_derived(archive_root: Path, derived_root: Path) -> Dict[str, Any]:
    verify_archive(archive_root)
    if derived_root.is_symlink() or not derived_root.is_dir():
        raise IntegrityError(f"derived root is not a non-symlink directory: {derived_root}")
    manifest_path = derived_root / "derived-manifest.json"
    _require_regular(manifest_path, "derived manifest")
    manifest = _load_json(manifest_path)
    if manifest.get("derived_manifest_version") != 1:
        raise IntegrityError("unsupported derived manifest version")
    if manifest.get("generation") != PROCESSING_RULE:
        raise IntegrityError("derived generation is stale or unknown")
    if manifest.get("source_manifest_sha256") != sha256_path(archive_root / "manifest.json"):
        raise IntegrityError("derived state refers to another source manifest")
    members = manifest.get("members")
    if not isinstance(members, dict):
        raise IntegrityError("derived manifest member map is missing")
    actual = tree_hashes(derived_root, exclude=("derived-manifest.json",))
    if actual != members:
        raise IntegrityError("derived state has missing, changed, or extra members")
    return manifest


def deterministic_find(
    archive_root: Path, derived_root: Path, query: str
) -> Dict[str, Any]:
    verify_archive(archive_root)
    verify_derived(archive_root, derived_root)
    index = _load_json(derived_root / "index.json")
    terms: List[str] = []
    for token in _normalize_tokens(query):
        if token not in terms:
            terms.append(token)
    if not terms:
        raise ScopeError("Find query has no supported token")
    term_map = index.get("terms")
    if not isinstance(term_map, dict):
        raise IntegrityError("index term map is missing")
    if any(term not in term_map for term in terms):
        return {"normalized_terms": terms, "query": query, "results": []}

    matched_by_source: MutableMapping[str, Dict[Tuple[Any, ...], Dict[str, Any]]] = defaultdict(dict)
    source_hashes: Dict[str, str] = {}
    for term in terms:
        for occurrence in term_map[term]:
            source_id = occurrence["source_id"]
            source_hashes[source_id] = occurrence["source_sha256"]
            key = (occurrence["locator"], occurrence["field"], occurrence["text"])
            matched_by_source[source_id][key] = {
                "citation": _citation(
                    source_id, occurrence["source_sha256"], occurrence["locator"]
                ),
                "field": occurrence["field"],
                "text": occurrence["text"],
            }
    common_sources = set(matched_by_source)
    for term in terms:
        common_sources &= {row["source_id"] for row in term_map[term]}
    results = []
    for source_id in sorted(common_sources):
        citations = [
            matched_by_source[source_id][key]
            for key in sorted(matched_by_source[source_id])
        ]
        results.append(
            {
                "citations": citations,
                "source_id": source_id,
                "source_sha256": source_hashes[source_id],
            }
        )
    return {"normalized_terms": terms, "query": query, "results": results}


def _part_by_locator(message: Message, locator: str) -> Message:
    parts = {part_locator: part for part_locator, part in _leaf_parts(message)}
    try:
        return parts[locator]
    except KeyError as error:
        raise ScopeError(f"MIME locator does not exist: {locator}") from error


def _indexed_occurrence(
    derived_root: Path, source_id: str, source_sha256: str, locator: str
) -> Dict[str, Any]:
    index = _load_json(derived_root / "index.json")
    term_map = index.get("terms")
    if not isinstance(term_map, dict):
        raise IntegrityError("index term map is missing")
    matches: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for rows in term_map.values():
        if not isinstance(rows, list):
            raise IntegrityError("index occurrence list is malformed")
        for occurrence in rows:
            if (
                isinstance(occurrence, dict)
                and occurrence.get("source_id") == source_id
                and occurrence.get("source_sha256") == source_sha256
                and occurrence.get("locator") == locator
                and isinstance(occurrence.get("field"), str)
                and isinstance(occurrence.get("text"), str)
            ):
                key = (occurrence["field"], occurrence["text"])
                matches[key] = occurrence
    if len(matches) != 1:
        raise IntegrityError("citation is not bound to one verified index occurrence")
    return next(iter(matches.values()))


def display_source(
    archive_root: Path, derived_root: Path, citation: str
) -> Dict[str, Any]:
    manifest = verify_archive(archive_root)
    verify_derived(archive_root, derived_root)
    match = CITATION_PATTERN.fullmatch(citation)
    if match is None:
        raise ScopeError("citation format is unsupported")
    source_id = match.group("source_id")
    item_by_id = {item["id"]: item for item in manifest["source_items"]}
    if source_id not in item_by_id:
        raise IntegrityError("citation source is not in the archive")
    item = item_by_id[source_id]
    if match.group("digest") != item["sha256"]:
        raise IntegrityError("citation digest does not match the source")
    raw = _contained(archive_root, item["relative_path"]).read_bytes()
    message = BytesParser(policy=policy.default).parsebytes(raw)
    locator = match.group("locator")
    if locator.startswith("header:"):
        components = locator.split(":")
        if len(components) != 3 or not components[2].isdigit():
            raise ScopeError("header citation locator is malformed")
        _, header_name, ordinal_text = components
        occurrence = _indexed_occurrence(
            derived_root, source_id, item["sha256"], locator
        )
        values = _header_values(message, header_name)
        ordinal = int(ordinal_text)
        if ordinal < 1 or ordinal > len(values):
            raise ScopeError("header citation ordinal is outside the source")
        source_text = _derived_header_value(
            message, header_name, values[ordinal - 1]
        )
        if occurrence["text"] != source_text:
            raise IntegrityError("indexed header text differs from the source")
        displayed = html.escape(source_text, quote=True)
    elif locator.startswith("mime:"):
        occurrence = _indexed_occurrence(
            derived_root, source_id, item["sha256"], locator
        )
        part_locator = locator.removeprefix("mime:")
        part = _part_by_locator(message, part_locator)
        payload = _decode_payload(part)
        warnings: List[str] = []
        if part.get_content_maintype() == "text":
            source_text = _decode_text(part, payload, warnings)
            if occurrence["text"] != source_text:
                raise IntegrityError("indexed MIME text differs from the source")
            displayed = html.escape(source_text, quote=True)
        else:
            raise IntegrityError("indexed citation refers to a non-text MIME part")
    else:
        raise ScopeError("citation locator type is unsupported")
    return {
        "citation": citation,
        "display": displayed,
        "display_mode": "escaped-inert-text-no-fetch",
        "provenance": item["provenance"],
        "source_id": source_id,
        "source_sha256": item["sha256"],
    }


def export_bundle(
    archive_root: Path, derived_root: Path, export_root: Path, recorded_at: str
) -> Dict[str, Any]:
    verify_archive(archive_root)
    verify_derived(archive_root, derived_root)
    if export_root.exists():
        raise ScopeError(f"export root already exists: {export_root}")
    export_root.mkdir(parents=True, mode=0o700)
    shutil.copytree(archive_root, export_root / "archive")
    shutil.copytree(derived_root, export_root / "derived")
    _atomic_write(
        export_root / "README.txt",
        (
            "Mneme synthetic hardening export version 1\n"
            "Contents are original EML bytes, JSON manifests/provenance, and deterministic derived state.\n"
            "All files are readable without running Mneme.\n"
        ).encode("utf-8"),
    )
    members = tree_hashes(export_root)
    manifest: Dict[str, Any] = {
        "export_version": 1,
        "members": members,
        "recorded_at": recorded_at,
    }
    _write_json(export_root / "export-manifest.json", manifest)
    verify_export(export_root)
    return manifest


def verify_export(export_root: Path) -> Dict[str, Any]:
    if export_root.is_symlink() or not export_root.is_dir():
        raise IntegrityError("export root must be a non-symlink directory")
    manifest_path = export_root / "export-manifest.json"
    _require_regular(manifest_path, "export manifest")
    manifest = _load_json(manifest_path)
    if manifest.get("export_version") != 1 or not isinstance(manifest.get("members"), dict):
        raise IntegrityError("unsupported export manifest")
    actual = tree_hashes(export_root, exclude=("export-manifest.json",))
    if actual != manifest["members"]:
        raise IntegrityError("export has missing, changed, or extra members")
    return manifest


def restore_bundle(export_root: Path, restore_root: Path) -> Dict[str, Path]:
    verify_export(export_root)
    if restore_root.exists():
        raise ScopeError(f"restore root already exists: {restore_root}")
    restore_root.mkdir(parents=True, mode=0o700)
    shutil.copytree(export_root / "archive", restore_root / "archive")
    shutil.copytree(export_root / "derived", restore_root / "derived")
    verify_archive(restore_root / "archive")
    verify_derived(restore_root / "archive", restore_root / "derived")
    return {"archive": restore_root / "archive", "derived": restore_root / "derived"}


def _prepare_workspace(workspace: Path) -> None:
    if workspace.is_symlink():
        raise ScopeError("workspace must not be a symlink")
    if workspace.exists():
        if not workspace.is_dir() or any(workspace.iterdir()):
            raise ScopeError("workspace must be a fresh empty directory")
    else:
        workspace.mkdir(parents=True, mode=0o700)


def run_experiment(
    workspace: Path, recorded_at: str, query: str
) -> Dict[str, Any]:
    _prepare_workspace(workspace)
    input_paths = fixtures.materialize(workspace / "incoming")
    archive = workspace / "archive"
    derived_a = workspace / "derived-a"
    derived_b = workspace / "derived-b"
    export_root = workspace / "export"
    restore_root = workspace / "restore"

    source_manifest = preserve_package(input_paths, archive, recorded_at)
    first = build_derived(archive, derived_a, recorded_at)
    build_derived(archive, derived_b, recorded_at)
    hashes_a = tree_hashes(derived_a)
    hashes_b = tree_hashes(derived_b)
    if hashes_a != hashes_b:
        raise IntegrityError("clean rebuilds produced different derived state")

    find_before = deterministic_find(archive, derived_a, query)
    if not find_before["results"]:
        raise IntegrityError("reviewed query unexpectedly returned no result")
    first_citation = find_before["results"][0]["citations"][0]["citation"]
    source_display = display_source(archive, derived_a, first_citation)

    export_manifest = export_bundle(archive, derived_a, export_root, recorded_at)
    restored = restore_bundle(export_root, restore_root)
    find_restored = deterministic_find(restored["archive"], restored["derived"], query)
    if find_restored != find_before:
        raise IntegrityError("restored Find results or citations differ")
    shutil.rmtree(restored["derived"])
    build_derived(restored["archive"], restored["derived"], recorded_at)
    restored_hashes = tree_hashes(restored["derived"])
    if restored_hashes != hashes_a:
        raise IntegrityError("restored clean rebuild differs from original derived state")

    status_counts = Counter(
        record["status"] for record in first["messages"]["messages"]
    )
    return {
        "citation": first_citation,
        "derived_file_hashes": hashes_a,
        "derived_tree_sha256": tree_digest(derived_a),
        "duplicate_relations": first["duplicates"],
        "export_manifest_sha256": sha256_path(export_root / "export-manifest.json"),
        "export_member_count": len(export_manifest["members"]),
        "find": find_before,
        "fixture_count": len(fixtures.FIXTURES),
        "rebuild_equal": hashes_a == hashes_b,
        "restore_find_equal": find_restored == find_before,
        "restore_rebuild_equal": restored_hashes == hashes_a,
        "source_display": source_display,
        "source_manifest_sha256": sha256_path(archive / "manifest.json"),
        "source_items": {
            item["id"]: {"byte_count": item["byte_count"], "sha256": item["sha256"]}
            for item in source_manifest["source_items"]
        },
        "status_counts": dict(sorted(status_counts.items())),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    run = subparsers.add_parser("run", help="run the complete hardening experiment")
    run.add_argument("--workspace", type=Path, required=True)
    run.add_argument("--recorded-at", required=True)
    run.add_argument("--query", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        if arguments.command != "run":
            raise ScopeError(f"unsupported command: {arguments.command}")
        result = run_experiment(arguments.workspace, arguments.recorded_at, arguments.query)
    except ExperimentError as error:
        print(f"STOPPED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
