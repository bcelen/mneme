# Synthetic Test-Corpus Design

**Status:** Accepted
**Review date:** 2026-09-17
**Authority:** ADR-003
**Data boundary:** Entirely fictional data; no copied, transformed, or paraphrased real correspondence.

## Purpose

The corpus will provide a deterministic, reviewable basis for preservation, parser-safety, provenance, retrieval, entity, and recovery tests before Mneme receives any real correspondence. This document specifies fixture intent and expected truth, not fixture files or implementation.

## Design rules

1. Every person, address, organization, event, document, and message is invented for the corpus.
2. Synthetic addresses use reserved or non-deliverable domains, and links use reserved targets; fixtures must not cause outbound mail or network traffic.
3. Hostile examples are inert text or safely packaged test artifacts. They express attack intent without containing live malware.
4. Each fixture has a stable corpus ID, source-family label, expected source-package membership, and human-reviewed expected outcomes.
5. Source bytes are fixed once a corpus version is released. Corrections create a new fixture version and preserve the old one for compatibility testing.
6. Expected truth distinguishes facts encoded in source, derived expectations, deliberate ambiguity, and outcomes that must remain unknown.
7. Provider-shaped fixtures emulate only the exported structures needed for testing and must never require provider authentication.
8. The corpus includes valid, malformed, ambiguous, duplicated, and adversarial material; passing only happy-path fixtures is insufficient.

## Fictional scenario

The baseline scenario follows a fictional community group, Meridian Field Society, from 2004 through 2025. Its members exchange meeting notices, travel plans, research notes, invoices, photographs, and reports across multiple fictional accounts and clients. The long timeline creates controlled identity changes, organization changes, repeated events, attachments, forwards, replies, conflicting dates, and topic shifts.

No name, address, event, or text should be drawn from the user's correspondence. A corpus review must check that examples do not accidentally reproduce personal information.

## Fixture catalog

### Source-family and baseline fixtures

| ID | Fixture set | Planned representation | Coverage and expected truth |
|---|---|---|---|
| CORP-001 | Gmail-shaped export | Synthetic provider-export package with MBOX/EML-like mail material and fictional provider metadata | Inbox and sent messages, labels, provider message/thread IDs, attachments, drafts excluded by declared scope, stable expected counts |
| CORP-002 | Google Workspace-shaped export | Synthetic organization-account export distinct from personal Gmail | Sent and received mail, organization metadata, aliases, shared-label ambiguity, declared export boundary |
| CORP-003 | Outlook-shaped export | Synthetic provider/client export representation | Inbox, sent mail, folders, flags, conversation identifiers, inline images, calendar-like attachment without live account access |
| CORP-004 | Eudora-shaped archive | Synthetic mailbox files, companion metadata, and attachment directory | Multiple mailboxes, sent mail, attachment links, stale index data, platform line-ending variants |
| CORP-005 | MBOX dialect set | Several synthetic MBOX containers | Separator escaping, mixed line endings, missing final newline, nested MIME, valid and malformed entries |
| CORP-006 | EML directory set | Synthetic individual-message tree | Meaningful and meaningless filenames, nested directories, duplicate files, sent messages, sidecars, filesystem-metadata ambiguity |

### Message, MIME, and attachment fixtures

| ID | Fixture set | Coverage and expected truth |
|---|---|---|
| CORP-007 | Header and address variants | Folded headers, comments, quoted display names, aliases, groups, Bcc, missing or repeated fields, internationalized text represented safely |
| CORP-008 | Date and timezone variants | Valid offsets, absent timezone, contradictory Received and Date fields, daylight-saving edges, impossible dates, expected uncertainty |
| CORP-009 | Encoding variants | UTF-8, legacy charset labels, mislabeled charset, quoted-printable, base64, malformed transfer encoding; source bytes always authoritative |
| CORP-010 | MIME structure variants | Multipart alternative, related, mixed, nested messages, inline resources, detached-looking parts, malformed boundaries |
| CORP-011 | Document attachments | Fictional text, PDF-like inert fixture, spreadsheet-like inert fixture, image-like inert fixture, zero-byte and truncated files; no active content |
| CORP-012 | Remote and missing attachments | Content-ID links, remote URLs on reserved domains, unavailable external files, broken references; no network fetch permitted |
| CORP-013 | Size and resource limits | Small fixtures plus safely generated boundary descriptors for oversized message, deep nesting, decompression expansion, and attachment-count limits |

### Conceptual-model fixtures

