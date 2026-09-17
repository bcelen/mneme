# Implementation-Stack Comparison Framework

**Status:** Accepted
**Review date:** 2026-09-17
**Authority:** ADR-005
**Decision boundary:** This framework defines evaluation; it does not identify candidates, select a stack, authorize prototypes, or add dependencies.

## Evaluation sequence

1. Define complete candidate boundaries: client, server/runtime, persistence, search, parsing/isolation, backup/export, and AI integration assumptions.
2. Apply every non-negotiable gate. A candidate that fails a gate is not scored as selectable.
3. Collect written evidence for each weighted criterion using the synthetic corpus and approved design analysis when implementation work is later authorized.
4. Score independently by the relevant specialist roles, resolve material disagreements in writing, and record uncertainty.
5. Compare failure modes, migration paths, lock-in, replacement boundaries, operational burden, and costs.
6. Propose a separate selection ADR. The user must explicitly approve it before implementation begins.

## Non-negotiable gates

| Gate | Candidate must demonstrate |
|---|---|
| G-01 Source preservation | Source bytes can remain immutable and independently verifiable; parsing and derived-data changes cannot rewrite them. |
| G-02 Export independence | Source archive, manifests, provenance, and user-controlled derived data have an application-independent export path. |
| G-03 Rebuildability | Machine-derived state can be removed and rebuilt from source plus recorded processing rules. |
| G-04 Provenance and citations | User-visible derived assertions can trace to source and processing evidence without fabricating lineage. |
| G-05 Parser isolation | Importers, parsers, renderers, and attachment handlers can run with bounded resources and without archive-write, credential, or unnecessary network privilege. |
| G-06 Privacy control | External transfer is default-deny, data routing is inspectable, and local-only operation remains meaningful. |
| G-07 Backup and restore | Complete backup scope, independent integrity verification, isolated restore, and recovery drills are feasible. |
| G-08 Portable ownership | The user can migrate preserved and user-authored data without depending on a vendor, hosted service, or proprietary runtime to interpret source bytes. |
| G-09 Security maintenance | Dependencies, updates, vulnerabilities, credentials, and compromise recovery can be managed for the expected lifetime. |
| G-10 Product boundary | The design supports a single-user research system and does not require sending email, source mutation, or public exposure. |

A gate may be marked **Pass**, **Fail**, or **Unproved**. Unproved is not pass. Exceptions require a new proposal identifying the affected accepted principle and explicit user approval.

## Weighted criteria

Scores use the rubric below. Weights total 100 and may be revised during review before candidate evaluation.

| ID | Criterion | Weight | Evidence expected |
|---|---|---:|---|
| STF-01 | Byte fidelity and preservation boundary | 14 | Architecture explanation plus AT-P01–P07 results when implementation testing is authorized |
| STF-02 | Integrity, manifests, provenance, and citation traceability | 10 | PRES-006–015 coverage and AT-L01/L06 evidence |
| STF-03 | Rebuildability and application-independent export | 10 | AT-L03–L05 and AT-R01–R03 evidence |
| STF-04 | Security isolation and hostile-content handling | 15 | THR-002–006 controls and AT-S01–S07 evidence |
| STF-05 | Privacy, local-first operation, and controlled hybrid AI | 10 | Network/data-flow analysis, default-deny proof, provider-boundary design |
| STF-06 | Cross-device product quality | 10 | Mac, iPhone, and iPad interaction review for core workflows; no client technology is assumed |
| STF-07 | Performance and accessibility | 5 | Measurable budgets, accessible interaction plan, and representative synthetic-corpus evidence |
| STF-08 | Operational simplicity, backup, restore, and observability | 8 | Single-user operating model, AT-R04–R08, maintenance and failure-state review |
| STF-09 | Portability and replaceable boundaries | 6 | Deployment alternatives, migration plan, interface boundaries, and lock-in analysis |
| STF-10 | Deterministic Find and grounded AI Ask | 5 | Separation of deterministic retrieval from AI; AT-M07/M08 evidence |
| STF-11 | Maintainability, ecosystem health, and supply-chain posture | 5 | Dependency inventory approach, update/vulnerability policy, licensing and stewardship evidence |
| STF-12 | Total cost and resource fit | 2 | Acquisition, operation, storage, model, maintenance, and migration cost ranges with assumptions |

## Scoring rubric

| Score | Meaning |
|---:|---|
| 0 | Cannot satisfy the criterion or directly conflicts with an accepted principle. |
| 1 | Major unresolved gaps; mitigation is speculative or would require redesign. |
| 2 | Partially satisfies the criterion; important risks or operating burden remain. |
| 3 | Satisfies the criterion with understood tradeoffs and credible evidence. |
| 4 | Strong fit with low residual risk and good evidence. |
| 5 | Excellent fit; independently verifiable evidence and clear long-term replacement/recovery path. |

The weighted score is the sum of `weight × score / 5`. A numerical score never overrides a failed or unproved gate. Any criterion supported only by assertion rather than reviewable evidence is capped at 2.

## Evidence-confidence annotation

Each score also receives a confidence label:

- **High:** Independently repeatable evidence or a passed acceptance test.
- **Medium:** Complete design evidence with assumptions identified, but no authorized implementation test yet.
- **Low:** Vendor claim, analogy, incomplete investigation, or material unresolved assumption.

Report weighted totals alongside confidence distribution and unresolved risks. Do not collapse uncertainty into a single ranking.

## Blank candidate worksheet

| Candidate ID | Boundary summary | Gates passed / failed / unproved | Weighted score | Confidence profile | Principal risks | Migration/exit path | Review status |
|---|---|---|---:|---|---|---|---|
| CAND-___ | To be completed only after candidate evaluation is authorized | — | — | — | — | — | Not evaluated |

For each candidate, attach:

- an architecture-neutral data-flow and trust-boundary description;
- preservation, export, backup, restore, and rebuild paths;
- dependency and external-service inventory;
- Mac/iPhone/iPad UX implications;
- performance and resource assumptions;
- failure, compromise, and recovery behavior;
- data and operational migration plan;
- unresolved questions and evidence needed.

## Specialist review responsibilities

- **Preservation/corpus:** G-01–G-03 and STF-01–03.
- **Security/privacy:** G-05–G-07 and G-09; STF-04–05, STF-08, and STF-11.
- **Product/UX:** G-10 and STF-06–07.
- **Research/AI:** G-04 and STF-10.
- **Quality/review:** evidence sufficiency, scoring consistency, acceptance-test traceability, and unresolved-risk accounting.
- **Orchestrator:** complete candidate boundary, conflict resolution, combined comparison, and selection-ADR proposal.

## Selection decision requirements

A later stack-selection ADR must identify every candidate considered, gate outcomes, criterion scores and confidence, rejected alternatives, material failure modes, lock-in and migration costs, residual threats, operational cost range, and dissenting specialist views. Selection remains an explicit user approval gate. This framework itself authorizes no implementation work.
