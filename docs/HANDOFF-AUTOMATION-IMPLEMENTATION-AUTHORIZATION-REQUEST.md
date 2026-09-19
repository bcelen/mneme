# Handoff Automation Implementation Authorization Request

**Status:** Accepted
**Request date:** 2026-09-19
**Review date:** 2026-09-19
**Authorization state:** Accepted for the exact four-file implementation; the approving instruction separately authorizes only the frozen 38-case synthetic test run after implementation
**Implementation state:** Not started; all four proposed implementation paths are absent
**Current authority:** After this authorization document is committed alone, create exactly the four frozen paths and run only `HT-001` through `HT-038` with the accepted local Perl boundary. Do not initialize a packet store, consume a packet, perform project work, commit implementation changes, push, or access the network.
**Governing plan:** [Local Handoff Packet Automation Implementation Plan](HANDOFF-AUTOMATION-IMPLEMENTATION-PLAN.md), Accepted 2026-09-19
**Frozen review package:** [Handoff Automation Implementation Review Package](HANDOFF-AUTOMATION-IMPLEMENTATION-REVIEW-PACKAGE.md), Accepted 2026-09-19
**Frozen-package commit:** `90d681c57da29116b4b8d8eba7b64d5a2296f3e2`
**Frozen-package SHA-256:** `6701aaa636fab1ddbe7740880c0578ea8241a1fbdb980bd82b30d7b3b5ce2fd8`

## Decision requested

After explicit acceptance of this exact request, authorize one documentation-controlled implementation step that adds only the four frozen tracked files listed below. The implementation step would write source, operator documentation, test source, and synthetic test-case definitions, then stop for the complete diff, hashes, static specialist review, and a new user decision.

Acceptance of this request alone would not authorize invoking the implementation, running a runtime or module preflight, creating the packet store, executing Git through the tool, creating runtime fixtures, running tests, creating a handoff packet, committing implementation files, pushing, or performing project work. The approving user instruction dated 2026-09-19 separately authorizes implementation of the exact four paths and one run of only the frozen 38 synthetic cases, while preserving every other prohibition.

This request was explicitly approved by filename and scope on 2026-09-19. No authority extends beyond the four frozen paths and the single 38-case synthetic test run.

## Interpretation of “verify before implementation”

The implementation files do not yet exist, so their contents, hashes, and behavior cannot truthfully be verified now. Pre-implementation verification therefore covers:

- the exact four-path object to be created;
- continued absence of those paths;
- the static identity of the already installed runtime and supporting binaries;
- completeness and internal consistency of the frozen command grammar, permissions, Git read scope, atomic-write contract, rollback contract, and 38-case test matrix; and
- the boundary of the future source-writing step.

Actual source conformance can be verified only after a separately authorized implementation creates the four files. That later verification is mandatory before any runtime invocation, packet-store creation, or test. This request does not collapse design verification and implementation verification.

## Pre-implementation verification record

The following checks were performed without creating an implementation path, invoking Perl, invoking the proposed Git commands, creating a fixture, or running a test.

