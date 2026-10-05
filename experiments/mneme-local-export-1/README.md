# Mneme Local Export 1 — Export, Verification, and Restore

This experiment gives the generation-based state of `experiments/mneme-local-prototype-3/` an application-independent export and a verified restore. The accepted export in `synthetic-hardening-1` covers only a single archive and derived directory; it cannot carry generations, container observations, or the `CURRENT` pointer. Prototype 3 is loaded by path and left unchanged.

## Export layout

```text
<export>/
  README.txt             how to read and verify the export without Mneme
  SHA256SUMS             every file except itself and the manifest, in `sha256sum -c` format
  EXPORT-MANIFEST.json   format, generations, current source-manifest and derived hashes, per-file hashes
  state/                 exact copy of the state: CURRENT and every published generation
  containers/            each observed mbox container of the current generation, reassembled from its segments
```

- Every published generation is exported, so the append-only history and its verification survive.
- The export contains no timestamps; exporting the same state twice produces identical bytes.
- Reconstructed containers are ordinary `.mbox` files, readable by any mbox client.

## Rules

- **Export** verifies the whole state chain first and refuses a state with unpublished leftovers. It stages beside the target and publishes by rename only after verifying the staged export, so a failure leaves nothing.
- **Verify** names every missing, extra, and changed file; checks `SHA256SUMS` against the manifest; re-verifies the exported state chain; and checks every container against its preserved segments. With `--against-state`, it classifies the export as `current`, `stale` (an earlier point of the same append-only history), or `diverged`.
- **Restore** verifies the export, copies its state into a staged directory, verifies the restored chain, requires its file hashes to equal the exported ones, and publishes by rename.

## Commands

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-export-1/mneme_export.py export --state <state> --output <new export dir>
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-export-1/mneme_export.py verify-export --export <export> [--against-state <state>]
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-export-1/mneme_export.py restore --export <export> --output <new state dir>
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-export-1/tests/test_export.py
cd <export> && sha256sum -c SHA256SUMS      # macOS: shasum -a 256 -c SHA256SUMS
```

## Boundary

Local, offline, synthetic-only, standard library only. This is an export format experiment, not a backup system: no encryption, retention, scheduling, off-site copy, or key recovery.
