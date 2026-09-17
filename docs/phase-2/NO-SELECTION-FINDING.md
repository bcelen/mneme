# Phase-2 No-Selection Finding

**Status:** Accepted
**Review date:** 2026-09-17
**Decision owner:** User
**Decision state:** No implementation stack is selected or proposed for selection.

## Finding

The accepted Phase-2 plan permits a proposed stack-selection ADR only when at least one complete candidate passes all ten mandatory gates. After primary-evidence collection and seven specialist review passes:

- no candidate has a `Fail` gate;
- all four candidates pass G-10 at the Phase-2 design-boundary level;
- G-01 through G-09 remain `Unproved` after unresolved specialist disagreement and evidence-gap calibration;
- only 26% of weighted criteria have supportable scores;
- the score spread is much smaller than the unresolved uncertainty.

Therefore no candidate is eligible for a stack-selection ADR. Producing one now would violate the accepted plan by turning missing evidence into an implicit pass.

## Candidates retained

| Candidate | Retained because | Principal unresolved condition |
|---|---|---|
| CAND-001 Python/Django/SQLite/FTS5 web monolith | Smallest operating surface; credible preservation/search path; browser reach | Corpus workload, SQLite contention/recovery, mobile UX, and all common gates |
| CAND-002 Next.js/Node/PostgreSQL web application | Strong self-hosted PWA path and mature database capabilities | Dependency/cache/service boundary, operations, and all common gates |
| CAND-003 SwiftUI/Go/PostgreSQL Apple-native clients | Strongest Apple-platform UX capability and a small, compatible service runtime | Distribution, multi-client maintenance, API/cache security, and all common gates |
| CAND-004 Flutter/Rust/Axum/PostgreSQL shared native clients | Shared native-client code and memory-safe service direction | Platform fidelity, multi-toolchain supply chain, maintenance, and all common gates |

No scored candidate is rejected. Screened-out architectural alternatives and revisit triggers are recorded in the rejection register.

## Required gap-closing decisions

A candidate may become eligible only after a reviewed architecture definition closes, at minimum:

1. archive write enforcement, manifest/hash/version profile, and independent verification;
2. application-independent export and migration contract;
3. durable/rebuildable state and processing-generation contract;
4. claim-to-source provenance and citation-validation contract;
5. enforceable parser/renderer isolation and quarantine profile;
6. privacy, authentication, client-cache, log/temp, egress, and AI-routing data flow;
7. complete backup, key recovery, clean restore, and compromise-recovery design;
8. supported-version, SBOM, licensing-notice, vulnerability, update, rollback, and end-of-life policy;
9. common cross-device workflows, offline semantics, accessibility targets, and performance budgets;
10. common workload and five-year cost assumptions.

This is architecture-definition work only. Closing documentary gaps does not claim that synthetic tests pass; implementation acceptance remains a later, separately authorized phase.

## Re-entry rule for the stack-selection ADR

After the gap-closing artifacts are reviewed:

1. each specialist re-evaluates its gates and criteria;
2. disagreements remain in the register and unresolved gate dissent stays `Unproved`;
3. the orchestrator recalculates coverage, confidence, and ranges;
4. a proposed stack-selection ADR may be created only if at least one candidate has ten `Pass` gates;
5. the ADR remains `Proposed` until the user explicitly approves one complete candidate and its residual risks.

Even an accepted stack ADR would not authorize code, dependencies, accounts, real data, external AI, costs, deployment, destructive operations, commit, or push unless those actions are separately and explicitly approved.

## Review options

The user may:

- accept this evidence set and authorize a focused Phase-2 architecture-completion round;
- revise the candidate set or evaluation boundary;
- propose a change to an accepted requirement through a separate reviewed decision;
- reject the evaluation and request additional primary evidence.

No exception to a mandatory gate is recommended.
