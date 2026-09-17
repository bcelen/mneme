# Phase 3 Plan: Controlled Synthetic Feasibility Evaluation

**Status:** Accepted
**Review date:** 2026-09-17
**Approval state:** Gate 0 approved. Phase-3 synthetic-only evaluation is authorized within this plan, but execution is paused at Gate 1 pending review of the exact experiment design. No prototype, dependency acquisition, fixture implementation, test execution, or test-service startup may begin before that review.
**Scope:** Narrow, local, reversible feasibility experiments using synthetic fixtures only.

## Purpose

Phase 2 correctly produced a no-selection finding. G-01 through G-09 remain `Unproved`, and no candidate is eligible for a stack-selection ADR. Phase 3 is intended to replace the highest-value documentary uncertainty with inspectable synthetic evidence while preserving that conclusion.

Phase 3 will compare two contrasting architecture references through deliberately incomplete experimental slices:

- `CAND-001` — the operational-simplicity reference: Django/Python, SQLite, and SQLite FTS5 with a web interface;
- `CAND-003` — the Apple-native reference: SwiftUI clients, a Go service, PostgreSQL, and PostgreSQL full-text search.

This is an evaluation shortlist, not a product shortlist or stack decision. `CAND-002` and `CAND-004` remain retained candidates. Their absence from Phase-3 prototyping is not a rejection, score reduction, or finding that they are inferior.

## Governing inputs

The following accepted artifacts remain normative:

- [Preservation-Contract Requirements](phase-1/PRESERVATION-CONTRACT.md)
- [Synthetic Test-Corpus Design](phase-1/SYNTHETIC-TEST-CORPUS.md)
- [Acceptance-Test Matrix](phase-1/ACCEPTANCE-TEST-MATRIX.md)
- [Security and Privacy Threat Register](phase-1/SECURITY-PRIVACY-THREAT-REGISTER.md)
- [Implementation-Stack Comparison Framework](phase-1/STACK-COMPARISON-FRAMEWORK.md)
- [Phase-2 Plan](PHASE-2-PLAN.md)
- [Phase-2 No-Selection Finding](phase-2/NO-SELECTION-FINDING.md)
- [Phase-2 Gap Register](phase-2/GAP-REGISTER.md)
- [Phase-2 Disagreement Register](phase-2/DISAGREEMENT-REGISTER.md)
- [Phase-2 Scorecard](phase-2/SCORECARD.md)

Phase 3 may create evidence against these requirements. It may not silently weaken, reinterpret, or waive them.

## Phase objective

Create the minimum synthetic prototypes and independent verification needed to determine whether `CAND-001` and `CAND-003` have credible, enforceable paths through the nine unproved gates.

Phase 3 must produce one of three outcomes for every scoped gate and candidate:

- **Synthetic Pass:** the reviewed design and authorized synthetic evidence satisfy the Phase-3 proof obligations;
- **Fail:** the candidate cannot satisfy the gate inside its declared boundary without conflicting with an accepted requirement or undergoing material redesign;
- **Still Unproved:** evidence is missing, contradictory, blocked, or too weak to support a pass.

A Synthetic Pass is not a production-security claim, real-corpus validation, or stack selection. It only permits later gate recalibration after specialist and user review.

## Authorization boundary requested

If this plan is explicitly accepted, Phase 3 would authorize:

- isolated prototype code under a dedicated experimental directory;
- synthetic fixtures implementing only approved `CORP` cases;
- minimal pinned development dependencies required for the two declared candidate slices;
- candidate-specific lock files, dependency inventories, SBOMs, and license reports;
- an ephemeral local SQLite database and an ephemeral local PostgreSQL test instance;
- local test-only process or container isolation needed to evaluate parser workers, with no production configuration or selected production runtime;
- disposable synthetic credentials and encryption keys that have no external authority;
- local execution of approved acceptance tests and fault-injection scenarios;
- documentation of evidence, failures, uncertainty, maintenance burden, and specialist review.

Approval would not authorize:

