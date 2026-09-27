# Handoff Automation Security CS-0 Execution Authorization

**Status:** Proposed

**Proposal date:** 2026-09-19

**Review date:** Not reviewed

**Current authority:** Documentation and review only

**Execution effect:** None

**Execution state:** Blocked; not execution-ready

**Route-selection state:** No route selected or approved

**Operational-use state:** Blocked

## Purpose

Define the separate authorization object that may eventually bind one `CS-0` run to the immutable Accepted request, its final recorded SHA-256, accepted direct-argv runner evidence, exact executable identities, and external user approval.

This Proposed document does not authorize request hashing, an executable invocation, evidence-root creation, synthetic-canary creation, target inspection, `CS-0`, a downstream screening unit, route selection, packet-store creation, or operational use.

## Governing records and unresolved bindings

| Object | Required identity | Current state |
|---|---|---|
| [Accepted CS-0 request](HANDOFF-AUTOMATION-SECURITY-CS-0-AUTHORIZATION-REQUEST.md) | Path, commit, and final Accepted-request SHA-256 | Path and commit fixed; SHA-256 `UNRECORDED` |
| [Accepted execution-boundary document](HANDOFF-AUTOMATION-SECURITY-CS-0-EXECUTION-BOUNDARY-PROPOSAL.md) | Accepted commit and unchanged bytes | Accepted in commit `b21734b67ed8823551d56b9c327ea64b08aaa167`; document SHA-256 not recorded here |
| [Accepted-request hash record](HANDOFF-AUTOMATION-SECURITY-CS-0-ACCEPTED-REQUEST-HASH-RECORD.md) | Accepted path, commit, SHA-256, and reconciled subject evidence | `Proposed`; no accepted identity exists |
| Direct-argv runner evidence | Accepted path, commit, and evidence-manifest SHA-256 | Missing and unaccepted |
| Four pre-execution specialist findings | Findings over the same request and runner-evidence hashes | `Unproved` |
| External user execution approval | Must name the final SHA-256 of this document after acceptance and isolated commit | Missing |

Every unresolved item is a blocker. No value may be inferred from a path, an earlier approval, successful documentation review, or the absence of contrary evidence.

## Immutable Accepted-request identity

| Field | Required value or present state |
|---|---|
| Literal path | `/Users/bogac/dev/forgejo/mneme/docs/HANDOFF-AUTOMATION-SECURITY-CS-0-AUTHORIZATION-REQUEST.md` |
| Repository-relative path | `docs/HANDOFF-AUTOMATION-SECURITY-CS-0-AUTHORIZATION-REQUEST.md` |
| Accepted-request commit | `d44935f93317ef0950cc38a4f443feed6fe7b79a` |
| Accepted review date | `2026-09-19` |
| Final Accepted-request SHA-256 | `UNRECORDED — no accepted hash record exists` |
| Accepted hash-record path | `docs/HANDOFF-AUTOMATION-SECURITY-CS-0-ACCEPTED-REQUEST-HASH-RECORD.md` |
| Accepted hash-record commit | `UNRECORDED` |
| Accepted hash-record SHA-256 | `UNRECORDED` |

The final request SHA-256 must come from the separately accepted hash record. This authorization never edits the Accepted request and never places a self-referential hash in it.

## Direct-argv runner binding

| Field | Required value or present state |
|---|---|
| Accepted runner-evidence path | `UNRECORDED — no runner evidence accepted` |
| Accepted runner-evidence commit | `UNRECORDED` |
| Runner evidence-manifest SHA-256 | `UNRECORDED` |
| Host process-interface identity and version | `UNOBSERVED` |
| Pre-launch structured-record SHA-256 | `UNRECORDED` |
| Required executable | `/usr/bin/env` |
| `/usr/bin/env` bytes | `167712` |
| `/usr/bin/env` SHA-256 | `2b2a1145527f00e8369fda0d2ffc523b520201bb08dbaf4b0bded837f7652ce0` |
| Required runtime | `/usr/bin/perl` |
| `/usr/bin/perl` bytes | `167184` |
| `/usr/bin/perl` SHA-256 | `85e5621137742a37be052f58800372b2005f91f609ad55019832214b5d9e61bc` |

