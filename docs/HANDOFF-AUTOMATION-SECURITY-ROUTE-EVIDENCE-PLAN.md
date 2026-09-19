# Handoff Automation Security Route-Evidence Plan

**Status:** Accepted

**Proposal date:** 2026-09-19

**Review date:** 2026-09-19

**Route-selection state:** No route selected

**Evidence-collection state:** Not authorized

**Operational-use state:** Blocked

**Current authority:** Documentation and review only. The currently allowed route-evidence command and API invocation set is empty. This plan does not authorize an API call, executable, dependency, helper, compiler, SDK, source change, build, test, packet-store operation, packet operation, service, watcher, network access, commit, push, or project work.

**Governing framework:** [Handoff Automation ACL and Mount-Alias Security Remediation Proposal](HANDOFF-AUTOMATION-SECURITY-REMEDIATION-PROPOSAL.md), Accepted 2026-09-19

**Comparison record:** [ADR-007: Handoff Security Remediation Route Comparison](decisions/007-handoff-security-remediation-route-comparison.md), Proposed; no route selected

## Purpose

Define how primary evidence would be gathered and reviewed for all four remediation candidates against mandatory gates `SR-G01` through `SR-G10` without selecting or executing a route.

This plan separates five activities that must not be collapsed:

1. planning the evidence object;
2. approving exact evidence sources and read-only collection boundaries;
3. collecting evidence without implementing a route;
4. specialist review and gate scoring; and
5. a later user decision selecting one route or preserving the operational block.

## Fixed conclusions

- ACL enumeration and same-device mount-alias detection remain mandatory.
- Device-number equality, owner/mode checks, successful access, or manual inspection are not substitutes.
- ADR-007 remains `Proposed` and records no selected route.
- Every gate is currently `Unproved` for Routes A through D.
- No command, API, dependency, helper, compiler, SDK, attestation trust root, or operational path is approved.
- The packet store must remain absent throughout route-evidence planning and collection.
- Evidence collection, route selection, implementation, synthetic execution, and operational use require separate approvals.

## Planned evidence workspace

This accepted plan proposes documentation-only evidence records under:

```text
docs/phase-3/security-remediation/
```

Proposed records, none of which is authorized or created by this plan:

```text
COMMON-EVIDENCE-MANIFEST.md
GATE-SCORING-REGISTER.md
SPECIALIST-REVIEW-FINDINGS.md
UNCERTAINTY-AND-DISAGREEMENT-REGISTER.md
ROUTE-A-IN-PROCESS-API-EVIDENCE.md
ROUTE-B-LOCAL-VERIFIER-EVIDENCE.md
ROUTE-C-NATIVE-HELPER-EVIDENCE.md
ROUTE-D-ATTESTATION-EVIDENCE.md
ROUTE-SELECTION-READINESS.md
```

Each record must carry `Proposed`, `Accepted`, `Rejected`, or `Incomplete`; proposal and review dates; the exact governing commit and SHA-256; source identities; reviewer identity or role; uncertainties; and a statement that evidence is not implementation authority.

No binary, command output, SDK copy, header copy, generated source, test result, cache, credential, key, packet, or real data may be stored under this documentation directory.

## Common evidence manifest

Before any route-specific read or invocation, a separately reviewed manifest must identify every proposed evidence source with these fields:

| Field | Requirement |
|---|---|
| Evidence ID | Stable `SR-EV-<route>-<number>` identifier |
| Gate mapping | One or more of `SR-G01` through `SR-G10` |
| Exact source | Absolute local path, approved repository path, or authoritative publisher reference |
| Source class | Documentation, header, library, executable, source, build input, attestation, or synthetic fixture |
| Publisher/owner | Exact provenance and controlling authority |
| Version | Exact version or immutable revision; no “current” or mutable-only identity |
| Bytes and SHA-256 | Required for every finite local artifact |
| Signature identity | Required where the platform supplies code or document signing |
| Access method | Exact read-only API or literal executable argv proposed for later authorization |
| Environment | Exact variables and omitted variables |
| Permission scope | Effective identity, readable paths, writable paths, and prohibited privileges |
| Expected output | Closed type, schema, byte limit, and canonicalization rule |
| Side effects | Expected files, locks, logs, configuration reads, helpers, or explicit `none` |
| Network behavior | Must be `none`; uncertainty is a stop |
| Rollback | Exact transient objects, if any, and removal or proof of no mutation |
| Stop conditions | Identity, output, side-effect, permission, or semantic deviations |