- authentication to Gmail, Google Workspace, Outlook, Microsoft, Apple services, or any other external account;
- reading, locating, inventorying, copying, hashing, parsing, or importing real correspondence or the live archive;
- cloud AI, hosted models, external embeddings, telemetry, analytics, or model-provider calls;
- production infrastructure, a production database, a production network listener, deployment, or public exposure;
- production Docker, ZFS, Tailscale, backup, or server configuration;
- a complete application, production schema, polished UI, provider importer, or production parser set;
- sending email, mutating preserved source, or exercising destructive operations outside disposable experiment state;
- a stack-selection ADR, a selected stack, a real-data dry run, a commit, or a push without separate approval.

## Experimental workspace boundary

After approval, all implementation material must remain under a clearly labeled experimental boundary such as:

```text
experiments/phase-3/
  README.md
  shared/
  cand-001/
  cand-003/
  fixtures/
  evidence/
```

The exact substructure may be refined during the design gate, but experimental code must not be placed in a production application tree or represented as a reusable deployment.

Every executable entry point must:

1. require an explicit synthetic-only marker;
2. accept input only from an allowlisted Phase-3 fixture root;
3. reject paths, symlinks, mounts, environment variables, or configuration that resolve outside the experiment boundary;
4. refuse input packages that do not carry the synthetic fixture marker and expected fixture identifiers;
5. use temporary output roots created specifically for the run;
6. emit no message bodies, addresses, token-shaped values, or attachment contents into routine logs;
7. fail closed when network denial, resource limits, or integrity preconditions cannot be established.

The experiments must never be pointed at the live archive, even for a metadata-only check.

## Comparison slices

### EXP-C001 — CAND-001 feasibility slice

The minimum slice may include:

- a supported Python/Django release;
- SQLite with FTS5;
- a command or minimal private test service that exercises preservation, derived state, deterministic Find, export, rebuild, backup, and restore;
- a minimal web safe-rendering probe sufficient to test hostile synthetic HTML and remote-resource blocking;
- an orchestrator for the shared external parser-worker protocol.

It must not include a complete application, general UI component system, provider authentication, production server configuration, or a migration commitment to SQLite.

### EXP-C003 — CAND-003 feasibility slice

The minimum slice may include:

- a supported Go release and a minimal private test API or command harness;
- an ephemeral PostgreSQL instance with built-in full-text search;
- a minimal SwiftUI/WebKit safe-rendering probe sufficient to test hostile synthetic HTML, navigation, storage, and remote-resource controls;
- an orchestrator for the same shared external parser-worker protocol;
- a disposable client/API credential flow sufficient to test unauthorized requests and revocation with synthetic credentials.

It must not include complete Mac, iPhone, or iPad applications, App Store/TestFlight distribution, production API design, provider authentication, or a commitment to PostgreSQL, Go, or SwiftUI.

### Shared experimental contracts

The two slices must use the same:

- synthetic source packages and expected outcomes;
- experimental preservation profile;
- parser-worker input/output protocol;
- application-independent export vocabulary;
- provenance and citation vocabulary;
- deterministic query cases and ordering rules;
- failure-injection cases;
- gate rubric and evidence template.

Candidate-specific shortcuts that make one result incomparable must be disclosed and treated as a gap.

## Workstream 1 — Preservation format and independent verification

### Question

Can source packages remain byte-identical, independently inventoried, tamper-evident, versioned, and verifiable without either candidate application?

### Authorized experiment after approval

Define one explicitly experimental preservation profile containing:

- source-package and source-item identifiers that contain no personal data;
- exact path/object-reference rules;
- byte lengths and at least one approved experimental cryptographic hash;
- algorithm identifiers and profile version;
- package membership and package-level integrity evidence;
- acquisition and verification events using synthetic identities only;
- explicit treatment of symlinks, extra files, missing files, ambiguous encodings, and malformed packages;
- a documented canonicalization rule wherever ordering or serialization affects integrity.

