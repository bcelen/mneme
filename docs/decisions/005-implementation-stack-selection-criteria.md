# ADR-005: Implementation-Stack Selection Criteria

**Status:** Accepted
**Phase:** 1 — Preservation Foundation

## Context

Mneme must eventually choose implementation technologies, but choosing them before preservation, security, test, and UX requirements are reviewed would turn provisional assumptions into hidden commitments.

## Proposal

Evaluate candidate stacks against a documented weighted or otherwise explicit comparison covering:

- byte fidelity and application-independent export;
- hashes, manifests, provenance, and rebuildability;
- parser and attachment isolation;
- local-first privacy and controlled hybrid AI;
- portability across the provisional deployment context and alternatives;
- beautiful, fast, low-maintenance Mac, iPhone, and iPad experience;
- deterministic Find and source-grounded AI Ask;
- backup, restore verification, observability, and operational simplicity;
- accessibility, maintainability, licensing, supply-chain risk, and total cost;
- fit with the staged agent-governance and approval model.

The comparison must include failure modes, migration costs, lock-in, and what remains replaceable. A later decision record must name the selected stack, explain tradeoffs, and receive explicit user approval.

## Alternatives considered

- Select a stack based on the provisional Ubuntu/Docker/ZFS context: rejected because deployment context is not an accepted product principle.
- Select a stack based primarily on AI or developer familiarity: rejected because preservation and privacy obligations are foundational.

## Consequences

The project gains a transparent basis for a later technology choice without making one now. Evaluation work must remain design-level until the selection is approved.

## Approval boundary

This proposal authorizes criteria and comparison design only. It does not authorize implementation-stack selection, dependencies, application code, or infrastructure.
