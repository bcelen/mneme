#!/usr/bin/env python3
"""Stale-derived-state detection and side rebuild with a rebuild report.

Prototype 3 already refuses derived state built under another rule, but only
with a generic integrity error. This experiment explains staleness: which rule
identity changed, which source records carry the old one, whether the derived
bytes are merely stale or actually corrupt, and what a rebuild under the
current rules produces. Rebuilds go to a separate directory; publishing them
into the state would need a reviewed change to prototype 3's generation
convention, which requires every generation to append one ingest batch.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import sys
import tempfile
from collections import Counter
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
REPORT_VERSION = 1


def current_rules() -> Dict[str, str]:
    """Rule identities the current code would record, read at call time."""

    return {
        "engine-rule": HARDENING.PROCESSING_RULE,
        "engine-tool": f"{HARDENING.TOOL_NAME}/{HARDENING.TOOL_VERSION}",
        "isolation-profile": json.dumps(P3.ISOLATION._marker(), sort_keys=True),
        "mbox-rule": P3.MBOXRD.MBOX_RULE,
    }


def _record_rules(record: Mapping[str, Any]) -> Dict[str, Optional[str]]:
    provenance = record.get("provenance", {})
    tool = provenance.get("tool", {})
    isolation = record.get("isolation", {})
    mbox = record.get("mbox")
    return {
        "engine-rule": provenance.get("rule"),
        "engine-tool": f"{tool.get('name')}/{tool.get('version')}",
        # Records quarantined before parsing carry no isolation profile.
        "isolation-profile": (
            json.dumps(isolation, sort_keys=True) if isolation.get("mode") == "one-source-per-process" else None
        ),
        "mbox-rule": mbox.get("rule") if isinstance(mbox, dict) else None,
    }


def _derived_integrity(archive: Path, derived: Path) -> List[str]:
    """Check derived bytes against their own manifest, independent of rule identity."""

    problems = []
    try:
        derived_manifest = HARDENING._load_json(derived / "derived-manifest.json")
    except HARDENING.ExperimentError as error:
        return [f"derived manifest unreadable: {error}"]
    if derived_manifest.get("source_manifest_sha256") != HARDENING.sha256_path(archive / "manifest.json"):
        problems.append("derived state is bound to another source manifest")
    members = derived_manifest.get("members")
    actual = HARDENING.tree_hashes(derived, exclude=("derived-manifest.json",))
    if not isinstance(members, dict):
        problems.append("derived member map is missing")
    else:
        for path in sorted(set(members) | set(actual)):
            if members.get(path) != actual.get(path):
                problems.append(f"derived member missing, extra, or changed: {path}")
    return problems


def check_staleness(state_root: Path) -> Dict[str, Any]:
    """Classify the current generation's derived state as current, stale, or corrupt."""

    published, leftovers = P3._state_layout(state_root)
    name = published[-1]
    archive = state_root / "generations" / name / "archive"
    derived = state_root / "generations" / name / "derived"
    manifest = HARDENING.verify_archive(archive)
    P3._verify_identity_extension(archive, manifest)
    report: Dict[str, Any] = {
        "generation": name,
        "report_version": REPORT_VERSION,
        "unpublished_leftovers": leftovers,
    }
    problems = _derived_integrity(archive, derived)
    if problems:
        report.update({"integrity_problems": problems, "status": "corrupt"})
        return report

    rules = current_rules()
    derived_manifest = HARDENING._load_json(derived / "derived-manifest.json")
    records = HARDENING._load_json(derived / "messages.json")["messages"]
    families = {item["id"]: item["source_family"] for item in manifest["source_items"]}
    components = []
    for component in sorted(rules):
        recorded: Dict[str, List[str]] = {}
        for record in records:
            value = _record_rules(record)[component]
            if value is not None:
                recorded.setdefault(value, []).append(record["source_id"])
        if component == "engine-rule":
            recorded.setdefault(str(derived_manifest.get("generation")), [])
        stale_ids = sorted(
            source_id for value, ids in recorded.items() if value != rules[component] for source_id in ids
        )
        stale_values = sorted(value for value in recorded if value != rules[component])
        components.append(
            {
                "component": component,
                "current": rules[component],
                "recorded": sorted(recorded),
                "stale": bool(stale_values),
                "stale_source_ids": stale_ids,
            }
        )
    stale = [c["component"] for c in components if c["stale"]]
    report.update(
        {
            "components": components,
            "family_counts": dict(sorted(Counter(families.values()).items())),
            "stale_components": stale,
            "status": "stale" if stale else "current",
        }
    )
    return report


