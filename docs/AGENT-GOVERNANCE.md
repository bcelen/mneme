# Agent governance

[AGENTS.md](../AGENTS.md) is the current agent workflow contract.
[The roadmap](ROADMAP.md) defines milestone outcomes and deep-review points.
This revision replaces the former per-step frame/design/build/verify/accept
procedure for routine synthetic implementation. It preserves the charter,
preservation requirements, privacy rules, and user authority over consequential
actions.

## Three different decisions

| Decision | Owner | Meaning |
|---|---|---|
| Implement an identified milestone | User, once per milestone or explicitly named group | Authorizes its bounded code, tests, internal review, fixes, documentation, and local checkpoint commits |
| Judge technical readiness | Agent/reviewer | Evidence-based recommendation; not user acceptance or publishing authority |
| Accept a result, publish, choose a product stack, or expose real data | User with explicit scope | Authorizes only the stated action; earlier authorization need not be requested again |

## Internal review while building

The implementing agent coordinates the work and its reviews. At meaningful
increments, ask a separate reviewer to challenge preservation, transactions,
parser boundaries, citations, and regressions where affected. Reviewers receive
the actual diff, milestone scope, and test evidence. They return actionable
findings with paths and a failure scenario. The implementer resolves findings
and continues; the user is not a message relay.

Delegation is permitted for bounded implementation or review tasks. Do not
claim independence if no separate reviewer ran; report the limitation and perform
a deliberate self-review. Do not create seven ceremonial approvals for a simple
change. There is no requirement for a separate process per specialist label.

## Deep review at milestone boundaries

Use the R0–R5 checkpoints and format in [ROADMAP.md](ROADMAP.md).
Deep review considers the combined system, product progress, and plan as well as
the diff. It checks whether tests establish the claimed behavior and whether the
next milestone is still the best use of effort.

A deep reviewer may recommend continuing, correcting specified issues, or
holding at a specific boundary. Reviewers do not approve their own scope
expansion. Passing every test does not establish production readiness.

## Scope of historical evidence

Accepted ADR-001 through ADR-006 remain meaningful: source inventory,
preservation, synthetic coverage, privacy review, stack evaluation criteria,
and separate real-data approval. Their planning work is historical; their
requirements are not erased by newer implementation permission.

Phase-2 candidate scoring and Phase-3 acquisition/planner work remain evidence
for a deferred architecture investigation. Their unfinished procedural gates do
not block an independently authorized synthetic milestone. Do not mark those
workstreams complete or reuse their incomplete results as verified evidence.

Handoff automation remains disabled. Neither this workflow nor a reviewer
verdict re-enables its packet commands. The existing experiments and historical
approval documents stay in place so prior reports and source references remain
resolvable.

## Definition of done

The authorized scope works end to end; relevant positive, negative, and recovery
tests pass; material review findings are addressed; source/provenance and privacy
requirements are preserved; documentation matches tested behavior; limitations
and platform gaps are explicit; and the next deep-review point is identified.
A blocked deployment or an unavailable unrelated tool is not a reason to prevent
in-scope synthetic progress.
