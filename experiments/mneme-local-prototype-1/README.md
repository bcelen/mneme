# Mneme Local Synthetic Prototype 1

This is a small, local product prototype over the corrected synthetic-hardening engine. It gives the accepted 14-message synthetic EML corpus a minimal end-to-end workflow:

1. `ingest` verifies the exact reviewed fixture inventory, preserves every original EML byte-for-byte, writes the SHA-256 source manifest, and builds derived records and the deterministic index;
2. `rebuild` regenerates derived state from the preserved archive into a new directory and requires byte-identical output;
3. `find` runs deterministic token search against verified derived state; and
4. `show` resolves one selected citation against the preserved source and displays only escaped inert text with source hash and provenance.

The prototype reuses `experiments/synthetic-hardening-1/hardening.py` and its corrected one-message-per-process isolation callback. It does not introduce another parser, archive format, index format, dependency, service, or implementation-stack decision.

## Runtime

- Invocation: `/usr/bin/python3 -B`
- CPython: `3.9.6`
- Resolved executable: `/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9`
- Resolved executable SHA-256: `dff595035109e19c43c4b3e73ee08b5f4651e719f25f8b4713f819d28964dc19`
- Standard library only; no network access.

## Commands

All state paths in this example are disposable paths outside the repository.

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B experiments/mneme-local-prototype-1/mneme.py ingest --incoming <synthetic-eml-directory> --state <new-state-directory> --recorded-at 2026-09-20T12:00:00Z
```

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B experiments/mneme-local-prototype-1/mneme.py rebuild --state <state-directory> --output <new-derived-directory>
```

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B experiments/mneme-local-prototype-1/mneme.py find --state <state-directory> --query "lantern observatory"
```

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B experiments/mneme-local-prototype-1/mneme.py show --state <state-directory> --citation <citation-from-find>
```

## Boundary

The input is restricted to the existing wholly fictional fixture inventory and hashes. State creation fails closed on missing, extra, changed, symlinked, or non-regular input. A new state or rebuild is assembled under a private sibling staging directory and published only after verification; a failed operation removes only that newly created staging directory.

This remains an experiment. It is not a production application, production archive, account importer, background service, network API, mobile interface, AI system, or stack selection.
