# ADR-007: Handoff Security Remediation Route Comparison

**Status:** Proposed

**Proposal date:** 2026-09-19

**Review date:** Not reviewed

**Decision state:** No route selected

**Operational-use state:** Blocked

**Current authority:** Comparison and review only. This record does not authorize route selection, a command, dependency, helper, compiler, SDK, source change, test, packet-store operation, packet operation, service, watcher, network access, commit, push, or project work.

**Governing framework:** [Handoff Automation ACL and Mount-Alias Security Remediation Proposal](../HANDOFF-AUTOMATION-SECURITY-REMEDIATION-PROPOSAL.md), Accepted 2026-09-19

**Governing-framework commit:** `60f3198e91588f7c14396734d9721395341b925d`

**Governing-framework SHA-256:** `e18142efafe676a2f7b5f0b162198937a8cada591dbb2a59f19dc23a10e5b00a`

## Context

The accepted handoff implementation and 38-case synthetic suite pass within their declared scope. Operational use remains blocked by two unresolved requirements:

1. enumerate and evaluate macOS ACLs for every controlling object; and
2. distinguish mount identity from device-number equality so that same-device aliases and equivalent namespace substitutions fail closed.

The governing framework defines four candidate resolution routes and ten mandatory gates. This record compares those routes without selecting one.

## Decision proposed

Preserve all four routes as candidates until primary evidence closes their route-specific gaps. Record the current result as **no selection** because `SR-G01` through `SR-G10` remain `Unproved` for every route.

No weighted preference, convenience argument, or user-interface benefit can override a mandatory gate. A route becomes eligible for selection only after its exact evidence object is frozen, independently reviewed, and shown to pass all ten gates.

## Common comparison boundary

Every candidate must preserve the accepted implementation's:

- exact physical repository-root policy;
- owner, mode, type, link-count, realpath, and containment checks;
- taint mode and empty bounded environment;
- fixed runtime and binary identities;
- closed command grammar and Git-read allowlist;
- no-network and one-shot operation;
- immutable packet cores and append-only transactions and rollbacks;
- lock, stage, sync, rename, uncertainty, and no-retry rules;
- verdict/user-approval separation; and
- explicit `project_work_authorized=false` and `project_work_executed=false` receipt fields.

Any route that weakens one of these controls is rejected rather than scored.

## Candidate comparison

### Route A — reviewed in-process platform primitive

**Boundary:** Extend the existing Perl process only enough to call a documented local operating-system primitive. No new executable, package, downloaded module, native extension, service, or network path is assumed.

**Potential strengths:**

- smallest process and command boundary if technically feasible;
- ACL and mount evidence could be bound directly to open file descriptors;
- no output parser for an external process;
- easiest route to preserve the existing empty environment and one-shot model.

**Principal risks:**

- the frozen Perl runtime may not expose the required API safely;
- an undocumented syscall number, binary structure, or ABI assumption would be unacceptable;
- mount semantics may differ across macOS and APFS versions;
- inability to prove portability must produce a hard failure, not a fallback.

**Eligibility condition:** Authoritative evidence proves a documented, stable, file-descriptor-bound primitive is callable within the reviewed runtime boundary without an undeclared component.

### Route B — frozen local verifier executable

**Boundary:** Add one absolute-path, identity-pinned, read-only local executable used only for bounded ACL and mount inspection through literal argument arrays and the existing empty environment.

**Potential strengths:**

- may use mature platform inspection behavior already present on the host;
- can be independently hashed and code-signature checked;
- could avoid a project-owned compiler and binary lifecycle;
- operational behavior can be constrained by exact argv and output grammar.

**Principal risks:**

- expands the external-command and supply-chain boundary;
- text output may be locale-, version-, or formatting-dependent;
- the executable may invoke helpers, configuration, plug-ins, or other implicit behavior;
- path-oriented output may not close replacement races;
- no executable is approved or even nominated by this record.

**Eligibility condition:** One exact publisher-proven executable and invocation contract demonstrates local, bounded, noninteractive, side-effect-free, object-bound evidence with a closed parser and no helper or network behavior.

### Route C — minimal reviewed native helper

**Boundary:** Add a project-owned helper that calls documented platform APIs and emits one closed canonical evidence record. The helper, compiler, SDK, linker, code-signing, and reproducible-build object become part of the reviewed trust boundary.

**Potential strengths:**

