# Mneme Local Synthetic Prototype 4 — Results

**Status:** Successful within the declared local, offline, synthetic-only experimental scope; committed locally on a feature branch, not pushed, awaiting review.
**Run date:** 2026-09-29.

## Runtime

- Linux container: CPython 3.11.15 (`/usr/bin/python3.11`, SHA-256 `f56a588548dd013906ae1dcd1b6faa417f4e204da634ff354840d9643e78ff9e`) for the evidence run and all suites; CPython 3.10.20 for a second run of the new suite.
- Not yet run on the accepted macOS CPython 3.9.6 runtime.
- Python standard library only; no network access.

## Verification

| Suite | Result |
|---|---|
| `mneme-local-prototype-4/tests/test_filters.py` | 14 passed (3.11: 9.3 s; 3.10: 9.1 s) |
| `mneme-local-prototype-3/tests/test_mbox.py` | 22 passed, unchanged |
| `mneme-local-prototype-2/tests/test_incremental.py` | 16 passed, unchanged |
| `mneme-local-prototype-1/tests/test_mneme.py` | 5 passed, unchanged |
| `synthetic-hardening-1/tests/test_hardening.py` | 16 passed, unchanged |
| `synthetic-hardening-1/tests/test_isolation.py` | 6 passed, unchanged |
| `vertical-slice-1/tests/test_vertical_slice.py` | 10 passed, unchanged |
| `tools/handoff/t/handoff.t`, Go planner | Not run; still outstanding, as recorded in prototype 3's results |

Seven deliberate code mutations were each caught and then reverted: ignoring the UTC offset; placing undated occurrences in date ranges; case-sensitive addresses; ignoring the attachment filter; decorating unfiltered output; listing quarantined occurrences; and an exclusive `until` bound.

| Requirement | Tests |
|---|---|
| Unfiltered Find unchanged | `test_unfiltered_find_is_prototype_3_find_unchanged` (API and CLI byte output) |
| Order and citation stability | `test_filtered_results_keep_order_and_citations`, `test_filter_only_listing_cites_subjects_that_resolve` |
| Each filter | `test_family_and_mailbox`, `test_attachment_filters_partition_the_candidates`, `test_status_filter_and_quarantine_exclusion`, `test_address_filters_are_case_insensitive_and_ignore_display_names`, `test_date_range_is_inclusive_in_utc_and_reports_undated_candidates` |
| Date and address normalization | `test_dates_are_normalized_to_utc_without_guessing`, `test_addresses_ignore_display_names_and_case` |
| Combinations and inspectability | `test_combined_filters_report_each_step` |
| Read-only, deterministic | `test_find_is_read_only_and_repeatable` |
| Validation before any state read | `test_invalid_filters_stop_before_reading_state`, `test_cli_filters_and_delegation` |

## CLI evidence

State: the 14 accepted EML fixtures (2026-09-20T12:00:00Z), then the three prototype-2 increment EML fixtures with `MBOX-001` (2026-09-28T09:00:00Z), then `MBOX-004` (2026-09-28T11:00:00Z). Result: `generation-0003`, 29 occurrences, source manifest `f45a77c1d1adb48d50f5272ba33fe70ef0bd3de21dd900a1a602483fbc7e4fd6`, derived tree `611eb37abf3f18fdec97e89c627f0943665c8f6066c13599aa1b03d1691d87cf`.

| Query and filters | Results | Report | Output SHA-256 |
|---|---|---|---|
| `lantern observatory`, no filters | nine occurrences; byte-identical to prototype 3 | none | `6b26b3137eba28daad72462049f4c8fde4e195e27f8be33e96e74e111870a470` |
| `lantern observatory`, `--family mbox` | `EML-018`, `EML-021`, `EML-022` | 9 candidates; family removed 6 | `ea31703ffcf08d6902b1a41d948f726bd7504ede61538a78be0dac387b6b1e3c` |
| `lantern observatory`, `--participant arin.vale@example.test`, 2025-10-14 | `EML-001`, `EML-005`, `EML-006`, `EML-016` | 9 candidates; participant removed 2, date removed 3 | `09db95ffde34617e1713b96c71e7b89bcf278f6a03fb387d64509487fc7d20ab` |
| `--has-attachment` | `EML-007`, `EML-019` | 19 candidates; attachment removed 17 | `a5e5226434eb2626327ff6523e02ea154be0175ceb91c6436eb36df824d875ab` |
| `--since 2025-10-15 --until 2025-10-15` | `EML-002` (18:45 +0300 = 15:45 UTC) | 19 candidates; date removed 18; undated `EML-009` | `33efa6050b52a72ad17e07f92c522c6ce69cb19772813d2e1eee5a5019f1f0d6` |
| `--mailbox damaged.mbox` | `EML-024` (the survivor record) | 19 candidates; mailbox removed 18 | `3cdec214626601c557fb1cb1306b5094f14b35d9fd270d246c05597f2e35d936` |
| `--since 2025-10-20 --until 2025-10-19` | exit 2: `since must not be later than until` | | |

A digest over every state file was identical before and after all of these Find calls.

## Limitations

- Only `From`, `To`, and `Date` are available, because the accepted engine derives only those headers. `Cc`, `Bcc`, `Reply-To`, and `Sender` cannot be filtered without a new, reviewed derivation rule.
- Address matching is exact on the address spec. There is no alias, identity, or person resolution, and no subaddress or domain matching.
- Date filtering uses the message's `Date` header, not a delivery or archive time, and whole UTC days only. Local-day filtering is not offered.
- Filters are recomputed from `messages.json` on every call, which is linear in the archive and fine only at synthetic scale.
- A filter-only listing cites the subject header; an occurrence without an indexed subject is listed without a citation.
- No ranking, fuzzy matching, pagination, saved searches, or UI.
