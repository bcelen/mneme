#!/usr/bin/env python3
"""Local Mneme prototype 4: deterministic, inspectable Find filters over prototype-3 state.

Filters are evaluated at query time from verified derived records and the source
manifest. No derived state is added or changed, so ingestion, rebuild output,
and every existing hash stay exactly as prototype 3 produces them.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from datetime import date, timezone
from email.utils import getaddresses, parsedate_to_datetime
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence


PROTOTYPE_ROOT = Path(__file__).resolve().parent
PROTOTYPE_3_PATH = PROTOTYPE_ROOT.parent / "mneme-local-prototype-3" / "mneme.py"


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

PROTOTYPE_NAME = "mneme-local-synthetic-prototype"
PROTOTYPE_VERSION = "4"
FILTER_RULE = "synthetic-find-filters-v1"
FILTER_ORDER = ("status", "family", "mailbox", "has_attachment", "sender", "recipient", "participant", "date")
FILTERABLE_STATUSES = ("indexed", "indexed_with_warnings")
FAMILIES = ("eml", "mbox")
DAY_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ADDRESS_PATTERN = re.compile(r"^[^@\s<>]+@[^@\s<>]+$")
MAILBOX_PATTERN = re.compile(r"^[0-9a-z][0-9a-z._-]{0,95}\.mbox$")


# ---------------------------------------------------------------------------
# Facts derived at query time


def classify_date(value: Optional[str]) -> Dict[str, Optional[str]]:
    """Normalize a derived Date header to UTC without guessing.

    ``valid``: parsed with an explicit offset. ``no-timezone``: parsed, but the
    header carries ``-0000`` or no offset; interpreted as UTC and flagged.
    ``invalid`` and ``missing`` never receive a date.
    """

    if value is None or not str(value).strip():
        return {"date_status": "missing", "date_utc": None}
    try:
        parsed = parsedate_to_datetime(str(value))
    except (TypeError, ValueError, IndexError, OverflowError):
        parsed = None
    if parsed is None:
        return {"date_status": "invalid", "date_utc": None}
    status = "valid"
    if parsed.tzinfo is None:
        status = "no-timezone"
        parsed = parsed.replace(tzinfo=timezone.utc)
    utc = parsed.astimezone(timezone.utc)
    return {"date_status": status, "date_utc": utc.strftime("%Y-%m-%dT%H:%M:%SZ")}


def addresses(value: Optional[str]) -> List[str]:
    """Return sorted, lower-cased address specs from a derived address header."""

    if value is None:
        return []
    found = {
        address.strip().lower()
        for _, address in getaddresses([str(value)])
        if ADDRESS_PATTERN.fullmatch(address.strip() or "-")
    }
    return sorted(found)


def record_facts(record: Mapping[str, Any], item: Mapping[str, Any]) -> Dict[str, Any]:
    fields = record.get("fields") if isinstance(record.get("fields"), dict) else {}
    parts = record.get("parts") if isinstance(record.get("parts"), list) else []
    facts: Dict[str, Any] = {
        "family": item["source_family"],
        "has_attachment": any(
            str(part.get("artifact_path", "")).startswith("attachments/") for part in parts
        ),
        "mailbox": item["container"]["name"] if item["source_family"] == "mbox" else None,
        "recipients": addresses(fields.get("to")),
        "senders": addresses(fields.get("from")),
        "status": record["status"],
    }
    facts.update(classify_date(fields.get("date")))
    return facts


# ---------------------------------------------------------------------------
# Filter validation and evaluation


def _day(value: str, label: str) -> date:
    if not isinstance(value, str) or DAY_PATTERN.fullmatch(value) is None:
        raise HARDENING.ScopeError(f"{label} must be a UTC day YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise HARDENING.ScopeError(f"{label} is not a calendar day: {value}") from error


def normalize_filters(
    status: Optional[str] = None,
    family: Optional[str] = None,
    mailbox: Optional[str] = None,
    has_attachment: Optional[bool] = None,
    sender: Optional[str] = None,
    recipient: Optional[str] = None,
    participant: Optional[str] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
) -> Dict[str, Any]:
    """Validate filter values; return only the filters that were supplied."""

    applied: Dict[str, Any] = {}
    if status is not None:
        if status not in FILTERABLE_STATUSES:
            raise HARDENING.ScopeError(
                f"status must be one of {FILTERABLE_STATUSES}; quarantined sources are never Find results"
            )
        applied["status"] = status
    if family is not None:
        if family not in FAMILIES:
            raise HARDENING.ScopeError(f"family must be one of {FAMILIES}")
        applied["family"] = family
    if mailbox is not None:
        if MAILBOX_PATTERN.fullmatch(mailbox) is None:
            raise HARDENING.ScopeError(f"mailbox must be a supported .mbox file name: {mailbox!r}")
        applied["mailbox"] = mailbox
    if has_attachment is not None:
        applied["has_attachment"] = bool(has_attachment)
    for label, value in (("sender", sender), ("recipient", recipient), ("participant", participant)):
        if value is not None:
            normalized = value.strip().lower()
            if ADDRESS_PATTERN.fullmatch(normalized) is None:
                raise HARDENING.ScopeError(f"{label} must be one address such as name@example.test")
            applied[label] = normalized
    if since is not None or until is not None:
        start = _day(since, "since") if since is not None else None
        end = _day(until, "until") if until is not None else None
        if start and end and start > end:
            raise HARDENING.ScopeError("since must not be later than until")
        applied["date"] = {
            "since": start.isoformat() if start else None,
            "until": end.isoformat() if end else None,
        }
    return applied


def _passes(name: str, value: Any, facts: Mapping[str, Any]) -> bool:
    if name == "status":
        return facts["status"] == value
    if name == "family":
        return facts["family"] == value
    if name == "mailbox":
        return facts["mailbox"] == value
    if name == "has_attachment":
        return facts["has_attachment"] is value
    if name == "sender":
        return value in facts["senders"]
    if name == "recipient":
        return value in facts["recipients"]
    if name == "participant":
        return value in facts["senders"] or value in facts["recipients"]
    if name == "date":
        if facts["date_utc"] is None:
            return False
        day = facts["date_utc"][:10]
        return (value["since"] is None or value["since"] <= day) and (
            value["until"] is None or day <= value["until"]
        )
    raise HARDENING.ScopeError(f"unsupported filter: {name}")


def _subject_citations(index: Mapping[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Return each source's indexed subject occurrence as a Find-style citation."""

    subjects: Dict[str, Dict[str, Any]] = {}
    for rows in index["terms"].values():
        for occurrence in rows:
            if occurrence.get("locator") == "header:subject:1":
                subjects[occurrence["source_id"]] = {
                    "citation": HARDENING._citation(
                        occurrence["source_id"], occurrence["source_sha256"], "header:subject:1"
                    ),
                    "field": occurrence["field"],
                    "text": occurrence["text"],
                }
    return subjects


