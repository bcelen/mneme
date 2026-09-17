# Phase-3 Test-to-Requirement Traceability

**Status:** Accepted
**Review date:** 2026-09-17
**Execution state:** No test has run. Every planned result is `Not executed`.

## Evidence identity

Each result record uses `P3-<candidate>-<test-id>-<run-id>` and names the fixture release, exact fixture IDs, contract versions, dependency-lock/SBOM digest, environment digest, command identity, start/end time, result, normalized evidence paths, and reviewer state.

`EXP-C001` and `EXP-C003` run equivalent assertions unless this matrix explicitly marks a candidate-specific probe. A missing result is `Blocked`, never implied pass. `Partial` below describes planned Phase-3 coverage, not a result.

## Preservation and lineage

| Test | Candidates | Fixtures | Governing contract / evidence | Workstream | Planned coverage |
|---|---|---|---|---:|---|
| AT-P01 | Both | CORP-001–006 | P-01; cross-verifier byte/membership report | 1 | Full |
| AT-P02 | Both | CORP-024 | P-01/W-01; denied-write and before/after digest evidence | 1, 4 | Full |
| AT-P03 | Both | CORP-024 | P-01; independent size/hash known-answer report | 1 | Full |
| AT-P04 | Both | CORP-024 | P-01; one-byte mutation stop evidence | 1 | Full |
| AT-P05 | Both | CORP-024 | P-01; missing/extra member stop evidence | 1 | Full |
| AT-P06 | Both | CORP-024, CORP-031 | P-01; explicit unsupported `v0.0` result | 1 | Full for failure path; no older production format implied |
| AT-P07 | Both | CORP-005, CORP-007–010 | P-01/W-01; warnings/quarantine plus unchanged bytes | 1, 4 | Full |
| AT-L01 | Both | CORP-031 | D-01/C-01; source-to-field lineage record | 3, 7 | Full |
| AT-L02 | Both | CORP-032 | D-01/E-01; append-only history and undo comparison | 3 | Full |
| AT-L03 | Both | CORP-031–033 | D-01; empty-store rebuild and equality report | 3 | Full |
| AT-L04 | Both | CORP-033 | D-01; stale/isolated generation result | 3 | Full |
| AT-L05 | Both | CORP-027, CORP-031, CORP-033 | C-01/F-01; deterministic stub identity, variance label, citations | 3, 7 | Partial: contract behavior only; no AI model |
| AT-L06 | Both | CORP-029, CORP-031 | C-01; provenance-gap rejection | 3, 7 | Full |

## Export, backup, and recovery

| Test | Candidates | Fixtures | Governing contract / evidence | Workstream | Planned coverage |
|---|---|---|---|---:|---|
| AT-R01 | Both, cross-import | CORP-035 | E-01; generic-tool enumeration and two-way migration | 2 | Full |
| AT-R02 | Both | CORP-035 | E-01; repeat semantic-equivalence report | 2 | Full |
| AT-R03 | Both | CORP-035 | E-01; partial marker and omission report | 2 | Full |
| AT-R04 | Both | CORP-034 | B-01/P-01; backup scope, checksums, membership | 6 | Full within simulated local failure domains |
| AT-R05 | Both | CORP-031–034 | B-01/D-01; clean restore and derived rebuild | 6 | Full |
| AT-R06 | Both | CORP-034 | B-01; stale/corrupt rejection before use | 6 | Full |
| AT-R07 | Both | CORP-034 | B-01; retention simulation preserving a valid source copy | 6 | Full |
| AT-R08 | Both | CORP-034 | B-01; unavailable synthetic age key fails safely | 6 | Full |

## Conceptual model, classification, Find, and Ask

| Test | Candidates | Fixtures | Governing contract / evidence | Workstream | Planned coverage |
|---|---|---|---|---:|---|
| AT-M01 | Both | CORP-001–013 | P-01/W-01; source-family package distinctions and retained metadata | 1, 4 | Partial: package shapes and small MIME cases; no production importers and no PST proof |
| AT-M02 | Both | CORP-014 | D-01/E-01; explainable links and unresolved candidates | 2, 3 | Full synthetic rule case |
| AT-M03 | Both | CORP-016 | D-01/E-01; provider evidence and visible disagreement | 2, 3 | Full synthetic rule case |
| AT-M04 | Both | CORP-015, CORP-017–019, CORP-029 | D-01/E-01/C-01; evidence, uncertainty, non-claim assertions | 2, 3, 7 | Full synthetic rule case |
| AT-M05 | Both | CORP-020–022 | D-01/E-01/P-01; preserved occurrences and reversible relations | 3 | Full |
| AT-M06 | Both | CORP-023, CORP-032 | D-01/E-01; reversible junk history and unchanged source | 3 | Full |
| AT-M07 | Both | CORP-001–024, CORP-033 | F-01; repeated/rebuilt ordered IDs and source references | 7 | Full within fixed synthetic scale |
| AT-M08 | Both | CORP-018–019, CORP-027, CORP-029 | C-01/F-01; deterministic claims, uncertainty, fabricated-citation rejection | 7 | Partial: Ask contract only; no model quality claim |

