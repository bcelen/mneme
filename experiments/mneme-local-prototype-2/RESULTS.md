# Mneme Local Synthetic Prototype 2 — Results

**Status:** Successful within the declared local, offline, synthetic-only experimental scope; uncommitted and awaiting review.
**Run date:** 2026-09-27.

## Runtime

- Linux container: CPython 3.11.15 (`python3`) for the evidence run and all suites; CPython 3.10.20 for a second run of the new suite.
- macOS (2026-09-28): the new suite passed on the accepted runtime, CPython 3.9.6 via `/usr/bin/python3 -B`. The resolved-executable SHA-256 was not re-checked in that run, and the CLI evidence run and hashes below come from the Linux container.
- Python standard library only; no network access. Socket creation is replaced by a failing test double during ingest tests.

## Verification

| Suite | Result |
|---|---|
| `mneme-local-prototype-2/tests/test_incremental.py` | 16 passed (macOS 3.9.6: 91.3 s; 3.11: 58.4 s; 3.10: 57.9 s) |
| `mneme-local-prototype-1/tests/test_mneme.py` | 5 passed, unchanged |
| `synthetic-hardening-1/tests/test_hardening.py` | 16 passed, unchanged |
| `synthetic-hardening-1/tests/test_isolation.py` | 6 passed, unchanged |
| `vertical-slice-1/tests/test_vertical_slice.py` | 10 passed, unchanged |

Five deliberate code mutations were each caught by the corresponding new test and then reverted: disabling the changed-bytes check, treating known keys as new, skipping rollback of a renamed generation, deriving with the batch time instead of each source's own batch time, and restarting ID numbering per batch.

Before any change, the accepted prototype-1 evidence reproduced exactly in this environment: source manifest `5e2011d2…a496a889` and derived tree `7d6ab2ed…588ef7af`.

## Coverage of the increment

| Requirement | Test |
|---|---|
| Immutable archive-assigned source IDs | `test_first_ingest_assigns_immutable_ids_in_source_key_order`, `test_incremental_batch_appends_without_rewriting_existing_identity`, `test_source_ids_stop_at_the_citation_compatible_limit` |
| Stable synthetic source keys | same, plus `test_full_rebuild_is_deterministic_in_source_id_order` (reverse materialization order gives an identical state) |
| Idempotent re-ingestion | `test_reingesting_the_same_batch_is_an_exact_no_op` (whole-state byte snapshot unchanged) |
| Exact-byte duplicates as distinct occurrences | `test_exact_byte_duplicate_is_a_distinct_occurrence` |
| Changed bytes for an existing key rejected before publication | `test_changed_bytes_for_an_existing_source_key_are_rejected_before_staging` (parser and staging are never invoked), `test_cli_reports_ingest_and_rejection` |
| Deterministic full rebuild in source-ID order | `test_full_rebuild_is_deterministic_in_source_id_order` |
| Staged publication with rollback | `test_failed_first_ingest_leaves_no_state`, `test_failure_before_or_during_publication_rolls_back`, `test_interrupted_publication_fails_closed`, `test_tampered_current_archive_blocks_ingest_and_reads` |
| Stable existing Find results and citations | `test_first_generation_matches_accepted_find_citations_and_derived_members`, `test_existing_find_results_and_citations_stay_stable_after_increment` |
| Input limited to reviewed synthetic bytes | `test_unreviewed_or_unsafe_incoming_members_are_rejected`, `test_increment_fixture_hashes_are_pinned_and_synthetic` |

## End-to-end CLI evidence

Batch 1 was the 14 reviewed fixtures, recorded at `2026-09-20T12:00:00Z`. Batch 2 was the three increment fixtures plus an unchanged copy of `01-plain-lf-7bit.eml`, recorded at `2026-09-27T12:00:00Z`.

