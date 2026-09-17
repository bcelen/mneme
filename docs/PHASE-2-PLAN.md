# Phase 2 Plan: Architecture and Stack Evaluation

**Status:** Accepted
**Review date:** 2026-09-17
**Scope:** Design and evidence-based evaluation only. This plan does not authorize implementation, prototypes, dependencies, external-account access, real-data inspection, deployment, commit, or push.

## Objective

Evaluate complete architecture and implementation-stack candidates against Mneme's accepted preservation, security, product, and operating requirements. Phase 2 will produce a reviewable comparison and a proposed stack-selection architecture decision record (ADR). It will not select or implement a stack until the user explicitly approves that ADR.

## Governing inputs

The following accepted Phase-1 artifacts are normative inputs:

- [Preservation-Contract Requirements](phase-1/PRESERVATION-CONTRACT.md)
- [Synthetic Test-Corpus Design](phase-1/SYNTHETIC-TEST-CORPUS.md)
- [Acceptance-Test Matrix](phase-1/ACCEPTANCE-TEST-MATRIX.md)
- [Security and Privacy Threat Register](phase-1/SECURITY-PRIVACY-THREAT-REGISTER.md)
- [Implementation-Stack Comparison Framework](phase-1/STACK-COMPARISON-FRAMEWORK.md)
- [Metadata-Only Source Inventory](phase-1/SOURCE-INVENTORY.md)

If a candidate conflicts with an accepted input, the candidate fails unless a separate proposal explicitly identifies the conflict and the user approves changing the governing requirement. Phase 2 may expose questions or recommend revisions, but it cannot silently weaken accepted obligations.

## Evaluation objects and candidate boundaries

### Complete architecture candidates

The unit eligible for eventual selection is a **complete architecture candidate**, not an isolated framework, database, client, or hosting product. Each candidate must declare one coherent boundary covering every category below. A category may be marked deliberately deferred only when the candidate explains the temporary boundary, replacement interface, risk, and path to completion.

Each complete candidate receives a stable identifier such as `CAND-001`. Names remain neutral until actual candidate evaluation is authorized.

### Candidate categories

| Category | Candidate boundary | Required boundary statement |
|---|---|---|
| Client experience | Mac, iPhone, and iPad user interfaces; local caches; source viewing; Find, Ask, citation, annotation, and recovery-status workflows | Supported form factors, offline assumptions, accessibility, trust boundary, cached data, update path, and what never reaches the client |
| Application and service runtime | Business rules, orchestration, background work, APIs or local interfaces, authorization checks, and lifecycle | Process boundaries, privilege levels, network listeners, concurrency, failure isolation, update/rollback, and whether operation requires a continuously running service |
| Source-archive preservation | Immutable source-package retention, integrity verification, manifests, and source access boundary | Authoritative bytes, write controls, identifier boundary, integrity mechanism, failure behavior, and application-independent readability |
| Derived state and provenance | Parsed metadata, entities, annotations, classifications, histories, lineage, configuration generations, and rebuild reports | Durable versus rebuildable state, undo/history behavior, transaction and consistency assumptions, versioning, and export boundary |
| Deterministic Find | Lexical, structured, metadata, attachment, and filtered retrieval independent of AI | Indexed inputs, deterministic semantics, update/rebuild behavior, explainability, scale assumptions, and failure/staleness visibility |
| Import and parser isolation | Source-family adapters, MIME/message parsing, document extraction, safe preview preparation, and quarantine | Inputs/outputs, filesystem and archive privileges, network denial, resource limits, unsupported-content behavior, and parser replacement path |
| AI Ask and model routing | Retrieval grounding, prompt construction, citations, local/cloud routing, model records, and uncertainty behavior | Exact data boundary, authority separation, provider assumptions, default-deny behavior, provenance, cost boundary, and operation when AI is unavailable |
| Export, backup, and recovery | Application-independent export, backup creation and verification, isolated restore, compromise recovery, and derived-state rebuild | Backup scope, failure domains, secret recovery, restore evidence, recovery objectives left open, and clean-environment requirements |
| Operations and observability | Installation, configuration, monitoring, audit, maintenance, updates, incident handling, and capacity management | Single-user maintenance burden, sensitive-data minimization, alerting, support horizon, administrative surface, and provisional deployment assumptions |

### Candidate boundary record

