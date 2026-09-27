# Mneme Local Synthetic Prototype 2 — Incremental Ingestion

This increment extends the accepted local prototype (`experiments/mneme-local-prototype-1/`) from a single fixed ingest to repeatable, incremental ingestion with stable message-occurrence identity. It reuses the corrected engine in `experiments/synthetic-hardening-1/` (`hardening.py`, `isolation.py`, `fixtures.py`) unchanged and leaves prototype 1 unchanged.

## Identity convention (`mneme-occurrence-identity-v1`)

- **Source key:** the source-side identity of one occurrence. For this synthetic prototype it is `synthetic-eml:<incoming file name>`. Two occurrences with identical bytes but different keys are distinct occurrences.
- **Source ID:** the archive-assigned identity, `EML-NNN`. IDs are assigned sequentially to new source keys in sorted source-key order within a batch, continuing after the highest existing ID. They are never reused, renumbered, or rewritten. The accepted citation grammar allows three digits, so assignment stops with an error after `EML-999`.
- **Consequence for the reviewed corpus:** a first ingest of the 14 reviewed fixtures assigns `EML-001`…`EML-014` to the same fixtures as before, so the accepted Find results and citations are reproduced exactly.
- The source manifest remains `manifest_version: 1` and passes the accepted engine's `verify_archive`. It adds `identity_convention`, `ingest_batches`, and per-item `source_key` and `ingest_batch` fields, which this prototype verifies strictly.

## Ingest rules

For each incoming batch:

1. Every member must be a regular, non-symlink, non-hard-linked `.eml` file with a supported name and bytes whose SHA-256 is in the reviewed synthetic allowlist (the 14 accepted fixtures plus the three increment fixtures in `increment_fixtures.py`). Anything else stops the operation.
2. A known source key with the same bytes is reported as already preserved and is not re-ingested.
3. A known source key with different bytes stops the whole batch before any staging, parsing, or publication.
4. New source keys receive new source IDs. If nothing is new, the operation is a no-op: nothing is written and the state is byte-identical afterward.

## State layout and publication

```text
<state>/
  CURRENT                      # "generation-NNNN\n"
  generations/
    generation-0001/archive/   # same shape as a prototype-1 state root
    generation-0001/derived/
    generation-0002/...
```

An ingest that adds occurrences:

1. verifies the current generation;
2. stages a complete new generation under `generations/.stage-*`, copying and re-hashing every existing preserved source and writing the new ones;
3. rebuilds all derived state from the staged archive in source-ID order, deriving each source with the logical time of its own ingest batch;
4. verifies the staged archive, derived state, identity extension, and that the new manifest only appends one batch to the previous one;
5. renames the staged directory to the next `generation-NNNN`, then atomically replaces `CURRENT`.

Any failure before `CURRENT` is replaced removes the staged or renamed generation and leaves the previous generation current. A first ingest stages the whole state root as a sibling and publishes it with one rename. Earlier generations are retained. Readers fail closed if they find leftover staging, a non-contiguous generation sequence, or a `CURRENT` that does not name the latest generation.

## Runtime

- Standard library only; no network access.
- Verified here with CPython 3.11.15 and 3.10.20. The accepted prototype-1 evidence used CPython 3.9.6 via `/usr/bin/python3` on macOS. This increment has not yet been run there.

## Commands

All state paths should be disposable paths outside the repository.

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-prototype-2/mneme.py ingest --incoming <synthetic-eml-directory> --state <state-directory> --recorded-at 2026-09-20T12:00:00Z
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-prototype-2/mneme.py verify --state <state-directory>
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-prototype-2/mneme.py rebuild --state <state-directory> --output <new-derived-directory>
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-prototype-2/mneme.py find --state <state-directory> --query "lantern observatory"
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-prototype-2/mneme.py show --state <state-directory> --citation <citation-from-find>
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-prototype-2/tests/test_incremental.py
```

## Boundary

This remains an experiment. It accepts only reviewed, wholly fictional synthetic bytes. It is not a production archive, importer, service, or stack selection, and the identity convention is experimental rather than an accepted architecture decision.