Both executables must remain regular, non-symlink Apple system files owned by `root:wheel` with mode `0755`. Static identities do not satisfy the runner gate. The accepted runner evidence must separately prove a structured executable/argv/envp invocation with `shell=false`, no command string, and literal metacharacter handling.

## Fixed execution mechanism

Every later process request must use:

```text
executable = "/usr/bin/env"
envp       = []
shell      = false
```

Each argv begins with the exact fixed prefix from the Accepted request:

```text
[
  "/usr/bin/env",
  "-i",
  "PATH=/usr/bin:/bin",
  "LC_ALL=C",
  "LANG=C",
  "TZ=UTC",
  "/usr/bin/perl",
  "-T",
  "-I-",
  "-e",
  "<EXACT-PROGRAM-SOURCE>",
  "<PROGRAM-MODULE-ARGUMENTS>",
  "--",
  "<EXACT-PROGRAM-ARGUMENTS>"
]
```

The accepted inline source, module arguments, and program arguments are incorporated by exact reference from the Accepted request. They may not be transcribed, reformatted, generated, wrapped, or changed in this authorization. No shell, terminal command string, wrapper script, helper, PATH lookup for Perl, inherited environment, standard input, retry, or fallback is allowed.

## Exact authorized CS-0 sequence

No sequence is currently authorized because the prerequisite bindings are unresolved. If this document later becomes execution-ready and receives hash-bound external user approval, the only permitted sequence is the following Accepted-request sections in this exact order:

| Order | Exact Accepted-request section | Invocation count | Exact arguments or substitutions | Declared outputs |
|---:|---|---:|---|---|
| 1 | `Exact root-creation command` | 1 | Literal root plus the accepted lowercase 64-hex request SHA-256 | `evidence/commands/CS0-ROOT.json` and declared owner-only directories |
| 2 | `Exact synthetic-fixture creation command` | 1 | Literal root plus the same accepted request SHA-256 | `fixture/cs0-canary.txt` and `evidence/commands/CS0-FIXTURE.json` |
| 3 | `Exact target-inspection command` | 6, sequentially in allowlist order | The same root and request SHA-256 plus exactly the six Accepted `(manifest ID, target path)` pairs | Six declared `evidence/tool-identities/*.json` records |
| 4 | `Exact core-evidence finalization command` | 1 | Literal root only | `evidence/OUTPUT-MANIFEST.sha256` and one bounded stdout digest |

The six target pairs remain exactly:

| Manifest ID | Non-candidate raw-byte target |
|---|---|
| `SR-COL-02` | `/usr/bin/shasum` |
| `SR-COL-04` | `/usr/bin/file` |
| `SR-COL-05` | `/usr/bin/otool` |
| `SR-COL-06` | `/usr/bin/nm` |
| `SR-COL-07` | `/usr/bin/sw_vers` |
| `SR-COL-08` | `/usr/bin/uname` |

The targets are read as raw bytes by Perl and are never executed. `/usr/bin/stat`, `/usr/bin/codesign`, candidate route paths, and every other path remain excluded.

## Request-hash substitution rule

Each `<ACCEPTED-CS0-REQUEST-SHA256>` token in the Accepted request must be replaced at process-request construction time by the one lowercase 64-hex value from the separately accepted hash record.

| Binding | Current value |
|---|---|
| Accepted request SHA-256 used for substitution | `UNRECORDED` |
| Hash-record commit supplying the value | `UNRECORDED` |
| Hash-record SHA-256 | `UNRECORDED` |

No other substitution is permitted. A missing, differently cased, differently sourced, mismatched, or unreconciled digest stops before root creation.

## Exact disposable root and writes

The only future runtime root is:

```text
/private/tmp/mneme-handoff-capability-cs0-20260919-01
```

It must be absent before execution. If later authorized, the commands may create only the root, directories, synthetic canary, command receipts, six non-candidate identity records, and self-excluding output manifest declared by the Accepted request. Directories are mode `0700`; regular evidence and fixture files are mode `0600`; all are owned by the current unprivileged user and group, contained on the root device, non-symlink, and exclusively created.

