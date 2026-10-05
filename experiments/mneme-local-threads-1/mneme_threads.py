#!/usr/bin/env python3
"""Evidence-only conversation threading over prototype-3 state.

Threads come only from `Message-ID`, `In-Reply-To`, and `References` in the
preserved source bytes; subjects are never used. Referenced messages that are
not in the archive become explicit placeholders, a reply that would create a
loop is refused and reported, and occurrences that share a Message-ID share
one node. Everything is computed at query time; no derived state changes.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from email import policy
from email.parser import BytesHeaderParser
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence


EXPERIMENT_ROOT = Path(__file__).resolve().parent
EXPERIMENTS = EXPERIMENT_ROOT.parent
if str(EXPERIMENT_ROOT) not in sys.path:
    sys.path.insert(0, str(EXPERIMENT_ROOT))

import thread_fixtures as THREAD_FIXTURES  # noqa: E402


def _load(name: str, path: Path):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


P4 = _load("mneme_local_synthetic_prototype_4", EXPERIMENTS / "mneme-local-prototype-4" / "mneme.py")
P3 = P4.P3
HARDENING = P3.HARDENING
# A separate copy of prototype 3 whose ingest also accepts the pinned threading
# fixtures. The shared copy above, and the file on disk, are unchanged.
P3_THREADS = _load("mneme_p3_with_thread_fixtures", EXPERIMENTS / "mneme-local-prototype-3" / "mneme.py")
_BASE_ALLOWLIST = P3_THREADS.reviewed_allowlist
P3_THREADS.reviewed_allowlist = lambda: {**_BASE_ALLOWLIST(), **THREAD_FIXTURES.reviewed_digests()}

THREAD_RULE = "synthetic-reference-threading-v1"
MESSAGE_ID_PATTERN = re.compile(r"<[^<>\s@]+@[^<>\s]+>")


def ingest(incoming: Path, state: Path, recorded_at: str) -> Dict[str, Any]:
    """Prototype 3 ingest that also accepts the pinned threading fixtures."""

    return P3_THREADS.ingest(incoming, state, recorded_at)


def message_ids(value: Optional[str]) -> List[str]:
    """Bracketed message IDs in order, case-folded; anything else is ignored."""

    if value is None:
        return []
    return [match.casefold() for match in MESSAGE_ID_PATTERN.findall(str(value))]


def _reference_headers(raw: bytes) -> Dict[str, List[str]]:
    headers = BytesHeaderParser(policy=policy.compat32).parsebytes(raw)
    return {
        "in_reply_to": [str(v) for v in headers.get_all("In-Reply-To") or []],
        "references": [str(v) for v in headers.get_all("References") or []],
    }


def _occurrences(state_root: Path) -> List[Dict[str, Any]]:
    _, generation_root, manifest = P3.current_generation(state_root)
    archive = generation_root / "archive"
    derived = generation_root / "derived"
    records = {r["source_id"]: r for r in HARDENING._load_json(derived / "messages.json")["messages"]}
    subjects = P4._subject_citations(HARDENING._load_json(derived / "index.json"))
    rows = []
    for item in manifest["source_items"]:
        record = records[item["id"]]
        if record["status"] == "quarantined":
            continue
        raw = HARDENING._contained(archive, item["relative_path"]).read_bytes()
        if hashlib.sha256(raw).hexdigest() != item["sha256"]:
            raise HARDENING.IntegrityError(f"preserved source changed: {item['id']}")
        if item["source_family"] == "mbox":
            raw = P3.MBOXRD.unescape_record(raw)
        headers = _reference_headers(raw)
        own = message_ids((record.get("fields") or {}).get("message_id"))
        references = [i for value in headers["references"] for i in message_ids(value)]
        in_reply_to = [i for value in headers["in_reply_to"] for i in message_ids(value)]
        rows.append(
            {
                "citation": subjects[item["id"]]["citation"] if item["id"] in subjects else None,
                "date_utc": P4.classify_date((record.get("fields") or {}).get("date"))["date_utc"],
                "in_reply_to": in_reply_to,
                "key": own[0] if own else f"occurrence:{item['id']}",
                "references": references,
                "source_id": item["id"],
                "unparseable_headers": bool(
                    (headers["references"] and not references) or (headers["in_reply_to"] and not in_reply_to)
                ),
            }
        )
    return rows


def build_threads(state_root: Path) -> Dict[str, Any]:
    rows = _occurrences(state_root)
    nodes: Dict[str, Dict[str, Any]] = {}

    def node(key: str) -> Dict[str, Any]:
        return nodes.setdefault(key, {"key": key, "occurrences": [], "parent": None})

    def is_ancestor(candidate: str, of: str) -> bool:
        current: Optional[str] = of
        while current is not None:
            if current == candidate:
                return True
            current = nodes[current]["parent"]
        return False

    cycles: List[Dict[str, str]] = []
    conflicts: List[Dict[str, str]] = []

    def link(child: str, parent: str, source_id: str, explicit: bool) -> None:
        node(parent)
        current = nodes[child]["parent"]
        if child == parent or current == parent:
            return
        if current is not None:
            if explicit:
                conflicts.append({"kept": current, "node": child, "rejected": parent, "source_id": source_id})
            return
        if is_ancestor(child, parent):
            cycles.append({"node": child, "rejected_parent": parent, "source_id": source_id})
            return
        nodes[child]["parent"] = parent

    for row in rows:  # source-ID order makes every decision deterministic
        node(row["key"])["occurrences"].append(row)
    for row in rows:
        chain = row["references"]
        for earlier, later in zip(chain, chain[1:]):
            node(later)
            link(later, earlier, row["source_id"], explicit=False)
        parent = chain[-1] if chain else (row["in_reply_to"][0] if row["in_reply_to"] else None)
        if parent is not None:
            link(row["key"], parent, row["source_id"], explicit=True)

    children: Dict[str, List[str]] = {key: [] for key in nodes}
    for key, value in nodes.items():
        if value["parent"] is not None:
            children[value["parent"]].append(key)

    def earliest(key: str) -> str:
        dates = [o["date_utc"] for o in nodes[key]["occurrences"] if o["date_utc"]]
        return min(dates) if dates else "~"  # undated and missing sort last

    def tree(key: str) -> Dict[str, Any]:
        value = nodes[key]
        return {
            "children": [tree(child) for child in sorted(children[key], key=lambda k: (earliest(k), k))],
            "message_id": None if key.startswith("occurrence:") else key,
            "missing_from_archive": not value["occurrences"],
            "occurrences": [
                {"citation": o["citation"], "date_utc": o["date_utc"], "source_id": o["source_id"]}
                for o in value["occurrences"]
            ],
        }

    def size(subtree: Mapping[str, Any]) -> int:
        return len(subtree["occurrences"]) + sum(size(child) for child in subtree["children"])

    roots = sorted((k for k, v in nodes.items() if v["parent"] is None), key=lambda k: (earliest(k), k))
    threads = []
    for root in roots:
        subtree = tree(root)
        threads.append({"occurrence_count": size(subtree), "root": subtree, "thread_id": f"thread:{root}"})
    return {
        "cycles_refused": cycles,
        "missing_messages": sorted(k for k, v in nodes.items() if not v["occurrences"]),
        "parent_conflicts": conflicts,
        "rule": THREAD_RULE,
        "threads": threads,
        "unparseable_reference_headers": [r["source_id"] for r in rows if r["unparseable_headers"]],
    }


def _members(subtree: Mapping[str, Any]) -> List[str]:
    found = [o["source_id"] for o in subtree["occurrences"]]
    for child in subtree["children"]:
        found.extend(_members(child))
    return found


def conversations(state_root: Path, include_singletons: bool = False) -> Dict[str, Any]:
    result = build_threads(state_root)
    if not include_singletons:
        result["threads"] = [
            t for t in result["threads"] if t["root"]["children"] or len(t["root"]["occurrences"]) > 1
        ]
    return result


def thread_of(state_root: Path, source_id: str) -> Dict[str, Any]:
    result = build_threads(state_root)
    for thread in result["threads"]:
        if source_id in _members(thread["root"]):
            return {**thread, "rule": THREAD_RULE}
    raise HARDENING.ScopeError(f"no non-quarantined occurrence {source_id}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    ingest_parser = commands.add_parser("ingest")
    ingest_parser.add_argument("--incoming", type=Path, required=True)
    ingest_parser.add_argument("--state", type=Path, required=True)
    ingest_parser.add_argument("--recorded-at", required=True)
    list_parser = commands.add_parser("threads")
    list_parser.add_argument("--state", type=Path, required=True)
    list_parser.add_argument("--all", action="store_true")
    one = commands.add_parser("thread")
    one.add_argument("--state", type=Path, required=True)
    one.add_argument("--source-id", required=True)
    arguments = parser.parse_args(argv)
    try:
        if arguments.command == "ingest":
            result = ingest(arguments.incoming, arguments.state, arguments.recorded_at)
        elif arguments.command == "threads":
            result = conversations(arguments.state, arguments.all)
        else:
            result = thread_of(arguments.state, arguments.source_id)
    except HARDENING.ExperimentError as error:
        print(f"STOPPED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
