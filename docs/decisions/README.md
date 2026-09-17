# Architecture Decision Records

This directory stores durable records of material decisions made after review. Each record should explain the context, decision, alternatives considered, consequences, approval boundary, and status.

## Status vocabulary

- **Proposed** — under discussion; not an implementation mandate.
- **Accepted** — explicitly approved and governing future work.
- **Superseded** — replaced by a later accepted decision.
- **Rejected** — considered and declined.

## Rules

- Do not use this directory to smuggle in unapproved implementation choices.
- Link decisions to the requirements and principles they affect.
- Record the approval boundary and date when a decision is accepted.
- Keep decisions small enough to review independently.
- Distinguish accepted product principles from provisional deployment context. Ubuntu 24.04, Docker, ZFS, and Tailscale are currently context to evaluate, not accepted implementation decisions.

No architecture decisions have been accepted in Phase 0 beyond the product and governance commitments documented elsewhere in `docs/`.

## Phase-1 proposed records

- [ADR-001: Metadata-Only Source Inventory](001-metadata-only-source-inventory.md)
- [ADR-002: Preservation Contract](002-preservation-contract.md)
- [ADR-003: Synthetic Test Corpus and Acceptance Tests](003-synthetic-test-corpus.md)
- [ADR-004: Security and Privacy Review for Preservation Work](004-security-and-privacy-review.md)
- [ADR-005: Implementation-Stack Selection Criteria](005-implementation-stack-selection-criteria.md)
- [ADR-006: Separately Approved Real-Data Dry Run](006-later-real-data-dry-run.md)

All Phase-1 records are accepted. They authorize planning and review only; none authorizes provider authentication, real-data access, implementation-stack selection, application code, deployment, or production operation.