Every complete candidate must provide:

1. a one-paragraph boundary summary;
2. a component/category map with all categories represented;
3. data-flow and trust-boundary diagrams or equivalent textual descriptions;
4. source, derived, credential, network, backup, and export boundaries;
5. external services, dependencies, licenses, and paid-resource assumptions;
6. replaceable components and migration interfaces;
7. provisional deployment assumptions separated from product requirements;
8. known exclusions, deferred areas, and conditions;
9. failure, compromise, rollback, restore, and exit paths;
10. an evidence ledger and unresolved-question register.

Two candidates must not be compared under the same identifier if their client, storage, isolation, cloud, or operational boundaries materially differ. Material variants receive separate identifiers or an explicitly bounded variant record.

## Evidence collection plan

### Evidence rules

- Prefer primary evidence: official documentation, specifications, license texts, source repositories, release and security policies, and reproducible published behavior.
- Record source location, publication or retrieval date, version, scope, claim supported, limitations, and reviewer.
- Separate vendor or maintainer claims from independently verifiable evidence.
- Do not infer a guarantee from the absence of contrary documentation.
- Phase 2 collects design and documentary evidence only. It does not install dependencies, run prototypes, create synthetic fixture files, or execute acceptance tests.
- When accepted requirements can be verified only through later implementation tests, mark the claim **Unproved** and carry the exact acceptance-test obligation forward.
- Time-sensitive evidence must be rechecked before the eventual ADR is accepted.

Each item receives an identifier such as `EVID-CAND-001-001` and records its confidence as **High**, **Medium**, or **Low** using the accepted comparison framework.

### Evidence by decision area

| Area | Evidence to collect | Governing references |
|---|---|---|
| Preservation | Architecture description of immutable source boundaries; byte-fidelity behavior; content-addressing or integrity capabilities; identifier separation; failure semantics; compatibility/version policy | PRES-001–015; G-01; STF-01–02; AT-P01–P07, AT-L01, AT-L06 |
| Exportability | Documented complete export path for source bytes, manifests, provenance, and user-controlled derived data; independent readability; format/version documentation; partial-export behavior | PRES-016–020; G-02, G-08; STF-03, STF-09; AT-R01–R03 |
| Rebuildability | Durable/rebuildable state inventory; reproducibility boundaries; rule/version capture; stale-generation handling; user-history preservation; nondeterminism treatment | PRES-028–033; G-03; STF-03; AT-L02–L05 |
| Security isolation | Process and privilege boundaries; parser/renderer sandbox capability; network denial; resource limits; credential separation; update and vulnerability model; hostile-content behavior | THR-001–011, THR-013–015; G-05, G-06, G-09; STF-04–05, STF-11; AT-S01–S09, AT-S11–S12 |
| Backup and restore | Backup scope; independent failure domains; encryption and key recovery; integrity verification; clean restore; retention; compromise recovery; rebuild after restore | PRES-021–027; THR-012–013; G-07; STF-08; AT-R04–R08, AT-S10, AT-S12 |
| UX | Core task flows for Find, Ask, citations, source inspection, annotations, uncertainty, integrity failures, backup and rebuild status across Mac, iPhone, and iPad; accessibility and offline assumptions | G-10; STF-06–07; AT-U01–U03; product requirements |
| Portability | Supported environments; separation from Ubuntu/Docker/ZFS/Tailscale assumptions; data migration; component replacement; hosted-service and proprietary-runtime dependencies; exit cost | G-08; STF-09; PRES-016–020 |
| Maintenance | Release cadence, support horizon, upgrade/rollback, dependency burden, observability, incident response, vulnerability handling, administrator effort, and failure-state clarity | G-09; STF-08, STF-11; THR-009–013 |
| Licensing | Licenses for direct and material transitive components; distribution, modification, network-service, model, data, and commercial-use terms; obligations; incompatibilities; uncertainty requiring specialist advice | STF-11; G-08, G-09 |
| Cost | One-time and recurring costs for software, hardware, storage, backup, network, hosted services, models, maintenance time, migrations, and exit; low/base/high scenarios with assumptions | STF-12; approval gates for services and costs |

### Evidence ledger fields