Implement independent verification in both candidate runtimes without sharing manifest-writing code. A package emitted by the CAND-001 slice must be verifiable by the CAND-003 verifier and vice versa. At least one verification path must require only the documented preservation profile and ordinary file/hash operations, not either application database.

### Evidence required

- exact byte equality for all accepted fixtures;
- successful independent cross-verification;
- deterministic detection of one-byte mutation, removal, addition, path escape, and unsupported profile version;
- proof that failed verification blocks parsing, indexing, export claims, and restore claims;
- mapping to PRES-001–015 and AT-P01–P07.

### Stop conditions

Stop the affected slice if it rewrites source, relies on parsed output to verify source, permits application state to redefine integrity, or cannot be independently checked.

## Workstream 2 — Application-independent export and migration

### Question

Can preserved bytes, manifests, provenance, user-authored history, processing generations, relationships, and declared omissions move between candidate implementations without requiring the exporting application?

### Authorized experiment after approval

Define a versioned experimental export bundle that documents:

- source packages and preservation evidence;
- provenance events and processing-rule identities;
- user-authored annotations and undo history;
- representative messages, people/identities, conversations, attachments/documents, organizations, topics, events, relationships, and timelines;
- machine-derived versus durable/user-controlled state;
- unsupported fields, omissions, partial status, and allowed packaging variance.

Run cross-migration in both directions:

1. CAND-001 synthetic state → independent export → empty CAND-003 derived store;
2. CAND-003 synthetic state → independent export → empty CAND-001 derived store.

Source hashes must remain identical. Canonical semantic records and user history must compare equal according to the documented export contract. Database dumps may support recovery but cannot serve as the independent export.

### Evidence required

- clean-environment enumeration without a running candidate application;
- complete and partial export behavior;
- repeat-export equivalence with allowed variance documented;
- two-way migration report listing transformed, preserved, unsupported, and rejected fields;
- mapping to PRES-016–020 and AT-R01–R03.

### Stop conditions

Stop if either candidate requires its database format, proprietary runtime, or undocumented code to interpret source bytes or user-controlled history.

## Workstream 3 — Derived-state rebuildability

### Question

Can each candidate delete and recreate all machine-derived state from verified source plus recorded rules while preserving user-authored history and preventing mixed generations?

### Authorized experiment after approval

For each slice:

- identify durable, user-controlled, and rebuildable records;
- record parser, extraction, normalization, tokenization, search, and relationship-rule versions;
- build derived records and search indexes from synthetic source packages;
- delete machine-derived state completely;
- rebuild into a clean derived store;
- compare deterministic outputs and explain permitted nondeterminism;
- change one processing-rule version and verify that prior output becomes stale or isolated;
- restore user-authored annotations/history and verify undo.

No AI model is needed or authorized. Model-derived fields may be represented by deterministic synthetic records solely to test provenance and nondeterminism labels.

### Evidence required

- complete durable/rebuildable inventory;
- rebuild report with inputs, versions, outputs, failures, skips, and integrity status;
- exact equality for deterministic derived records under the same generation;
- stale-generation and provenance-gap behavior;
- mapping to PRES-028–033 and AT-L01–L06.

### Stop conditions

Stop if machine-derived state becomes authoritative, rebuilding mutates source, or user-authored history is lost or silently rewritten.

## Workstream 4 — Parser-worker isolation and safe rendering

### Question

Can untrusted parsing and rendering be constrained by enforceable operating-system boundaries rather than language/framework promises?

### Authorized experiment after approval

Define one shared parser-worker protocol and at least one local experimental isolation profile covering:

- one synthetic input item mounted or exposed read-only;
- an empty scratch/output area;
- no credentials, archive write access, administrative capability, unrelated filesystem access, or external network;
- explicit CPU, memory, process, time, output-count, output-size, nesting, and expansion limits;
- structured success, unsupported, quarantine, timeout, crash, and policy-violation results;
- output validation before derived state accepts worker results.

The worker may be a deliberately small synthetic parser rather than a production email/parser library. Its purpose is to test the trust boundary, not source-family completeness.

