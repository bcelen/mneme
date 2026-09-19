#!/usr/bin/env python3
"""A synthetic-only, standard-library Mneme vertical slice."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
import unicodedata
from email import policy
from email.parser import BytesParser
from pathlib import Path, PurePosixPath
from typing import Any, Dict, List, Mapping, Sequence


TOOL_NAME = "mneme-synthetic-vertical-slice"
TOOL_VERSION = "1"
PROCESSING_RULE = "plain-text-eml-v1"
MAX_SOURCE_BYTES = 64 * 1024
TOKEN_PATTERN = re.compile(r"[a-z0-9]+(?:[-'][a-z0-9]+)*")
CITATION_PATTERN = re.compile(
    r"^mneme-source:(?P<source_id>[a-z0-9-]+)@sha256:"
    r"(?P<digest>[0-9a-f]{64})#L(?P<start>[1-9][0-9]*)-L(?P<end>[1-9][0-9]*)$"
)


class SliceError(RuntimeError):
    """Base error for a stopped vertical-slice operation."""


class IntegrityError(SliceError):
    """Raised when source or manifest integrity cannot be proved."""


class ScopeError(SliceError):
    """Raised when input is outside the approved synthetic slice."""


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(64 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


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
    payload = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")
    _atomic_write(path, payload, mode=mode)


def _load_json(path: Path) -> Dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise IntegrityError(f"cannot read valid JSON from {path.name}: {error}") from error
    if not isinstance(value, dict):
        raise IntegrityError(f"{path.name} must contain a JSON object")
    return value


def _require_regular_file(path: Path, label: str) -> os.stat_result:
    try:
        status = path.lstat()
    except FileNotFoundError as error:
        raise IntegrityError(f"missing {label}: {path}") from error
    if stat.S_ISLNK(status.st_mode) or not stat.S_ISREG(status.st_mode):
        raise IntegrityError(f"{label} must be a regular non-symlink file: {path}")
    return status


def _contained_member(root: Path, relative_path: str) -> Path:
    member = PurePosixPath(relative_path)
    if member.is_absolute() or ".." in member.parts:
        raise IntegrityError(f"unsafe manifest member path: {relative_path}")
    candidate = root.joinpath(*member.parts)
    resolved_root = root.resolve()
    try:
        candidate.resolve().relative_to(resolved_root)
    except (OSError, ValueError) as error:
        raise IntegrityError(f"manifest member escapes archive: {relative_path}") from error
    return candidate


def preserve_eml(source_path: Path, archive_root: Path, recorded_at: str) -> Dict[str, Any]:
    """Preserve one synthetic EML before any parsing and write its manifest."""

    source_status = _require_regular_file(source_path, "synthetic fixture")
    if source_status.st_size > MAX_SOURCE_BYTES:
        raise ScopeError(f"fixture exceeds {MAX_SOURCE_BYTES} bytes")
    if archive_root.exists():
        raise ScopeError(f"archive root already exists: {archive_root}")

    source_bytes = source_path.read_bytes()
    digest = hashlib.sha256(source_bytes).hexdigest()
    source_id = f"src-sha256-{digest[:24]}"
    package_id = "pkg-synthetic-eml-001"
    relative_path = f"source-items/{source_id}.eml"
    preserved_path = archive_root / relative_path

    archive_root.mkdir(parents=True, mode=0o700)
    _atomic_write(preserved_path, source_bytes, mode=0o400)
    if preserved_path.read_bytes() != source_bytes:
        raise IntegrityError("preserved bytes differ from fixture")

    manifest: Dict[str, Any] = {
        "manifest_version": 1,
        "hash_algorithm": "sha256",
        "source_package": {
            "id": package_id,
            "members": [source_id],
            "source_family": "synthetic-eml",
        },
        "source_items": [
            {
                "byte_count": len(source_bytes),
                "content_type": "message/rfc822",
                "id": source_id,
                "relative_path": relative_path,
                "sha256": digest,
                "provenance": {
                    "event": "preserve",
                    "event_id": f"prov-preserve-{digest[:24]}",
                    "input_name": source_path.name,
                    "recorded_at": recorded_at,
                    "source_kind": "wholly-fictional-synthetic-fixture",
                    "tool": {"name": TOOL_NAME, "version": TOOL_VERSION},
                },
            }
        ],
    }
    _write_json(archive_root / "manifest.json", manifest, mode=0o400)
    verify_archive(archive_root)
    return manifest


def verify_archive(archive_root: Path) -> Dict[str, Any]:
    """Independently verify archive membership, byte counts, and SHA-256 values."""

    if archive_root.is_symlink() or not archive_root.is_dir():
        raise IntegrityError(f"archive root must be a non-symlink directory: {archive_root}")
    manifest_path = archive_root / "manifest.json"
    _require_regular_file(manifest_path, "manifest")
    manifest = _load_json(manifest_path)

    if manifest.get("manifest_version") != 1:
        raise IntegrityError("unsupported manifest version")
    if manifest.get("hash_algorithm") != "sha256":
        raise IntegrityError("unsupported hash algorithm")
    source_items = manifest.get("source_items")
    package = manifest.get("source_package")
    if not isinstance(source_items, list) or len(source_items) != 1:
        raise IntegrityError("manifest must contain exactly one source item")
    if not isinstance(package, dict):
        raise IntegrityError("manifest source package is missing")

    item = source_items[0]
    if not isinstance(item, dict):
        raise IntegrityError("source item must be an object")
    required = {"id", "relative_path", "byte_count", "sha256", "provenance"}
    if not required.issubset(item):
        raise IntegrityError("source item is incomplete")
    if package.get("members") != [item["id"]]:
        raise IntegrityError("source-package membership disagrees with source item")

    relative_path = item["relative_path"]
    if not isinstance(relative_path, str):
        raise IntegrityError("source-item path must be text")
    preserved_path = _contained_member(archive_root, relative_path)
    status = _require_regular_file(preserved_path, "preserved source item")

    actual_members = set()
    for candidate in archive_root.rglob("*"):
        if candidate.is_symlink():
            raise IntegrityError(f"archive contains a symlink: {candidate}")
        if candidate.is_file() and candidate != manifest_path:
            actual_members.add(candidate.relative_to(archive_root).as_posix())
    if actual_members != {relative_path}:
        raise IntegrityError(
            f"archive membership mismatch: expected {[relative_path]}, got {sorted(actual_members)}"
        )
    if status.st_size != item["byte_count"]:
        raise IntegrityError(
            f"byte-count mismatch for {item['id']}: expected {item['byte_count']}, got {status.st_size}"
        )
    actual_digest = sha256_path(preserved_path)
    if actual_digest != item["sha256"]:
        raise IntegrityError(
            f"SHA-256 mismatch for {item['id']}: expected {item['sha256']}, got {actual_digest}"
        )
    return manifest


def _header_locator(lines: Sequence[bytes], name: str) -> Dict[str, int]:
    prefix = (name + ":").encode("ascii").lower()
    for index, line in enumerate(lines):
        if line.lower().startswith(prefix):
            end = index
            while end + 1 < len(lines) and lines[end + 1].startswith((b" ", b"\t")):
                end += 1
            return {"line_start": index + 1, "line_end": end + 1}
    raise ScopeError(f"required header is missing: {name}")


def _normalize_tokens(text: str) -> List[str]:
    normalized = unicodedata.normalize("NFKC", text).casefold()
    return TOKEN_PATTERN.findall(normalized)


def _citation(source_id: str, digest: str, start: int, end: int) -> str:
    return f"mneme-source:{source_id}@sha256:{digest}#L{start}-L{end}"


def build_derived(archive_root: Path, derived_root: Path, recorded_at: str) -> Dict[str, Any]:
    """Build disposable metadata and an index after archive verification."""

    manifest = verify_archive(archive_root)
    if derived_root.exists():
        raise ScopeError(f"derived root already exists: {derived_root}")
    item = manifest["source_items"][0]
    preserved_path = _contained_member(archive_root, item["relative_path"])
    raw = preserved_path.read_bytes()
    original_digest = hashlib.sha256(raw).hexdigest()

    message = BytesParser(policy=policy.default).parsebytes(raw)
    if message.is_multipart() or message.get_content_type() != "text/plain":
        raise ScopeError("the first slice accepts one non-multipart text/plain EML only")
    transfer_encoding = (message.get("Content-Transfer-Encoding") or "7bit").lower()
    if transfer_encoding not in {"7bit", "8bit"}:
        raise ScopeError("encoded body would not preserve direct source-line locators")

    required_headers = {
        "from": "From",
        "to": "To",
        "date": "Date",
        "message_id": "Message-ID",
        "subject": "Subject",
    }
    fields: Dict[str, str] = {}
    field_sources: Dict[str, Dict[str, int]] = {}
    raw_lines = raw.splitlines(keepends=True)
    for field_name, header_name in required_headers.items():
        header_value = message.get(header_name)
        if header_value is None:
            raise ScopeError(f"required header is missing: {header_name}")
        fields[field_name] = str(header_value)
        field_sources[field_name] = _header_locator(raw_lines, header_name)

    separator_index = next(
        (index for index, line in enumerate(raw_lines) if line in {b"\n", b"\r\n"}),
        None,
    )
    if separator_index is None:
        raise ScopeError("EML has no header/body separator")
    charset = message.get_content_charset() or "ascii"
    body_lines: List[Dict[str, Any]] = []
    for index, line in enumerate(raw_lines[separator_index + 1 :], start=separator_index + 2):
        try:
            text = line.rstrip(b"\r\n").decode(charset, errors="strict")
        except (LookupError, UnicodeDecodeError) as error:
            raise ScopeError(f"body cannot be decoded as {charset}: {error}") from error
        body_lines.append({"line": index, "text": text})

    record: Dict[str, Any] = {
        "generation": PROCESSING_RULE,
        "source_id": item["id"],
        "source_sha256": item["sha256"],
        "fields": fields,
        "field_sources": field_sources,
        "body_lines": body_lines,
        "provenance": {
            "event": "derive",
            "event_id": f"prov-derive-{item['sha256'][:24]}",
            "input_event_id": item["provenance"]["event_id"],
            "recorded_at": recorded_at,
            "rule": PROCESSING_RULE,
            "tool": {"name": TOOL_NAME, "version": TOOL_VERSION},
        },
    }

    occurrences: Dict[str, List[Dict[str, Any]]] = {}
    for field_name in ("from", "to", "date", "subject"):
        locator = field_sources[field_name]
        occurrence = {
            "field": field_name,
            "line_start": locator["line_start"],
            "line_end": locator["line_end"],
            "text": fields[field_name],
        }
        for token in sorted(set(_normalize_tokens(fields[field_name]))):
            occurrences.setdefault(token, []).append(occurrence)
    for body_line in body_lines:
        occurrence = {
            "field": "body",
            "line_start": body_line["line"],
            "line_end": body_line["line"],
            "text": body_line["text"],
        }
        for token in sorted(set(_normalize_tokens(body_line["text"]))):
            occurrences.setdefault(token, []).append(occurrence)

    for token_occurrences in occurrences.values():
        token_occurrences.sort(
            key=lambda value: (
                value["line_start"], value["line_end"], value["field"], value["text"]
            )
        )
    index: Dict[str, Any] = {
        "generation": PROCESSING_RULE,
        "normalization": "Unicode NFKC, casefold, ASCII alphanumeric/hyphen/apostrophe tokens",
        "source_id": item["id"],
        "source_sha256": item["sha256"],
        "terms": {token: occurrences[token] for token in sorted(occurrences)},
    }

    derived_root.mkdir(parents=True, mode=0o700)
    _write_json(derived_root / "record.json", record)
    _write_json(derived_root / "index.json", index)
    if sha256_path(preserved_path) != original_digest:
        raise IntegrityError("source changed during derivation")
    return {"record": record, "index": index}


def deterministic_find(archive_root: Path, derived_root: Path, query: str) -> Dict[str, Any]:
    """Return stable results only when all normalized query terms are present."""

    manifest = verify_archive(archive_root)
    record = _load_json(derived_root / "record.json")
    index = _load_json(derived_root / "index.json")
    item = manifest["source_items"][0]
    for value in (record, index):
        if value.get("generation") != PROCESSING_RULE:
            raise IntegrityError("derived generation is stale or unknown")
        if value.get("source_id") != item["id"] or value.get("source_sha256") != item["sha256"]:
            raise IntegrityError("derived state does not match the verified source")

    terms: List[str] = []
    for token in _normalize_tokens(query):
        if token not in terms:
            terms.append(token)
    if not terms:
        raise ScopeError("Find query must contain at least one supported token")
    term_index = index.get("terms")
    if not isinstance(term_index, dict):
        raise IntegrityError("derived index has no term map")
    if any(term not in term_index for term in terms):
        return {"normalized_terms": terms, "query": query, "results": []}

    citation_rows: Dict[tuple, Dict[str, Any]] = {}
    for term in terms:
        for occurrence in term_index[term]:
            key = (
                occurrence["line_start"],
                occurrence["line_end"],
                occurrence["field"],
                occurrence["text"],
            )
            citation_rows[key] = {
                "citation": _citation(
                    item["id"], item["sha256"], occurrence["line_start"], occurrence["line_end"]
                ),
                "field": occurrence["field"],
                "text": occurrence["text"],
            }
    citations = [citation_rows[key] for key in sorted(citation_rows)]
    result = {
        "citations": citations,
        "source_id": item["id"],
        "source_sha256": item["sha256"],
        "subject": record["fields"]["subject"],
    }
    return {"normalized_terms": terms, "query": query, "results": [result]}


def display_source(archive_root: Path, citation: str) -> Dict[str, Any]:
    """Resolve a citation to an inert text view of verified preserved bytes."""

    manifest = verify_archive(archive_root)
    match = CITATION_PATTERN.fullmatch(citation)
    if match is None:
        raise ScopeError("citation has an unsupported format")
    item = manifest["source_items"][0]
    if match.group("source_id") != item["id"] or match.group("digest") != item["sha256"]:
        raise IntegrityError("citation does not identify the verified source")

    start = int(match.group("start"))
    end = int(match.group("end"))
    preserved_path = _contained_member(archive_root, item["relative_path"])
    raw_lines = preserved_path.read_bytes().splitlines()
    if start > end or end > len(raw_lines):
        raise ScopeError("citation line range is outside the preserved source")
    lines = [
        {"line": number, "text": raw_lines[number - 1].decode("utf-8", errors="replace")}
        for number in range(start, end + 1)
    ]
    return {
        "citation": citation,
        "display_mode": "inert-text-no-html-no-fetch",
        "lines": lines,
        "provenance": item["provenance"],
        "source_id": item["id"],
        "source_sha256": item["sha256"],
    }


def _prepare_workspace(workspace: Path) -> None:
    if workspace.is_symlink():
        raise ScopeError("workspace must not be a symlink")
    if workspace.exists():
        if not workspace.is_dir() or any(workspace.iterdir()):
            raise ScopeError("workspace must be a fresh empty directory")
    else:
        workspace.mkdir(parents=True, mode=0o700)


def run_slice(fixture: Path, workspace: Path, query: str, recorded_at: str) -> Dict[str, Any]:
    _prepare_workspace(workspace)
    archive_root = workspace / "archive"
    derived_root = workspace / "derived"
    manifest = preserve_eml(fixture, archive_root, recorded_at)
    build_derived(archive_root, derived_root, recorded_at)
    find_result = deterministic_find(archive_root, derived_root, query)
    first_result = find_result["results"][0] if find_result["results"] else None
    first_citation = first_result["citations"][0]["citation"] if first_result else None
    source_display = display_source(archive_root, first_citation) if first_citation else None
    return {
        "derived_hashes": {
            "index.json": sha256_path(derived_root / "index.json"),
            "record.json": sha256_path(derived_root / "record.json"),
        },
        "find": find_result,
        "manifest": manifest,
        "source_display": source_display,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    run = subparsers.add_parser("run", help="run the complete synthetic slice")
    run.add_argument("--fixture", required=True, type=Path)
    run.add_argument("--workspace", required=True, type=Path)
    run.add_argument("--query", required=True)
    run.add_argument("--recorded-at", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        if arguments.command == "run":
            result = run_slice(
                arguments.fixture, arguments.workspace, arguments.query, arguments.recorded_at
            )
        else:
            raise ScopeError(f"unsupported command: {arguments.command}")
    except SliceError as error:
        print(f"STOPPED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