## Security and privacy

| Test | Candidates | Fixtures | Governing contract / evidence | Workstream | Planned coverage |
|---|---|---|---|---:|---|
| AT-S01 | C001 web + C003 WebKit | CORP-025 | R-01; render assertions and zero-request canary | 4 | Full for minimal probes |
| AT-S02 | Both/shared worker | CORP-011, CORP-013, CORP-026 | W-01; isolation/resource evidence | 4 | Full for synthetic worker boundary; not production parser assurance |
| AT-S03 | Both/shared worker | CORP-026 | W-01; traversal/expansion containment | 4 | Full |
| AT-S04 | Both/stub | CORP-027–028 | C-01/F-01/N-01; no tools/authority/policy change | 5, 7 | Full for deterministic stub |
| AT-S05 | Both | CORP-030 | N-01; redaction and authentication-source separation | 5 | Full |
| AT-S06 | Both + render probes | CORP-012, CORP-025, CORP-028 | W-01/R-01/N-01; denied egress and canary evidence | 4, 5 | Full only if network denial is independently observed; otherwise Blocked |
| AT-S07 | Both/shared worker | CORP-013, CORP-026 | W-01; crash/timeout containment and next-job recovery | 4 | Full |
| AT-S08 | Both | All | N-01; synthetic unauthorized/expired/revoked session evidence | 5 | Full for local test surfaces |
| AT-S09 | Both | Synthetic dependency evidence | Dependency manifest; missing/wrong digest and graph-drift gate | 8 | Full for experimental inputs |
| AT-S10 | Both | CORP-034 | B-01; encrypted/tampered backup outcomes | 6 | Full with synthetic keys |
| AT-S11 | Both/stub | CORP-028 | N-01; blocked unapproved route and no cloud fallback | 5 | Full |
| AT-S12 | Both | CORP-031, CORP-034 | B-01/D-01; isolate, revoke, trusted restore, provenance review, rebuild | 6 | Full synthetic drill |

## UX and operations

| Test | Candidates | Fixtures | Governing contract / evidence | Workstream | Planned coverage |
|---|---|---|---|---:|---|
| AT-U01 | C001 responsive contract + C003 minimal Mac probe | Representative synthetic records | R-01/C-01 plus product/UX walkthrough | 4, 7 | Partial: no complete Mac, iPhone, or iPad app; cross-device product quality remains unproved |
| AT-U02 | Both | CORP-024, CORP-033–035 | P-01/D-01/B-01; operator-state/error review | 1, 3, 6 | Partial: synthetic single-user procedure, not production maintenance |
| AT-U03 | Both | Fixed small/boundary descriptors | Recorded budgets and accessibility checklist | Cross-cutting | Partial: budgets and probe measurements only; representative corpus scale remains unproved |

## Preservation-contract coverage

| Requirement group | Contract and tests | Evidence owner |
|---|---|---|
| PRES-001–005 source boundary | P-01; AT-P01–P02, AT-P07, AT-M01 | Preservation/corpus |
| PRES-006–010 hashes/manifests | P-01; AT-P03–P06 | Preservation/corpus + quality/review |
| PRES-011–015 provenance/traceability | P-01, D-01, C-01; AT-L01–L02, AT-L06 | Preservation/corpus + research/AI |
| PRES-016–020 exportability | E-01; AT-R01–R03 | Preservation/corpus + quality/review |
| PRES-021–027 backup/restore | B-01; AT-R04–R08 | Preservation/corpus + security/privacy |
| PRES-028–033 rebuildability | D-01, C-01, F-01; AT-L03–L05, AT-M07 | Preservation/corpus + quality/review |

## Threat coverage