Fault cases must include path traversal, absolute paths, symlink escape, decompression expansion, fork/process pressure, memory pressure, timeout, crash, malformed output, attempted network access, and attempted source write.

Safe-rendering probes must use hostile synthetic HTML and verify:

- plain-text safe representation is always available;
- scripts, forms, event handlers, plugins, application bridges, and active content do not execute;
- remote images, fonts, styles, trackers, links, and redirects do not load automatically;
- navigation is denied or requires explicit controlled action;
- cookies and persistent website storage are disabled for hostile content;
- source bytes remain separately accessible as evidence without entering the application origin or privileged native context.

### Evidence required

- zero successful writes outside scratch/output;
- zero source-byte changes;
- zero external network connections during execution;
- deterministic quarantine and recovery after every fault case;
- evidence that one worker failure does not corrupt the archive, derived store, or another job;
- mapping to THR-002–005, THR-008, AT-S01–S03, and AT-S06–S07.

### Stop conditions

Stop immediately if the isolation profile cannot be established, a worker escapes its boundary, hostile content executes, or source-controlled content initiates network traffic.

## Workstream 5 — Privacy and network-boundary enforcement

### Question

Can each slice operate meaningfully with external transfer denied and with inspectable boundaries around credentials, logs, caches, and routing?

### Authorized experiment after approval

- Run prototype execution with external network denied.
- Separate one-time dependency acquisition from experiment execution; dependency downloads, if needed, must come only from documented official registries, contain no project data, require no account, and be captured in lock/SBOM evidence.
- Use only disposable synthetic credentials and token-shaped fixture strings.
- Verify token-shaped correspondence content is never treated as authority and is redacted from routine logs.
- Exercise unauthorized requests, expired/revoked synthetic credentials, and missing-session behavior where a slice exposes a test service.
- Use a deterministic local model-router stub that has no network, tools, credentials, or source-write capability; it must fail closed rather than fall back to cloud.
- Inventory every experimental cache, temporary file, log, and telemetry path and verify cleanup/retention rules.

No local or cloud AI model is authorized. The router stub tests authority and fallback behavior only.

### Evidence required

- documented network and data-flow map;
- denied egress attempts visible without sensitive payloads;
- no telemetry or remote resource retrieval;
- synthetic credential creation, revocation, and cleanup evidence;
- log/cache/temp inventory and cleanup report;
- mapping to THR-006–011, THR-014, and AT-S04–S06, AT-S08, AT-S11.

### Stop conditions

Stop if any experiment requires a real credential, account, external AI, telemetry, public listener, uncontrolled egress, or live archive path.

## Workstream 6 — Backup, restore, and compromise recovery

### Question

Can each slice create a complete, independently verifiable synthetic backup and recover into a clean location after corruption or compromise?

### Authorized experiment after approval

For each candidate slice:

- define backup scope for source packages, manifests, provenance, user history, interpretation configuration, and database-consistent state;
- use only local temporary directories to simulate independent failure domains;
- use disposable synthetic encryption/recovery material if encryption is evaluated;
- create and verify a backup;
- restore into a clean, isolated root;
- compare source hashes and durable/user-controlled records;
- rebuild machine-derived state rather than trusting a compromised copy;
- inject stale, corrupt, partial, extra-file, missing-file, unavailable-key, and tampered-history cases;
- simulate compromise containment, synthetic credential revocation, trusted-point selection, clean restore, and derived rebuild.

SQLite backup must use a documented consistency mechanism rather than unsafe live copying. PostgreSQL recovery must include all state needed for the chosen experimental recovery method and must not treat successful dump verification as a substitute for restore.

### Evidence required

- reviewed backup inventory and exclusions;
- creation and periodic-verification procedure;
- clean-restore report;
- corruption, retention, key-loss, and compromise-recovery results;
- source and user-history equality after restore;
- mapping to PRES-021–027, THR-012–013, AT-R04–R08, AT-S10, and AT-S12.

### Stop conditions

