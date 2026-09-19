# Mneme Synthetic Hardening Experiment 1

This experiment extends the accepted first vertical slice across multiple EML encodings, Unicode and malformed headers, duplicate occurrences, attachments, hostile HTML, controlled parser failures, deterministic rebuild, and plain-directory export/restore.

It remains an experimental implementation. It does not select a product stack and uses no third-party dependency, account, network service, database, container, model, or persistent process.

## Runtime identity recorded before implementation

- Recording date: `2026-09-20`
- Invocation path: `/usr/bin/python3`
- Invocation-path SHA-256: `34129c71a01a74f7f3b2443521519b2e5447553fa187f5fcafaaf8c42cc192e2`
- Runtime-reported executable: `/Applications/Xcode.app/Contents/Developer/usr/bin/python3`
- Resolved CPython binary: `/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9`
- Resolved-binary SHA-256: `dff595035109e19c43c4b3e73ee08b5f4651e719f25f8b4713f819d28964dc19`
- Runtime: `CPython 3.9.6`, built with `Clang 21.0.0 (clang-2100.3.34.2)`
- Platform: `macOS-27.0-arm64-arm-64bit`, little-endian

## Reviewed artifacts

- `fixtures.py`: exact synthetic EML byte definitions.
- `fixture-catalog.json`: fixture identities, hashes, intended coverage, and expected outcomes.
- `hardening.py`: preservation, derivation, duplicate classification, Find, source display, export, and restore.
- `tests/test_hardening.py`: focused standard-library test suite.

Fixture EML files, archives, indexes, attachment derivatives, HTML derivatives, exports, and restores are materialized only beneath a fresh temporary workspace. Python bytecode is disabled for reviewed runs.

## Reviewed commands

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B -m unittest discover -s experiments/synthetic-hardening-1/tests -v
```

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B experiments/synthetic-hardening-1/hardening.py run --workspace <fresh-temporary-directory> --recorded-at 2026-09-20T00:00:00Z --query "lantern observatory"
```

The complete run emits JSON evidence. The temporary workspace is disposable and is not part of the repository.