def guarded_find(state_root: Path, query: str) -> Dict[str, Any]:
    """Find only over current derived state; explain staleness instead of mixing."""

    report = check_staleness(state_root)
    if report["status"] != "current":
        detail = report.get("stale_components") or report.get("integrity_problems")
        raise HARDENING.IntegrityError(
            f"derived state is {report['status']} ({', '.join(detail)}); "
            "run rederive and review the rebuild report"
        )
    return P3.find(state_root, query)


def rederive(state_root: Path, output_root: Path) -> Dict[str, Any]:
    """Rebuild derived state from the archive under current rules, beside the state."""

    before = check_staleness(state_root)
    name = before["generation"]
    archive = state_root / "generations" / name / "archive"
    derived = state_root / "generations" / name / "derived"
    if output_root.exists() or output_root.is_symlink():
        raise HARDENING.ScopeError(f"rederive output already exists: {output_root}")
    if output_root.parent.is_symlink() or not output_root.parent.is_dir():
        raise HARDENING.ScopeError("rederive output parent must be an existing non-symlink directory")
    stage = Path(tempfile.mkdtemp(prefix=f".{output_root.name}.mneme-stage-", dir=str(output_root.parent)))
    stage.chmod(0o700)
    try:
        staged = stage / "derived"
        P3.rebuild_derived(archive, staged)
        HARDENING.verify_derived(archive, staged)
        manifest = HARDENING.verify_archive(archive)
        rebuilt = HARDENING.tree_hashes(staged)
        previous = HARDENING.tree_hashes(derived)
        records = HARDENING._load_json(staged / "messages.json")["messages"]
        report = {
            "comparison_with_current": {
                "added": sorted(set(rebuilt) - set(previous)),
                "changed": sorted(p for p in set(rebuilt) & set(previous) if rebuilt[p] != previous[p]),
                "removed": sorted(set(previous) - set(rebuilt)),
                "unchanged_count": sum(1 for p in set(rebuilt) & set(previous) if rebuilt[p] == previous[p]),
            },
            "failures": {r["source_id"]: r["failure"] for r in records if r["status"] == "quarantined"},
            "inputs": {
                "generation": name,
                "source_count": len(manifest["source_items"]),
                "source_manifest_sha256": HARDENING.sha256_path(archive / "manifest.json"),
            },
            "integrity": {"archive_verified": True, "rebuilt_derived_verified": True},
            "outputs": {"derived_tree_sha256": HARDENING.tree_digest(staged), "members": rebuilt},
            "previous_status": before["status"],
            "published_into_state": False,
            "report_version": REPORT_VERSION,
            "rules": current_rules(),
            "skipped": [],
            "status_counts": dict(sorted(Counter(r["status"] for r in records).items())),
        }
        HARDENING._write_json(stage / "REBUILD-REPORT.json", report)
        if output_root.exists() or output_root.is_symlink():
            raise HARDENING.ScopeError(f"rederive output appeared during rebuild: {output_root}")
        os.rename(stage, output_root)
        return report
    except BaseException:
        if stage.exists():
            shutil.rmtree(stage)
        raise


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check").add_argument("--state", type=Path, required=True)
    rederive_parser = commands.add_parser("rederive")
    rederive_parser.add_argument("--state", type=Path, required=True)
    rederive_parser.add_argument("--output", type=Path, required=True)
    find_parser = commands.add_parser("find")
    find_parser.add_argument("--state", type=Path, required=True)
    find_parser.add_argument("--query", required=True)
    arguments = parser.parse_args(argv)
    try:
        if arguments.command == "check":
            result = check_staleness(arguments.state)
        elif arguments.command == "rederive":
            result = rederive(arguments.state, arguments.output)
        else:
            result = guarded_find(arguments.state, arguments.query)
    except HARDENING.ExperimentError as error:
        print(f"STOPPED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    if arguments.command == "check" and result["status"] != "current":
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
