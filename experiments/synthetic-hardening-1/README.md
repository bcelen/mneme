# Mneme Synthetic Hardening Experiment 1

This experiment extends the accepted first vertical slice across multiple EML encodings, Unicode and malformed headers, duplicate occurrences, attachments, hostile HTML, controlled parser failures, deterministic rebuild, and plain-directory export/restore.

The follow-on isolation harness runs each parser invocation in a fresh child process connected by a standard-library pipe. It applies a wall-clock timeout, POSIX CPU/file-size/core-dump/file-descriptor limits, and a parent-enforced resident-memory ceiling; `RLIMIT_DATA` applies the same memory ceiling where the host supports it. Oversized inputs fail before launch; time, memory, parser, and MIME-depth failures become deterministic quarantine records with no trusted index entries or derived artifacts. The harness uses a private temporary working directory per invocation and removes it after collecting the result.

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
- `isolation.py`: direct child-process parser protocol, resource limits, quarantine mapping, and cleanup evidence.
- `tests/test_hardening.py`: focused standard-library test suite.
- `tests/test_isolation.py`: hostile/oversized input, time/memory limit, quarantine, cleanup, and rebuild tests.

Fixture EML files, archives, indexes, attachment derivatives, HTML derivatives, exports, and restores are materialized only beneath a fresh temporary workspace. Python bytecode is disabled for reviewed runs.

## Reviewed commands

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B -m unittest discover -s experiments/synthetic-hardening-1/tests -v
```

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B experiments/synthetic-hardening-1/hardening.py run --workspace <fresh-temporary-directory> --recorded-at 2026-09-20T00:00:00Z --query "lantern observatory"
```

The complete run emits JSON evidence. The temporary workspace is disposable and is not part of the repository.

The focused isolation tests use the same runtime and no additional dependency:

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B -m unittest discover -s experiments/synthetic-hardening-1/tests -p 'test_isolation.py' -v
```

The memory experiment proves enforcement of the configured resident-memory ceiling on the recorded macOS runtime. Other platforms must independently validate their resident-memory observation or `RLIMIT_DATA` behavior. The process boundary is experimental and does not claim a complete production sandbox.

## Accepted follow-on result

- Status: Accepted within the declared local, offline, synthetic-only scope.
- Review date: `2026-09-20`.
- Five focused parser-isolation tests passed.
- Eighteen complete hardening tests passed, comprising the thirteen earlier hardening tests and the five isolation tests.
- Hostile input ran in a distinct parser process and was quarantined without trusted index entries or artifacts.
- Input above the 128 KiB source limit was rejected before a parser worker was created.
- CPU time, wall time, and a 64 MiB memory ceiling were enforced; limit failures were quarantined.
- Two complete isolated builds produced identical derived files and hashes.
- Every per-message temporary root was removed, and no bytecode or generated experiment state remained in the repository.
- macOS rejected a finite `RLIMIT_DATA` value for the recorded Python runtime, so the parent enforced the memory ceiling by observing and terminating on resident memory. `RLIMIT_DATA` remains an additional control where supported.

This result does not establish a production sandbox, choose a stack, or authorize production implementation. The next product decision is the smallest useful Mneme prototype expansion.