An incomplete manifest is not executable. Redirects, PATH lookup, shell expansion, aliases, mutable tags, implicit SDK selection, package managers, installers, or fallback sources are forbidden.

## Current and future command/API boundary

### Current boundary

Under this Proposed plan:

```text
Allowed route-evidence executable invocations: none
Allowed route-evidence API invocations:        none
Allowed builds or tests:                       none
Allowed network hosts or paths:                none
```

Ordinary repository inspection needed to draft and review Markdown remains outside route execution and must not inspect real data or protocol state.

### Future evidence-collection boundary

A later evidence-collection authorization must include one closed manifest per route. The manifest must enumerate exact symbols or exact executable paths; descriptions such as “system ACL API,” “mount command,” “compiler,” or “verification tool” are insufficient.

The candidate boundaries to be populated are:

| Route | Candidate invocation class | Permitted purpose only | Current state |
|---|---|---|---|
| A | Documented read-only in-process ACL and mount APIs bound to an already open object | Establish ACL entries, mount instance, and replacement detection | No symbol approved |
| B | One absolute-path, identity-pinned local verifier executable with literal argv | Emit bounded read-only ACL and mount evidence | No executable approved |
| C | One reproducibly built project-owned native helper using documented read-only APIs | Emit one canonical ACL/mount record for an already identified object | No source, toolchain, build command, or helper approved |
| D | One frozen attestation verification mechanism | Verify authenticated, fresh, object-bound external evidence | No trust root, schema, API, or executable approved |

Any candidate requiring multiple hidden helpers, a shell, a network path, elevated identity, a service, a watcher, a daemon, an installer, a package manager, or a general command runner is rejected before collection.

## Runtime and permission boundary

All future route evidence must preserve these defaults unless a separate proposal explicitly requests a narrower, reviewed exception:

- real and effective user and group identities match and are non-root;
- no `sudo`, entitlement change, authorization prompt, full-disk-access request, or privilege escalation;
- no read outside the exact evidence paths and owner-only synthetic root;
- no write inside the repository except separately authorized evidence documents;
- owner-only temporary directory mode `0700` and temporary file mode `0600`;
- empty environment with fixed locale and timezone where a process is eventually authorized;
- no `HOME`, proxy, credential, SSH-agent, editor, pager, plug-in, or user-configuration influence;
- no network interface, DNS, socket, telemetry, analytics, or update check;
- bounded stdin, stdout, stderr, runtime, memory, file count, and path count;
- no packet store, `.mneme-local` protocol state, review-root data, credentials, keys, retained experiment inputs, or real correspondence;
- no mutation of implementation, Git state, ACLs, mounts, system settings, or application files during evidence collection; and
- exact rollback or proof that the step is read-only.

Evidence that genuinely requires ACL creation, mount creation, privilege, compilation, code signing, or another mutation must stop at a new proposal. It cannot be smuggled into a read-only evidence step.

## Gate-by-gate evidence requirements

### `SR-G01` — ACL completeness

Every route must provide:

1. authoritative semantics for ACL presence, absence, inheritance, ordering, allow/deny entries, unknown entry types, and errors;
2. exact coverage of repository components, implementation source, future protocol objects, locks/stages, and external review files;
3. a canonical representation independent of locale and display formatting;
4. proof that “no ACL” is distinguished from “ACL unreadable” and “API unsupported”; and
5. a source-to-policy trace showing how every ACL state passes or fails.

### `SR-G02` — mount-instance identity

Every route must provide:

1. authoritative semantics for the proposed mount identity fields;
2. proof that the identity is stronger than ordinary device equality;
3. treatment of mount points, remounts, aliases, firmlink-like paths, external review roots, and publication parents;
4. exact comparison and canonicalization rules; and
5. fail-closed behavior when the platform cannot distinguish the case.

