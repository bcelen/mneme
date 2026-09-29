# Mneme Local Synthetic Prototype 3 — Results

**Status:** Successful within the declared local, offline, synthetic-only experimental scope; merged to `main` at `739b645`.
**Run date:** 2026-09-28.

## Runtime

- Linux container: CPython 3.11.15 (`/usr/bin/python3.11`, SHA-256 `f56a588548dd013906ae1dcd1b6faa417f4e204da634ff354840d9643e78ff9e`) for the evidence run and all suites; CPython 3.10.20 for a second run of the new suite.
- macOS (reported 2026-09-29): the new suite passed on the accepted runtime, CPython 3.9.6 via `/usr/bin/python3 -B`, in 239.5 s, on commit `739b645` fetched from a verified Git bundle. That run did not print the interpreter version or re-check the resolved-executable SHA-256; the version was confirmed separately on 2026-09-28. The CLI evidence and hashes below come from the Linux container.
- Python standard library only. Socket creation is replaced by a failing test double during ingest tests.

## Verification

| Suite | Result |
|---|---|
| `mneme-local-prototype-3/tests/test_mbox.py` | 22 passed (macOS 3.9.6: 239.5 s; 3.11: 85.8 s; 3.10: 80.8 s) |
| `mneme-local-prototype-2/tests/test_incremental.py` | 16 passed, unchanged |
| `mneme-local-prototype-1/tests/test_mneme.py` | 5 passed, unchanged |
| `synthetic-hardening-1/tests/test_hardening.py` | 16 passed, unchanged |
| `synthetic-hardening-1/tests/test_isolation.py` | 6 passed, unchanged |
| `vertical-slice-1/tests/test_vertical_slice.py` | 10 passed, unchanged |
| `tools/handoff/t/handoff.t` | Not run: hard-codes `/Users/bogac/dev/forgejo/mneme/...` paths, which do not exist in this container; still outstanding and must be run on macOS |
| `phase-3/r3-g2-tile-planner` (Go) | Not run: see the network incident below; still outstanding, and any run must set `GOTOOLCHAIN=local` and `GOPROXY=off` |

No parser temporary directory, generated state, or bytecode remained after the runs.

Nine deliberate code mutations were each caught by the corresponding test and then reverted: disabling the changed-bytes check; making unescaping the identity; dropping the preamble as `mailbox.mbox` does; recording a new container observation on every ingest; skipping rollback of a renamed generation; making `recover` remove nothing; not quarantining ambiguous boundaries; binding citations to the unescaped rather than the preserved hash; and skipping re-segmentation of recorded boundaries.

## Test coverage

| Requirement | Tests |
|---|---|
| Byte preservation and boundaries | `test_segments_tile_every_container_byte_exactly_once`, `test_boundaries_agree_with_the_standard_library_mailbox`, `test_mbox_segments_are_preserved_exactly_with_boundaries_and_ids`, `test_recorded_boundaries_are_rederived_from_preserved_bytes` |
| mboxrd escaping | `test_mboxrd_unescaping_matches_the_literal_fixture` (the escaped record is written literally in the fixture) |
| Source IDs and keys | `test_mbox_segments_are_preserved_exactly_with_boundaries_and_ids`, `test_mixed_eml_and_mbox_batch_keeps_accepted_eml_identity` |
| Idempotency and append | `test_reingestion_is_idempotent_and_appends_only_new_records` |
| Duplicates and Message-ID | `test_duplicates_are_distinct_occurrences_and_message_id_is_not_identity` |
| Changed-source rejection | `test_changed_bytes_at_an_existing_offset_are_rejected_before_staging` (parser and staging never invoked), `test_cli_ingest_and_changed_source_rejection` |
| Malformed-input quarantine | `test_malformed_records_are_classified`, `test_malformed_and_unsafe_records_are_preserved_and_quarantined` |
| Deterministic rebuild | `test_full_rebuild_is_deterministic_across_mixed_sources` |
| Find and citation stability | `test_eml_only_generation_reproduces_accepted_derived_members`, `test_existing_find_results_and_citations_are_stable`, `test_mbox_citation_displays_unescaped_inert_text_with_span` |
| Rollback and interruption | `test_failed_first_ingest_leaves_no_state`, `test_failures_roll_back_and_leave_the_previous_generation_usable`, `test_interrupted_staging_keeps_current_usable_until_recovered`, `test_tampered_segment_blocks_reads_and_ingest` |
| Input boundary | `test_fixture_hashes_are_pinned_and_synthetic`, `test_unreviewed_container_bytes_are_out_of_scope` |