Stop if a backup is declared valid without integrity verification and clean restore, if recovery trusts tainted derived state, or if any test can delete the only fixture source copy.

## Workstream 7 — Citation and deterministic-search contracts

### Question

Can both candidates produce stable Find results and reject unsupported citations using a common source/provenance contract?

### Authorized experiment after approval

Define and version:

- corpus and derived-generation identifiers;
- tokenizer, language configuration, collation, extraction version, field weights, query parser, ranking rule, and stable source-derived tie-breaker;
- query scope, filters, result limits, stale/incomplete-state behavior, and explainability record;
- citation targets for source items, MIME parts, attachment derivatives, and text spans;
- a deterministic validator that accepts only application-issued citation identifiers linked to the current verified generation.

Run the same query cases against SQLite FTS5 and PostgreSQL FTS. Repeated runs and full rebuilds must return the same ordered source identifiers for a fixed generation. Differences in tokenization or ranking are evidence to explain, not errors to hide.

Use deterministic synthetic answer records to test supported claims, inference labels, insufficient-evidence responses, fabricated citation identifiers, and provenance gaps. Do not call a model.

### Evidence required

- stable ordered results across repeated runs and rebuilds;
- explicit explanation of cross-engine result differences;
- source references independent of generated snippets;
- deterministic rejection of unknown, stale, unsupported, or mismatched citations;
- safe escaping/sanitization of excerpts;
- mapping to PRES-011–015, AT-L01, AT-L06, AT-M07–M08.

### Stop conditions

Stop if deterministic Find depends on model reranking, result order is implicit, excerpts execute as markup, or citations are accepted from unverified model text.

## Workstream 8 — Dependency, licensing, and maintenance evidence

### Question

Can each experimental slice be built and maintained with an inspectable, supportable, and legally reviewable dependency boundary?

### Authorized experiment after approval

Before candidate prototype code is considered build-ready, record:

- runtime, framework, database, parser-worker, rendering, test, build, and packaging components;
- exact direct versions and resolved transitive dependencies;
- official source location, artifact digest where available, license, notice obligation, maintainer, security policy, support window, and end-of-life date or policy;
- native-code, build-script, network-at-build, telemetry, and post-install behavior;
- lockfile and SBOM generation procedure;
- vulnerability/advisory review route;
- update, rollback, and unsupported-version response;
- clean rebuild instructions and required toolchains;
- estimated recurring maintenance actions and candidate exit steps.

Unknown, incompatible, abandoned, unverifiable, or restrictively licensed components must remain explicit. They cannot be converted to “acceptable” by a score.

### Evidence required

- complete direct and transitive inventory for the experimental slices;
- third-party notice report;
- unresolved-license and unsupported-component report;
- reproducible clean build or a documented failure;
- synthetic compromised/unverifiable dependency gate test;
- mapping to THR-010, G-09, STF-11–12, and AT-S09.

### Stop conditions

Stop the affected component if its provenance, license, ownership, support, or rollback path cannot be assessed, or if it requires an account, paid service, production credential, or unapproved network behavior.

## Gate-to-workstream matrix

| Gate | Primary workstreams | Minimum Phase-3 evidence for reconsideration |
|---|---|---|
| G-01 Source preservation | 1, 4 | Cross-verified byte-preserving packages; mutation and parser-write attempts denied/detected |
| G-02 Export independence | 2 | Independently readable complete/partial export with no candidate runtime requirement |
| G-03 Rebuildability | 3, 7 | Clean rebuild, generation isolation, stable deterministic outputs, complete rebuild report |
| G-04 Provenance and citations | 2, 3, 7 | End-to-end source/processing/citation trace and deterministic unsupported-citation rejection |
| G-05 Parser isolation | 4 | Enforceable no-network/read-only/resource-bounded worker and safe-rendering evidence |
| G-06 Privacy control | 4, 5 | Denied egress, synthetic credential separation, cache/log/temp controls, no cloud fallback |
| G-07 Backup and restore | 6 | Verified backup, clean restore, corruption/key-loss handling, compromise-recovery drill |
| G-08 Portable ownership | 1, 2 | Source plus user-controlled state cross-migrate without proprietary interpretation |
| G-09 Security maintenance | 5, 8 | Complete experimental SBOM/licenses/support/update/rollback evidence and supply-chain gate |
| G-10 Product boundary | All | Remains design-boundary `Pass`; experiments must preserve private, single-user, no-send, no-source-mutation scope |

