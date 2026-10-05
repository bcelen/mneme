# Mneme Local Staleness 1 — Stale Derived State Detection and Rebuild Report

Prototype 3 already refuses derived state produced under another rule, but only with a generic integrity error. This experiment explains staleness (AT-L04, PRES-032) and produces a rebuild report (PRES-033). Prototype 3 is loaded by path and left unchanged.

## Rule identities compared

| Component | Current value comes from | Recorded value comes from |
|---|---|---|
| `engine-rule` | `hardening.PROCESSING_RULE` | each record's derivation provenance, and the derived manifest |
| `engine-tool` | `hardening.TOOL_NAME` / `TOOL_VERSION` | each record's derivation provenance |
| `isolation-profile` | the isolation marker (mode, start method, limits) | each record parsed in an isolated worker |
| `mbox-rule` | `mboxrd.MBOX_RULE` | each MBOX record |

## Operations

- `check` classifies the current generation's derived state:
  - `corrupt` if derived bytes disagree with the derived manifest or the manifest is bound to another archive (rule identities are not trusted then);
  - `stale` if any recorded identity differs from the current one, listing each stale component and exactly which source IDs carry the old value;
  - `current` otherwise.
  Exit codes: 0 current, 3 stale or corrupt, 2 error.
- `find` runs Find only over `current` derived state and otherwise stops with the stale or corrupt components named.
- `rederive` rebuilds derived state from the archive under the current rules into a new directory, verifies it, and writes `REBUILD-REPORT.json`: inputs, rule identities, outputs and member hashes, per-source failures, skips, integrity results, and which derived members changed relative to the current state. It never modifies the state.

## Why rederive does not publish

Prototype 3 requires every new generation to append exactly one ingest batch. A generation that changes only derived state would fail that chain verification. Publishing re-derived state needs a reviewed change to the generation convention, so this experiment stops at a verified side rebuild.

## Commands

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-staleness-1/mneme_staleness.py check --state <state>
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-staleness-1/mneme_staleness.py find --state <state> --query "lantern observatory"
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-staleness-1/mneme_staleness.py rederive --state <state> --output <new dir>
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-staleness-1/tests/test_staleness.py
```