## Fixtures

| Fixture | Name | Bytes | SHA-256 | Purpose |
|---|---|---:|---|---|
| `MBOX-001` | `observatory-inbox.mbox` | 2,473 | `2f008aab90a5d7dd4ac68a6277b3e994a8ca4783a73f967695c449777f8259a7` | five records: ordinary, attachment, literal mboxrd escaping, same Message-ID as `EML-001`, exact copy of record 1 |
| `MBOX-002` | `observatory-inbox.mbox` | 2,857 | `2749de8a0c0a572a34d324fe6631c221090cac1d178ada4ef37faa7785f36073` | `MBOX-001` plus one appended record |
| `MBOX-003` | `observatory-inbox.mbox` | 2,473 | `bf198ca3d53ceb492891ca5a2faadabc28ab8ca372f3e74c35b84e811c6a9a79` | negative: record 2's attachment edited |
| `MBOX-004` | `damaged.mbox` | 140,565 | `2561e9e24eb50568ef11cdbfb61e06947b7346f858bdbaeccbf7446ab1f54bf7` | preamble, survivor, malformed envelope, unterminated, ambiguous boundary, oversized, truncated |

## End-to-end CLI evidence

| Step | Recorded at | Result |
|---|---|---|
| 1. Ingest the 14 accepted EML fixtures | 2026-09-20T12:00:00Z | `generation-0001`; 6 indexed, 4 with warnings, 4 quarantined; Find output byte-identical to prototypes 1 and 2 (SHA-256 `10bb0313a2807d3ea2e4a83c2371197e3bacfd49dd15af4dfba5f677f1b5fcb0`) |
| 2. Ingest `MBOX-001` | 2026-09-28T09:00:00Z | `generation-0002`; new `EML-015`…`EML-019`; `obs-0001`; `EML-015` and `EML-019` are exact-byte duplicates |
| 3. Re-ingest `MBOX-001` | 2026-09-28T09:30:00Z | `published: false`, 5 already preserved |
| 4. Ingest `MBOX-002` | 2026-09-28T10:00:00Z | `generation-0003`; only `EML-020` new; `obs-0002` reuses `EML-015`…`EML-019` |
| 5. Ingest `MBOX-003` | 2026-09-28T10:30:00Z | exit 2: `source key synthetic-mbox:observatory-inbox.mbox#offset=398 is already bound to EML-016 with different bytes; changed source bytes are rejected` |
| 6. Ingest `MBOX-004` | 2026-09-28T11:00:00Z | `generation-0004`; `EML-021`…`EML-027`; 6 quarantined, survivor `EML-022` indexed |
| Find `lantern observatory` | | `EML-001`, `EML-005`, `EML-006`, `EML-008` unchanged, then `EML-015`, `EML-018`, `EML-019` |
| Find `north dome` | | `mneme-source:EML-017@sha256:7ae3af93e86d895aeb09f9cdad01e98f317e5eb6c924a04d17f22317b202b4aa#mime:1`; displays `From the north dome…` with one escaping level removed |
| Rebuild | | byte-identical |
| Verify | | four generations, append-only chain, three container observations, no leftovers |

The whole sequence was run twice in fresh directories and produced identical generation-4 hashes.

### Generation hashes

