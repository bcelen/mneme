# Proposed Synthetic Fixture Manifest

**Status:** Accepted
**Review date:** 2026-09-17
**Release identifier:** `phase3-corpus-v0.1`
**Creation state:** Manifest design only; no fixture files or hashes exist yet.

## Corpus declaration

The release is generated from the fictional Meridian Field Society scenario defined in the accepted corpus design. Every person, address, organization, event, message, attachment, identifier, credential, and timestamp is invented. No source may be copied from, transformed from, paraphrased from, or compared against real correspondence.

The release marker at `fixtures/releases/phase3-corpus-v0.1/SYNTHETIC_ONLY.json` must contain exactly these policy fields before generation begins:

```json
{
  "schema": "mneme.synthetic-release/v0.1",
  "release_id": "phase3-corpus-v0.1",
  "synthetic": true,
  "contains_real_data": false,
  "scenario": "Meridian Field Society",
  "generator_seed": "mneme-phase3-corpus-v0.1",
  "allowed_root": "experiments/phase-3/fixtures/releases/phase3-corpus-v0.1",
  "allowed_domains": ["example.com", "example.net", "example.org", "invalid"],
  "external_authority": false,
  "email_delivery_capability": false
}
```

Every package repeats `synthetic: true`, `contains_real_data: false`, its `CORP` identifier, version, generator identity, seed, source-family claim, declared omissions, and expected-truth reference. A missing or conflicting marker is a hard failure.

## Exact fixture catalog

| ID | Planned package path | Concrete Phase-3 representation | Primary tests |
|---|---|---|---|
| CORP-001 | `CORP-001-gmail-shaped-v1/` | Provider-shaped directory containing MBOX/EML bytes, inbox/sent labels, synthetic provider message/thread IDs, attachments, and declared omission of drafts | AT-P01, AT-M01, AT-M07 |
| CORP-002 | `CORP-002-workspace-shaped-v1/` | Organization-account export stand-in with aliases, inbox/sent mail, provider metadata, and shared-label ambiguity | AT-P01, AT-M01, AT-M02 |
| CORP-003 | `CORP-003-outlook-shaped-v1/` | Plain-file Outlook export stand-in with folders, flags, conversation IDs, sent mail, inline images, and calendar-like attachment; not a PST file and not PST proof | AT-P01, AT-M01, AT-M03 |
| CORP-004 | `CORP-004-eudora-shaped-v1/` | Mailbox files, companion metadata, attachment directory, stale index, and CR/LF variants | AT-P01, AT-P07, AT-M01 |
| CORP-005 | `CORP-005-mbox-dialects-v1/` | MBOX variants for separator escaping, mixed line endings, missing final newline, nested MIME, and malformed entries | AT-P01, AT-P07, AT-M01 |
| CORP-006 | `CORP-006-eml-tree-v1/` | Nested EML tree with meaningful/meaningless filenames, sidecars, duplicate files, sent mail, and filesystem-metadata ambiguity | AT-P01, AT-M01, AT-M05 |
| CORP-007 | `CORP-007-headers-v1/` | Folded/repeated/missing headers, comments, groups, aliases, Bcc, quoted names, and safe international text | AT-P07, AT-M02 |
| CORP-008 | `CORP-008-dates-v1/` | Valid and absent offsets, conflicting `Date`/`Received`, DST edges, impossible dates, and explicit uncertainty | AT-P07, AT-M04 |
| CORP-009 | `CORP-009-encodings-v1/` | UTF-8, legacy and mislabeled charsets, quoted-printable, base64, and malformed transfer encoding | AT-P07, AT-M01 |
| CORP-010 | `CORP-010-mime-v1/` | Multipart alternative/related/mixed, nested messages, inline resources, detached-looking parts, and malformed boundaries | AT-P07, AT-M01 |
| CORP-011 | `CORP-011-documents-v1/` | Inert text, PDF-like, spreadsheet-like, and image-like bytes plus zero-byte and truncated attachments | AT-S02 |
| CORP-012 | `CORP-012-remote-missing-v1/` | Content-ID links, broken references, and remote URLs using reserved domains only | AT-S01, AT-S06 |
| CORP-013 | `CORP-013-resource-limits-v1/` | Small files plus descriptors that generate bounded deep-nesting, attachment-count, timeout, memory, and expansion probes at runtime | AT-S02, AT-S03, AT-S07 |
| CORP-014 | `CORP-014-identities-v1/` | Multiple addresses per person, shared addresses, changing display names, aliases, and deliberately unresolved identity | AT-M02 |
| CORP-015 | `CORP-015-organizations-v1/` | Membership changes, renaming, overlapping domains, contractors, and non-employment cases | AT-M04 |
| CORP-016 | `CORP-016-conversations-v1/` | Replies, forwards, subject changes, missing ancestors, provider disagreement, and split/merge candidates | AT-M03 |
| CORP-017 | `CORP-017-topics-documents-v1/` | Explicit/implicit topics and repeated document versions with controlled filename/hash relations | AT-M04 |
| CORP-018 | `CORP-018-events-timelines-v1/` | Planned, canceled, rescheduled, and retrospective events with conflicting dates | AT-M04, AT-M08 |
| CORP-019 | `CORP-019-relationships-v1/` | Explicit collaboration, inferred contact frequency, ambiguous introductions, and no-claim cases | AT-M04, AT-M08 |
| CORP-020 | `CORP-020-exact-duplicates-v1/` | Byte-identical occurrences in distinct source packages and paths | AT-M05 |
| CORP-021 | `CORP-021-logical-duplicates-v1/` | Semantically equivalent messages with transport/header changes | AT-M05 |
| CORP-022 | `CORP-022-near-duplicates-v1/` | Quoted replies, forwarded copies, edited attachments, and repeated newsletters that must not collapse as exact duplicates | AT-M05 |
| CORP-023 | `CORP-023-junk-v1/` | Synthetic spam, newsletters, receipts, false-positive traps, and reversible classification history | AT-M06 |
| CORP-024 | `CORP-024-integrity-failures-v1/` | Pristine package plus separately generated changed-byte, missing, extra, wrong-size, altered-manifest, and partial variants | AT-P02–P06 |
| CORP-025 | `CORP-025-hostile-html-v1/` | Inert scripts, handlers, trackers, remote resources, deceptive links, forms, and CSS concealment | AT-S01, AT-S06 |
| CORP-026 | `CORP-026-hostile-attachments-v1/` | Signature-only or textual mock artifacts for executable, macro, traversal, expansion, malformed document, and polyglot risks | AT-S02, AT-S03, AT-S07 |
| CORP-027 | `CORP-027-prompt-injection-v1/` | Plain and encoded instructions requesting policy override, secrets, tools, network, source mutation, or fabricated citations | AT-L05, AT-S04, AT-M08 |
| CORP-028 | `CORP-028-exfiltration-v1/` | Reserved URLs, hidden text, fake tool calls, and unrelated-source requests | AT-S04, AT-S06, AT-S11 |
| CORP-029 | `CORP-029-misleading-evidence-v1/` | Forged-looking headers, quoted text posed as original, contradictory witnesses, fake provider IDs, and uncertain chronology | AT-L06, AT-M04, AT-M08 |
| CORP-030 | `CORP-030-token-traps-v1/` | Nonfunctional `mneme_test_...` values shaped like passwords/OAuth tokens; expected log redaction and zero authority | AT-S05 |
| CORP-031 | `CORP-031-provenance-v1/` | Known synthetic acquisition, verify, parse, classify, correct, export, and rebuild chain | AT-L01, AT-L03, AT-S12 |
| CORP-032 | `CORP-032-derived-history-v1/` | Annotation and classification event history with known undo states | AT-L02, AT-M06 |
| CORP-033 | `CORP-033-generations-v1/` | Same source with two processing-rule versions and a deliberately stale generation | AT-L03–L05, AT-M07 |
| CORP-034 | `CORP-034-recovery-v1/` | Complete, stale, partial, corrupted, tampered-history, and unavailable-synthetic-key recovery scenarios | AT-R04–R08, AT-S10, AT-S12 |
| CORP-035 | `CORP-035-export-v1/` | Complete and deliberately partial independent exports with known omissions and allowed packaging variance | AT-R01–R03 |

