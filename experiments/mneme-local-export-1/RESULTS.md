# Mneme Local Export 1 — Results

**Status:** Successful within the declared local, offline, synthetic-only experimental scope; committed on a feature branch, awaiting review.
**Run date:** 2026-10-05.

## Runtime

- Linux container: CPython 3.11.15 and 3.10.20. Not yet run on the accepted macOS CPython 3.9.6 runtime.
- Python standard library only; no network access.

## Verification

`tests/test_export.py`: 13 tests pass. They cover layout and self-description; independent `SHA256SUMS` verification of every file; byte-for-byte container reconstruction; repeatable, read-only export; restore with identical state, Find, citations, and rebuild; identical continued ingestion after restore; a failed export publishing nothing; rejection of changed, missing, and extra files by name; a tampered checksum file; a container edit with consistently rewritten hashes; `current`, `stale`, and `diverged` classification; refusal to export an interrupted state; and the CLI.

Six deliberate mutations were each caught and reverted: tolerating extra files, skipping the `SHA256SUMS` check, skipping cleanup after a failed export, reporting a stale export as current, exporting a state with leftovers, and skipping the container-to-segment comparison. The last one initially survived, because any container change also fails the per-file hash; a test that edits a container and rewrites every hash consistently was added and now catches it.

## CLI evidence

State: the 14 accepted EML fixtures, then the three increment EML fixtures with `MBOX-001`, then `MBOX-004`, then `MBOX-002`. Result: `generation-0004`, 30 sources, source manifest `d45c73114e0c6685da3f3134eea04a246cbc467708135eabd3fb115e04e049f8`, derived tree `33931fcc40f799a5291f56df12d44d1549cfe26f3756998f45c3afa73042cbc2`.

| Step | Result |
|---|---|
| Export | 139 files; `SHA256SUMS` SHA-256 `2592632efc6343a31f0c4c5881d47fbb23bc311c0e742b05f0bde4e5260b76aa`; containers `obs-0001-observatory-inbox.mbox`, `obs-0002-damaged.mbox`, `obs-0003-observatory-inbox.mbox` |
| Second export | byte-identical to the first (`diff -r`) |
| `sha256sum -c SHA256SUMS` (system tool, no Mneme) | all 139 files OK |
| Restore | four generations; restored state byte-identical to the original (`diff -r`) |
| Delete one container, then verify | exit 2: `export is incomplete or altered; missing=['containers/obs-0002-damaged.mbox'], extra=[], changed=[]` |

## Limitations

- The export's hashes are self-asserted. Someone who rewrites the preserved bytes, the source manifest, the derived state, and every hash consistently produces an export that verifies. Tamper evidence needs an external anchor: record the `SHA256SUMS` digest returned by `export` somewhere else.
- Every generation is a full copy, so the export grows with the number of generations.
- No encryption, compression, retention, or backup scheduling, and no recovery of secrets (PRES-021–027 remain open).
- File modes are copied but not verified; only bytes and paths are.
- Only prototype-3 states are supported; prototype-1 and prototype-2 states keep their own formats.
