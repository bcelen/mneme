# Acceptance-Test Matrix

**Status:** Accepted
**Review date:** 2026-09-17
**Authority:** ADR-002, ADR-003, and ADR-004
**Execution status:** Test definitions only; no test code or dependencies have been added.

## Result vocabulary

- **Pass:** Required evidence is present and every prohibited side effect is absent.
- **Fail:** A required assertion is false, evidence is missing, or an unexplained side effect occurs.
- **Blocked:** A separately gated capability is unavailable; blocked is never counted as pass.
- **Not applicable:** Permitted only with written justification and reviewer approval.

All tests run first on the synthetic corpus. Real-data execution requires the separate dry-run approval in ADR-006.

## Preservation and integrity

| Test ID | Scenario | Required result | Requirement / fixture links |
|---|---|---|---|
| AT-P01 | Preserve a complete synthetic source package | Preserved bytes and package membership equal the supplied fixture; no normalization | PRES-001–005; CORP-001–006 |
| AT-P02 | Attempt mutation of a preserved item through processing paths | Mutation is denied or detected; source hash and bytes remain unchanged | PRES-002; CORP-024 |
| AT-P03 | Verify known hashes and byte lengths | Independently calculated values match the manifest | PRES-006–008; CORP-024 |
| AT-P04 | Change one byte after preservation | Integrity verification fails and downstream processing stops | PRES-009; CORP-024 |
| AT-P05 | Remove or add a package member | Completeness verification fails and identifies the discrepancy | PRES-003, PRES-009; CORP-024 |
| AT-P06 | Verify an older supported manifest convention | Verification succeeds or gives an explicit unsupported-version failure; never silent acceptance | PRES-010; versioned CORP-031 |
| AT-P07 | Parse malformed or ambiguous source | Source bytes remain unchanged; warnings or quarantine capture ambiguity | PRES-004; CORP-005, CORP-007–010 |

## Provenance and derived-data reversibility

| Test ID | Scenario | Required result | Requirement / fixture links |
|---|---|---|---|
| AT-L01 | Trace a derived field to source | Trace includes source item, parser/rule identity, version, event, and outcome | PRES-011–014; CORP-031 |
| AT-L02 | Correct a user annotation | Prior state remains in recorded history and undo restores it | PRES-015, PRES-029; CORP-032 |
| AT-L03 | Delete all machine-derived state and rebuild | Rebuild completes from source plus recorded rules without source mutation | PRES-028, PRES-031, PRES-033; CORP-031–033 |
| AT-L04 | Change a processing-rule version | Prior generation is marked stale or isolated; generations are not silently mixed | PRES-032; CORP-033 |
| AT-L05 | Recreate nondeterministic derived output | Report identifies model/context/version and allowed variance; citations remain traceable | PRES-030, PRES-033; CORP-027, CORP-031 |
| AT-L06 | Encounter a provenance gap | Affected output is blocked or prominently marked unsupported; no fabricated lineage | PRES-014; CORP-029, CORP-031 |

## Export, backup, and recovery

| Test ID | Scenario | Required result | Requirement / fixture links |
|---|---|---|---|
| AT-R01 | Produce an application-independent export | Independent inspection can enumerate source bytes, manifests, provenance, and documented derived data without Mneme | PRES-016–018; CORP-035 |
| AT-R02 | Repeat an export from unchanged inputs | Content is equivalent; allowed packaging variance is documented | PRES-019; CORP-035 |
| AT-R03 | Inject a partial-export failure | Export is marked incomplete, omissions are listed, and it is not presented as a valid complete export | PRES-020; CORP-035 |
| AT-R04 | Verify a newly created synthetic backup | Hashes, manifest membership, scope, and exclusions validate | PRES-021–024; CORP-034 |
| AT-R05 | Restore into an isolated clean environment | Restored source equals original; provenance and user history recover; derived state can rebuild | PRES-025, PRES-028–033; CORP-034 |
| AT-R06 | Restore a stale or corrupted backup | Validation rejects or clearly identifies the stale/corrupt state before use | PRES-024–025; CORP-034 |
| AT-R07 | Simulate retention and deletion | No policy path can remove the only valid source copy or required provenance | PRES-027; CORP-034 |
| AT-R08 | Simulate unavailable recovery secret | Recovery fails safely with a documented escalation path and no data exposure | PRES-023; CORP-034 |

## Source-model and classification behavior