| Step | Result |
|---|---|
| Ingest batch 1 | `generation-0001`, 14 sources, 6 indexed / 4 with warnings / 4 quarantined |
| Re-ingest batch 1 | `published: false`, 14 already preserved, state unchanged |
| Find `lantern observatory` on generation 1 | `EML-001`, `EML-005`, `EML-006`, `EML-008`; output byte-identical to accepted prototype 1 (SHA-256 `10bb0313a2807d3ea2e4a83c2371197e3bacfd49dd15af4dfba5f677f1b5fcb0`) |
| Ingest batch 2 | `generation-0002`, new `EML-015`, `EML-016`, `EML-017`; `EML-001` already preserved; `EML-016` is an exact-byte duplicate of `EML-001` and `EML-005` |
| Ingest `01-plain-lf-7bit.eml` with `EML-006` bytes | Exit 2: `source key synthetic-eml:01-plain-lf-7bit.eml is already bound to EML-001 with different bytes; changed source bytes are rejected` |
| Find on generation 2 | the same four results, unchanged, followed by `EML-015` and `EML-016` |
| Rebuild generation 2 | byte-identical |
| Verify state | both generations and the append-only chain verified |

### Generation hashes

| Evidence | Generation 1 | Generation 2 |
|---|---|---|
| Source count | 14 | 17 |
| Source-manifest SHA-256 | `8b3c77070e3d0d4f329646d25c14d58d32924fddc5b1b72523dd9444f7b1067e` (10,682 bytes) | `3f5a6c796132af5661466527130a5d6a76a6ff5adeeee7cc37e3bb630996d4c7` (13,013 bytes) |
| Derived-tree SHA-256 | `e7500849dd0742ed4632718627975f519461c66252e6f769431d6d4f90024de9` | `e4894d4e284002d10fcbf440fcaa4efb03e84e1d0d15c48b54e8f7ca2f9cbea5` |
| `index.json` | `0961bd45…` (accepted, identical) | `a5e9282bdb3788579de1786d96385755a257b5c1e92a281b150e17636ce65ea6` |
| `messages.json` | `c8b7c67f…` (accepted, identical) | `4add64ed2f7e4c0375463d5fc64099433378d5605c413acdc70fad78425571f0` |
| `duplicates.json` | `2a63201c…` (accepted, identical) | `4373921cfc8b856e812dc6ec3f0547c4ae30004e423114ccb7d9b1ce4a5f263a` |
| `derived-manifest.json` | `19e17c15c8f99803c87cae9d689ae4db227fabeca16060ae6ffb87a27494d171` | `eff8cd63c89255738426b37d272b653c88ed41b929e02d2df51de6c38869e2a1` |

The generation-1 source manifest and derived-tree digests differ from the accepted prototype-1 values (`5e2011d2…`, `7d6ab2ed…`). This is expected: the manifest now records source keys and the batch ledger, and `derived-manifest.json` binds to the manifest's hash. Every other derived member for the reviewed corpus is byte-identical to the accepted evidence.

### New preserved sources

| Source ID | Source key | Bytes | SHA-256 |
|---|---|---:|---|
| `EML-015` | `synthetic-eml:15-lantern-follow-up.eml` | 355 | `57da0246e8c6977f10005676264368d34eae5fffdceaaab44899614fda482482` |
| `EML-016` | `synthetic-eml:16-resent-plain-lf-7bit.eml` | 351 | `befec305981577844c8b233135125394886ffc26d7dedf589bbb152a0d51f208` |
| `EML-017` | `synthetic-eml:17-dome-maintenance.eml` | 353 | `132e520c3fb6eb4447a814f46f47b6306ad8e93c3dbdb40612ab8afbb1e1d7b9` |

## Limitations

- Input is restricted to reviewed synthetic bytes. Source keys are derived from incoming file names, which is adequate for fixtures but not a design for provider identity (Gmail IDs, IMAP UIDs, Outlook entry IDs, MBOX offsets).
- IDs are capped at `EML-999` by the accepted citation grammar. Widening it would change the citation format and needs its own review.
- A key is bound to its first bytes permanently. There is no reviewed path for a legitimate correction to a source; the batch is rejected.
- Each ingest copies and rehashes the whole archive and rebuilds all derived state; cost grows linearly with the archive. Earlier generations are retained, so storage grows with every published ingest.
- Single-user and synchronous, with no lock. Two concurrent ingests are not safe.
- Publication is atomic with respect to `CURRENT`. Durability across power loss (directory `fsync`) is not demonstrated, and a crash between the generation rename and the `CURRENT` replacement leaves a state that readers refuse until someone inspects it by hand.
- Derivation provenance uses each batch's logical `recorded_at`, not wall-clock derivation time, to keep rebuilds byte-identical.
- Parser process separation remains the experimental control from the hardening increment.
- No UI, AI, real data, account integration, network service, deployment, or stack selection.