## Synthetic corpus scope

Phase 3 may implement only synthetic fixtures derived from the accepted corpus design. The minimum set must cover:

- representative Gmail/Google Workspace export shape;
- Outlook/PST shape or a legally redistributable synthetic stand-in sufficient for package-boundary tests;
- Eudora mailbox, companion, and attachment-directory ambiguity;
- MBOX variants and EML/MIME messages;
- sent mail, attachments, provider metadata, duplicates, and junk classifications;
- malformed headers, encodings, MIME boundaries, line endings, and timestamps;
- hostile HTML, remote URLs, tracker-like resources, path traversal, expansion, crashes, and timeouts;
- synthetic identities, conversations, organizations, topics, events, relationships, and timelines;
- user annotations, corrections, undo history, provenance gaps, stale generations, and fabricated citations;
- backup, export, tamper, and compromise-recovery cases.

Every person, address, domain, message, attachment, identifier, token, and event must be invented for the fixtures. No fixture may be derived from real correspondence, even after redaction.

## Test execution rules

- Execute preservation and security tests before search, migration, or recovery claims are accepted.
- Use fresh temporary roots for independent verification, migration, restore, and rebuild tests.
- Record command, environment, dependency lock/SBOM identity, test IDs, inputs, outputs, duration, and result without sensitive payload logging.
- Treat `Blocked` as not passed.
- Repeat deterministic tests after a clean rebuild.
- Preserve failing evidence when safe, but never preserve unsafe executable output outside quarantine.
- Do not weaken a test to make a candidate pass; document the failure and remediation hypothesis.
- Candidate-specific tests must use equivalent fixtures and assertions unless the difference is itself the finding.

## Specialist review model

The orchestrator owns scope, sequencing, evidence integration, and stop conditions. Required independent review passes are:

- **Preservation/corpus:** workstreams 1–3 and 6; PRES-001–033; source-family completeness;
- **Security/privacy:** workstreams 4–6 and 8; THR-001–015; isolation, rendering, credentials, egress, recovery;
- **Research/AI:** workstream 7 and the model-router stub in workstream 5; citations, Find/Ask separation, prompt injection;
- **Product/UX:** safe-rendering behavior, error/quarantine/recovery presentation, and G-10 boundary preservation;
- **Quality/review:** fixture provenance, test determinism, candidate comparability, failure reproduction, and gate calibration;
- **Maintenance/supply chain:** workstream 8; support windows, build provenance, update, rollback, and operator burden;
- **Licensing/cost:** component terms, notice obligations, local-tooling costs, and five-year maintenance assumptions.

No specialist may turn an unexecuted test into a pass. Gate disagreement remains visible and calibrates to `Still Unproved` until resolved.

## Staged execution gates

### Gate 0 — Plan approval

The user reviews and explicitly accepts this plan. Until then, documentation planning only is authorized.

### Gate 1 — Experiment design

Produce, for review within the accepted plan:

- exact experiment directory layout;
- fixture manifest and synthetic-only safeguards;
- experimental preservation/export/citation/worker contracts;
- candidate dependency manifests and proposed acquisition sources;
- test-to-requirement traceability;
- rollback and cleanup procedure.

The orchestrator may proceed beyond Gate 1 only if no dependency or mechanism introduces an external service, account, cost, real-data path, production change, or material scope expansion. Such a change requires new user approval.

### Gate 2 — Safety baseline

Before candidate behavior is evaluated:

- verify fixtures are synthetic and allowlisted;
- establish external-network denial for execution;
- establish temporary roots and source read-only controls;
- confirm logs, caches, and evidence paths;
- record toolchain and dependency integrity.

