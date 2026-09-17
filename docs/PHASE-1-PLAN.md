# Phase 1 Plan: Preservation Foundation

**Status:** Accepted
**Scope:** Documentation, design, and approval preparation only. Implementation and real-data access remain separately gated.

## Objective

Establish the preservation, security, testing, and decision framework needed before Mneme processes any real correspondence. Phase 1 does not authenticate to external accounts, inspect message content, import real correspondence, choose an implementation stack, or authorize production deployment.

## Workstreams

### 1. Metadata-only source inventory

Create a catalog of intended source families and acquisition constraints without authenticating to providers or inspecting real correspondence. The inventory may record only user-supplied or already-known metadata such as source family, format, provider, approximate coverage, expected export mechanism, ownership, sensitivity, and open questions. It must not contain message subjects, bodies, addresses, attachment contents, tokens, or downloaded source material.

Initial source families are Gmail/Google Workspace, Outlook, Eudora, MBOX, and EML, including sent mail, attachments, and provider metadata. The inventory is a planning artifact, not an import authorization.

### 2. Preservation contract

Define and review the contract for the source archive:

- preserve source bytes without normalization or silent rewriting;
- calculate and retain integrity hashes and manifests;
- record source, acquisition, transformation, and derived-data provenance;
- provide an application-independent export path;
- define backup scope, integrity checks, retention, and recovery responsibilities;
- verify restores rather than assuming backups work;
- rebuild derived data from the source archive and recorded processing rules;
- keep all annotations and classifications outside the source archive and reversible under the project definition.

No storage format, database, filesystem, container, or library is selected by this plan.

### 3. Synthetic test corpus and acceptance tests

Design a synthetic corpus that exercises all planned source families and the conceptual model without using real correspondence. Include messages and sent mail, attachments, provider metadata, duplicates, junk, malformed inputs, missing fields, encodings, threading, people and identities, organizations, topics, events, relationships, and timelines. Include hostile HTML, malicious-looking attachments, prompt injection, contradictory dates, and ambiguous identities.

Acceptance tests must cover byte fidelity, hash and manifest correctness, provenance completeness, export/import independence, backup and restore verification, derived-data rebuildability, deterministic Find behavior, citation/provenance behavior for AI Ask, security isolation, and refusal to treat source content as instructions.

### 4. Security and privacy review

Review importer and parser boundaries, hostile HTML and attachments, prompt injection, OAuth tokens and provider credentials, dependency and supply-chain risk, backups and exports, network exposure, logging, cloud transfer, and compromise recovery. The review must identify threats, mitigations, residual risks, approval gates, and tests. No provider authentication or external service is used in this phase.

### 5. Implementation-stack selection criteria

Define criteria and a comparison method, without selecting a stack. Candidates must be evaluated for preservation fidelity, portability, rebuildability, provenance, security isolation, local-first operation, cross-device UX, maintainability, observability, backup/restore behavior, licensing, supply-chain risk, and total cost. Any eventual choice requires a separate proposed decision record and explicit user approval.

### 6. Later real-data dry run

Specify a separately approved, staged dry run for a small, user-selected real-data slice. It must have an explicit source, scope, consent, credentials plan, data boundary, backup and rollback plan, preservation checks, quarantine/isolation plan, success criteria, and stop conditions. Approval for the plan does not authorize authentication, import, indexing, classification, cloud transfer, or AI processing of real correspondence.

## Gates and deliverables

1. **Frame:** approve this plan's scope, risks, terminology, and no-real-data boundary.
2. **Design:** review and approve or revise the six proposed decision records.
3. **Verify:** validate the synthetic corpus design, acceptance-test matrix, preservation obligations, and security review coverage.
4. **Accept:** record the accepted decisions and separately authorize implementation work.
5. **Later dry run:** require a new explicit approval after implementation and before any real-data operation.

Phase 1 is complete only when the plan and relevant decisions are accepted, the synthetic test corpus and acceptance criteria are ready, security and privacy risks have owners or explicit deferrals, and no unapproved implementation or real-data action has occurred.

## Planning deliverables

- [Metadata-Only Source Inventory](phase-1/SOURCE-INVENTORY.md)
- [Preservation-Contract Requirements](phase-1/PRESERVATION-CONTRACT.md)
- [Synthetic Test-Corpus Design](phase-1/SYNTHETIC-TEST-CORPUS.md)
- [Acceptance-Test Matrix](phase-1/ACCEPTANCE-TEST-MATRIX.md)
- [Security and Privacy Threat Register](phase-1/SECURITY-PRIVACY-THREAT-REGISTER.md)
- [Implementation-Stack Comparison Framework](phase-1/STACK-COMPARISON-FRAMEWORK.md)

These artifacts were accepted on 2026-09-17. They do not authorize implementation or real-data access.

## Out of scope

Application code, dependencies, infrastructure, Docker configuration, implementation-stack selection, provider authentication, external-account access, real correspondence inspection or import, AI processing of real data, production deployment, and sending email.
