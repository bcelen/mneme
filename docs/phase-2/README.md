# Phase 2 Architecture and Stack Evaluation

**Status:** Accepted
**Review date:** 2026-09-17
**Evidence cutoff:** 2026-09-17
**Authorization boundary:** Design and documentary evaluation only. Nothing in this directory selects a stack or authorizes code, dependencies, prototypes, external-account access, real-data inspection, deployment, commit, or push.

## Governing inputs

This evaluation is governed by the accepted Phase-1 preservation contract, synthetic-corpus design, acceptance-test matrix, threat register, source inventory, and stack-comparison framework, together with the accepted [Phase-2 plan](../PHASE-2-PLAN.md).

## Evaluation set

The comparison uses four complete architecture candidates:

- `CAND-001` — Python web monolith: Django, SQLite, and SQLite FTS5 with a responsive, progressively enhanced web/PWA client.
- `CAND-002` — TypeScript web application: Next.js/Node.js and PostgreSQL full-text search with a responsive PWA client.
- `CAND-003` — Apple-native clients: SwiftUI apps for Mac, iPhone, and iPad, backed by a Go service and PostgreSQL full-text search.
- `CAND-004` — Shared native clients: Flutter apps for Mac, iPhone, and iPad, backed by a Rust/Axum service and PostgreSQL full-text search.

Each candidate includes the same preservation, provenance, parser-isolation, controlled-AI, export, recovery, and private-access obligations. Differences in those common obligations are not treated as optional advantages.

## Artifacts

- [Candidate Set](CANDIDATE-SET.md)
- [Evidence Register](EVIDENCE-REGISTER.md)
- [Uncertainty Register](UNCERTAINTY-REGISTER.md)
- [Evidence-Gap Register](GAP-REGISTER.md)
- [Reviewer-Disagreement Register](DISAGREEMENT-REGISTER.md)
- [Rejected-Alternative Register](REJECTION-REGISTER.md)
- [Seven Specialist Reviews](SPECIALIST-REVIEWS.md)
- [Gate and Weighted-Criteria Scorecard](SCORECARD.md)
- [No-Selection Finding](NO-SELECTION-FINDING.md)

## Current evaluation outcome

All four candidates have credible architectural directions, and none has a documented `Fail`. However, unresolved specialist disagreement and missing enforceable designs leave G-01 through G-09 `Unproved`; only G-10 receives a Phase-2 design `Pass`. Under the accepted plan, no candidate is eligible for a stack-selection ADR.

The scorecard therefore reports supported partial scores and very wide potential ranges rather than a winner. `CAND-003` leads the supported 26% of weighted evidence, but the difference is not meaningful and cannot override the unproved gates. The required Phase-2 output is a no-selection finding with specific resolution triggers.

No stack is selected or proposed for selection by these artifacts.