| ID | Fixture set | Coverage and expected truth |
|---|---|---|
| CORP-014 | People and identities | One person with several addresses, shared address used by several people, changed display names, aliases, and intentionally unresolved identity |
| CORP-015 | Organizations | Membership changes, renamed organization, overlapping domains, contractors, and correspondence that must not imply employment |
| CORP-016 | Conversations | Replies, forwards, subject changes, missing ancestors, provider-thread disagreement, split and merged conversation candidates |
| CORP-017 | Topics and documents | Explicit and implicit topics, repeated document versions, same filename/different bytes, different filename/same bytes, topic uncertainty |
| CORP-018 | Events and timelines | Planned, canceled, rescheduled, and retrospectively described events; conflicting dates and source-quality differences |
| CORP-019 | Relationships | Explicit collaboration, inferred contact frequency, ambiguous introductions, and cases where no relationship claim is justified |

### Classification and integrity fixtures

| ID | Fixture set | Coverage and expected truth |
|---|---|---|
| CORP-020 | Exact duplicates | Identical source bytes in separate packages and paths; retain both source occurrences while allowing a derived duplicate relation |
| CORP-021 | Logical duplicates | Semantically equivalent messages with transport/header changes; never delete either source occurrence |
| CORP-022 | Near duplicates and versions | Quoted replies, forwarded copies, edited attachments, repeated newsletters; expected not to collapse into exact duplicates |
| CORP-023 | Junk and non-junk | Obvious synthetic spam, newsletters, receipts, false-positive traps, and user-controlled classification history |
| CORP-024 | Integrity failures | Changed byte, missing file, extra file, wrong size, altered manifest, and incomplete export; each must trigger a stop condition |

### Security and AI-adversarial fixtures

| ID | Fixture set | Coverage and expected truth |
|---|---|---|
| CORP-025 | Hostile HTML | Inert script tags, event handlers, tracking pixels, remote resources, deceptive links, forms, and CSS-based concealment; no execution or network access |
| CORP-026 | Hostile attachments | Inert signature-only or mock artifacts representing executable, macro, archive traversal, decompression bomb, malformed document, and polyglot risks |
| CORP-027 | Prompt injection | Messages and attachments that tell an AI or agent to ignore policy, reveal secrets, access the network, alter records, or fabricate citations; all remain untrusted data |
| CORP-028 | Data exfiltration traps | Reserved URLs, encoded instructions, hidden HTML text, fake tool calls, and requests to include unrelated sources; no outbound access or privilege gain |
| CORP-029 | Misleading evidence | Forged-looking headers, quoted text presented as original, contradictory witnesses, fabricated provider IDs, and low-confidence chronology |
| CORP-030 | Credential leakage traps | Synthetic token-shaped strings, passwords, OAuth-like values, and secrets in quoted text; they must be redacted from logs and never treated as usable credentials |

### Preservation and recovery fixtures

| ID | Fixture set | Coverage and expected truth |
|---|---|---|
| CORP-031 | Provenance chain | Synthetic acquisition, verification, parse, classification, correction, export, and rebuild events with known lineage |
| CORP-032 | Derived-history undo | User annotation and classification changes with known prior states and expected undo behavior |
| CORP-033 | Rebuild generations | Same source with two recorded processing-rule versions; stale generation must be detected rather than silently mixed |
| CORP-034 | Backup and restore | Synthetic complete, stale, partial, corrupted, and key-unavailable backup scenarios with expected recovery outcomes |
| CORP-035 | Export independence | Complete and deliberately partial application-independent export examples with known omissions and integrity expectations |

## Expected-truth catalog

Every fixture set must have a human-readable expected-truth entry containing:

- corpus ID and version;
- source-family claim and source-package boundary;
- fixed byte hashes after a hash algorithm is separately approved;
- expected manifest members and declared omissions;
- expected parse successes, warnings, quarantines, and failures;
- source-grounded facts and citations;
- intentionally ambiguous or unknowable claims;
- expected entities and relationships, including non-merges;
- expected duplicate and junk classifications without source deletion;
- expected security behavior and prohibited side effects;
- expected provenance chain, rebuild generation, and undo behavior.

The catalog describes expected behavior without prescribing a database schema or implementation language.

## Corpus versioning and review

- Corpus releases use immutable version labels; fixture bytes do not change within a release.
- New releases include a change log and compatibility expectation.
- A preservation/corpus specialist reviews source-shape realism.
- A security/privacy specialist reviews adversarial fixtures and ensures they are inert.
- A quality/review specialist checks expected truth, requirement coverage, and absence of personal data.
- Any fixture suspected of containing real personal data is quarantined and removed from distribution pending review.

## Exit criteria before implementation tests

The design is ready for fixture creation only after reviewers confirm coverage of all planned source families, preservation requirements, threat-register entries, and acceptance-test rows; agree that hostile fixtures can be made inert; and confirm that no real correspondence is needed to achieve the planned coverage.