| Generation | Sources | Source-manifest SHA-256 | Derived-tree SHA-256 |
|---|---:|---|---|
| 1 | 14 EML | `05ea125d94ac757c303af28ef8b1249d5a23ffef6c08fc7bf5f73d9228ed0411` | `3b9b75989a819b509cd77432f9fef0554d9a1d3957b2f55ea00610b46ec2efde` |
| 2 | +5 MBOX | `fbb5353f387a5b5072d9f99e57b8435a91b7406e00855417d23cf396bf1a6daa` | `f3f9969b180eab69adb6184fe64d5cd69ea09e1c6b72b3591d317783e1e7648c` |
| 3 | +1 MBOX | `80aebad1239997628303c822537fb04e16f7f98627e09ab02cc933e0b6bf9a65` | `583bed832ca72a88b52311953c73c1eebf55f02234908da6c0e58c2cc81c493f` |
| 4 | +7 MBOX | `726e46edc0a72f79334c562443141483d0dfd2f969761822bff8bbfff7b9912d` (26,762 bytes) | `0888935e84eea95713ed511ca845de004ad457419f8484d89338190f43a31ecb` |

In generation 1, `index.json`, `messages.json`, and `duplicates.json` equal the accepted prototype-1 hashes (`0961bd45…`, `c8b7c67f…`, `2a63201c…`). Generation-4 derived members: `index.json` `85328d38c08f42c7a9f2c3fce77ea90f692999e6883eb3f3ccb146670fdc5d9a`, `messages.json` `58743dfb20be653f5a8a595e5ce793b0dfc0284d57cedec67e153ab4327c6424`, `duplicates.json` `2e4b9e9e53e2a45a9ac0e82269508267c019117a2ddce10acc403eba2fa52610`, `derived-manifest.json` `cb6e70d997d5dc7a48695215010a61e8ab33718dfaa0fdf8b698626471f1b9a0`.

### Preserved MBOX segments

| ID | Offset | Bytes | SHA-256 | Outcome |
|---|---:|---:|---|---|
| `EML-015` | 0 | 398 | `beb1336ea1aee7949ca41e590bd6ddc314655d4af01a06f065a22eb9cab1d844` | indexed |
| `EML-016` | 398 | 685 | `2460abe62a42b8931e92b4f9a85073437aa3bd9f0360816e50d362b6ea37ac8a` | indexed (attachment) |
| `EML-017` | 1,083 | 568 | `7ae3af93e86d895aeb09f9cdad01e98f317e5eb6c924a04d17f22317b202b4aa` | indexed (escaped lines) |
| `EML-018` | 1,651 | 424 | `8e02b80585709f0c6808fd7435f805c5fe69313875e0bcaf2351789ff657747e` | indexed (Message-ID of `EML-001`) |
| `EML-019` | 2,075 | 398 | `beb1336ea1aee7949ca41e590bd6ddc314655d4af01a06f065a22eb9cab1d844` | indexed (exact copy of `EML-015`) |
| `EML-020` | 2,473 | 384 | `3b3abdab5303d8b23018d45994c16fafebd120b7c398f9a1d980d0e5248d8d92` | indexed (appended) |
| `EML-021` | 0 | 48 | `1c210743babb8d28667ad6184e90c7dd42ac93d3849e7f4698eeb10699964411` | quarantined: preamble |
| `EML-022` | 48 | 420 | `59d0499473fca42b43197b6147520d0ed0672ff293c2c21027487a6e4a95e347` | indexed (survivor) |
| `EML-023` | 468 | 157 | `f58e75b146a211e95a821ee7ad68028292306566ed3bfad75de1b07e64f178d9` | quarantined: malformed envelope |
| `EML-024` | 625 | 183 | `4742927ec709c2e4f1ab23bc8669a341b5adfbf0be4f04195f308909122e47fa` | quarantined: unterminated |
| `EML-025` | 808 | 188 | `ae2a1b759014eddfaba045502e80c7a5df22434da1f1c861f6c667df081f600b` | quarantined: ambiguous boundary |
| `EML-026` | 996 | 139,424 | `606848115cc70ef67e8901a51a9421d360e389a93cd19deb4a16a3ea09cf73b1` | quarantined: oversized |
| `EML-027` | 140,420 | 145 | `d6664eb875bd33a6bdc62571a4d0c6bd893387c1f2a46fddf9ebe2dc5362d163` | quarantined: truncated |