| Field | Meaning |
|---|---|
| Evidence ID | Stable candidate-scoped identifier |
| Candidate and category | Exact boundary to which the evidence applies |
| Claim | One falsifiable statement supported or challenged |
| Evidence type | Official documentation, specification, license, repository, policy, published test, or analysis |
| Source and version | Exact source, product/version/date, and retrieval date |
| Relevant requirements | PRES, THR, AT, gate, and STF identifiers |
| Confidence | High, Medium, or Low with rationale |
| Limitations | Missing detail, marketing claim, unsupported version, or conditional behavior |
| Contradictions | Conflicting evidence IDs or reviewer findings |
| Later verification | Acceptance tests or implementation evidence still required |
| Reviewer and review date | Specialist role and date, without inventing an approval |

## Gate assessment

The ten mandatory gates from the accepted framework remain unchanged:

| Gate | Lead review | Minimum Phase-2 evidence |
|---|---|---|
| G-01 Source preservation | Preservation/corpus | Complete source-boundary design mapped to PRES-001–015, with no unexplained write path |
| G-02 Export independence | Preservation/corpus | End-to-end export design and independently readable format evidence covering PRES-016–020 |
| G-03 Rebuildability | Preservation/corpus + quality/review | Durable/rebuildable inventory and mapped rebuild obligations for PRES-028–033 |
| G-04 Provenance and citations | Research/AI + preservation/corpus | Traceability design from user-visible claims to source and processing evidence |
| G-05 Parser isolation | Security/privacy | Enforceable privilege, network, resource, and failure boundaries for every untrusted-content processor |
| G-06 Privacy control | Security/privacy + research/AI | Default-deny external transfer, explicit routing, local-only behavior, and inspectable data flows |
| G-07 Backup and restore | Preservation/corpus + security/privacy | Complete backup/restore/compromise-recovery design mapped to PRES-021–027 |
| G-08 Portable ownership | Preservation/corpus + quality/review | Credible export, migration, replacement, and exit path without proprietary interpretation of source bytes |
| G-09 Security maintenance | Security/privacy + quality/review | Dependency/update/vulnerability/incident model with sustainable ownership |
| G-10 Product boundary | Product/UX | Single-user research workflows across target devices without outbound mail, source mutation, or public exposure |

### Gate scoring

Each gate receives exactly one status:

- **Pass:** Phase-2 evidence demonstrates a complete and credible design path satisfying the gate, with all later implementation-verification obligations listed.
- **Fail:** Evidence shows the candidate cannot satisfy the gate within its declared boundary, or satisfying it would conflict with an accepted principle.
- **Unproved:** Evidence is missing, contradictory, dependent on an undeclared component, or requires empirical proof that Phase 2 is not authorized to collect.

`Unproved` is not `Pass`. A candidate with any `Fail` or `Unproved` gate is not eligible for the proposed stack-selection ADR. Gate passage in Phase 2 establishes design eligibility only; it does not claim that implementation acceptance tests have passed.

Every gate record includes evidence IDs, lead and required reviewers, assumptions, residual risk, disagreements, and exact later acceptance tests. Exceptions require a separate proposal and explicit user approval; scoring cannot waive a gate.

## Weighted-criteria scoring

The twelve accepted criteria and weights remain unchanged:

| Criterion | Weight |
|---|---:|
| STF-01 Byte fidelity and preservation boundary | 14 |
| STF-02 Integrity, manifests, provenance, and citation traceability | 10 |
| STF-03 Rebuildability and application-independent export | 10 |
| STF-04 Security isolation and hostile-content handling | 15 |
| STF-05 Privacy, local-first operation, and controlled hybrid AI | 10 |
| STF-06 Cross-device product quality | 10 |
| STF-07 Performance and accessibility | 5 |
| STF-08 Operational simplicity, backup, restore, and observability | 8 |
| STF-09 Portability and replaceable boundaries | 6 |
| STF-10 Deterministic Find and grounded AI Ask | 5 |
| STF-11 Maintainability, ecosystem health, and supply-chain posture | 5 |
| STF-12 Total cost and resource fit | 2 |

### Criterion score

Use the accepted 0–5 rubric:

- **0:** Cannot satisfy the criterion or directly conflicts with an accepted principle.
- **1:** Major unresolved gaps; mitigation is speculative or would require redesign.
- **2:** Partial fit with important risks or operating burden.
- **3:** Satisfies the criterion with understood tradeoffs and credible evidence.
- **4:** Strong fit with low residual risk and good evidence.
- **5:** Excellent fit with independently verifiable evidence and a clear long-term replacement/recovery path.