def find(state_root: Path, query: Optional[str] = None, **filter_values: Any) -> Dict[str, Any]:
    """Deterministic Find with optional filters.

    Without filters this returns prototype 3's Find output unchanged. With
    filters, a query narrows candidates by the unchanged term match; without a
    query, every non-quarantined occurrence is a candidate and is cited by its
    indexed subject header when one exists.
    """

    applied = normalize_filters(**filter_values)
    if not applied:
        if query is None:
            raise HARDENING.ScopeError("Find needs a query, at least one filter, or both")
        return P3.find(state_root, query)

    _, generation_root, manifest = P3.current_generation(state_root)
    archive = generation_root / "archive"
    derived = generation_root / "derived"
    items = {item["id"]: item for item in manifest["source_items"]}
    records = {
        record["source_id"]: record
        for record in HARDENING._load_json(derived / "messages.json")["messages"]
    }

    output: Dict[str, Any] = {"query": query}
    if query is not None:
        matched = HARDENING.deterministic_find(archive, derived, query)
        output["normalized_terms"] = matched["normalized_terms"]
        rows = list(matched["results"])
    else:
        subjects = _subject_citations(HARDENING._load_json(derived / "index.json"))
        rows = [
            {
                "citations": [subjects[source_id]] if source_id in subjects else [],
                "source_id": source_id,
                "source_sha256": items[source_id]["sha256"],
            }
            for source_id in items
            if records[source_id]["status"] != "quarantined"
        ]

    facts = {row["source_id"]: record_facts(records[row["source_id"]], items[row["source_id"]]) for row in rows}
    steps = []
    remaining = rows
    for name in FILTER_ORDER:
        if name not in applied:
            continue
        kept = [row for row in remaining if _passes(name, applied[name], facts[row["source_id"]])]
        steps.append({"filter": name, "removed": len(remaining) - len(kept), "remaining": len(kept), "value": applied[name]})
        remaining = kept

    report: Dict[str, Any] = {"candidates": len(rows), "rule": FILTER_RULE, "steps": steps}
    if "date" in applied:
        report["undated_candidates"] = sorted(
            source_id for source_id, fact in facts.items() if fact["date_utc"] is None
        )
    output.update(
        {
            "filter_report": report,
            "filters": applied,
            "results": [{**row, "facts": facts[row["source_id"]]} for row in remaining],
        }
    )
    return output


# ---------------------------------------------------------------------------
# CLI: `find` is extended here; every other command is prototype 3's.


def _find_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mneme.py find", description="Find with optional filters.")
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--query")
    parser.add_argument("--status", choices=FILTERABLE_STATUSES)
    parser.add_argument("--family", choices=FAMILIES)
    parser.add_argument("--mailbox")
    attachment = parser.add_mutually_exclusive_group()
    attachment.add_argument("--has-attachment", dest="has_attachment", action="store_true", default=None)
    attachment.add_argument("--no-attachment", dest="has_attachment", action="store_false")
    parser.add_argument("--from", dest="sender")
    parser.add_argument("--to", dest="recipient")
    parser.add_argument("--participant")
    parser.add_argument("--since")
    parser.add_argument("--until")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] != "find":
        return P3.main(argv)
    arguments = _find_parser().parse_args(argv[1:])
    try:
        result = find(
            arguments.state,
            arguments.query,
            status=arguments.status,
            family=arguments.family,
            mailbox=arguments.mailbox,
            has_attachment=arguments.has_attachment,
            sender=arguments.sender,
            recipient=arguments.recipient,
            participant=arguments.participant,
            since=arguments.since,
            until=arguments.until,
        )
    except HARDENING.ExperimentError as error:
        print(f"STOPPED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