- strongest control over API choice, canonical output, error handling, and object binding;
- can expose exactly the ACL and mount fields the policy requires;
- can avoid locale-dependent text parsing;
- negative behavior can be designed directly around Mneme's failure classes.

**Principal risks:**

- largest implementation, build, licensing, maintenance, and compromise-recovery expansion;
- adds a generated executable and toolchain identities;
- introduces memory-safety and native-interface review obligations;
- reproducibility and cross-version behavior require substantial evidence;
- no source, compiler, SDK, or binary is authorized by this record.

**Eligibility condition:** A zero-third-party-dependency helper has frozen source and toolchain identities, reproducible output, narrow permissions, independent review, and complete synthetic adversarial evidence.

### Route D — explicit reviewed operational disposition

**Boundary:** Keep ACL and mount verification outside the implementation under a separately controlled attestation or host-hardening process. The implementation either verifies a strong immutable attestation or remains disabled.

**Potential strengths:**

- can preserve the accepted implementation without adding a runtime command or native binary;
- may align verification with host security administration;
- can keep operational authority external and explicit.

**Principal risks:**

- creates a new trust, freshness, signing, storage, and revocation boundary;
- path-to-object and time-of-check/time-of-use races are difficult to close externally;
- manual assurance or an unsigned report cannot satisfy the requirement;
- residual risk may be too high to permit operation at all.

**Eligibility condition:** A canonical, authenticated, fresh, object-bound attestation design passes all gates. Otherwise the only acceptable Route-D outcome is continued operational disablement.

## Ten mandatory-gate comparison

Status vocabulary for this record:

- `Pass` — primary evidence and specialist review prove the gate for the frozen route object;
- `Fail` — evidence contradicts the gate;
- `Unproved` — required evidence is absent, incomplete, or not yet reviewed;
- `Not applicable` — permitted only with a written proof that the gate genuinely does not apply; convenience is not a basis.

| Gate | Requirement | Route A | Route B | Route C | Route D |
|---|---|---|---|---|---|
| `SR-G01` | Complete ACL evidence for every controlling path class | Unproved | Unproved | Unproved | Unproved |
| `SR-G02` | Mount-instance evidence stronger than device equality | Unproved | Unproved | Unproved | Unproved |
| `SR-G03` | Evidence bound to the exact object later used | Unproved | Unproved | Unproved | Unproved |
| `SR-G04` | Unknown, changing, malformed, or unsupported state fails closed | Unproved | Unproved | Unproved | Unproved |
| `SR-G05` | Every command, dependency, helper, toolchain, or artifact separately approved and frozen | Unproved | Unproved | Unproved | Unproved |
| `SR-G06` | Local, one-shot, bounded, read-only, noninteractive, and no network | Unproved | Unproved | Unproved | Unproved |
| `SR-G07` | Existing atomicity, uncertainty, rollback, and non-authorization rules preserved | Unproved | Unproved | Unproved | Unproved |
| `SR-G08` | Reproducible positive, negative, race, malformed, and recovery tests | Unproved | Unproved | Unproved | Unproved |
| `SR-G09` | Unsupported hosts fail closed without fallback or policy reduction | Unproved | Unproved | Unproved | Unproved |
| `SR-G10` | Security, operations, quality, and governance reviewers agree on one frozen object | Unproved | Unproved | Unproved | Unproved |

**Gate conclusion:** No candidate is eligible for selection.

## Required evidence by candidate

### Route A evidence object

1. Authoritative platform API documentation with exact supported operating-system versions.
2. Exact Perl exposure mechanism and proof that it is already present in the frozen runtime.
3. Function signatures, data layouts, constants, ownership rules, encoding, limits, and error returns.
4. File-descriptor binding and race analysis for every controlling path class.
5. ACL canonicalization rules, including inherited and deny entries.
6. Mount-instance identity fields and same-device-alias semantics.
7. Unsupported-host and partial-result behavior.
8. Synthetic adapter and eventual exact execution plan.
9. Implementation diff, rollback, and compromise-recovery plan.
10. Four completed specialist reviews.

### Route B evidence object

1. Exact publisher, provenance, absolute path, version, owner/group, mode, byte count, code signature, and SHA-256.
2. Proof of no dependency acquisition, helper invocation, configuration loading, plug-in discovery, network use, or write side effect.
3. Exact empty environment and literal argument arrays.
4. Bounded stdout, stderr, exit-status, timeout, and interruption contract.
5. Closed output grammar with malformed, duplicate, reordered, localized, and oversized cases.
6. Object-binding and path-replacement analysis.
7. ACL and mount-instance semantics from authoritative documentation.
8. Binary replacement, operating-system update, and compromise-recovery behavior.
9. Exact source and test changes plus rollback.
10. Four completed specialist reviews.