| ID | Verification object | Evidence | Finding |
|---|---|---|---|
| `HIV-001` | Frozen package identity | Commit `90d681c57da29116b4b8d8eba7b64d5a2296f3e2`; SHA-256 `6701aaa636fab1ddbe7740880c0578ea8241a1fbdb980bd82b30d7b3b5ce2fd8` | `Pass` |
| `HIV-002` | Exact implementation paths | Static path checks returned absent for all four paths | `Pass`; absence is required before implementation |
| `HIV-003` | Runtime identity | `/usr/bin/perl`; regular file; `root:wheel`; mode `0755`; 167,184 bytes; SHA-256 `85e5621137742a37be052f58800372b2005f91f609ad55019832214b5d9e61bc` | `Pass` for static binary identity; runtime not executed |
| `HIV-004` | Supporting identities | `/usr/bin/env`, `/usr/bin/false`, and direct Command Line Tools Git matched the frozen bytes and SHA-256 values | `Pass` for static binary identities |
| `HIV-005` | Command grammar | Exactly four top-level operations; initialization and rollback are explicit modes; unknown forms fail before writes | `Pass` at frozen-design level |
| `HIV-006` | Permission boundary | Tracked files `0644`; future protocol state `0700`/`0600`; no elevated identity or write outside exact store | `Pass` at frozen-design level |
| `HIV-007` | Git read scope | One direct Git path; five read-only subcommands plus exact options; no remote, write, commit, push, hook, or external-command path | `Pass` at frozen-design level |
| `HIV-008` | Atomic-write contract | Exclusive lock, same-filesystem staging, file/directory sync, validation, atomic rename, no retry, uncertainty stop | `Pass` at frozen-design level; source/runtime behavior remains unproved |
| `HIV-009` | Append-only rollback | Separate user approval; exact receipt binding; one added rollback record; no rewrite or deletion | `Pass` at frozen-design level |
| `HIV-010` | Synthetic cases | Frozen package contains exactly 38 rows, `HT-001` through `HT-038` | `Pass` for matrix completeness; no test executed |
| `HIV-011` | No-authority boundary | Receipt requires `project_work_authorized=false` and `project_work_executed=false`; consumption cannot invoke work | `Pass` at frozen-design level |
| `HIV-012` | User/agent separation | Proposed agent verdict and Accepted user-approval record are distinct schemas and hashes | `Pass` at frozen-design level |
| `HIV-013` | Hidden-change boundary | Packet store permits protocol records only; source and implementation remain tracked; unexpected store entries invalidate state | `Pass` at frozen-design level |

`Pass at frozen-design level` is not a claim that absent code works. It means the accepted specification is complete enough to constrain implementation. Any later source discrepancy changes the finding to `Fail` or `Blocked` and stops before execution.

## Exact authorized implementation object

If separately approved, implementation may create exactly:

| ID | Path | Required mode | Maximum bytes | Required role |
|---|---|---:|---:|---|
| `HIF-001` | `tools/handoff/mneme-handoff.pl` | `0644` | 163,840 | Single production entry point and protocol logic |
| `HIF-002` | `tools/handoff/README.md` | `0644` | 65,536 | Exact operator boundary, commands, states, reason codes, and recovery guidance |
| `HIF-003` | `tools/handoff/t/handoff.t` | `0644` | 163,840 | Synthetic unit and fault-injection test source; not executed under this authorization |
| `HIF-004` | `tools/handoff/t/fixture-cases.json` | `0644` | 262,144 | Canonical fictional protocol cases only; not runtime output |

The necessary `tools/handoff/` and `tools/handoff/t/` parent directories may exist only as containers for those four tracked files. No sentinel, cache, log, lock, bytecode, result, coverage, temporary, package, module, generated, or fifth tracked path is authorized.

Implementation must use `apply_patch`-style repository edits. It must not install, copy from an external source, generate files by executing a program, or alter file modes to executable.

## Exact file-content requirements

### `HIF-001` — production source

The source must contain only:

- fixed imports from the accepted Perl core-module allowlist;
- closed constants for paths, schemas, enums, reason codes, limits, Git argv, and state precedence;
- canonical JSON and TSV readers/writers;
- byte-count and SHA-256 helpers;
- path, realpath, ownership, mode, type, link, mount, and containment validators;
- read-only repository-state collection through the frozen direct Git binary;
- packet identity, lineage, stale, conflict, verdict, approval, receipt, and rollback validation;
- exclusive-lock, same-filesystem staging, sync, atomic-rename, and uncertainty handling;
- the four-operation dispatcher; and
- `main()` guarded so tests may load pure functions without invoking the CLI.

The source must not contain:

- a network, socket, HTTP, DNS, IPC-service, database, container, mail, cloud, telemetry, analytics, scheduler, watcher, daemon, or agent API;
- shell evaluation, backticks, scalar `system`/`exec`, input `eval`, `qx`, dynamic import, plug-in loading, or PATH command discovery;
- a Git write or remote subcommand;
- a project command, build command, test command, commit command, or push command;
- a general-purpose command runner;
- an automatic repair, cleanup, retry, wait, resume, or fallback;
- a way for packet text to become code, a command, or authority;
- a production option that enables test adapters or fault injection; or
- a write outside the exact future packet store.