| Test ID | Scenario | Required result | Requirement / fixture links |
|---|---|---|---|
| AT-M01 | Import equivalent source shapes from each planned family | Each package remains distinguishable and traceable; source-specific metadata is retained | CORP-001–006 |
| AT-M02 | Resolve identity candidates | Supported links are explainable; ambiguous identities remain unresolved; no silent person merge | CORP-014 |
| AT-M03 | Reconstruct conversations | Provider threading is evidence, not unquestioned truth; missing and conflicting links remain visible | CORP-016 |
| AT-M04 | Model organizations, topics, events, relationships, and timelines | Every derived assertion has evidence and uncertainty; absence of evidence is not converted to a fact | CORP-015, CORP-017–019, CORP-029 |
| AT-M05 | Classify exact and logical duplicates | Source occurrences remain preserved; classification is reversible and provenance-bearing | PRES-002, PRES-029; CORP-020–022 |
| AT-M06 | Classify junk and revise the classification | No source deletion occurs; history or reconstruction satisfies reversibility | PRES-015, PRES-029; CORP-023, CORP-032 |
| AT-M07 | Deterministic Find over a fixed corpus generation | Repeated identical queries produce identical scoped results and source references | CORP-001–024 |
| AT-M08 | AI Ask over sufficient and insufficient evidence | Supported claims cite sources; inference is labeled; insufficient evidence yields uncertainty rather than invention | CORP-018–019, CORP-027, CORP-029 |

## Security and privacy

| Test ID | Scenario | Required result | Requirement / fixture links |
|---|---|---|---|
| AT-S01 | Render hostile HTML | No script, form, tracker, remote resource, or deceptive navigation executes; source remains available as evidence | THR-002; CORP-025 |
| AT-S02 | Process a hostile or malformed attachment | Processing is isolated and bounded; executable behavior is blocked; failure does not affect the archive | THR-003–005; CORP-011, CORP-013, CORP-026 |
| AT-S03 | Process archive traversal and expansion fixtures | Paths cannot escape isolation; resource limits stop excessive expansion | THR-004–005; CORP-026 |
| AT-S04 | Present prompt injection to AI/agent workflow | Embedded instructions receive no authority, trigger no tools, and cannot alter policy or source data | THR-006; CORP-027–028 |
| AT-S05 | Present token-shaped strings in source | Values are treated as content, redacted from logs, and never used as credentials | THR-007, THR-011; CORP-030 |
| AT-S06 | Run importer/parser with network denied | Parsing succeeds where network is unnecessary; no source content causes outbound traffic | THR-001, THR-002, THR-008; CORP-012, CORP-025, CORP-028 |
| AT-S07 | Trigger parser crash or timeout | Failure is contained, recorded, and recoverable; archive and other jobs remain intact | THR-003–005, THR-013; CORP-013, CORP-026 |
| AT-S08 | Attempt unauthorized archive or admin access | Access is denied and auditable without leaking sensitive content in the audit trail | THR-009, THR-011; all fixtures |
| AT-S09 | Simulate compromised dependency or unverifiable build input | Release gate fails or quarantines the component pending review | THR-010; synthetic supply-chain evidence |
| AT-S10 | Simulate backup disclosure or tampering | Confidentiality/integrity controls detect or prevent exposure; recovery uses a verified clean copy | THR-012, THR-013; CORP-034 |
| AT-S11 | Attempt cloud transfer without an approved policy | Transfer is blocked and the event is visible without exposing content | THR-014; CORP-028 |
| AT-S12 | Exercise compromise-recovery drill | Credentials can be revoked, network isolated, clean state restored, provenance reviewed, and derived state rebuilt | THR-013; CORP-031, CORP-034 |

## Cross-device and operational review

| Test ID | Scenario | Required result | Requirement / fixture links |
|---|---|---|---|
| AT-U01 | Review core research tasks on Mac, iPhone, and iPad design targets | Find, source inspection, citation navigation, annotation, and uncertainty remain understandable at each form factor | Product requirements; STF-06 |
| AT-U02 | Operate with a single-user maintenance scenario | Backup state, integrity failures, rebuild status, and required actions are legible without routine specialist intervention | PRES-021–033; STF-08 |
| AT-U03 | Review accessibility and performance budgets | Candidate evaluation defines measurable budgets; missing evidence is recorded and scored under the framework rather than silently treated as satisfied | STF-07 |

## Acceptance gate

Before any implementation is accepted, every applicable row must have an automated test, a deterministic review procedure, or both; named evidence; and an accountable reviewer role. Before a real-data dry run, all preservation and security rows must pass on the synthetic corpus, and blocked rows must have explicit user-approved deferrals.