## Package shape

Each package is generated in a staging root, passes the synthetic-data review, and is then frozen under its release path:

```text
CORP-<id>-<slug>-v1/
├── SYNTHETIC_ONLY.json
├── package-intent.md
├── payload/
├── expected-truth.json
└── generation-record.json
```

- `payload/` contains only the bytes presented to the preservation profile as the synthetic source package.
- `expected-truth.json` contains source facts, derived expectations, explicit ambiguity, prohibited side effects, and expected failures or quarantines.
- `generation-record.json` records generator version, fixed seed, command identity, creation time, reviewer roles, and exact payload hashes after creation.
- The release-level `manifest.json` enumerates every package, member, byte length, SHA-256 digest, expected-truth digest, and declared omission.
- Once `phase3-corpus-v0.1` is released, its payload bytes never change. A correction creates `v0.2` and retains `v0.1` for compatibility tests.

## Inert adversarial design

- No fixture contains a functional executable, macro, exploit, live malware, real credential, or routable exfiltration endpoint.
- Executable and macro cases are signature-only or textual descriptors that a deliberately tiny worker recognizes as policy violations.
- Expansion cases commit only bounded generator descriptors. The run harness creates the smallest artifact that crosses the experimental limit inside disposable storage.
- Path traversal cases are archive entries with inert text payloads and names such as `../escape.txt`; extraction outside scratch must never occur.
- Timeout, crash, process-pressure, and memory-pressure cases are explicit synthetic worker modes selected by fixture ID, not uncontrolled hostile binaries.
- HTML uses reserved domains and inert payloads. A loopback canary verifies that attempted remote loads are blocked without contacting those domains.

## Identifier and address rules

- Fixture identifiers are ASCII and contain no personal data: `CORP-###`, `spkg-corp-###-v1`, and `sitem-corp-###-<sequence>`.
- Email domains are limited to `example.com`, `example.net`, `example.org`, and the `.invalid` top-level domain.
- URLs are limited to HTTPS URLs on those reserved domains or a run-specific loopback canary URL inserted by the harness.
- Token-shaped values begin `mneme_test_`, have no external authority, and are generated separately from any user or host credential.
- Fictional names are drawn only from a reviewed project wordlist; accidental matches do not license use of real biographical facts.

## Release checks

The quality/review specialist and security/privacy specialist must jointly confirm before release:

1. all 35 fixture IDs are present or an omission is explicitly marked `Blocked`;
2. every package has matching synthetic markers and expected truth;
3. all addresses and URLs satisfy the reserved-domain allowlist;
4. no file contains material copied from real correspondence;
5. adversarial artifacts are inert and bounded;
6. payload hashes and release membership are independently recomputed;
7. a scan finds no live credentials, account identifiers, user paths, or project-external references;
8. the Outlook stand-in and every other emulation are labeled so they cannot be mistaken for format-coverage proof.

Failure of any check quarantines the unreleased staging corpus and blocks Gate 2.