### `HIF-002` — operator documentation

The README must reproduce the exact four-operation grammar and fixed environment from the accepted package. It must clearly state:

- consumption records a handoff only;
- a verdict is not user approval;
- immutable packet cores are never edited;
- unsafe states fail closed;
- rollback appends history and deletes nothing;
- the packet store may contain protocol state only;
- no operation executes project work, commits, pushes, builds, tests, watches, or accesses the network; and
- every implementation, test, first-use, recovery, commit, and push step remains separately gated.

It must not present a command as currently authorized.

### `HIF-003` — test source

The test source must define exactly `HT-001` through `HT-038`, map each case to its frozen requirement, and use only:

- standard-library testing;
- owner-only temporary state after a future separate test authorization;
- fixed synthetic adapters and `fixture-cases.json`;
- internal function-level fault injection unavailable from production CLI; and
- explicit pre/post immutability assertions.

It must not invoke Git, Perl subprocesses, the production CLI, a shell, a network API, project code, or a real packet store during the frozen synthetic test run.

### `HIF-004` — synthetic cases

The JSON fixture file must contain only invented protocol metadata, hashes, paths, states, verdicts, approvals, receipts, rollbacks, and expected reason codes. It must not contain real correspondence, retained experiment data, credentials, keys, user identifiers, provider data, production paths other than the already accepted repository/runtime constants, or copied external content.

The file must be canonical JSON and include all 38 IDs exactly once.

## Runtime and dependency boundary

Source may target only the frozen `/usr/bin/perl` binary identity and the exact accepted core modules. Implementation does not authorize executing Perl to confirm its textual version or module inventory.

No dependency file, lockfile, package manager, CPAN action, downloaded module, local library, vendor tree, build step, or generated source is permitted. If implementation cannot be expressed within the accepted core-module boundary, stop and return with the precise missing primitive; do not substitute a runtime or module.

The implementation source must embed the expected runtime, `/usr/bin/env`, `/usr/bin/false`, and direct Git binary hashes as reviewed constants or document them as mandatory preflight inputs exactly as specified by the frozen package. It must not treat a path match alone as identity proof.

## Command grammar verification requirement

Static review after implementation must prove that the source accepts only:

```text
create --repo-root ... --initialize-store

create --repo-root ... --request-file ... --approval-gate ... --source ...
       [--source ...] [--prior-packet-id ...] [--supersedes-packet-id ...]

validate --repo-root ... --packet ...

validate --repo-root ... --packet ... --review-root ...
         --verdict-file ... --approval-file ...

list --repo-root ... [--verbose]

consume --repo-root ... --packet ... --review-root ...
        --verdict-file ... --approval-file ...
        --approved-verdict-sha256 ...

consume --repo-root ... --rollback --packet ... --receipt-sha256 ...
        --review-root ... --approval-file ...
```

Ellipses above denote fields with exact validators from the accepted package; they are not shell expansion or runtime defaults. Static review must enumerate every option and prove that there is no hidden alias, environment-controlled mode, positional fallback, abbreviation, configuration-file override, or fifth operation.

No handoff command, Perl invocation, test, or implementation-owned Git subprocess may run under this authorization. Host-side read-only status, diff, file-mode, byte-count, and SHA-256 inspection is permitted only to prepare the later review evidence. This section otherwise constrains source content only.

## Permission and path verification requirement

Static review must prove that source logic requires:

- tracked implementation files mode `0644`;
- future packet-store directories, locks, stages, packets, transactions, and rollback directories mode `0700`;
- future protocol files mode `0600`;
- external review root mode `0700` and verdict/approval files mode `0600`;
- matching real/effective non-elevated user IDs;
- exact physical containment and one-link regular files;
- no symlink, alias, mount, device, socket, FIFO, permissive mode, or unexpected ACL state;
- no mode or ownership mutation outside the packet store; and
- no read of prohibited content before path-policy validation.

The future packet store remains absent during implementation.

## Git read-scope verification requirement

Static review must extract every subprocess argv from source and prove that:

- the executable is always `/Library/Developer/CommandLineTools/usr/bin/git`;
- the fixed empty environment and `-c` restrictions are exact;
- allowed subcommands are only `rev-parse`, `symbolic-ref`, `status`, `ls-files`, and `check-ignore`;
- all repository roots and source paths are validated literal arguments;
- no shell is involved;
- no Git write, filter, hook, helper, remote, network, config-write, index-write, object-write, or ref-write form exists; and
- subprocess stderr, byte limits, timeouts if any, and nonzero statuses fail closed without retry.

No Git subprocess may be executed during implementation or static review.

## Atomic-write verification requirement

Static review must trace every future write from entry point through:

1. exact-root validation;
2. exclusive lock acquisition by `mkdir` without wait or retry;
3. repeated mutable-state validation under the lock;
4. same-filesystem owner-only staging;
5. `O_CREAT|O_EXCL|O_NOFOLLOW` regular-file creation;
6. bounded write, flush, file sync, close, reopen, and full validation;
7. staging-directory sync;
8. final-path absence check;
9. atomic rename;
10. parent-directory sync; and
11. exact successful lock removal only after publication is proven.

Source must preserve the lock and staged or published bytes when completion is uncertain. It must never retry publication, overwrite a final path, choose a winner among conflicts, or clean an orphan automatically.

Whether the frozen runtime actually exposes every required primitive remains an execution-time precondition. If static source review finds a fallback or cannot prove fail-closed behavior, the implementation result is rejected before any runtime invocation.

## Append-only rollback verification requirement

Static review must prove that rollback:

- is a mode of `consume`, not a hidden fifth operation;
- requires a new exact user-approval record distinct from the original verdict;
- binds the exact packet, transaction, and receipt hashes;
- records original and current repository-state hashes;
- creates one new canonical rollback record by the atomic protocol;
- changes only derived active state;
- does not open the packet core or transaction for writing;
- does not delete, rename, truncate, replace, or normalize prior history; and
- treats a second, mismatched, orphaned, or ambiguous rollback as conflict.

No cleanup or packet-store deletion command is authorized or implemented.

## Test-source verification requirement

Static review must produce a traceability table with one row for each `HT-001` through `HT-038`. Each row must identify:

- the frozen requirement and expected state or exit class;
- exact synthetic fixture ID;
- exact test-source location;
- production function under review;
- whether the test is pure, filesystem-local, or fault-injection;
- expected pre/post immutable hashes; and
- proof that the case cannot invoke a production command or external process.

Missing, duplicate, reordered-without-record, weakened, skipped, TODO, expected-failure, network-dependent, timing-dependent, or real-data-dependent cases block test authorization.

Writing the test source and static fixture definitions is within the requested future implementation scope. Executing them is not.

## Future implementation procedure

Only after explicit user approval of this request may the implementation turn:

1. re-read the accepted plan, frozen package, and accepted request hash;
2. confirm that all four exact paths remain absent;
3. confirm no implementation path is staged and no unrelated worktree state changed;
4. create only the required parent directories and four files through reviewable patches;
5. keep all four files mode `0644` and uncommitted;
6. perform static text inspection only, without invoking Perl, Git through the source, or any test;
7. record exact path, line count, byte count, mode, and SHA-256 for all four files;
8. present the complete diff and static import, subprocess, write-path, schema, state-machine, and test-traceability inventories; and
9. stop for review.

No packet-store, review root, fixture output, temporary test root, cache, command output, generated file, or evidence file may be created by the implementation step. Evidence is reported from read-only inspection in the review response unless a later document path is separately approved.

## Stop conditions

Stop without repair, substitution, cleanup, commit, or retry if:

- an authorized path already exists or changes after approval;
- a fifth path or file-mode change would be required;
- the accepted package, commit, or SHA-256 differs;
- the runtime or supporting static identity differs;
- a non-core module, dependency, generated source, or package action is needed;
- the four-operation grammar cannot be implemented exactly;
- a permission, path, Git, atomicity, rollback, or test requirement is ambiguous;
- source would need a shell, network module, general runner, dynamic loader, watcher, service, or project executor;
- a packet directory, runtime fixture, command, build, test, commit, push, or network operation would be required;
- real data, retained experiment inputs, credentials, keys, or production state would be read; or
- unrelated user changes overlap an authorized path.