The weighted contribution is `weight × score / 5`, and contributions sum to a maximum of 100. Evidence supported only by assertion is capped at 2. Scores must cite evidence IDs and identify later test obligations.

### Missing evidence and score ranges

Missing evidence is recorded as **Unknown**, not misrepresented as a score of 0. Report:

- **confirmed score:** weighted total of criteria with supportable scores;
- **potential range:** confirmed score through the theoretical total if unknown criteria later score 5;
- **evidence coverage:** percentage of total criterion weight with supportable scores;
- **confidence profile:** weight assessed at High, Medium, and Low confidence;
- **validation debt:** acceptance tests and empirical claims deferred beyond Phase 2.

An Unknown criterion contributes nothing to the confirmed score but remains visible in the potential range. A candidate cannot be recommended merely because its uncertainty creates a high theoretical ceiling. Criterion totals never override gate status.

### Calibration and comparability

- Score complete candidates at the same declared level of detail and time horizon.
- Use the same cost horizon, workload assumptions, corpus-size scenarios, and product workflows.
- Separate inherent capability from custom work, operational burden, and speculative future features.
- Apply the same evidence cutoff date and record material evidence changes.
- Do not claim meaningful numerical superiority when score differences are smaller than unresolved uncertainty or reviewer disagreement.

## Required specialist reviews

| Review | Required scope | Sign-off condition |
|---|---|---|
| Preservation/corpus | G-01–G-03, G-07–G-08; STF-01–03, STF-08–09; source-family fit and PRES-001–033 traceability | No preservation-contract conflict; all gaps and later tests explicit |
| Security/privacy | G-05–G-07, G-09; STF-04–05, STF-08, STF-11; THR-001–015 | Trust boundaries complete; residual risks and unproved controls explicit |
| Product/UX | G-10; STF-06–07; Mac/iPhone/iPad workflows, accessibility, uncertainty, integrity/recovery states | Core journeys and measurable evaluation assumptions documented |
| Research/AI | G-04, G-06; STF-05, STF-10; Find/Ask separation, grounding, routing, citations, and prompt injection | No AI authority over source content; local/cloud boundary and citation obligations explicit |
| Quality/review | Evidence ledger, gate consistency, criterion calibration, AT matrix coverage, rejected alternatives, and reproducibility of the comparison | Every score traceable; missing evidence and contradictions preserved |
| Maintenance and supply-chain | G-09; STF-08, STF-11; dependency, release, vulnerability, rollback, support, and operational ownership | Sustainable maintenance claim supported or marked unproved |
| Licensing and cost | STF-11–12; license obligations, incompatibilities, service/model terms, and comparable cost scenarios | Primary terms cited; unresolved legal or commercial questions explicit |

The orchestrator checks candidate-boundary completeness, assigns review work, reconciles terminology, prevents scope drift, and prepares the combined comparison. It cannot convert specialist dissent into consensus or approve a gate on the user's behalf.

## Uncertainty, missing evidence, and disagreement records

Maintain four append-only registers:

| Register | Identifier | Required fields |
|---|---|---|
| Uncertainty | `UNC-###` | Claim, candidate, consequence, probability or range where defensible, evidence, owner, resolution trigger, and decision impact |
| Evidence gap | `GAP-###` | Missing evidence, affected gates/criteria, why unavailable, search performed, later verification, and whether it blocks eligibility |
| Reviewer disagreement | `DIS-###` | Exact disputed claim/status/score, each position and evidence, attempted resolution, orchestrator synthesis, and user-decision need |
| Rejected alternative | `REJ-###` | Candidate or variant, complete boundary, evidence reviewed, rejection reason, failed gates or weak criteria, consequences, and revisit trigger |

Rules:

- Never delete an uncertainty, gap, dissent, or rejection because it complicates the recommendation; close or supersede it with rationale.
- A gate-status disagreement, a criterion-score difference greater than one point, or a disputed privacy/security assumption requires a `DIS` record.
- Missing evidence that affects a mandatory gate forces `Unproved`.
- Contradictory credible evidence lowers confidence and remains linked from the score or gate record.
- Rejected alternatives receive enough boundary detail to show they were compared fairly; labels such as “too complex” require measurable explanation.
- The user decides unresolved tradeoffs that materially affect architecture, privacy/security, external services/costs, or operational burden.

