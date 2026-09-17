# Gate and Weighted-Criteria Scorecard

**Status:** Accepted
**Review date:** 2026-09-17
**Evidence cutoff:** 2026-09-17
**Scoring boundary:** Documentary Phase-2 evidence only. No implementation, synthetic-corpus execution, or acceptance-test result exists.

## Calibration rules applied

- Unresolved gate-status disagreement is `Unproved`.
- A documented generic capability is not a Mneme implementation result.
- Unknown criteria are not scored as zero.
- Assertion-only evidence cannot exceed 2; supportable capability evidence can receive a provisional 3 or 4 when its limitations are explicit.
- Numerical totals never override gate status.
- The same common preservation, security, AI, export, and recovery contract applies to all candidates.

## Mandatory gates

`P` means Phase-2 design `Pass`; `U` means `Unproved`. There are no `Fail` results.

| Gate | CAND-001 | CAND-002 | CAND-003 | CAND-004 | Governing evidence, gap, and later tests |
|---|:---:|:---:|:---:|:---:|---|
| G-01 Source preservation | U | U | U | U | Source boundary is credible, but GAP-001/GAP-014 remain; AT-P01–P07 |
| G-02 Export independence | U | U | U | U | Portable intent exists, but GAP-002 remains; AT-R01–R03 |
| G-03 Rebuildability | U | U | U | U | FTS/index rebuild is documented, but GAP-003 and UNC-015 remain; AT-L02–L05, AT-R05 |
| G-04 Provenance and citations | U | U | U | U | Relational lineage is feasible, but GAP-004/GAP-015 remain; AT-L01/L05/L06, AT-M08 |
| G-05 Parser isolation | U | U | U | U | Common worker contract is directional; GAP-005/GAP-006 remain; AT-S01–S07 |
| G-06 Privacy control | U | U | U | U | Default-local intent is credible; GAP-007/GAP-015 remain; AT-S05/S06/S08/S11 |
| G-07 Backup and restore | U | U | U | U | Database mechanisms exist; GAP-008 remains; AT-R04–R08, AT-S10/S12 |
| G-08 Portable ownership | U | U | U | U | Source bytes are portable; exported history/migration evidence in GAP-002/GAP-009 is missing; AT-R01/R05 |
| G-09 Security maintenance | U | U | U | U | Direct support policies exist; GAP-010/GAP-014/GAP-015 remain; AT-S09/S12 |
| G-10 Product boundary | P | P | P | P | All candidates inherit private single-user, no-send, no-source-mutation boundaries; AT-U01–U03 remain implementation validation |

**Eligibility:** `0/4` candidates are eligible for a stack-selection ADR because each has at least one `Unproved` mandatory gate.

## Twelve weighted criteria

`U` means Unknown. Numeric entries are `score / 5` followed by confidence (`M` Medium, `L` Low).

| Criterion | Weight | CAND-001 | CAND-002 | CAND-003 | CAND-004 | Calibration rationale |
|---|---:|:---:|:---:|:---:|:---:|---|
| STF-01 Byte fidelity and preservation boundary | 14 | U | U | U | U | Common source design is promising; archive enforcement/profile disputed under DIS-001 |
| STF-02 Integrity, manifests, provenance, citations | 10 | U | U | U | U | GAP-001/GAP-004 prevent comparable scores |
| STF-03 Rebuildability and independent export | 10 | U | U | U | U | FTS rebuild capability is insufficient without GAP-002/GAP-003 |
| STF-04 Security isolation and hostile content | 15 | U | U | U | U | Security lead holds G-05 Unproved; GAP-005/GAP-006 |
| STF-05 Privacy, local-first, controlled hybrid AI | 10 | U | U | U | U | Default-local intent exists, but GAP-007/GAP-015 and DIS-005 remain |
| STF-06 Cross-device product quality | 10 | 3 M | 3 M | 4 M | 3 M | Web/PWA routes are credible; SwiftUI has strongest native capability; all UX untested |
| STF-07 Performance and accessibility | 5 | U | U | U | U | No common budgets, workload, or device/accessibility tests; GAP-011/GAP-012 |
| STF-08 Operational simplicity, backup, restore, observability | 8 | U | U | U | U | Service-count differences exist but complete recovery/operations are absent |
| STF-09 Portability and replaceable boundaries | 6 | 4 M | 4 M | 3 M | 3 M | Web candidates have portable clients; native data remain portable but Apple distribution/client replacement adds coupling |
| STF-10 Deterministic Find and grounded Ask | 5 | 3 L | 3 L | 3 L | 3 L | Both FTS engines are credible; citation, generation, router, and tests remain open |
| STF-11 Maintainability, ecosystem, supply chain | 5 | 3 M | 2 M | 3 M | 2 M | CAND-001 has the smallest service surface; Go policies aid CAND-003; Node/Next and Flutter/Rust have broader lifecycle surfaces |
| STF-12 Total cost and resource fit | 2 | U | U | U | U | No five-year TCO or hardware/labor assumptions; GAP-013 |

