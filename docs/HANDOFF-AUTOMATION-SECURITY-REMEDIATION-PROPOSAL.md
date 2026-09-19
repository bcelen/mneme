# Handoff Automation ACL and Mount-Alias Security Remediation Proposal

**Status:** Accepted

**Proposal date:** 2026-09-19

**Review date:** 2026-09-19

**Operational-use state:** Blocked

**Current authority:** Accepted as a planning framework only. No remediation route is selected or authorized. This record does not authorize a command, dependency, source change, test, packet-store operation, packet operation, service, watcher, network access, push, or project work.

**Accepted implementation commit:** `c4f2df6425082a584de348d967bcebfc168e4103`

**Accepted implementation evidence:** [`tools/handoff/README.md`](../tools/handoff/README.md)

## Purpose

Resolve the two qualified security findings that prevent operational use of the local handoff automation:

1. the current core-only Perl boundary cannot enumerate and evaluate macOS access-control lists; and
2. device-number comparison alone cannot conclusively exclude a same-device mount alias or another mount topology that presents the same underlying device identity.

Both controls remain mandatory. Until they are technically proved or receive an explicit reviewed disposition, every operational command remains blocked, including store initialization, packet creation, validation, listing, consumption, and rollback.

## Non-negotiable security requirements

### ACL requirement

Before an operational read or write, the implementation must determine the ACL state of every controlling path class:

- repository root and each traversed source-path component;
- tracked implementation source;
- `.mneme-local`, `handoffs`, packet-store root, and every protocol directory and file;
- lock and staging objects;
- external review root, verdict, approval, and rollback-approval files; and
- every path reopened during atomic validation.

The accepted default is no extended ACL entries. A future nonempty ACL policy would require a separately reviewed canonical allowlist describing exact principals, permissions, inheritance flags, ordering, and scope. Unknown, unreadable, malformed, inherited-but-unapproved, changing, or ambiguous ACL state must fail closed before content is read or bytes are published.

ACL verification must bind the inspected object to the object subsequently read or written. A path-only preflight is insufficient if the object can change before use.

### Mount-alias requirement

Before an operational read or write, the implementation must establish the filesystem and mount identity of:

- the physical repository root;
- the future packet-store root and all publication parents;
- every staging and final destination; and
- the external review root and reviewed files.

The evidence must distinguish mount identity from device-number equality. It must detect a mount point, bind mount, firmlink-like alias, remounted path, or other namespace alias even when ordinary `stat` device values are equal. Staging and final publication must be proved to share the intended physical filesystem and mount identity. Any identity change between preflight, open, validation, and publication must stop without retry or cleanup.

## Current evidence and exact gap

The accepted implementation already enforces:

- exact physical repository root;
- owner, mode, regular-file or directory type, and one-link file requirements;
- no-follow opens and component-by-component symlink rejection;
- realpath containment;
- device-number equality for protocol objects;
- fixed runtime and supporting-binary identities;
- taint mode and an empty bounded environment;
- exact command and Git-read allowlists; and
- fail-closed atomic publication and append-only recovery behavior.

Those controls do not prove ACL absence and do not identify the mount instance independently of the device number. The accepted synthetic suite does not claim otherwise.

## Candidate resolution routes

No route is selected or authorized by this proposal.

### Route A — reviewed in-process platform primitive

Use an operating-system primitive from the existing process to obtain ACL and mount-instance information without invoking another executable.

Evidence required before selection:

- authoritative platform documentation for the exact API and field semantics;
- proof that the frozen Perl runtime can call the primitive without a downloaded module, native extension, unsafe hard-coded ABI assumption, or undeclared dependency;
- exact return-value, encoding, size, and error behavior;
- file-descriptor or equivalent object binding that closes path-replacement races;
- mount identity stronger than `st_dev` alone;
- behavior on APFS volumes, aliases, firmlinks, external review roots, and absent paths; and
- a fail-closed account of unsupported operating-system versions.

Selection is blocked if the route depends on an unstable syscall number, undocumented structure layout, implicit FFI, or an unreviewed native component.

### Route B — frozen local verifier executable

Add one narrowly scoped, locally available verifier path whose only purpose is bounded ACL and mount-identity inspection.

Evidence required before selection:

- exact publisher and platform provenance;
- absolute executable path, owner, mode, byte count, code-signing identity, and SHA-256;
- exact non-shell argument arrays and empty environment;
- proof of no network, configuration, plug-in, pager, locale, helper, or write behavior;
- complete bounded output grammar and adversarial parser cases;
- exit-status and stderr contract;
- object-binding and race analysis;
- proof that the output distinguishes same-device mount aliases; and
- explicit addition to the runtime identity, command allowlist, threat register, and test matrix.

This route would be a command-boundary expansion. It requires a separate architecture/security approval before any binary is invoked or source is changed. This proposal does not name or approve an executable.

### Route C — minimal reviewed native helper

Create a project-owned helper that calls documented platform ACL and mount APIs and emits one closed canonical record.

Evidence required before selection:

- exact source, compiler, SDK, linker, entitlement, signing, and reproducible-build identities;
- zero third-party dependencies;
- a narrow input/output schema with no general path discovery or command execution;
- memory-safety and parser review;
- deterministic build and independent binary verification;
- sandbox and permission boundary;
- source and binary licensing record;
- complete hostile-path, ACL, alias, race, and malformed-output tests; and
- removal and compromise-recovery procedures.

This route adds code, a build boundary, and a generated binary. It therefore requires separate design, dependency/toolchain, implementation, build, test, and commit approvals. None is granted here.

### Route D — explicit reviewed operational disposition

Keep the automation operationally disabled and record that ACL and mount verification occurs outside the implementation under a separately controlled host-hardening or attestation process.

For this route to avoid weakening the requirement, the disposition must specify:

- who or what produces the attestation;
- exact attested paths, filesystem and mount identities, ACL records, time, and expiry;
- immutable attestation schema, signature or hash binding, and storage location;
- how the implementation validates freshness and object identity without circular trust;
- how drift invalidates authorization before any operation;
- compromise and recovery handling; and
- why the residual race and trust boundary are acceptable.

A narrative assurance, manual spot check, warning-only mode, or permanent waiver is insufficient. If a strong attestation design is not accepted, Route D means the automation remains disabled.

## Evaluation matrix

Each candidate must be evaluated against the same mandatory questions:

| ID | Requirement | Pass condition |
|---|---|---|
| `SR-G01` | ACL completeness | Every controlling path class has exact ACL evidence before content read or publication |
| `SR-G02` | Mount identity | Evidence distinguishes mount instance from device equality and rejects aliases |
| `SR-G03` | Object binding | Inspection is bound to the subsequently used object and detects replacement |
| `SR-G04` | Fail-closed behavior | Unknown, unsupported, changing, malformed, or oversized evidence stops safely |
| `SR-G05` | Command/dependency boundary | Every new executable, module, helper, compiler, or artifact is separately approved and frozen |
| `SR-G06` | No network or side effects | Verification is local, one-shot, bounded, read-only, and noninteractive |
| `SR-G07` | Atomicity preservation | Existing lock, staging, sync, rename, uncertainty, and append-only rules remain intact |
| `SR-G08` | Testability | Positive, negative, race, malformed, and recovery cases are reproducible with synthetic-only fixtures |
| `SR-G09` | Portability and failure | Unsupported hosts fail closed without fallback or silent policy reduction |
| `SR-G10` | Independent review | Security, operations, quality, and governance reviewers agree on the same frozen object |

Failure of any gate leaves operational use blocked. There is no weighted override.

## Required synthetic evidence

A later selected route must define and separately authorize tests for:

- no ACL, one allowed ACL, one unapproved ACL, inherited ACL, unreadable ACL, malformed ACL evidence, and ACL drift between checks;
- ordinary directory, true mount point, same-device alias model, changed mount identity, external review-root mount, and publication-parent mismatch;
- path replacement before and after open;
- symlink, hard-link, owner, mode, realpath, and ACL interactions;
- verifier absence, wrong identity, wrong signature, nonzero exit, stderr, oversized output, timeout or interruption, and ambiguous output if a verifier executable is selected;
- pre-rename and post-rename failures with the new checks present;
- no cleanup, retry, fallback, or warning-only downgrade; and
- unchanged packet cores, transactions, receipts, rollback records, and non-authorization fields.

Synthetic tests do not authorize a packet store or operational use. Any test requiring a real ACL, mount, privilege, helper, compiler, or executable needs its own exact execution authorization.

## Specialist reviews

The same frozen remediation object requires:

1. **Security/privacy review** — ACL semantics, mount aliasing, object binding, TOCTOU, untrusted output, and compromise recovery.
2. **Operations/recovery review** — host compatibility, failure preservation, orphan handling, diagnostics, and rollback.
3. **Quality/independent-verification review** — authoritative evidence, deterministic schemas, negative cases, and gate traceability.
4. **Governance review** — no authority expansion, explicit user/agent separation, and preserved operational block.

Any disagreement is recorded with the exact disputed claim, evidence, reviewer, proposed resolution, and gate impact. Silence is not acceptance.

## Staged approval gates

| Gate | Decision | Current state |
|---|---|---|
| `SR-1` | Accept or revise this remediation framework | Proposed |
| `SR-2` | Select one candidate route or explicit blocked disposition from primary evidence | Blocked |
| `SR-3` | Approve exact command, dependency, helper, toolchain, or attestation boundary if required | Blocked |
| `SR-4` | Approve the frozen implementation and synthetic-test plan | Blocked |
| `SR-5` | Approve implementation only | Blocked |
| `SR-6` | Accept static and specialist findings | Blocked |
| `SR-7` | Authorize exact synthetic execution | Blocked |
| `SR-8` | Accept evidence and close both security requirements | Blocked |
| `SR-9` | Authorize first packet-store initialization and operational trial | Blocked |

Gate `SR-9` cannot open unless `SR-G01` through `SR-G10` pass and the user explicitly approves operational use in a later instruction.

## Stop conditions

Stop and return for review if a route would:

- treat mode bits or `st_dev` as sufficient evidence;
- infer ACL absence from successful access;
- use an unapproved executable, module, compiler, SDK, helper, package, or generated artifact;
- invoke a shell, PATH-resolved command, network path, service, watcher, daemon, or elevated process;
- accept unbounded, locale-dependent, ambiguous, or unauthenticated evidence;
- add a retry, fallback, cleanup, warning-only mode, or user-bypass flag;
- create or inspect a real packet store, real packet, real correspondence, credential, key, or retained experiment input; or
- weaken the existing owner, mode, link, containment, identity, atomicity, rollback, or non-authorization controls.

## Rollback and recovery

This proposal is one additive uncommitted document. Rejection requires only an explicit decision about this exact path; it does not change the accepted implementation.

Any later remediation implementation must remain reversible before commit, name every changed path and hash, preserve the accepted implementation commit, and provide exact rollback instructions. No rejected verifier, helper, command, or dependency may remain installed, cached, enabled, or implicitly trusted.

## Review request

Review is requested on:

1. whether the ACL and mount-alias requirements are complete and remain non-negotiable;
2. whether Routes A through D cover the defensible resolution space without selecting one prematurely;
3. the mandatory evidence and ten pass/fail gates;
4. the synthetic-only test and specialist-review boundary;
5. the staged approvals and stop conditions; and
6. the preserved conclusion that operational use remains blocked.