## Evaluation stages and review gates

1. **Frame:** approve this Phase-2 plan, candidate-category boundaries, evidence method, and scoring protocol.
2. **Candidate set:** propose complete candidates and material variants without selecting one; record inclusion and exclusion rationale.
3. **Evidence collection:** populate evidence ledgers, category boundary records, costs, licenses, and uncertainty/gap registers.
4. **Specialist review:** conduct required reviews independently before combined scoring.
5. **Calibration:** reconcile factual errors and rubric interpretation while preserving substantive disagreement.
6. **Gate assessment:** mark every gate Pass, Fail, or Unproved with evidence and later tests.
7. **Weighted comparison:** score eligible evidence, report confirmed totals, ranges, coverage, confidence, and validation debt.
8. **ADR proposal:** prepare the stack-selection ADR only if at least one candidate passes all gates.
9. **User approval:** present the complete comparison and proposed ADR; no selection becomes accepted without explicit user approval.

## Eventual stack-selection ADR structure

The future ADR must contain:

1. **Title, status, date, and decision owner.** It begins as `Proposed`.
2. **Decision scope and authorization boundary.** Exact parts of the stack covered and actions not authorized.
3. **Governing inputs.** Accepted Phase-1 artifacts and this approved Phase-2 plan.
4. **Decision drivers and assumptions.** Corpus, product, deployment, workload, privacy, and operating assumptions.
5. **Candidate set and complete boundaries.** Category maps and material variants for every candidate.
6. **Evidence summary.** Ledger coverage, confidence, evidence cutoff date, contradictions, and validation debt.
7. **Mandatory-gate matrix.** Ten gate statuses, evidence, reviewers, residual risks, and later tests for each candidate.
8. **Weighted comparison.** Twelve scores, contributions, confirmed totals, potential ranges, evidence coverage, and confidence profile.
9. **Specialist findings and disagreements.** Sign-offs, reservations, `DIS` records, and unresolved user choices.
10. **Security, privacy, and preservation analysis.** Threat coverage, source boundary, export, backup/restore, rebuild, and compromise recovery.
11. **UX and operational analysis.** Cross-device experience, accessibility, performance assumptions, maintenance, observability, and failure states.
12. **Licensing and cost analysis.** Terms, obligations, incompatibilities, cost scenarios, and unresolved specialist advice.
13. **Rejected alternatives.** `REJ` records and revisit triggers.
14. **Proposed decision and rationale.** Selected complete boundary, why it best satisfies accepted requirements, and why scores alone are insufficient.
15. **Consequences and migration/exit path.** Benefits, tradeoffs, lock-in, replacement boundaries, rollback, and future decision triggers.
16. **Conditions and implementation-verification obligations.** Exact acceptance tests, risk mitigations, and stop conditions required in the next phase.
17. **Approval record.** User decision, date, approved scope, exceptions, and any required follow-up ADRs.

### User approval gate

The stack-selection ADR remains `Proposed` until the user explicitly approves it. Approval must identify the selected complete candidate, accepted residual risks, unresolved conditions, and the precise scope authorized for a later implementation phase. Approval of the ADR does not by itself authorize external accounts, real-data access, cloud transfer, production deployment, destructive operations, or costs not explicitly named. Those remain separate gates.

If no candidate passes all mandatory gates, Phase 2 produces a no-selection finding, preserves the evidence and rejected alternatives, and asks the user whether to revise the candidate set, requirements, or phase scope. It must not select the least-bad failing candidate.

## Definition of done

Phase 2 planning is complete when this plan is reviewed and accepted. Phase 2 evaluation is complete only when candidate boundaries are complete, evidence and uncertainty registers are reviewable, required specialists have completed their reviews, all gates and criteria are assessed consistently, rejected alternatives are recorded, and either a proposed stack-selection ADR or a documented no-selection finding is ready for user review.

## Out of scope

- selecting or accepting an implementation stack before the user approval gate;
- application code, dependencies, schemas, infrastructure, Docker configuration, or prototypes;
- provider authentication, external-account access, or real correspondence inspection/import;
- synthetic fixture implementation or acceptance-test execution;
- production deployment, public exposure, destructive operations, or sending email;
- commit or push without separate user authorization.