### Route C evidence object

1. Complete helper source and closed input/output schema.
2. Exact compiler, SDK, linker, code-signing, and build-environment identities.
3. Reproducible-build procedure and independent binary hash reproduction.
4. Platform API documentation and source-to-requirement traceability.
5. Memory-safety, bounds, encoding, and hostile-path review.
6. Sandbox, permissions, object binding, and no-network proof.
7. License and supply-chain record proving zero undeclared third-party components.
8. Installation, binary replacement, update, removal, and compromise-recovery procedures.
9. Full synthetic and negative test design plus rollback.
10. Four completed specialist reviews.

### Route D evidence object

1. Attestation producer identity and authority.
2. Canonical schema covering exact paths, object identities, ACLs, mount identities, time, and expiry.
3. Signature or equivalent authentication, trust root, verification method, and revocation policy.
4. Freshness, drift, replay, substitution, storage, and deletion controls.
5. Object-binding and time-of-check/time-of-use analysis.
6. Exact implementation behavior when evidence is missing, stale, unsupported, or invalid.
7. Host-hardening owner, operating procedure, audit frequency, and compromise recovery.
8. Proof that no manual assurance, warning, or unsigned report can enable operation.
9. Synthetic attestation and rejection test design plus rollback.
10. Four completed specialist reviews and explicit user acceptance of residual trust.

## Preliminary specialist findings

These are comparison-level findings only. No specialist has accepted a candidate implementation or closed a mandatory gate.

### Security/privacy

- Route A has the smallest prospective trust expansion but the greatest immediate feasibility uncertainty.
- Route B creates parser, binary-replacement, helper-behavior, and path-binding risks.
- Route C offers the clearest semantics but adds the broadest supply-chain and native-code attack surface.
- Route D moves rather than removes the trust problem and has the hardest freshness and race obligations.
- No route currently proves ACL completeness or same-device mount-alias rejection.

**Finding:** `Unproved`; operational block remains mandatory.

### Operations/recovery

- Route A would have the least deployment overhead if the primitive exists and is stable.
- Route B requires binary identity monitoring across operating-system updates.
- Route C requires build, installation, update, removal, and compromised-helper recovery procedures.
- Route D requires durable attestation production, expiry, revocation, and outage handling.
- Every route must preserve uncertain-write evidence and forbid automatic cleanup or fallback.

**Finding:** `Unproved`; no operating procedure is approved.

### Quality/independent verification

- Routes A and C can potentially provide canonical structured fields directly.
- Route B needs a strict adversarial parser for version- and locale-sensitive output.
- Route D needs cryptographic and temporal verification in addition to ACL and mount semantics.
- Synthetic models alone cannot prove platform behavior; exact local execution would require a later gate.

**Finding:** `Unproved`; no evidence package or execution plan is frozen.

### Governance

- Every route changes a material security boundary and requires explicit user selection.
- Route B requires command-boundary approval; Route C requires code, toolchain, dependency, build, and artifact approvals; Route D requires explicit residual-trust acceptance.
- Route selection must not be combined with implementation or execution authorization.
- Packet-store initialization and first operational use remain later independent gates.

**Finding:** `Pass` for the comparison's no-selection boundary only; `SR-G10` remains `Unproved` for every candidate.

## Residual uncertainty register

| ID | Applies to | Uncertainty | Closure evidence |
|---|---|---|---|
| `SR-U01` | A | Whether frozen Perl exposes documented ACL APIs safely | Runtime/API dossier and static proof |
| `SR-U02` | A | Whether mount-instance identity is available without ABI assumptions | Authoritative API and exact field evidence |
| `SR-U03` | B | Which, if any, local executable has acceptable semantics and side effects | Publisher, binary, invocation, and behavior dossier |
| `SR-U04` | B | Whether textual output can be closed across host updates and locale | Versioned grammar and adversarial corpus |
| `SR-U05` | C | Whether a helper can be reproducibly built with zero undeclared components | Toolchain closure and independent rebuild |
| `SR-U06` | C | Native memory-safety and long-term maintenance burden | Source review, hardening evidence, and ownership plan |
| `SR-U07` | D | Whether external attestation can bind the object at use time | Signed schema and TOCTOU proof |
| `SR-U08` | D | Whether residual trust is acceptable for private correspondence governance | Explicit user disposition after specialist review |
| `SR-U09` | All | Exact same-device alias behavior on the target macOS/APFS host | Authorized platform evidence and negative test |
| `SR-U10` | All | ACL inheritance and mutation behavior during one-shot operations | Authorized race and failure evidence |
| `SR-U11` | All | Behavior across operating-system updates | Version policy, identity drift stop, and reapproval rule |
| `SR-U12` | All | Whether the frozen synthetic matrix needs extension | Reviewed requirement-to-test traceability |

