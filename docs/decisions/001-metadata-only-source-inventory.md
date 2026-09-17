# ADR-001: Metadata-Only Source Inventory

**Status:** Accepted
**Phase:** 1 — Preservation Foundation

## Context

Mneme needs to understand the planned corpus and acquisition constraints before preservation work is designed. Inspecting real correspondence or authenticating to external accounts would cross an approval boundary before the preservation and security contracts exist.

## Proposal

Create a metadata-only inventory using user-supplied or already-known information. Record source family, format, provider, approximate coverage, expected export mechanism, ownership, sensitivity, and unresolved questions. Do not record message content, subjects, addresses, attachment contents, tokens, credentials, or downloaded source material.

The initial inventory scope is Gmail/Google Workspace, Outlook, Eudora, MBOX, and EML, including sent mail, attachments, and provider metadata. This list describes planning scope and does not promise importer support.

## Alternatives considered

- Inspect or authenticate to sources immediately: rejected because it would process real data before approval and before preservation controls exist.
- Defer all inventory: rejected because source formats and acquisition constraints affect preservation requirements.

## Consequences

The project can plan preservation and tests without exposing correspondence. The inventory will remain incomplete until the user separately approves source access or provides non-sensitive export metadata.

## Approval boundary

This proposal authorizes no authentication, provider access, content inspection, download, import, or processing of real correspondence.
