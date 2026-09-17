# Phase-3 Gate-1 Experiment Design

**Status:** Accepted
**Review date:** 2026-09-17
**Authority:** Accepted `docs/PHASE-3-PLAN.md`
**Execution state:** Paused at Gate 1. No fixture bytes, prototype code, dependencies, services, credentials, keys, or test runs have been created.

## Purpose

This package fixes the exact boundary for the Controlled Synthetic Feasibility Evaluation before any experiment is built. It describes two contrasting reference slices, `EXP-C001` and `EXP-C003`, without selecting either architecture or changing the Phase-2 no-selection finding.

## Gate-1 artifacts

| Artifact | Review question |
|---|---|
| [Experiment Layout](EXPERIMENT-LAYOUT.md) | Is every future file and process confined to a visibly experimental boundary? |
| [Fixture Manifest](FIXTURE-MANIFEST.md) | Is the proposed corpus entirely synthetic, complete enough for the scoped tests, and honest about stand-ins? |
| [Synthetic-Only Safeguards](SYNTHETIC-ONLY-SAFEGUARDS.md) | Do preflight, runtime, logging, network, and stop controls fail closed? |
| [Experimental Contracts](EXPERIMENTAL-CONTRACTS.md) | Are preservation, export, worker, privacy, backup, search, and citation behaviors exact enough for independent implementations? |
| [Dependency Manifests](DEPENDENCY-MANIFESTS.md) | Are proposed toolchains minimal, pinned, attributable, and separable from execution? |
| [Rollback and Cleanup](ROLLBACK-AND-CLEANUP.md) | Can every disposable artifact be removed without touching the repository, live archive, accounts, or production state? |
| [Traceability](TRACEABILITY.md) | Does every scoped requirement and acceptance test have a fixture, evidence target, and reviewer? |

## Candidate references, not selection

- `EXP-C001` tests the `CAND-001` boundary: Python/Django, SQLite/FTS5, and a minimal web rendering surface.
- `EXP-C003` tests the `CAND-003` boundary: Go, PostgreSQL/FTS, and a minimal SwiftUI/WebKit rendering surface.
- Shared contracts, fixtures, worker boundaries, expected truth, and outcome vocabulary apply to both.
- `CAND-002` and `CAND-004` remain retained. Their absence from these experiments is not rejection or adverse evidence.
- No Gate-1 artifact is a stack-selection ADR, production design, dependency approval for a product, or reusable deployment specification.

## Deliberate limitations

- `CORP-003` uses a documented Outlook-shaped synthetic stand-in. It does not implement or prove PST parsing.
- Parser workers are deliberately tiny fault probes. They do not establish production source-family coverage.
- The local model router and answer records are deterministic stubs. No model, embedding service, cloud AI, or hosted inference is present.
- Mac, iPhone, and iPad product quality is reviewed only at the contract and minimal-rendering-probe level. Full cross-device UX remains unproved.
- A container or database artifact whose immutable digest is unavailable before acquisition cannot run until the acquisition record captures and freezes that digest.

## Approval boundary

Approval of this package would permit Gate 2 safety-baseline work and then only the experiments described here. It would not select a stack; create a stack-selection ADR; authorize accounts, real correspondence, the live archive, cloud AI, telemetry, production infrastructure, deployment, public exposure, email sending, or source mutation; or authorize a push.

Any material deviation requires a revised Gate-1 diff and user review. Prototype work remains paused until this package is explicitly accepted.