Unknowns remain blockers. They may not be converted to assumptions during scoring.

## Rejected shortcuts

The following are rejected for all candidates:

- treating owner and mode bits as proof that no ACL exists;
- treating equal device numbers as proof of equal mount identity;
- inferring security from successful file access;
- manual spot checks, screenshots, prose assurances, or unsigned reports;
- an unpinned PATH command, shell pipeline, downloaded module, opaque installer, or mutable binary;
- warning-only behavior, automatic fallback, retry, cleanup, or bypass flags;
- a synthetic-only claim about undocumented platform behavior; and
- combining route selection, implementation, execution, packet-store initialization, and operational use in one approval.

## Rollback comparison

### Route A

Before commit, remove only the exact reviewed source/test changes. After commit, revert through a new reviewed commit. No runtime or system component should remain because the route must use an already present primitive.

### Route B

Remove the exact source/test changes and revoke the verifier identity from the allowlist. If the route installed or altered anything, that would violate its current candidate boundary and require a separate exact-target recovery plan. No binary may remain implicitly trusted after rejection.

### Route C

Remove exact source/test/build-manifest changes and the exact generated helper only under separately approved cleanup. Revoke compiler, SDK, signing, and binary identities. Preserve build and test evidence for audit; do not leave an installed helper or cache.

### Route D

Revoke the attestation trust root or accepted evidence identity, remove only separately approved local integration changes, and return to the explicit disabled state. Preserve prior attestations as audit records unless a separately approved retention decision says otherwise.

### Common rollback invariant

Rollback never initializes or deletes the packet store, rewrites packet history, runs project work, weakens a security check, or authorizes operational use. Rejection of every route leaves the accepted implementation committed but operationally blocked.

## Exact user approval required for route selection

Route selection requires a new user instruction that names exactly one route and its frozen evidence record. The minimum sufficient selection language is:

```text
I select Route [A|B|C|D] as the proposed handoff-security remediation design, based on [exact evidence-document path] with SHA-256 [exact digest]. Mark ADR-007 Accepted with the review date [YYYY-MM-DD] and record the selected route and unresolved conditions. Commit only the decision record. This selection does not authorize any command, dependency, helper, compiler, SDK, source change, build, test, packet-store operation, packet operation, service, watcher, network access, operational use, push, or project work. Prepare the next route-specific authorization request separately.
```

Additional language is mandatory for Route D:

```text
I explicitly accept the documented residual attestation trust boundary and its specialist-reviewed limitations. If the attestation design cannot bind fresh evidence to the exact object at use time, operational use remains disabled.
```

An approval that says only “approved,” refers to multiple routes, omits the exact evidence identity, or combines selection with implementation or execution is insufficient and fails closed.

## Later route-specific approvals

Even after valid route selection, the following remain separate:

1. evidence-package acceptance;
2. exact command/dependency/helper/toolchain or attestation-boundary approval;
3. frozen implementation-plan approval;
4. implementation authorization;
5. static and specialist finding acceptance;
6. exact synthetic-test authorization;
7. test-evidence acceptance;
8. security-gate closure; and
9. first packet-store initialization and operational trial approval.

No route-selection approval implies any later approval.

## Consequences of no selection

- The accepted implementation remains unchanged.
- No command or dependency is added.
- No packet store or protocol state is created.
- No synthetic or operational command is run.
- The ACL and mount-alias requirements remain mandatory.
- Operational use remains blocked.

## Review request

Review is requested on:

1. the neutral boundaries and tradeoffs for Routes A through D;
2. the `Unproved` status of every candidate across `SR-G01` through `SR-G10`;
3. the required evidence objects and preliminary specialist findings;
4. the residual uncertainty and rejected shortcuts;
5. route-specific and common rollback; and
6. the exact user approval language that selects one route without authorizing implementation or execution.
