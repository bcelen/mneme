#!/usr/bin/env python3
"""Address identities over prototype-3 state: evidence about addresses, not people.

An identity here is exactly one normalized address specification. Display
names are recorded as evidence and never used to merge identities; no
identity is linked to a person. Everything is computed at query time from the
verified current generation, so no derived state is added or changed.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter
from email.utils import getaddresses
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple


EXPERIMENT_ROOT = Path(__file__).resolve().parent
PROTOTYPE_4_PATH = EXPERIMENT_ROOT.parent / "mneme-local-prototype-4" / "mneme.py"


def _load_prototype_4():
    name = "mneme_local_synthetic_prototype_4"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, PROTOTYPE_4_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {PROTOTYPE_4_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


P4 = _load_prototype_4()
P3 = P4.P3
HARDENING = P4.HARDENING
IDENTITY_RULE = "synthetic-address-identity-v1"
IDENTITY_NOTE = "An identity is one normalized address. It is not a person, and display names never merge identities."


def _named_addresses(value: Optional[str]) -> List[Tuple[str, str]]:
    """(display name, normalized address) pairs from a derived address header."""

    if value is None:
        return []
    pairs = []
    for name, address in getaddresses([str(value)]):
        normalized = address.strip().lower()
        if P4.ADDRESS_PATTERN.fullmatch(normalized or "-"):
            pairs.append((name.strip(), normalized))
    return pairs


def _occurrences(state_root: Path) -> List[Dict[str, Any]]:
    """One entry per non-quarantined occurrence, in source-ID order."""

    _, generation_root, manifest = P3.current_generation(state_root)
    derived = generation_root / "derived"
    records = {r["source_id"]: r for r in HARDENING._load_json(derived / "messages.json")["messages"]}
    subjects = P4._subject_citations(HARDENING._load_json(derived / "index.json"))
    rows = []
    for item in manifest["source_items"]:
        record = records[item["id"]]
        if record["status"] == "quarantined":
            continue
        fields = record.get("fields") or {}
        rows.append(
            {
                "citation": subjects.get(item["id"]),
                "facts": P4.record_facts(record, item),
                "recipients": _named_addresses(fields.get("to")),
                "senders": _named_addresses(fields.get("from")),
                "source_id": item["id"],
                "source_sha256": item["sha256"],
            }
        )
    return rows


def _roles(row: Mapping[str, Any], address: str) -> List[str]:
    roles = []
    if any(a == address for _, a in row["senders"]):
        roles.append("sender")
    if any(a == address for _, a in row["recipients"]):
        roles.append("recipient")
    return roles


def _summary(address: str, rows: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    involved = [row for row in rows if _roles(row, address)]
    dated = sorted(row["facts"]["date_utc"] for row in involved if row["facts"]["date_utc"])
    names = sorted(
        {name for row in involved for name, a in row["senders"] + row["recipients"] if a == address and name}
    )
    return {
        "address": address,
        "as_recipient": sum("recipient" in _roles(row, address) for row in involved),
        "as_sender": sum("sender" in _roles(row, address) for row in involved),
        "display_names": names,
        "distinct_source_hashes": len({row["source_sha256"] for row in involved}),
        "families": dict(sorted(Counter(row["facts"]["family"] for row in involved).items())),
        "first_seen_utc": dated[0] if dated else None,
        "last_seen_utc": dated[-1] if dated else None,
        "occurrences": len(involved),
        "undated_occurrences": sum(1 for row in involved if not row["facts"]["date_utc"]),
    }


def identities(state_root: Path) -> Dict[str, Any]:
    rows = _occurrences(state_root)
    addresses = sorted({a for row in rows for _, a in row["senders"] + row["recipients"]})
    return {
        "identities": [_summary(address, rows) for address in addresses],
        "note": IDENTITY_NOTE,
        "rule": IDENTITY_RULE,
    }


def identity(state_root: Path, address: str) -> Dict[str, Any]:
    normalized = address.strip().lower()
    if P4.ADDRESS_PATTERN.fullmatch(normalized) is None:
        raise HARDENING.ScopeError("identity must be one address such as name@example.test")
    rows = _occurrences(state_root)
    involved = [row for row in rows if _roles(row, normalized)]
    if not involved:
        raise HARDENING.ScopeError(f"no non-quarantined occurrence involves {normalized}")
    correspondents: Dict[str, Counter] = {}
    for row in involved:
        others_as_recipient = {a for _, a in row["recipients"]} - {normalized}
        others_as_sender = {a for _, a in row["senders"]} - {normalized}
        if "sender" in _roles(row, normalized):
            for other in others_as_recipient:
                correspondents.setdefault(other, Counter())["sent_to"] += 1
        if "recipient" in _roles(row, normalized):
            for other in others_as_sender:
                correspondents.setdefault(other, Counter())["received_from"] += 1
    return {
        **_summary(normalized, rows),
        "correspondents": [
            {"address": other, "received_from": counts["received_from"], "sent_to": counts["sent_to"]}
            for other, counts in sorted(correspondents.items())
        ],
        "note": IDENTITY_NOTE,
        "occurrence_list": [
            {
                "citation": row["citation"]["citation"] if row["citation"] else None,
                "date_status": row["facts"]["date_status"],
                "date_utc": row["facts"]["date_utc"],
                "display_names": sorted(
                    {n for n, a in row["senders"] + row["recipients"] if a == normalized and n}
                ),
                "roles": _roles(row, normalized),
                "source_id": row["source_id"],
                "source_sha256": row["source_sha256"],
            }
            for row in involved
        ],
        "rule": IDENTITY_RULE,
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("identities").add_argument("--state", type=Path, required=True)
    detail = commands.add_parser("identity")
    detail.add_argument("--state", type=Path, required=True)
    detail.add_argument("--address", required=True)
    arguments = parser.parse_args(argv)
    try:
        if arguments.command == "identities":
            result = identities(arguments.state)
        else:
            result = identity(arguments.state, arguments.address)
    except HARDENING.ExperimentError as error:
        print(f"STOPPED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
