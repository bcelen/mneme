# ADR-003: Synthetic Test Corpus and Acceptance Tests

**Status:** Accepted
**Phase:** 1 — Preservation Foundation

## Context

Mneme needs meaningful preservation and security tests before any real correspondence is imported. The corpus must exercise source formats, edge cases, research entities, and hostile content without containing private correspondence.

## Proposal

Create a synthetic, versioned test corpus covering Gmail/Google Workspace, Outlook, Eudora, MBOX, and EML representations; sent mail; attachments; provider metadata; duplicates; junk; malformed messages; missing fields; unusual encodings; threading; people and identities; organizations; topics; events; relationships; and timelines.

Include adversarial cases for hostile HTML, malicious-looking attachments, prompt injection, contradictory dates, ambiguous identities, misleading metadata, oversized inputs, and parser failures. Keep fixtures clearly synthetic and never mix them with real source data.

Acceptance tests must verify byte fidelity, hashes, manifests, provenance, application-independent export, backup/restore verification, derived-data rebuildability, deterministic Find, source citations for AI Ask, parser isolation, refusal to follow embedded instructions, credential non-disclosure, and safe failure behavior.

## Alternatives considered

- Test only with a small real mailbox: rejected because it exposes private data before controls are validated and will miss adversarial coverage.
- Test only happy-path messages: rejected because preservation and security failures occur at boundaries and malformed inputs.

## Consequences

The project can establish repeatable quality gates without personal data. Synthetic fixtures require deliberate maintenance and must be expanded when new source families or processing rules are proposed.

## Approval boundary

This proposal authorizes synthetic test design and creation only. It does not authorize access to or processing of real correspondence.
