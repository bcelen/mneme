# Metadata-Only Source Inventory

**Status:** Accepted
**Review date:** 2026-09-17
**Authority:** ADR-001
**Data boundary:** Planning metadata only; no account access, content inspection, download, or import has occurred.

## Purpose

This inventory records the source families Mneme is expected to support and the questions that preservation design must answer. It contains no account identifiers, email addresses, message subjects or bodies, attachment contents, credentials, tokens, file listings, message counts, or verified date ranges.

## Inventory vocabulary

- **Source family:** A provider, legacy client, or interchange format from which a source package may later be acquired.
- **Source package:** A future user-approved export or file collection presented for preservation. No source package currently exists in this workspace.
- **Provider metadata:** Provider-created identifiers and organization such as labels, folders, thread identifiers, flags, timestamps, and export context, where present in an approved source package.
- **Acquisition route:** A future method of obtaining a source package. Every route remains unapproved until a separate gate authorizes it.
- **Coverage:** The types of records expected in scope, not a statement that any real corpus has been inspected.

## Planned source families

| ID | Source family | Expected representations | Expected coverage | Possible later acquisition route | Current knowledge | Preservation questions |
|---|---|---|---|---|---|---|
| SRC-001 | Gmail / Google Workspace | Provider export in its supplied structure; MBOX or EML where supplied; attachments and provider metadata | Received and sent mail, attachments, labels or folders, thread and message metadata | User-provided export or separately approved provider access | Planned only; account count, ownership, size, date range, and export shape unknown | Which source bytes are authoritative? Which provider metadata survives export? How are labels, threads, drafts, and sent-state represented? |
| SRC-002 | Outlook | Provider or client export in its supplied structure; MBOX or EML where available; attachments and provider metadata | Received and sent mail, attachments, folders, conversation and message metadata | User-provided export or separately approved provider access | Planned only; service/client variants, account count, size, date range, and export shape unknown | Which Outlook variants exist? What export preserves original messages and provider metadata? How are folders, flags, and conversation identifiers represented? |
| SRC-003 | Eudora | Native mailbox and companion files as supplied; MBOX-like representations where present; attachments | Received and sent mail, mailbox organization, attachments, available client metadata | User-provided copy of an explicitly approved export or archive | Planned only; version, platform, mailbox layout, attachment layout, size, and date range unknown | Which files are required as one preservation unit? Are line endings or separators significant? How are attachments and mailbox indexes linked? |
| SRC-004 | MBOX | MBOX files exactly as supplied, plus any sidecar metadata and attachments supplied separately | Messages including sent mail where represented; headers, bodies, MIME parts, and container ordering | User-provided files from a separately approved source package | Planned only; dialect, producer, encoding, size, and date range unknown | Which MBOX dialect and escaping rules apply? Are sidecars needed? How will container bytes and individual logical messages both remain traceable? |
| SRC-005 | EML | Individual EML files exactly as supplied, with directory context and sidecars where present | Individual received or sent messages, headers, bodies, MIME attachments, and available filesystem context | User-provided files from a separately approved source package | Planned only; producer, naming, directory organization, size, and date range unknown | Is directory structure meaningful? Are filesystem timestamps evidentiary or incidental? How will duplicate files and equivalent messages be distinguished? |
| SRC-006 | Attachments and documents | Original MIME parts, exported files, or externally stored files supplied with source context | Binary and text attachments, inline resources, and correspondence-linked documents | Included only in a separately approved source package | Planned only; types, sizes, external-link behavior, and availability unknown | Which bytes are present versus remote references? How are inline and ordinary attachments distinguished? What safe-preview limits apply? |
| SRC-007 | Provider metadata | Metadata embedded in or accompanying an approved export | Provider IDs, labels, folders, flags, timestamps, thread or conversation IDs, export context | Supplied with an approved export or separately approved provider access | Planned only; fields and completeness unknown | Which fields are authoritative, derived, undocumented, mutable, or absent? How is provenance retained without treating provider organization as universal truth? |

## Inventory fields for later completion

When the user separately authorizes metadata collection for a real source, record only the minimum planning metadata below before any content access:

| Field | Purpose | Allowed before real-data import approval? |
|---|---|---|
| Inventory ID | Stable reference without embedding personal identifiers | Yes |
| Source family and format | Select preservation and test obligations | Yes, when user-supplied |
| Ownership and authority | Confirm the user has authority to preserve the source | Yes, as a confirmation rather than credentials |
| Approximate size and item count | Capacity and duration planning | Only if user-supplied or available without content inspection |
| Approximate date coverage | Completeness planning | Only if user-supplied or available without content inspection |
| Expected acquisition route | Identify future credential, export, and privacy gates | Yes, as a proposal |
| Sensitivity notes | Identify handling constraints | Yes, at category level only |
| Known exclusions | Prevent accidental scope expansion | Yes |
| Open questions | Track uncertainty without inspecting content | Yes |
| Message-level metadata or content | Not needed for planning | No |
| Account identifiers, credentials, or tokens | Secrets and personal data | No |

## Cross-source concerns

- Preserve each source package as supplied before parsing, normalization, deduplication, or classification.
- Do not assume provider threads, client mailboxes, or file containers are equivalent to Mneme conversations.
- Keep provider identifiers and source-specific organization as provenance-bearing evidence.
- Treat duplicates and junk as derived classifications; never delete source items because of either classification.
- Distinguish absent data from parser failure and from data intentionally excluded by the user.
- Record timezone, encoding, line-ending, and container ambiguity without silently correcting source bytes.

## Unknowns requiring later user input or approved inspection

- Which real source families actually exist, and who owns or controls them?
- What approximate sizes, counts, and date ranges are involved?
- Which provider/client versions and export mechanisms are available?
- Are any sources shared, delegated, legally restricted, or subject to retention obligations?
- Are attachments external, missing, encrypted, password-protected, or represented only by links?
- What must be excluded from any first dry run?

These unknowns do not block planning. They must remain unknown until the user supplies non-sensitive metadata or separately authorizes inspection.