## Weighted results and uncertainty

The assessed weight is 26%. The remaining 74% is Unknown and contributes nothing to the confirmed score.

| Candidate | Confirmed weighted score | Potential range | Evidence coverage | Confidence profile | Principal unresolved discriminator |
|---|---:|---:|---:|---|---|
| CAND-001 | **16.8** | 16.8–90.8 | 26% | 21 weight Medium; 5 Low; 74 Unknown | SQLite workload/recovery versus minimal operations |
| CAND-002 | **15.8** | 15.8–89.8 | 26% | 21 Medium; 5 Low; 74 Unknown | PWA richness versus dependency/service burden |
| CAND-003 | **17.6** | 17.6–91.6 | 26% | 21 Medium; 5 Low; 74 Unknown | Native UX value versus Apple and multi-client maintenance |
| CAND-004 | **14.6** | 14.6–88.6 | 26% | 21 Medium; 5 Low; 74 Unknown | Shared client code versus Flutter/Rust/platform lifecycle burden |

The supported totals are not rankings. CAND-003's 0.8-point lead over CAND-001 is immaterial relative to 74 points of Unknown evidence and unresolved gate dissent. CAND-001 is the operations reference; CAND-003 is the UX reference; CAND-002 and CAND-004 remain credible comparison candidates.

## Candidate-specific validation debt

### CAND-001

- SQLite lock-contention, WAL/backup coherence, long-running import and rebuild scheduling, FTS build/configuration, deterministic ordering, and migration thresholds.
- Deliberate mobile/PWA navigation, cache policy, and richer interaction without expanding the dependency surface invisibly.

### CAND-002

- Exact Next.js/Node service and worker boundary, server/client data exposure, cache invalidation, service-worker scope, dependency inventory, private ingress, and PostgreSQL coordinated restore.
- Proof that richer client behavior adds enough product value to justify the operating and supply-chain surface.

### CAND-003

- Versioned API, bounded client cache, device revocation, three-platform workflow design, signing/distribution, Apple toolchain support, PostgreSQL recovery, and total maintenance effort.
- Proof that native interaction materially improves Mneme's research workflows over the web candidates.

### CAND-004

- Flutter platform fidelity, plugin/native-bridge inventory, accessibility, latest-Apple-platform validation, Rust/crate ownership, Axum operational boundary, signing/distribution, and PostgreSQL recovery.
- Proof that client-code sharing offsets the two-toolchain and platform-adaptation burden.

## Acceptance-test debt carried forward

Every applicable accepted test remains `Unproved`. The most decision-critical groups are:

- AT-P01–P07 and AT-L01–L06 for preservation, lineage, rebuilds, and user history;
- AT-R01–R08 for export, backup, clean restore, retention, and key loss;
- AT-M01 and AT-M07–M08 for source-family coverage, deterministic Find, and grounded Ask;
- AT-S01–S12 for hostile content, parser isolation, credentials, egress, supply chain, and compromise recovery;
- AT-U01–U03 for cross-device workflows, maintenance comprehension, accessibility, and performance.

No score in this document claims those tests passed.