### `SR-G03` — object binding

Every route must provide:

1. the sequence from path policy through open, identity capture, ACL/mount inspection, content read or publication, and recheck;
2. descriptor or equivalent object binding;
3. device, inode/object ID, type, link, owner, mode, ACL, and mount revalidation points;
4. path-replacement and rename-race analysis; and
5. a proof that evidence for one object cannot authorize another.

### `SR-G04` — fail-closed behavior

Every route must define stable failure classes for unavailable, malformed, ambiguous, changing, oversized, partial, unsigned, expired, unsupported, or contradictory evidence. No warning, default allow, retry, fallback, sampling, truncation, or repair is permitted.

### `SR-G05` — command and dependency closure

Every finite artifact must have exact provenance, version, bytes, SHA-256, signature identity where available, license, transitive components, acquisition history if any, and update/revocation rule. Route A must prove no hidden component; Route B must close the executable boundary; Route C must close source and toolchain; Route D must close schema, verifier, and trust root.

### `SR-G06` — local and side-effect-free operation

Every route must prove no network, helper, service, watcher, configuration discovery, user prompt, write side effect, persistent cache, telemetry, or analytics. Evidence must include the exact environment, permissions, bounded inputs/outputs, and interruption behavior.

### `SR-G07` — accepted protocol preservation

Static traceability must show that the route cannot weaken packet immutability, user-approval separation, receipt non-authorization, locks, stage validation, sync order, atomic rename, uncertainty preservation, append-only rollback, or the no-cleanup/no-retry policy.

### `SR-G08` — synthetic testability

The route must map every positive, negative, malformed, race, interruption, and recovery requirement to an exact synthetic test. Platform-behavior claims that cannot be represented synthetically require a later, separately authorized local feasibility test; they remain unproved until then.

### `SR-G09` — portability and unsupported-host behavior

The route must define supported operating-system, filesystem, runtime, binary, SDK, and architecture identities. Identity drift or unsupported state must block operation and require re-review. No alternate implementation or fallback is selected automatically.

### `SR-G10` — independent agreement

Security/privacy, operations/recovery, quality/independent-verification, and governance specialists must review the same frozen evidence object. Every disagreement must name the claim, evidence, reviewer, impact, and resolution. All four reviews must pass; silence or majority vote is insufficient.

## Route A evidence plan — in-process API

### Exact evidence needed

- local authoritative header and documentation identities for each proposed ACL and mount symbol;
- exact owning system library and code-signing identity;
- exact runtime binding mechanism already available to frozen Perl;
- type, constant, structure-layout, allocation/free, encoding, and error contracts;
- operating-system and architecture availability matrix;
- descriptor-binding and same-device-alias proof;
- proof that no hard-coded syscall number, undocumented ABI, FFI package, native extension, or generated binding is required;
- closed canonical evidence schema and size limits;
- static integration diff and rollback plan; and
- all four specialist findings.

### Candidate API allowlist rule

The eventual allowlist may contain only symbols that are individually named in an Accepted Route-A manifest and are documented as read-only ACL retrieval, ACL entry enumeration, descriptor metadata, mount-instance retrieval, or required release/free operations. Path-only variants are rejected where a descriptor-bound variant is required. No symbol is currently approved.

### Synthetic tests

Route A must cover `SR-T001` through `SR-T024` below plus API-specific unsupported-symbol, invalid-return, allocation, and structure-version cases.

### Route-A stop conditions

Stop if the runtime lacks a documented safe binding; a structure or constant must be guessed; evidence is path-only; mount identity is no stronger than `st_dev`; an extension must be installed; or any API can mutate ACLs, mounts, or file content.

## Route B evidence plan — frozen local verifier

### Exact evidence needed