No packet store, home, cache, key, credential, socket, listener, service, watcher, log, source tree, installation, database, account artifact, correspondence, or real-data path may be created or read.

## Environment, permissions, and containment

- The working directory is exactly `/private/tmp`.
- Standard input is closed.
- The only process environment entries are `PATH=/usr/bin:/bin`, `LC_ALL=C`, `LANG=C`, and `TZ=UTC` supplied after `/usr/bin/env -i`.
- The current unprivileged identity is used; no elevation, identity switch, entitlement, or sandbox exception is permitted.
- `/private`, `/private/tmp`, the root, each child, each target, and each output must satisfy the ownership, mode, type, final-component symlink, realpath, link-count, device, inode, exclusive-create, sync, and containment rules frozen in the Accepted request.
- Empty outputs are captured outside the unit root by the separately accepted direct executor and bound by byte count and SHA-256. Only the finalizer may emit the one newline-terminated manifest digest within its 128-byte cap.
- No network API, proxy, DNS request, package manager, credential source, user configuration, Git write, or project-file write is permitted.

## Pre-execution specialist reviews

All four specialists must review the same final request SHA-256, accepted hash-record identity, runner-evidence manifest SHA-256, and final bytes of this authorization.

| Specialist | Current finding | Required pre-execution finding |
|---|---|---|
| Security/privacy | `Unproved` | Only the two frozen executables run; runner proof excludes shell mediation; six non-candidate targets are raw-read; no candidate, network, credential, real-data, API, packet, or operational path exists |
| Operations/recovery | `Unproved` | Exact root, permissions, partial-failure preservation, direct argv, evidence layout, output caps, and rollback boundary reconcile |
| Quality/independent verification | `Unproved` | Request hash, record hash, runner manifest, inline-program references, allowlist pairs, deterministic fixture, manifest members, and authorization bytes independently reconcile |
| Governance | `Unproved` | Request acceptance, hash recording, authorization acceptance, authorization hashing, external user approval, execution, and evidence acceptance remain distinct gates |

Each finding must record `Pass`, `Fail`, or `Unproved`, evidence hashes, disagreements, residual uncertainty, and acceptance conditions. Silence or majority vote is insufficient.

## Acceptance and external approval sequence

This authorization cannot become execution-ready until all of the following occur in order:

1. the direct-argv runner probe is separately authorized, executed, reviewed, and accepted;
2. the Accepted request is hashed under a separately accepted one-file hash authorization;
3. the Accepted-request hash record is completed, reviewed, marked `Accepted`, dated, and committed alone;
4. this document is updated with every final request, hash-record, runner-evidence, executable, command, root, exclusion, stop, rollback, and specialist binding;
5. all four pre-execution specialists review the same final bytes and hashes;
6. the user marks this authorization `Accepted`, records the review date, and commits it alone;
7. the accepted direct runner hashes the final committed bytes of this authorization, with that digest stored outside this document;
8. the user provides a new explicit execution approval that names that exact final execution-authorization SHA-256; and
9. a pre-execution reconciliation proves that all accepted bytes, hashes, commits, executable identities, repository state, root absence, and specialist approvals still match.

Acceptance of this document alone never authorizes execution. This document must not contain its own SHA-256.

## Required external hash-bound approval

The future approval must identify all of the following without ambiguity:

| Approval field | Current value |
|---|---|
| Accepted execution-authorization path | `docs/HANDOFF-AUTOMATION-SECURITY-CS-0-EXECUTION-AUTHORIZATION.md` |
| Accepted execution-authorization commit | `UNRECORDED` |
| Final execution-authorization SHA-256 | `UNRECORDED — intentionally external to this document` |
| Accepted request SHA-256 | `UNRECORDED` |
| Accepted runner-evidence manifest SHA-256 | `UNRECORDED` |
| Authorized unit | Exactly `CS-0` |
| Downstream authorization | None |

An approval that omits or mismatches the final execution-authorization SHA-256 is invalid and stops the sequence.

## Evidence required after any authorized run

The complete evidence package must preserve and reconcile:

- Accepted-request path, commit, final SHA-256, and accepted hash-record identity;
- execution-authorization path, commit, final externally named SHA-256, and approval reference;
- accepted runner-evidence path, commit, and evidence-manifest SHA-256;
- executable paths, bytes, hashes, owners, groups, modes, and types;
- canonical direct executable/argv/environment records and SHA-256 values for all nine invocations;
- start/end times, process identities, exit/signal states, and bounded stdout/stderr byte counts and SHA-256 values;
- `CS0-ROOT.json`, `CS0-FIXTURE.json`, the synthetic canary, six tool-identity records, and the self-excluding `OUTPUT-MANIFEST.sha256`;
- root, ownership, mode, symlink, device, inode, link-count, physical-containment, exclusive-write, and sync evidence;
- repository pre/post commit and working-tree status;
- `CS0-STOP-RECORD.md` if any deviation occurs;
- `CS0-ROLLBACK-STATE.md` describing preserved-root state and later disposition; and
- all four post-execution specialist findings over the same core-manifest SHA-256.

Evidence is not acceptance. All 25 `UNOBSERVED` entries remain unresolved until a separate evidence review and user acceptance.

## Stop conditions

Stop before root creation if any prerequisite is Proposed, unaccepted, uncommitted, missing, changed, ambiguous, or hash-mismatched, including the request hash record, runner evidence, specialist findings, this authorization, its external hash-bound user approval, or preflight reconciliation.

Stop immediately without retry, substitution, fallback, automatic cleanup, or downstream work if:

- a direct executable/argv/envp launch with `shell=false` cannot be proved;
- a shell, command string, wrapper, helper, retry, fallback, inherited environment, or unapproved executable would participate;
- either executable differs in path, bytes, hash, owner, group, mode, type, or provenance;
- the request, hash record, runner evidence, execution authorization, user approval, or substituted request digest does not reconcile;
- the CS-0 root exists before the first operation;
- an Accepted-request command, inline source, module argument, program argument, invocation count, ordering rule, target pair, output, cap, or boundary would change;
- an owner, mode, type, symlink, realpath, device, inode, link-count, containment, exclusive-create, sync, or required-core-module check fails;
- a process emits unexpected output, exceeds a cap, exits nonzero, receives a signal, or has uncertain completion;
- a candidate, forbidden prefix, retained input, credential, real-data path, network endpoint, packet path, service, watcher, build, test, or operational path would be accessed;
- `/usr/bin/stat` or `/usr/bin/codesign` would be inspected;
- repository state changes beyond separately authorized evidence documentation; or
- a missing or unavailable fact would be treated as success, route evidence, or approval.

On stop, preserve any already created CS-0 root owner-only, record the exact last completed operation and state, leave all 25 `UNOBSERVED` entries unresolved, and return for review. Do not retry or clean up automatically.

## Rollback

This Proposed document authorizes no runtime action and creates no runtime state. Its present rollback is deletion of this uncommitted draft only.

After a future complete or stopped run, preserve the exact root unchanged through evidence review. Any removal requires a separate authorization that names every existing path, removes files before directories through direct argv, uses no recursive operation, wildcard, shell, or discovery, and proves exact-root absence afterward. Stop on an unexpected child, symlink, device change, ownership change, or containment discrepancy.

Rollback may not modify a repository file, project history, packet store, handoff history, system path, candidate path, source path, or another evidence root.

## Explicit exclusions

This authorization never includes:

- `CS-COM`, `CS-A`, `CS-B1` through `CS-B4`, `CS-C`, `CS-D1`, or `CS-D2`;
- route selection, route execution, or mandatory-gate closure;
- network access, dependency addition, installation, package management, account access, or real-data access;
- packet-store creation, packet consumption, watcher, service, listener, or operational handoff use;
- application implementation, build, test, deployment, infrastructure, or production work;
- changing the Accepted request, evidence-source manifest, 25 `UNOBSERVED` entries, or another accepted record; or
- automatic rollback, retries, substituted paths, alternate tools, or expanded scope.

## Review request

Review this document only as the Proposed future `CS-0` execution-authorization record. Keep it Proposed and uncommitted until the final Accepted-request hash, accepted runner evidence, four specialist reviews, and exact external user approval sequence are complete. No command or runtime action is authorized by this draft.
