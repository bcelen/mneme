# Synthetic Hardening Experiment: Results

**Status:** Accepted
**Execution date:** 2026-09-20
**Review date:** 2026-09-20
**Approved proposal commit:** `e56d6d235f4b2078b9c3f92e2be5e8e55bbd28e0`
**Implementation status:** Accepted experimental implementation committed with this record; no production-stack or follow-on decision is implied.

## Result

The approved local, offline, synthetic-only experiment completed successfully using the Python standard library. It preserved and processed fourteen fixed EML occurrences covering line-ending and transfer-encoding variants, Unicode and malformed headers, duplicate messages, attachments, hostile HTML, malformed MIME, controlled parser failure, deterministic rebuild, citations, and plain-directory export/restore.

Final outcome counts were:

- `indexed`: 6
- `indexed_with_warnings`: 4
- `quarantined`: 4

All fourteen source occurrences remained in the preserved archive regardless of processing outcome.

## Runtime identity

- Invocation: `/usr/bin/python3 -B`
- Invocation-path SHA-256: `34129c71a01a74f7f3b2443521519b2e5447553fa187f5fcafaaf8c42cc192e2`
- Runtime-reported executable: `/Applications/Xcode.app/Contents/Developer/usr/bin/python3`
- Resolved CPython binary: `/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9`
- Resolved-binary SHA-256: `dff595035109e19c43c4b3e73ee08b5f4651e719f25f8b4713f819d28964dc19`
- Runtime: `CPython 3.9.6`, built with `Clang 21.0.0 (clang-2100.3.34.2)`
- Platform: `macOS-27.0-arm64-arm-64bit`, little-endian
- Dependencies: Python standard library only

## Fixture inventory and source hashes

| ID | Bytes | SHA-256 | Outcome | Primary coverage |
|---|---:|---|---|---|
| `EML-001` | 351 | `befec305981577844c8b233135125394886ffc26d7dedf589bbb152a0d51f208` | indexed | LF, 7bit |
| `EML-002` | 365 | `82a6bba4ab0b7cb5c29b8db4ec6c755d0e6f5694e4ab7a3f4f28ba5298e0f23a` | indexed | CRLF, 8bit, Unicode |
| `EML-003` | 422 | `855df1de395bcda3f1b49f7951573b85d5462ab5643240732c76e69301c995a7` | indexed | quoted-printable, folded encoded words |
| `EML-004` | 352 | `7afcd03a25c0ca3b6af942916f7179ea6d8b246173739ebb5b3ef620220da121` | indexed | base64 body |
| `EML-005` | 351 | `befec305981577844c8b233135125394886ffc26d7dedf589bbb152a0d51f208` | indexed | exact duplicate occurrence |
| `EML-006` | 366 | `b6fe2178d33445a52b8b4f09fcc5c65483876df6a1ef2c5c8eb8e57b3b75bda2` | indexed | same message ID, different bytes |
| `EML-007` | 938 | `78e93f0ac3c122e9ad38c3f74ff89bb25704ec531deebdd44c83d3c92c07bbd0` | indexed with warnings | attachments and hostile filenames |
| `EML-008` | 851 | `5858ca7dcc5ad2b5eb7b13a4785c483f8a7d88115eff67aa357154244ebb3726` | indexed with warnings | active HTML and remote references |
| `EML-009` | 360 | `2027ede28398f83f6381418717cf186532d2d81425ac4af3461ae964e12cae1a` | indexed with warnings | malformed and repeated headers |
| `EML-010` | 342 | `79f58a4ca1dd972a93717074b41c8952f4ea929aaeecded0b7201c7ccd8f55f2` | quarantined | unclosed MIME boundary |
| `EML-011` | 370 | `5ec3b1c6783e095a33144bd9dc4aeb6885e61a7a674f0b4bf3ee0536d105039f` | quarantined | controlled parser fault injection |
| `EML-012` | 347 | `4c98f370962a9d85b667be9d9ec084e5ad5f5775ba54840cdcb5ad61f938d299` | indexed with warnings | unknown charset fallback |
| `EML-013` | 666 | `0aa7ed1418d120e07021cd7a763f1ca5710770f6791c88c534e36fd9ae2531ea` | quarantined | MIME nesting beyond limit |
| `EML-014` | 312 | `12a994c79683eea8db343d6254d50b17ced5ece971a8acf48a828a80a9e7211f` | quarantined | invalid base64 transfer encoding |

All fourteen materialized fixture files compared byte-for-byte equal to their preserved source occurrences. The source manifest was 8,772 bytes with SHA-256 `1c5723cb9d1392eb9267ba903337f84e510e1e082d4fb112447877a0201661f0`.

## Derived-state hashes and rebuild evidence

| Derived member | Bytes | SHA-256 |
|---|---:|---|
| `attachments/EML-007/part-2.bin` | 44 | `f728068645229393674b139b9c78d6eb99ca79e7b930d94aa269d2c66f3817f2` |
| `attachments/EML-007/part-3.bin` | 8 | `0cade2034913a1aad284cfda3dc63341b2e5f14323717c8357c39f593e78c44f` |
| `attachments/EML-007/part-4.bin` | 29 | `b560a5c70cbb148bbd2768463a9715d5ad017e5892b1a2717c28ef305dc21cfd` |
| `derived-manifest.json` | 1,270 | `3a3ef52fa0770218d2d3e9cc4880231ef016b215944882c8ad2d23d91792051c` |
| `duplicates.json` | 433 | `dcc681bf6c4ab269d8d62c0e08bc916072fe3972c83802a91b814d359352bbed` |
| `index.json` | 34,243 | `969c4e3f8fcdb0167eca0429e76a0e50b0b684f0c30c2d4a91f49ca2cc526985` |
| `inert-html/EML-008/part-2.txt` | 490 | `769bb3ffef2a1afaa0e731657666770518ce13a4a1eabee4fec355e06bb42f49` |
| `messages.json` | 16,393 | `83873f229a74b348b95ea542f4cb1c884163c6420b817165315e68c1741905cf` |

