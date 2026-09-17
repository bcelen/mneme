# Seven Specialist Reviews

**Status:** Accepted
**Review date:** 2026-09-17
**Evidence cutoff:** 2026-09-17

## Review method and limits

Seven role-separated review passes assessed the same four candidates against the accepted artifacts. These are specialist analytic passes coordinated by the project orchestrator; they are not independent human audits, legal advice, security certification, or user approval. Each pass used primary documentary evidence and identified later acceptance tests. No prototype, dependency installation, account access, real-data inspection, or test execution occurred.

The orchestrator may correct factual or rubric inconsistencies, but cannot erase substantive dissent. Under the accepted plan, unresolved gate dissent is calibrated to `Unproved`, not averaged into `Pass`.

## Review 1 — Preservation and corpus

**Scope:** G-01–G-03, G-07–G-08; STF-01–03, STF-08–09; PRES-001–033 and source-family fit.

**Finding:** Qualified continuation for all candidates. The common filesystem source boundary makes byte-preserving acquisition, independent manifests, portable export, and rebuildable indexes architecturally feasible. SQLite and PostgreSQL both have documented consistent-backup paths and rebuildable full-text indexes. Neither database is the preservation authority.

**Reservations:** Archive write enforcement, manifest/hash profile, provenance/user-history export, Eudora package boundaries, database-consistent coordinated backup, clean restore, parser behavior, and all preservation tests remain unproved. The review would reject any design that round-trips parsed MBOX/EML/PST as source, discards provider containers, or treats a database/index as the only authoritative copy.

**Role outcome:** Proposed design-level `Pass` for G-01–G-03, G-07–G-08, with Medium confidence. Quality and security dissent is recorded in DIS-001–004; the calibrated matrix is `Unproved` until GAP-001–009 close.

## Review 2 — Security and privacy

**Scope:** G-05–G-07, G-09; STF-04–05, STF-08, STF-11; THR-001–015.

**Finding:** Continue comparing all candidates; no security-based rejection. No candidate currently passes the security-led gates.

**Reservations:** The parser isolation objective lacks an enforceable worker profile; safe HTML/attachment rendering is unspecified; egress, caches, logs, telemetry, sessions, credentials, backup encryption, key recovery, compromise recovery, dependency inventories, and update/rollback rules are incomplete. Runtime memory safety, template escaping, Node permissions, App Sandbox, or private networking cannot replace operating-system isolation and application authorization.

**Role outcome:** G-05, G-06, G-07, and G-09 `Unproved` for all candidates. CAND-001 has the smallest operational surface; CAND-003 has useful native isolation facilities; the difference is below uncertainty. Required resolution is GAP-005–010 and GAP-015 plus AT-S01–S12/AT-R04–R08.

## Review 3 — Product and UX

**Scope:** G-10; STF-06–07; Mac/iPhone/iPad workflows, accessibility, performance, offline assumptions, and failure-state comprehension.

**Finding:** Every candidate can credibly remain a private single-user research product without sending mail, mutating source, or requiring public exposure. SwiftUI is the strongest documented platform-native capability; browser/PWA candidates reduce distribution and maintenance burden; Flutter offers shared code but needs deliberate Apple adaptation.

**Reservations:** No candidate has actual Mneme workflows, offline/cache semantics, performance budgets, device matrix, real-device accessibility evidence, or tested recovery-state UX. “PWA,” “native,” and “shared code” are capabilities, not outcomes.

**Role outcome:** G-10 `Pass` at design-boundary level. STF-06: CAND-001 `3`, CAND-002 `3`, CAND-003 `4`, CAND-004 `3`. STF-07 remains Unknown in the calibrated score because there are no common budgets or tests. AT-U01–U03 remain mandatory.

## Review 4 — Research and AI

**Scope:** G-04, G-06; STF-05, STF-10; deterministic Find, grounded Ask, citations, routing, and prompt injection.

**Finding:** SQLite FTS5 and PostgreSQL FTS both provide credible deterministic Find foundations when generation, tokenizer/configuration, collation, ranking, and total ordering are versioned. All candidates can separate Find from Ask and retain source identifiers and model records. No candidate receives a research/AI preference on documentary evidence alone.

**Reservations:** Citation contract, exact retrieval record, model runner, egress enforcement, no-fallback behavior, prompt-injection defenses, and local-model suitability are absent. RAG does not neutralize indirect prompt injection. Search excerpts require independent escaping/sanitization.