`EML-015`…`EML-020` belong to `observatory-inbox.mbox`; `EML-021`…`EML-027` belong to `damaged.mbox`.

## Rollback evidence

Run against a copy of the four-generation evidence state, comparing a digest over every path and file hash in the state (`c6ada16f63ef7f7fc7617f3a43b72c2d6d1bb4f41cd5f855095faa2ac8dab0ed`):

| Scenario | Result |
|---|---|
| Exception during derivation of a new container | Rolled back; state digest unchanged |
| Simulated crash after renaming `generation-0005`, before replacing `CURRENT` (cleanup disabled) | `CURRENT` still `generation-0004`; Find output unchanged; `verify` lists `generation-0005` as an unpublished leftover; `ingest` refuses with "run recover first" |
| `recover` | Removed only `generation-0005`; state digest back to `c6ada16f…` |
| Ingest after recovery | `generation-0005` published with `EML-028`…`EML-032` and `obs-0004` |

The test suite also covers a crash while staging (`.stage-*` leftover) and checks that the recovered state then ingests to a result byte-identical to a state that never crashed.

## Network incident

While checking whether the existing Go planner tests could run offline, `go version` inside `experiments/phase-3/r3-g2-tile-planner/` triggered Go's default `GOTOOLCHAIN=auto` behavior, because `go.mod` pins Go 1.27.1 and the container has Go 1.24.7. Go downloaded `golang.org/toolchain@v0.0.1-go1.27.1.linux-amd64` from `proxy.golang.org` into `/root/go/pkg/mod` (about 326 MB) at 17:46:48 UTC. No repository file changed, no Go test ran, and nothing else used the network. Removing the downloaded toolchain was blocked by the session's permission policy, so it remains in the container's module cache until someone removes it or the container is discarded. Future Go runs here must set `GOTOOLCHAIN=local` and `GOPROXY=off`.

## Limitations

- Input is restricted to reviewed synthetic bytes. Real mailboxes are out of scope.
- Only LF mboxrd is supported. CRLF mailboxes, mboxo, mboxcl, mboxcl2 (Content-Length framing), MMDF, and Eudora variants are not handled. A CRLF record is quarantined as unterminated.
- A key is `container name + byte offset`, so it survives appends but not rewrites. If a client compacts or reorders a mailbox, every record after the change conflicts with an existing key and the whole batch is rejected. There is no reviewed path to record a rewritten mailbox.
- Container keys come from file names, so renaming a mailbox makes all of its records new occurrences, which are exact-byte duplicates of the old ones.
- The first ingest that sees a record fixes its boundary context. A record that was the final, truncated record and is later completed by an append conflicts and is rejected.
- Envelope validation checks form only; it does not check that weekday and date agree.
- Source IDs share the `EML-NNN` namespace and the 999-ID cap with EML.
- Each ingest copies and re-hashes the whole archive and rebuilds all derived state; every published generation is retained.
- Single-user and synchronous, with no lock. Directory `fsync` and power-loss durability are not demonstrated. A crash during a first ingest can leave a sibling `.<state>.mneme-stage-*` directory that `recover` does not see.
- Parser isolation remains the experimental control from the hardening increment.

## Unresolved design questions

1. What is the durable source key for a message inside a container once real providers are involved: byte offset, record ordinal, provider ID, or a content-plus-context hash? Offsets fail on compaction; content hashes conflate true duplicates.
2. Should a rewritten mailbox be modeled as a new container observation that supersedes an old one, with explicit links between surviving records, instead of being rejected?
3. Should the preserved unit be the container (with segments as derived views) rather than the segments (with the container reconstructible)? This experiment stores segments only; the container is proven by reassembly.
4. Should source IDs become family-neutral, which would require a reviewed change to the accepted citation grammar?
5. How should a mboxrd processing-rule change be surfaced? The rule is recorded per derived record and verified, but not versioned at the derived-manifest level.
6. How should prototype-2 states migrate to this identity convention, given PRES-010 requires older manifests to stay verifiable?