- candidate executable absolute path, publisher, platform provenance, version, owner/group, mode, bytes, SHA-256, and code-signing identity;
- exact literal argv for ACL and mount inspection, with no alternate form;
- proof of no shell, PATH lookup, helper, plug-in, configuration, pager, localization, network, or write behavior;
- exact stdin, stdout, stderr, exit-status, timeout, signal, and byte-limit contracts;
- a closed parser grammar with duplicate, reordered, missing, malformed, localized, oversized, and contradictory cases;
- descriptor or equivalent object-binding proof;
- operating-system update and executable-replacement policy;
- license and component record;
- static integration diff and rollback plan; and
- all four specialist findings.

### Candidate command allowlist rule

The eventual allowlist may contain one absolute executable path and only the literal argument arrays in an Accepted Route-B manifest. No shell metacharacter, environment-derived value, wildcard, recursive discovery, output file, write flag, privilege flag, remote target, or fallback executable is permitted. No executable or argv is currently approved.

### Synthetic tests

Route B must cover `SR-T001` through `SR-T024` plus every parser token, exit status, stderr condition, timeout/interruption state, identity mismatch, and forbidden side-effect case.

### Route-B stop conditions

Stop if the executable cannot bind evidence to the object; output is locale- or version-ambiguous; it invokes a helper or configuration; identity cannot be pinned; code-signing or licensing evidence is incomplete; or more than the accepted single-purpose command boundary is needed.

## Route C evidence plan — native helper

### Exact evidence needed

- complete proposed source and closed canonical input/output schema;
- authoritative platform API and header identities;
- compiler, SDK, linker, architecture, flags, environment, code-signing, and build-command manifest;
- zero-third-party-dependency proof and complete license record;
- deterministic and independently reproduced binary bytes and SHA-256;
- memory, bounds, encoding, error, descriptor, and race analysis;
- sandbox, entitlements, owner/mode, installation path, invocation, and output limits;
- update, removal, revocation, and compromise-recovery procedures;
- exact integration diff, generated-artifact inventory, and rollback plan; and
- all four specialist findings.

### Candidate API and command allowlist rule

The helper source may call only symbols in an Accepted Route-C API manifest. Build and signing may invoke only absolute executable paths and literal argv in a separately Accepted toolchain manifest. Runtime may invoke only the exact verified helper binary. No API, compiler, SDK, linker, signer, build command, or helper is currently approved.

### Synthetic tests

Route C must cover `SR-T001` through `SR-T024`, API-specific negative cases, malformed canonical records, memory/bounds cases, independent rebuild comparison, wrong-binary identity, and removal/revocation.

### Route-C stop conditions

Stop if a third-party component appears; the build is not reproducible; compiler or SDK identity drifts; signing or entitlements broaden access; memory-safety obligations are unresolved; the helper can mutate state; or installation/cleanup cannot be exact and reviewable.

## Route D evidence plan — external attestation or continued disablement

### Exact evidence needed

- attestation producer, authority, operating procedure, and host-security boundary;
- canonical schema for exact object identity, ACLs, mount identity, time, expiry, and policy version;
- signature algorithm, trust root, public-key identity, verification mechanism, and revocation;
- storage path, owner/mode, immutability, replay prevention, retention, and compromise recovery;
- fresh object-binding and time-of-check/time-of-use proof;
- exact behavior for missing, stale, expired, unsigned, malformed, contradictory, or revoked evidence;
- evidence-generation and verification side-effect analysis;
- explicit residual-risk statement;
- exact integration diff and rollback-to-disabled plan; and
- all four specialist findings plus explicit user acceptance of residual trust.

### Candidate API and command allowlist rule

Only the exact attestation verification mechanism in an Accepted Route-D manifest may be considered. Evidence generation is a separate authority and may not be bundled. If verification requires a command, API, library, trust root, or key, each must be separately frozen and approved. None is currently approved.

### Synthetic tests

Route D must cover `SR-T001` through `SR-T024` plus signature, trust-root, expiry, replay, revocation, producer compromise, storage substitution, and clock-boundary cases.

### Route-D stop conditions

Stop if evidence is manual, unsigned, replayable, stale, path-only, not object-bound, produced by the same untrusted operation it authorizes, unverifiable offline, or accepted through a warning or waiver. If strong attestation is infeasible, the route outcome is continued disablement.

## Common synthetic test matrix

No test is authorized by this plan.