**Role outcome:** Proposed design-level `Pass` for G-04/G-06, but security/quality dissent makes both `Unproved` in the calibrated matrix. STF-10 is `3` with Low confidence for all candidates. STF-05 remains Unknown after calibration. AT-L01/L05/L06, AT-M07/M08, AT-S04/S05/S06/S11 remain mandatory.

## Review 5 — Quality and review

**Scope:** Candidate completeness, evidence sufficiency, gate consistency, score calibration, AT traceability, uncertainty, and rejected alternatives.

**Finding:** Pass to continue evaluation; not approved for stack selection. The normalized candidate records cover the required categories, but the exact preservation, isolation, privacy, recovery, export, and maintenance mechanisms are still too incomplete for mandatory-gate passage.

**Reservations:** Capability documentation must not be treated as Mneme evidence. All relevant acceptance tests remain unexecuted. Candidate complexity must include services, clients, distribution, caches, parsers, and operations hidden outside the framework label.

**Role outcome:** G-01–G-09 `Unproved`, G-10 `Pass`. Only STF-06, STF-09, STF-10, and STF-11 have supportable partial scores; evidence coverage is 26%. The observed score spread is not decision-significant.

## Review 6 — Maintenance and supply chain

**Scope:** G-09; STF-08, STF-11; release support, dependency ownership, vulnerabilities, build provenance, rollback, operational ownership, and end-of-life migration.

**Finding:** All named ecosystems have active projects, public security processes, and viable supported-release paths. CAND-001 has the smallest declared service boundary. CAND-003 combines a relatively small Go service with Apple release work. CAND-002 and CAND-004 expose broader multi-package/toolchain surfaces.

**Reservations:** This is pre-dependency evidence. No candidate has an SBOM, parser/model inventory, third-party notice process, advisory ownership, patch deadlines, artifact verification, rollback, secret rotation, or end-of-life plan. Rust's project policy excludes third-party crates; Node's aggregate distribution contains separately licensed components; Flutter plugins and Apple tooling add external lifecycles; Python parsers also require independent ownership review.

**Role outcome:** G-09 `Unproved`. STF-11: CAND-001 `3`, CAND-002 `2`, CAND-003 `3`, CAND-004 `2`, all Low-to-Medium confidence. STF-08 remains Unknown because no complete operational model or restore evidence exists.

## Review 7 — Licensing and cost

**Scope:** STF-11–12; direct and transitive terms, distribution, Apple tooling, cash/labor cost, and exit cost.

**Finding:** No headline direct-component license blocks any candidate. Django, Python, SQLite, Next.js, Node, PostgreSQL, Swift, Go, Flutter, Dart, Rust, and Axum have permissive or public-domain core terms, subject to notices and component-specific obligations. CAND-001 currently has the smallest obvious cash and operating boundary; CAND-003/004 have Apple-controlled signing/distribution considerations.

**Reservations:** No transitive inventory, parser/model terms, five-year cash-and-labor model, hardware/backup inventory, or legal review exists. Swift's open-source license does not define SwiftUI/Apple SDK terms. Free personal provisioning is not a credible low-maintenance production baseline.

**Role outcome:** No licensing rejection. G-08 receives no licensing objection; G-09 remains `Unproved`. STF-12 remains Unknown. Cost scenarios may record zero software fees, the current USD 99/year Apple membership where applicable, and unknown hardware/storage/maintenance costs, but cannot produce a defensible TCO.

## Cross-review calibration

| Question | Agreed result |
|---|---|
| Is any candidate known to conflict irreparably with an accepted requirement? | No. There are no `Fail` gates. |
| Has any candidate proved all mandatory gates? | No. G-01–G-09 are calibrated to `Unproved`; G-10 passes at design-boundary level. |
| Can a weighted score select a candidate? | No. Only 26% of weighted criteria have supportable scores and the differences are smaller than uncertainty. |
| Is parser implementation ordinary deferred work? | The parser libraries may be deferred, but the isolation, IPC, resource, quarantine, and rendering architecture must be defined before G-05 can pass. |
| Does local-only AI remove prompt injection risk? | No. It limits exfiltration but not answer manipulation; content receives no authority. |
| Do database backups satisfy Mneme export or recovery by themselves? | No. Source, manifests, user history, configuration, keys, clean restore, and compromise recovery are separate obligations. |
| Is native UI automatically better? | No. SwiftUI has the strongest capability evidence, but workflows and accessibility still require design and tests. |

## Review-trigger summary

Repeat the affected specialist review before accepting a stack, choosing a parser or renderer, defining export/manifest formats, enabling any model or network route, choosing authentication or backup topology, changing supported devices, adopting a dependency set, approving Apple distribution, beginning a real-data dry run, or deploying a service.