| Threats | Principal tests | Required review |
|---|---|---|
| THR-001 acquisition scope | Preflight and synthetic marker release checks; AT-M01 boundary evidence | Preservation/corpus + security/privacy |
| THR-002–005 hostile content/isolation/resources | AT-S01–S03, AT-S06–S07 | Security/privacy + quality/review |
| THR-006 prompt injection | AT-S04, AT-M08 | Research/AI + security/privacy |
| THR-007 credentials | AT-S05, AT-S08 | Security/privacy |
| THR-008 egress | AT-S06, AT-S11 | Security/privacy |
| THR-009 unauthorized access | AT-S08 | Security/privacy + product/UX |
| THR-010 supply chain | AT-S09 and dependency freeze | Maintenance/supply chain + licensing/cost |
| THR-011 logs/caches/temp | AT-S05, AT-S08 and cleanup evidence | Security/privacy |
| THR-012 backup/export | AT-R04–R08, AT-S10 | Preservation/corpus + security/privacy |
| THR-013 compromise recovery | AT-S07, AT-S10, AT-S12 | Orchestrator + security/privacy |
| THR-014 unapproved cloud | AT-S11 | Research/AI + security/privacy |
| THR-015 evidence tampering | AT-P03–P06, AT-L01–L06 | Preservation/corpus + quality/review |

## Gate and gap closure targets

| Phase-2 gap | Phase-3 target | Gate impact if reviewed evidence passes |
|---|---|---|
| GAP-001 | P-01 plus cross-verification and mutation stops | G-01 may move to Synthetic Pass |
| GAP-002 | E-01 plus independent two-way migration | G-02 and G-08 evidence strengthened |
| GAP-003 | D-01 plus clean rebuild/generation isolation | G-03 may move to Synthetic Pass |
| GAP-004 | C-01 plus lineage and fabricated-citation rejection | G-04 may move to Synthetic Pass at synthetic-contract level |
| GAP-005–006 | W-01/R-01 plus escape, fault, rendering, and egress evidence | G-05 may move to Synthetic Pass only with enforceable boundaries |
| GAP-007 | N-01 plus data-flow, denied routes, log/cache cleanup | G-06 evidence strengthened |
| GAP-008 | B-01 plus clean restore and compromise drill | G-07 may move to Synthetic Pass |
| GAP-009 | E-01 two-way clean-store import and field report | G-08 evidence strengthened |
| GAP-010 | Frozen graphs, SBOMs, licenses, offline build, AT-S09 | G-09 evidence strengthened |
| GAP-011 | Minimal workflow/error/recovery review | G-10 remains boundary Pass; product depth remains limited |
| GAP-012 | Small synthetic measurements and declared budgets | STF-07/08/12 remain provisional; no production scale claim |
| GAP-013 | Tool/acquisition/maintenance observations only | STF-12 remains incomplete without five-year assumptions |
| GAP-014 | Source-shape packages and worker protocol | Parser boundary evidence improves; production format coverage remains open |
| GAP-015 | Deterministic local router/citation stub | Authority/citation contract improves; model runner remains unselected |
| GAP-016 | Synthetic Eudora package shape | Ambiguity handling evidence only; actual format knowledge remains open |

## Specialist review assignments

| Review | Must inspect | Trigger for mandatory rerun |
|---|---|---|
| Preservation/corpus | Fixture release, P-01/E-01/D-01/B-01, AT-P/L/R/M evidence | Fixture/source-family, manifest, export, rebuild, or backup-contract change |
| Security/privacy | Safeguards, W-01/R-01/N-01/B-01, AT-S evidence, cleanup | Worker/runtime, renderer, credential, network, parser, backup, or recovery change |
| Research/AI | C-01/F-01/N-01 router behavior, AT-L05/L06/M07/M08/S04/S11 | Citation, query, prompt boundary, routing, or Ask-stub change |
| Product/UX | Safe render, errors/quarantine, citations, recovery state, AT-U evidence | User-visible workflow or client-probe change |
| Quality/review | Expected truth, independent implementations, deterministic reruns, trace links | Test, comparator, evidence schema, or result-calibration change |
| Maintenance/supply chain | Dependency graph, artifact integrity, SBOM, advisories, offline build, rollback | Any version, source, build input, image, or update-policy change |
| Licensing/cost | License/notice report, distribution obligations, acquisition and maintenance observations | Any dependency/license/distribution or material cost assumption change |

The orchestrator checks completeness and disagreement but cannot replace a specialist pass. Material disagreement is recorded, and the affected outcome remains `Still Unproved` until resolved.

## Gate-1 definition of done

Gate 1 is reviewable when this package has an exact layout, all 35 fixture intents, fail-closed safeguards, versioned contracts, proposed dependency pins and acquisition boundaries, cleanup rules, and complete acceptance-test mapping. It is accepted only by explicit user approval. Acceptance authorizes the Gate-2 safety baseline; it does not itself mark any acceptance test or stack gate passed.