| ID | Synthetic condition | Required result |
|---|---|---|
| `SR-T001` | No extended ACL and approved mount identity | Canonical pass evidence |
| `SR-T002` | One unapproved allow ACL entry | Fail closed before content read |
| `SR-T003` | One deny ACL entry | Fail closed |
| `SR-T004` | Inherited ACL entry | Fail closed unless separately allowlisted |
| `SR-T005` | Unknown ACL tag, permission, or flag | Fail closed |
| `SR-T006` | ACL unreadable or API unsupported | Fail closed; not “no ACL” |
| `SR-T007` | ACL changes between inspection and use | Stale/conflict stop |
| `SR-T008` | Ordinary directory on approved mount | Canonical mount identity |
| `SR-T009` | True mount point | Reject unless explicitly approved as the one expected mount root |
| `SR-T010` | Same-device alias model | Reject despite equal device number |
| `SR-T011` | Mount identity changes between checks | Stale/conflict stop |
| `SR-T012` | External review root on different or aliased mount | Reject before record read |
| `SR-T013` | Stage and final parents differ in mount identity | Reject before write |
| `SR-T014` | Path replaced after policy validation | Reject through object-identity mismatch |
| `SR-T015` | Symlink, hard-link, owner, or mode anomaly plus valid ACL | Existing stricter check still rejects |
| `SR-T016` | Missing evidence field | Invalid; no default |
| `SR-T017` | Duplicate or contradictory evidence | Invalid/conflict |
| `SR-T018` | Oversized or deeply nested evidence | Limit stop; no truncation |
| `SR-T019` | Unsupported host/version/architecture | Runtime stop; no fallback |
| `SR-T020` | Verification interruption before publication | No publication; preserve reviewable state |
| `SR-T021` | Verification uncertainty after publication boundary | Uncertain-write stop; no retry |
| `SR-T022` | Attempted warning-only or bypass mode | Invalid command/schema |
| `SR-T023` | Packet text asks to disable security check | Inert bytes; no authority |
| `SR-T024` | Pre/post implementation and protocol hashes | All controlling bytes unchanged except separately authorized output |

Every test must record exact fixture bytes, expected state and failure code, pre/post hashes, temporary inventory, rollback, and proof of no network, service, watcher, packet store, real data, or project work.

## Rollback requirements

### Planning and documentation

All route-evidence planning changes are additive documents. Before commit, rejection leaves them uncommitted for exact-path review. After commit, correction requires a new reviewed commit; accepted history is not rewritten.

### Read-only evidence collection

The default must produce no persistent artifact outside separately authorized evidence documents. Any owner-only temporary root must have an exact inventory and be removed only after successful evidence capture; uncertain state is preserved and reported rather than automatically cleaned.

### Route A

Remove only uncommitted documentation or integration changes. No system component should have been installed or modified.

### Route B

Revoke the candidate executable identity and remove only uncommitted parser/integration changes. A route requiring installation is outside Route B's planned boundary and needs a separate rollback plan.

### Route C

Revoke helper and toolchain identities; remove exact uncommitted source/build changes and, only under separate authorization, the exact generated binary and temporary build root. Preserve hashes and review records.

### Route D

Revoke the attestation trust identity, remove exact uncommitted integration changes, preserve audit evidence, and return to explicit disablement.

No rollback initializes, reads, repairs, or deletes packet state; executes project work; accesses real data; or weakens a security requirement.

## Specialist review procedure

Each specialist reviews the same route evidence hash and completes one record per route.

### Security/privacy

Review ACL semantics, mount-instance strength, object binding, TOCTOU, untrusted output, privileges, trust roots, compromise, and recovery. Any unclosed security claim fails its mapped gate.

### Operations/recovery

Review host/version compatibility, identities, environment, interruption, limits, update drift, orphan preservation, rollback, revocation, and disabled-state recovery.

### Quality/independent verification

Review primary-source provenance, canonical schemas, parser or API completeness, requirement-to-test traceability, reproducibility, negative cases, and evidence hashes.

### Governance

Review scope, command/dependency authority, user/agent separation, no-selection status, approval sequencing, and the continuing operational block.