On stop, preserve the uncommitted partial files exactly, report their paths and hashes, and return for review. Do not remove, normalize, or complete them implicitly.

## Rollback of the implementation step

All four authorized paths are currently absent. The implementation is therefore additive and remains uncommitted.

No automatic rollback is authorized. If the user later rejects the implementation and explicitly requests cleanup, cleanup must:

1. identify the exact four uncommitted paths and their reviewed hashes;
2. prove they did not pre-exist and are not staged or committed;
3. prove no other entry exists beneath `tools/handoff/`;
4. remove only the explicitly authorized files;
5. remove `tools/handoff/t/` and `tools/handoff/` only if each is then empty; and
6. show repository status afterward.

Cleanup must not use Git reset, checkout, clean, a wildcard, recursive removal of a nonempty directory, or removal of unrelated paths.

## Evidence required after implementation

Before any runtime or test authorization, present:

1. complete four-file diff;
2. exact path, mode, line, byte, and SHA-256 table;
3. proof that no fifth path, dependency, packet store, cache, or generated artifact exists;
4. full import/module inventory;
5. every external-command argv and caller;
6. every writable path and atomic transition;
7. all schemas, enums, limits, states, reason codes, and exit codes;
8. packet-core immutability and user-approval separation findings;
9. stale, conflict, malformed, and ambiguity failure paths;
10. append-only transaction and rollback findings;
11. `HT-001`–`HT-038` traceability;
12. four specialist static reviews required by the frozen package;
13. all uncertainties, disagreements, and stop findings; and
14. the exact separately authorized 38-case test command and its evidence.

No passing test result is expected or permitted at this stage.

## Requested authorization boundary

If accepted, this request would authorize only:

- creating the parent directories needed for the four tracked paths;
- writing those four files within their exact modes and byte ceilings;
- read-only static inspection and hashing of those four files and the repository status; and
- presenting the complete uncommitted implementation diff and static review package.

It would not authorize:

- invoking `/usr/bin/perl`, any implementation command, or a module/version preflight;
- invoking the direct Git binary through the implementation;
- running the test source or creating runtime fixtures;
- initializing `.mneme-local/handoffs/v1/` or any packet/review directory;
- creating, validating, listing, consuming, rejecting, approving, or rolling back a packet;
- executing project work or treating a receipt as authority;
- adding a dependency, installing anything, building, generating, watching, serving, or scheduling;
- accessing the network, accounts, real correspondence, retained experiment inputs, credentials, keys, the live archive, or production data;
- modifying another file, staging, committing, pushing, or configuring a remote; or
- beginning P3 execution, planner execution, R3-O1, Checkpoint B, stack selection, deployment, or real-data work.

## Approval record

The user explicitly approved this request on 2026-09-19 and:

1. named `HANDOFF-AUTOMATION-IMPLEMENTATION-AUTHORIZATION-REQUEST.md` explicitly;
2. accepted the design-level nature and limits of `HIV-001`–`HIV-013`;
3. authorized creation of exactly `HIF-001`–`HIF-004` and no other path; and
4. preserved the stop-before-packet-use, stop-before-project-work, stop-before-implementation-commit, and no-push boundaries.

The same instruction separately authorizes one execution of the frozen `HT-001`–`HT-038` synthetic test suite after implementation. Approval does not approve the later implementation diff or findings, packet-store initialization, first packet trial, operational use, project work, implementation commit, or push.

## Review request

Review is requested on:

1. the pre-implementation verification findings and their design-only limits;
2. the exact four-file additive implementation object;
3. runtime and dependency boundaries;
4. command, permission, Git read, atomic-write, and rollback verification requirements;
5. complete `HT-001`–`HT-038` source-traceability requirement;
6. stop, preservation, and exact cleanup conditions;
7. post-implementation evidence and specialist reviews; and
8. the narrow authorization boundary that stops before every command, test, packet-store action, commit, push, and project task.

Implementation and the single frozen synthetic test run may begin only after this document is committed alone. Every other operation remains unauthorized.
