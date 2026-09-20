# Mneme Local Synthetic Prototype 1 — Results

**Status:** Successful within the declared local, offline, synthetic-only experimental scope; uncommitted and awaiting review.
**Run date:** 2026-09-21.

## Runtime

- `/usr/bin/python3 -B`
- CPython `3.9.6`
- resolved executable SHA-256 `dff595035109e19c43c4b3e73ee08b5f4651e719f25f8b4713f819d28964dc19`
- Python standard library only

## Verification

- five focused prototype tests passed in 11.540 seconds;
- all 22 corrected synthetic-hardening and parser-isolation regression tests passed in 6.993 seconds;
- ingest completed while socket creation was replaced by a failing test double;
- all generated archive, derived, rebuild, and fixture state was confined to disposable temporary roots outside the repository; and
- the demonstration root was removed after evidence collection.

## End-to-end result

The prototype ingested all 14 reviewed synthetic EML occurrences. Each preserved source matched the exact bytes, byte count, and SHA-256 in `experiments/synthetic-hardening-1/fixture-catalog.json`.

| Evidence | Result |
|---|---|
| Source count | `14` |
| Indexed | `6` |
| Indexed with warnings | `4` |
| Quarantined | `4` |
| Source-manifest SHA-256 | `5e2011d276e2bf5252f26ca63a6c714b79c20901c9f60f542f7c7cb93496a889` |
| Derived-tree SHA-256 | `7d6ab2ed9603265007a7cc947ae71e80f3e5771ad86d7ec44561777f588ef7af` |
| Rebuilt-tree SHA-256 | `7d6ab2ed9603265007a7cc947ae71e80f3e5771ad86d7ec44561777f588ef7af` |
| Rebuild comparison | Byte-identical |
| Find query | `lantern observatory` |
| Normalized terms | `lantern`, `observatory` |
| Find result count | `4` (`EML-001`, `EML-005`, `EML-006`, `EML-008`) |
| Selected citation | `mneme-source:EML-001@sha256:befec305981577844c8b233135125394886ffc26d7dedf589bbb152a0d51f208#header:subject:1` |
| Selected display text | `North observatory lantern schedule` |
| Display mode | `escaped-inert-text-no-fetch` |
| Selected source kind | `wholly-fictional-synthetic-fixture` |
| Cleanup | Disposable demonstration root removed |

Every derived message records the corrected `one-source-per-process` isolation marker. Quarantined messages contribute no trusted index occurrences or artifacts.

## Derived-member evidence

| Member | Bytes | SHA-256 |
|---|---:|---|
| `attachments/EML-007/part-2.bin` | 44 | `f728068645229393674b139b9c78d6eb99ca79e7b930d94aa269d2c66f3817f2` |
| `attachments/EML-007/part-3.bin` | 8 | `0cade2034913a1aad284cfda3dc63341b2e5f14323717c8357c39f593e78c44f` |
| `attachments/EML-007/part-4.bin` | 29 | `b560a5c70cbb148bbd2768463a9715d5ad017e5892b1a2717c28ef305dc21cfd` |
| `derived-manifest.json` | 1,270 | `c01d11bf0c9dbb754a8de9d4b7b54d2f5716c709a42289c00ec8352fe3159151` |
| `duplicates.json` | 433 | `2a63201c9cc2cef10cd0eace5449d0fc030f2913cf325a2bc6831ffb50776335` |
| `index.json` | 34,243 | `0961bd45b5ef4cefe573cab596db5d11dd42539f6076250a811bfebafc21a729` |
| `inert-html/EML-008/part-2.txt` | 490 | `769bb3ffef2a1afaa0e731657666770518ce13a4a1eabee4fec355e06bb42f49` |
| `messages.json` | 19,711 | `c8b7c67fa9763dae936eb3378a09b284c130899960146d4e9cb88fcf6e54cfe6` |

## Limitations

- The accepted input is exactly the fixed 14-message synthetic corpus; arbitrary EML collections and incremental imports are not implemented.
- The CLI is synchronous and single-user. Its checked sibling-directory rename is not a multi-process transaction or lock protocol.
- Parser process separation and resource limits remain experimental controls, not a production sandbox or proof of containment after parser compromise.
- Rebuild creates a separately verified derived directory; it does not replace current state automatically.
- Find is deterministic token matching, not ranking, semantic search, conversation reconstruction, or AI Ask.
- There is no product UI, annotation workflow, account integration, provider import, real-data handling, persistent service, network API, deployment, or selected production stack.
