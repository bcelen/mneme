# Mneme Synthetic Vertical Slice 1

This experiment implements one local, offline path:

`synthetic EML -> preserved bytes and SHA-256 manifest -> derived metadata/index -> deterministic Find -> cited source display`

It is an experimental implementation, not a product-stack selection. It uses no third-party dependencies, network service, database, container, account, model, or persistent process.

## Runtime identity recorded before implementation

- Recording date: `2026-09-20`
- Invocation path: `/usr/bin/python3`
- Invocation-path SHA-256: `34129c71a01a74f7f3b2443521519b2e5447553fa187f5fcafaaf8c42cc192e2`
- Runtime-reported executable: `/Applications/Xcode.app/Contents/Developer/usr/bin/python3`
- Resolved CPython binary: `/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9`
- Resolved-binary SHA-256: `dff595035109e19c43c4b3e73ee08b5f4651e719f25f8b4713f819d28964dc19`
- Implementation: `CPython 3.9.6`
- Build: `3.9.6 (default, Aug 25 2026, 21:26:21) [Clang 21.0.0 (clang-2100.3.34.2)]`
- Platform: `macOS-27.0-arm64-arm-64bit`
- Byte order: `little`

## Files

- `fixtures/meridian-observatory.eml`: wholly fictional, inert, 464-byte plain-text EML input; SHA-256 `508c2211ad8e9ad40c0b31fc665244774970b973f90e1d426ab6137cb3909c69`.
- `mneme_slice.py`: preservation, verification, derivation, Find, citation, and source-display implementation.
- `tests/test_vertical_slice.py`: focused standard-library tests.

All runtime state is written beneath an explicitly supplied temporary workspace. Tests use fresh temporary directories and remove them automatically. Python bytecode generation is disabled during the reviewed commands so no generated state is written into the repository.

## Reviewed commands

Run the focused tests:

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B -m unittest discover -s experiments/vertical-slice-1/tests -v
```

Run the complete slice in a fresh temporary workspace:

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B experiments/vertical-slice-1/mneme_slice.py run --fixture experiments/vertical-slice-1/fixtures/meridian-observatory.eml --workspace <fresh-temporary-directory> --query "observatory lantern" --recorded-at 2026-09-20T00:00:00Z
```

The second command emits JSON containing the manifest summary, derived-state hashes, deterministic Find result, citation, and inert source display. The temporary workspace is disposable and is not part of the repository.