Failure blocks further execution.

### Gate 3 — Build

Implement only the approved experimental slices and common contracts. Do not add product features, real importers, model integrations, or production configuration.

### Gate 4 — Verify

Run mapped synthetic tests, fault injection, cross-verification, migration, rebuild, restore, and supply-chain checks. Record Pass, Fail, or Blocked without reinterpretation.

### Gate 5 — Specialist review and calibration

Run all seven specialist passes. Update evidence, uncertainty, gap, disagreement, and rejection registers. Re-score gates and criteria without selecting a stack.

### Gate 6 — User acceptance

Present the complete Phase-3 diff and evidence package. The user decides whether to accept the evidence, request remediation, expand the candidate set, or end the evaluation. No stack-selection ADR is created in Phase 3.

## Deliverables after execution is authorized

Phase 3 would produce:

1. a synthetic-fixture manifest and provenance statement;
2. experimental preservation, export, rebuild, worker-isolation, rendering, privacy, backup, citation, and search contracts;
3. the two minimal candidate slices and shared test harness;
4. pinned dependency manifests, lock files, SBOMs, license/notice reports, and maintenance records;
5. machine-readable test results linked to accepted `AT` cases;
6. independent verification, two-way migration, rebuild, backup/restore, and compromise-recovery reports;
7. candidate-specific security and failure analyses;
8. seven specialist review reports;
9. updated Phase-2 evidence, uncertainty, gap, disagreement, rejection, gate, and weighted-score records;
10. a Phase-3 completion report stating which gates are Synthetic Pass, Fail, or Still Unproved.

These deliverables remain experimental evidence. They do not become production components by acceptance.

## Definition of done

Phase 3 is complete only when:

- every experiment used synthetic, independently documented fixtures;
- no account, real correspondence, live archive, cloud AI, external model, production system, or public service was accessed;
- every scoped requirement and test has a recorded outcome;
- source bytes remained unchanged and independently verifiable;
- cross-export/migration, rebuild, parser containment, safe rendering, denied egress, clean restore, and compromise recovery were exercised or explicitly remain Blocked;
- dependency, license, support, update, rollback, and cost evidence is complete for the experimental slices;
- all seven specialist reviews are complete;
- all disagreements, failures, and unknowns remain visible;
- the experiment workspace can be removed without affecting accepted documentation or any live system;
- the user reviews and accepts or rejects the complete evidence package.

Completion does not select a stack. If at least one candidate later has ten reviewed gate passes, returning to the Phase-2 ADR re-entry process requires a separate user instruction.

## Stop and escalation conditions

Stop the affected work and request user direction if:

- any input may contain real correspondence or private identifiers;
- a path could reach the live archive or non-experiment files;
- an account, credential, paid resource, external service, cloud AI, telemetry endpoint, or public listener is required;
- production infrastructure or durable deployment configuration would be changed;
- a parser, renderer, or worker escapes its boundary;
- source bytes change or integrity cannot be independently established;
- dependency provenance or licensing cannot be assessed;
- a candidate requires material redesign beyond its declared Phase-2 boundary;
- a destructive operation would affect anything outside disposable experiment state;
- an experiment would implicitly select a stack or weaken an accepted requirement.

## Approval record

On 2026-09-17, the user explicitly accepted this plan and authorized the narrowly bounded synthetic-only experiments, minimal pinned development dependencies, ephemeral local test services, disposable synthetic credentials and keys, deterministic local stubs, documented dependency acquisition, SBOMs, license reports, and local test execution described above.

The approval does not select a stack or authorize a stack-selection ADR, external accounts, real correspondence, the live archive, cloud AI, hosted models, telemetry, analytics, external embeddings, production infrastructure, deployment, public exposure, durable server configuration, sending email, or source mutation.

Per the approval instruction, execution stops at Gate 1 until the exact experiment layout, fixture manifest, safeguards, contracts, dependency manifests, rollback procedure, and test-to-requirement traceability are presented and reviewed. No prototype work may begin before that review.