Required finding fields:

```text
route
reviewer_role
evidence_object_sha256
gate
finding = Pass | Fail | Unproved | NotApplicableWithProof
claim
evidence_ids
residual_uncertainty
disagreement
acceptance_condition
review_date
```

One `Fail`, `Unproved`, unresolved disagreement, or unproved “not applicable” claim makes the route ineligible.

## Evidence scoring and readiness

There is no weighted score. For each route:

```text
Eligible = SR-G01 Pass
        AND SR-G02 Pass
        AND SR-G03 Pass
        AND SR-G04 Pass
        AND SR-G05 Pass
        AND SR-G06 Pass
        AND SR-G07 Pass
        AND SR-G08 Pass
        AND SR-G09 Pass
        AND SR-G10 Pass
```

The readiness record must list each gate, evidence IDs, specialist findings, disagreements, uncertainties, and status. Missing evidence is `Unproved`, never zero-risk or implicitly passing.

## Staged approval gates

| Gate | Required user decision | Current state |
|---|---|---|
| `RE-1` | Accept or revise this route-evidence plan | Proposed |
| `RE-2` | Accept exact local primary-source inventory for all four routes | Blocked |
| `RE-3` | Authorize exact read-only evidence commands or API calls for one named route | Blocked |
| `RE-4` | Accept collected evidence and integrity record | Blocked |
| `RE-5` | Accept four specialist findings and ten-gate scoring | Blocked |
| `RE-6` | Accept route-readiness comparison | Blocked |
| `RE-7` | Select one route under ADR-007 with exact evidence hash | Blocked |
| `RE-8` | Approve route-specific implementation plan | Blocked |
| `RE-9` | Authorize implementation only | Blocked |
| `RE-10` | Authorize exact synthetic execution only | Blocked |
| `RE-11` | Accept security closure | Blocked |
| `RE-12` | Authorize first packet-store initialization and operational trial | Blocked |

Approval of one gate does not approve the next.

## Global stop conditions

Stop and return for review if:

- any evidence source, symbol, executable, library, helper, compiler, SDK, trust root, or path is undeclared or changes identity;
- an API or command is needed before its exact manifest and authorization are Accepted;
- a shell, PATH lookup, wildcard, recursive discovery, network path, service, watcher, daemon, installer, package manager, or elevated identity appears;
- evidence collection would mutate ACLs, mounts, system settings, implementation, Git state, packet state, or real data;
- output is unbounded, localized, ambiguous, malformed, partial, unsigned, expired, replayable, or contradictory;
- object binding or same-device-alias detection cannot be proved;
- a command invokes a helper, reads user configuration, creates a cache, or writes a log;
- a third-party or transitive component is discovered;
- a test requires real correspondence, credentials, retained experiment input, cloud AI, or production infrastructure;
- a reviewer disagrees or a gate remains `Unproved`; or
- any step attempts to combine evidence collection, route selection, implementation, testing, packet-store creation, or operational use.

On stop, preserve the exact evidence and uncertainty record, make no retry or substitution, and keep all routes unselected and operational use blocked.

## Definition of done for route evidence

This evidence phase is complete only when:

1. all four route manifests have been reviewed, including rejected or infeasible candidates;
2. every evidence artifact has exact provenance and identity;
3. every allowed API or command is explicitly named and separately authorized before use;
4. `SR-T001` through `SR-T024` have route-specific traceability without being executed prematurely;
5. all four specialist reviews are complete for each route;
6. all ten gates are scored from primary evidence;
7. uncertainties, disagreements, and rejected alternatives are preserved;
8. rollback and compromise recovery are complete;
9. a route-readiness record truthfully identifies eligible candidates or records no selection; and
10. operational use remains blocked pending a later explicit user decision.

## Review request

Review is requested on:

1. the empty current invocation boundary and future manifest requirements;
2. the exact evidence required for Routes A through D;
3. the gate-by-gate evidence and runtime/permission boundaries;
4. the common and route-specific synthetic test matrix;
5. rollback, specialist review, scoring, and stop conditions; and
6. the preserved no-selection and operational-block conclusions.
