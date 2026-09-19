# First Synthetic Mneme Vertical Slice: Results

**Status:** Accepted
**Execution date:** 2026-09-20
**Review date:** 2026-09-20
**Approved proposal commit:** `370bd8a8dad1c25523bdf62adce0b99ee1c4ef6e`
**Implementation status:** Accepted experimental implementation committed with this record; no stack selection or follow-on work is implied.

## Result

The approved synthetic path completed successfully:

`synthetic EML -> byte-preserved source plus SHA-256 manifest -> derived metadata/index -> deterministic Find -> cited inert source display`

The optional Ask stub was not needed and was not implemented.

## Runtime identity

- Invocation: `/usr/bin/python3 -B`
- Invocation-path SHA-256: `34129c71a01a74f7f3b2443521519b2e5447553fa187f5fcafaaf8c42cc192e2`
- Runtime-reported executable: `/Applications/Xcode.app/Contents/Developer/usr/bin/python3`
- Resolved CPython binary: `/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9`
- Resolved-binary SHA-256: `dff595035109e19c43c4b3e73ee08b5f4651e719f25f8b4713f819d28964dc19`
- Runtime: `CPython 3.9.6`, built with `Clang 21.0.0 (clang-2100.3.34.2)`
- Platform: `macOS-27.0-arm64-arm-64bit`, little-endian
- Dependencies: Python standard library only

## Reviewed repository artifacts

| Path | Bytes | SHA-256 |
|---|---:|---|
| `experiments/vertical-slice-1/README.md` | 2,484 | `ffdec1bffb3dd7e947c42cbbcdcf014fb2cde3e9ae12f9d4fd85887c1c8fcb18` |
| `experiments/vertical-slice-1/fixtures/meridian-observatory.eml` | 464 | `508c2211ad8e9ad40c0b31fc665244774970b973f90e1d426ab6137cb3909c69` |
| `experiments/vertical-slice-1/mneme_slice.py` | 19,479 | `6320c5564a6eae5a8f8411c8da9e5470cdd63ae58723adafd254118b481bc582` |
| `experiments/vertical-slice-1/tests/test_vertical_slice.py` | 7,088 | `9ba12c3c841901164c9bc329d038dfb0e90f83f42c4ed9d3f4ad3b8a4c994651` |

The EML fixture is wholly fictional, inert, plain text, and uses reserved `.test` addresses.

## Focused tests

Command:

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B -m unittest discover -s experiments/vertical-slice-1/tests -v
```

Result: seven tests passed in 0.055 seconds.

The tests cover byte equality, independent digest and size checks, source immutability during derivation, same-size byte tampering, size mismatch, missing source membership, manifest hash mismatch, deterministic Find, empty results without fabricated citations, complete derived-state deletion and deterministic rebuild, citation resolution, inert source display, and execution with socket creation blocked.

## End-to-end evidence

The reviewed run used a fresh owner-only directory under `/tmp`, a fixed synthetic provenance time, and the query `observatory lantern`. The preserved source compared byte-for-byte equal to the fixture using `/usr/bin/cmp` with exit status zero.

| Temporary artifact | Bytes | SHA-256 |
|---|---:|---|
| Complete JSON result | 3,328 | `eaf5aae285e2069e8b0de29aa91fcce1815dad283e1d77f4ef899551d5087251` |
| Archive manifest | 925 | `147a9d2f3a01c54318676aeaae7d1b47ac41e0bae51c8c575054f0a1a0461e81` |
| Preserved EML | 464 | `508c2211ad8e9ad40c0b31fc665244774970b973f90e1d426ab6137cb3909c69` |
| Derived record | 1,649 | `cd4070632d25a339970aed2d5c614704b1ae1be194f7e736da3648ed0cc9d9b7` |
| Derived index | 7,871 | `9b6f19038bd458a3366626aaade0610a4fd189c2119d4cd031464713f202e5cb` |

Find returned one result with three citations. The first citation was:

```text
mneme-source:src-sha256-508c2211ad8e9ad40c0b31fc@sha256:508c2211ad8e9ad40c0b31fc665244774970b973f90e1d426ab6137cb3909c69#L5-L5
```

It resolved to an inert display of `Subject: Meridian observatory lantern schedule` with the source ID, source digest, and preservation provenance attached.

The temporary root, workspace, archive, source-items directory, and derived directory were owner-only. The manifest and preserved source were mode `0400`; derived files were mode `0600`. The complete temporary root was removed after evidence capture, and its absence was verified. No Python bytecode or generated runtime state remains in the repository.

## Boundaries and limitations

No network, account, cloud AI, model, container, database, persistent service, real correspondence, handoff automation, route screening, or checksum-planner work was used. The accepted commit contains only the five reviewed slice files, and nothing was pushed.

This result is narrow evidence for one UTF-8, non-multipart, plain-text EML. It does not cover attachments, HTML, hostile content, multiple messages, provider exports, mobile UX, production storage, deployment, or implementation-stack selection. The six previously pending documents were not modified or included.