The canonical derived-tree SHA-256 was `565e08c9cb5b743ce3aea62ba12706ee7c00823c7dff093e4bfde1e16dd1b106`. Two independent clean builds from the same preserved archive produced identical member sets, byte counts, hashes, Find ordering, and citations.

Exact duplicate classification retained `EML-001` and `EML-005`. Message-ID duplicate classification retained `EML-001`, `EML-005`, and `EML-006`. No source occurrence was collapsed or deleted.

## Find, citation, and hostile-content evidence

The deterministic query `lantern observatory` returned four source occurrences. Its first citation was:

```text
mneme-source:EML-001@sha256:befec305981577844c8b233135125394886ffc26d7dedf589bbb152a0d51f208#header:subject:1
```

The citation resolved to source `EML-001`, its source digest and preservation provenance using display mode `escaped-inert-text-no-fetch`.

The hostile HTML fixture was stored only as escaped inert text. Script markup was escaped, reserved remote URLs remained nonactive text, and the end-to-end build passed while socket creation was replaced with a failing test double. This proves absence of network use through the tested Python socket interface, not operating-system-level network isolation or browser-renderer safety.

Three attachment payloads were written only to generated part-ID paths beneath the temporary derived root. Original filenames never became write paths. Path-like names, duplicate normalized names, and content-type/extension disagreement produced the declared warnings. Attachment bytes were never executed.

## Failure behavior

- An unclosed MIME boundary was quarantined on a fatal parser defect.
- The controlled parser fault was quarantined while unrelated fixtures completed.
- MIME depth six was quarantined against the configured depth-four limit.
- Invalid base64 was quarantined before trusted derived state was created.
- Quarantined source IDs appeared in no trusted index occurrence and created no attachment or HTML artifact.
- Changed, missing, and extra export members were each rejected by deterministic tests.

During implementation, the malformed-date fixture exposed an exception in Python's structured date-header accessor, and the Unicode fixture exposed surrogate-escaped raw header bytes. The implementation was changed to derive headers defensively from preserved raw values when structured parsing fails. Fixture bytes and expected hashes were not changed. The final suite passed after these corrections.

## Tests

Command:

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B -m unittest discover -s experiments/synthetic-hardening-1/tests -v
```

Result: thirteen tests passed in 0.686 seconds. They cover catalog/hash reconciliation, byte preservation, declared parse outcomes, transfer encodings and Unicode, duplicates, safe attachment paths, inert HTML with socket blocking, quarantine isolation, deterministic rebuild and citations, complete export/restore/rebuild, and changed/missing/extra export-member rejection.

## Export, restore, and cleanup

The plain-directory export contained 24 independently hashed members. Its 3,809-byte export manifest had SHA-256 `6d9b27e47d5529c1186b581504d73c45ece03ecde252593add8cdc3f2d0e2480`.

A clean restore reproduced the complete preserved archive and deterministic derived state. Restored Find output and citations matched the originals. Deleting the restored derived state and rebuilding it from the restored source produced the same eight derived members and hashes.

The final captured JSON result was 7,777 bytes with SHA-256 `adb21c57f6f0c04941421cf9fee617cddb69ef2473a250c97608ac2806a0686a`. The owner-only temporary root contained 93 files and 30 directories during the complete run. It was removed after evidence capture, and its absence was verified. No Python bytecode or generated experiment state remains in the repository.

## Reviewed repository artifacts

| Path | Bytes | SHA-256 |
|---|---:|---|
| `experiments/synthetic-hardening-1/README.md` | 2,197 | `6d551966a9f2c7d5862415b49da5a0e4f9461f84735d3b86479a3a7e9c2ecad3` |
| `experiments/synthetic-hardening-1/fixtures.py` | 13,647 | `54fe9273dcdba9215842cbe787e8ef3fb4873e38c00a5503d7c1e6d32caad500` |
| `experiments/synthetic-hardening-1/fixture-catalog.json` | 4,891 | `3cc47fc9ea6301a57f482e02a3c79e1b9cc0133fcc261953624b9092409b5ef3` |
| `experiments/synthetic-hardening-1/hardening.py` | 36,618 | `1ee69509a135c1fdaa6eb228301353c62448ff139eead1166e4e0b71c3e31a19` |
| `experiments/synthetic-hardening-1/tests/test_hardening.py` | 11,245 | `e26bb95d7502f06ed829a6026fcb8c4dadaaa30aea13e0fa1a6fc39aaca3efec` |

## Limitations

This result is limited to fourteen small synthetic EML occurrences and the tested standard-library parser behavior. It does not establish parser process isolation, operating-system network denial, CPU or memory timeouts, decompression limits, browser rendering, safe opening of attachments, malware detection, encryption, backup custody, versioned migration, provider exports, MBOX, Eudora, Gmail/Workspace, Outlook, production scale, mobile UX, AI behavior, deployment, or a production stack.

No account, network access, real correspondence, cloud AI, external dependency, container, database, persistent service, handoff automation, or production configuration was used. The accepted commit contains only the six reviewed hardening files, and nothing was pushed.
