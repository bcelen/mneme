# Handoff Automation Security CS-0 Execution-Boundary Proposal

**Status:** Accepted

**Proposal date:** 2026-09-19

**Review date:** 2026-09-19

**Current authority:** Documentation and review only

**Execution state:** Blocked

**Route-selection state:** No route selected or approved

**Operational-use state:** Blocked

**Current allowed command/API invocation set:** Empty

**Accepted CS-0 request:** [Handoff Automation Security CS-0 Authorization Request](HANDOFF-AUTOMATION-SECURITY-CS-0-AUTHORIZATION-REQUEST.md), Accepted 2026-09-19

**Accepted-request commit:** `d44935f93317ef0950cc38a4f443feed6fe7b79a`

## Purpose

Resolve the two procedural blockers recorded before `CS-0` root creation without changing or re-accepting the immutable CS-0 request:

1. define a separately reviewed direct-argv runner boundary that cannot use a shell; and
2. move the final hash binding into a separate hash record and execution authorization so no document contains a self-referential hash.

This proposal does not authorize a runner invocation, hash calculation, evidence-root creation, synthetic-canary creation, tool inspection, `CS-0`, a downstream screening unit, route selection, packet-store creation, or operational use.

## Fixed conclusions

- The Accepted CS-0 request at commit `d44935f93317ef0950cc38a4f443feed6fe7b79a` remains immutable.
- Its exact commands, inline programs, root path, synthetic canary, six non-candidate inspection targets, permissions, checks, evidence layout, stop conditions, rollback boundary, and specialist reviews are not rewritten here.
- The Accepted request contains a substitution token for its final SHA-256. That token is resolved only by a later execution authorization; the request does not contain its own digest.
- The current shell-string command runner is ineligible for `CS-0`.
- All 25 `UNOBSERVED` occurrences in the accepted evidence-source manifest remain unresolved.
- No candidate path may be inspected while establishing the runner boundary or hashing the Accepted request.
- `CS-0` remains isolated from `CS-COM`, `CS-A`, `CS-B1` through `CS-B4`, `CS-C`, `CS-D1`, and `CS-D2`.

## Document separation

Four immutable objects must remain distinct:

| Object | Purpose | May contain its own SHA-256? |
|---|---|---|
| Accepted CS-0 request | Defines the frozen CS-0 operation and safety boundary | No |
| Direct-argv runner evidence | Proves one exact launcher/runtime boundary without a shell | No self-hash requirement; its containing evidence manifest supplies the hash |
| Accepted-request hash record | Records the final SHA-256 of the already Accepted CS-0 request | No; its later commit and external review identify it |
| CS-0 execution authorization | Names the Accepted-request SHA-256, runner evidence, and exact execution scope | No; the user approval outside the document names its final SHA-256 |

The execution authorization must never be merged into the Accepted request. Editing the Accepted request invalidates its hash record and requires a new request, new review, and new acceptance.

## Direct-argv runner boundary

### Exact executable identities

The boundary contains exactly one launcher and one runtime. Both identities come from previously accepted static evidence.

| Role | Exact path | Required type and permissions | Bytes | SHA-256 | Provenance |
|---|---|---|---:|---|---|
| Empty-environment launcher | `/usr/bin/env` | Regular Apple system executable; `root:wheel`; mode `0755` | 167,712 | `2b2a1145527f00e8369fda0d2ffc523b520201bb08dbaf4b0bded837f7652ce0` | Apple macOS; previously accepted static identity |
| Direct-argv runner/runtime | `/usr/bin/perl` | Regular Mach-O universal binary; `root:wheel`; mode `0755` | 167,184 | `85e5621137742a37be052f58800372b2005f91f609ad55019832214b5d9e61bc` | Apple macOS; previously accepted static identity |

No shell path is part of the boundary. In particular, `/bin/sh`, `/bin/zsh`, `/bin/bash`, a terminal application, `system`, backticks, a pipe-open, and a command-string API are prohibited.

### Invocation mechanism

A separately reviewed host process interface must invoke `/usr/bin/env` by supplying three structured values rather than a command string:

```text
executable = "/usr/bin/env"
argv       = [the literal argv vector approved for the operation]
envp       = []
shell      = false
```

The first argv element must be `/usr/bin/env`. Its next argument must be `-i`, followed only by the exact `NAME=value` entries frozen for the operation, then the absolute `/usr/bin/perl` path and its literal arguments. `/usr/bin/env` must replace itself with the absolute Perl path; no PATH lookup is used for Perl.

The current Codex command interface accepts a shell command string and therefore does not satisfy this mechanism. It remains ineligible unless a separately reviewed product capability exposes a true executable/argv/envp interface and produces the evidence below. Documentation that a tool is “shell-like,” command-line quoting, or successful output is insufficient.

### Fixed environment

Runner-boundary verification and Accepted-request hashing use exactly:

```text
PATH=/usr/bin:/bin
LC_ALL=C
LANG=C
TZ=UTC
```

No other variable may be present. The later CS-0 commands use the exact environment already frozen in the Accepted request. No `HOME`, proxy, credential, SSH agent, Perl module path, developer directory, pager, editor, shell, or user configuration may be inherited.

### Runner permissions

- Invocation uses the current unprivileged user and group; no elevation, entitlement, sandbox exception, or identity switch is permitted.
- The launcher and runner must match their frozen regular-file, owner, group, mode, byte-count, and SHA-256 identities before a runner probe can be authorized.
- Runner evidence may be written only beneath a separately approved owner-only disposable root; no such root is authorized or created by this proposal.
- Standard input is closed. Standard output and standard error are separately bounded and hashed.
- The runner may use only the Perl core modules named in the Accepted CS-0 request.

## Evidence that no shell mediated the command

The direct-argv boundary remains `Unproved` until one separately authorized synthetic runner probe produces all of the following:

1. a host-interface record showing `executable`, each argv byte string, the empty `envp`, and `shell=false` before process creation;
2. the host interface's own immutable implementation or product identity and version;
3. a canonical SHA-256 over the exact executable, argv, and environment record;
4. child output showing that a fixed shell-metacharacter canary arrived as one unchanged argv element;
5. child output showing that only the four fixed environment variables exist;
6. empty standard error, expected zero exit status, bounded output, and start/end process identifiers;
7. proof that no shell path, command string, pipe, redirection, glob, variable expansion, command substitution, or helper appeared in the launch request;
8. proof that no canary side-effect path was created; and
9. security, operations, quality, and governance findings over the same evidence-manifest hash.

The synthetic canary must be inert data. It must contain characters that a shell would interpret—space, semicolon, dollar sign, parentheses, asterisk, question mark, brackets, and quotes—without naming a real command or path. The Perl probe compares the received bytes with a literal expected byte string and fails closed on any difference. This runner probe is not `CS-0`, does not create the CS-0 evidence root or canary, and requires its own proposal and execution authorization.

If the host interface cannot identify itself, cannot guarantee direct argv, cannot set an empty environment without a shell, or cannot provide pre-launch structured evidence, the runner boundary remains blocked. No wrapper script, quoting strategy, or shell `exec` is an acceptable substitute.

## Accepted-request hash recording

The final SHA-256 of the Accepted CS-0 request must be produced only after the direct-argv runner evidence is accepted. The hash operation is separate from `CS-0` and reads exactly one non-candidate repository file:

```text
/Users/bogac/dev/forgejo/mneme/docs/HANDOFF-AUTOMATION-SECURITY-CS-0-AUTHORIZATION-REQUEST.md
```

The direct argv must use the frozen `/usr/bin/env` and `/usr/bin/perl` identities. The Perl program may perform only:

- exact literal-path validation;
- `lstat` and physical-containment checks;
- regular-file, non-symlink, owner, group, mode, link-count, and byte-count recording;
- raw read of that one file;
- SHA-256 calculation through the accepted core `Digest::SHA`; and
- one bounded canonical JSON record on standard output.

It may not write a file, inspect another path, invoke a subprocess, access Git, inspect a candidate, read an ignored path, or use a network API. Its exact inline source and argv must be frozen in a later hash-recording authorization and reviewed before invocation.

The resulting documentation record is proposed at:

```text
docs/HANDOFF-AUTOMATION-SECURITY-CS-0-ACCEPTED-REQUEST-HASH-RECORD.md
```

That record must contain:

- status and review date;
- the literal Accepted-request path;
- commit `d44935f93317ef0950cc38a4f443feed6fe7b79a`;
- observed type, owner, group, mode, link count, byte count, physical path, and SHA-256;
- launcher and runner identities;
- direct-argv runner-evidence manifest SHA-256;
- hash-command argv/environment record SHA-256;
- stdout/stderr byte counts and SHA-256 values;
- a statement that no candidate path was read; and
- specialist findings and unresolved uncertainty.

The hash record is reviewed and accepted as a separate document. It does not authorize `CS-0`.

## Separate execution authorization

After the hash record is accepted, prepare but do not execute:

```text
docs/HANDOFF-AUTOMATION-SECURITY-CS-0-EXECUTION-AUTHORIZATION.md
```

The execution authorization must name, literally:

1. the Accepted CS-0 request path and commit;
2. its final SHA-256 from the accepted hash record;
3. the accepted hash-record path, commit, and SHA-256;
4. the accepted direct-argv runner-evidence path, commit, and evidence-manifest SHA-256;
5. `/usr/bin/env` and `/usr/bin/perl` with the frozen identities above;
6. the exact CS-0 root, fixture, inspection, and finalization command identifiers from the Accepted request;
7. the substitution of the Accepted-request SHA-256 for every `<ACCEPTED-CS0-REQUEST-SHA256>` token;
8. the exact disposable root and authorized writes;
9. the preserved CS-0 exclusions, stop conditions, rollback, and specialist reviews; and
10. an explicit statement that no downstream unit, route, packet operation, or operational use is authorized.

The execution authorization must not contain its own SHA-256. After it is accepted and committed alone, the direct-argv hash operation records its final bytes in an external execution-authorization hash record or approval statement. The user's execution approval must name that exact SHA-256. This avoids self-reference while binding execution to immutable bytes.

## Exact staged sequence

The sequence is mandatory and may not be collapsed:

1. **Accept this proposal.** Mark this execution-boundary proposal `Accepted`, record the review date, and commit only it. No command runs.
2. **Prepare runner-probe documents.** Freeze the host direct-process interface, synthetic metacharacter probe, exact argv/envp, output caps, disposable probe root, rollback, and evidence manifest in separate `Proposed` documents.
3. **Accept and execute the runner probe.** Only after separate approval, run the synthetic probe. Stop on any shell mediation, identity drift, malformed evidence, or side effect.
4. **Accept runner evidence.** Four specialists review the same evidence hash; the user accepts the evidence in a separate record. This still does not authorize `CS-0`.
5. **Authorize Accepted-request hashing.** Freeze the exact read-only hash command and direct argv. Separately approve it.
6. **Record the Accepted-request hash.** Hash only the already Accepted request, prepare the hash record, review it, mark it `Accepted`, and commit it alone.
7. **Prepare the execution authorization.** Create the separate Proposed execution authorization naming the final Accepted-request SHA-256 and every controlling runner/hash identity.
8. **Accept the execution authorization.** Review, mark `Accepted`, date, and commit only that document. No execution is implied by document acceptance alone.
9. **Record the execution-authorization hash.** Use the accepted direct runner to hash the final Accepted execution-authorization bytes. Keep this hash outside that document.
10. **Issue explicit execution approval.** The user names the exact execution-authorization SHA-256 and authorizes `CS-0` only.
11. **Pre-execution reconciliation.** Rehash the Accepted request and execution authorization; require matches to the accepted records; validate runner identities, repository status, root absence, permissions, boundaries, and all four specialist approvals.
12. **Execute exactly `CS-0`.** Run only the commands frozen in the original Accepted request through the accepted direct-argv boundary.
13. **Stop for evidence review.** Preserve the evidence root and present the complete package. Do not resolve any `UNOBSERVED` marker until the user accepts a separate evidence record.

Any skipped, reordered, combined, or ambiguous stage stops the sequence.

## Reconciliation contract

Before `CS-0`, one canonical reconciliation record must show:

| Object | Required equality |
|---|---|
| Accepted CS-0 request | Current bytes equal the accepted hash record and commit path |
| Accepted-request hash record | Current bytes equal its accepted commit; it names the request hash actually substituted into argv |
| Direct-argv runner evidence | Evidence-manifest hash equals all four specialist findings and the execution authorization |
| Execution authorization | Current bytes equal the SHA-256 named by the user's external approval |
| Executables | Paths, bytes, SHA-256, owner, group, mode, and type equal the frozen identities |
| Commands | Inline source and argv equal the original Accepted request; only the accepted request-hash token is substituted |
| Repository | No unapproved path or state drift; packet store remains absent |
| Disposable root | Exact CS-0 root is absent before execution |

The reconciliation record is evidence, not authority. A mismatch cannot be repaired in place or waived with a warning.

After `CS-0`, the evidence summary must bind both documents independently:

- Accepted-request path, commit, SHA-256, and hash-record identity;
- execution-authorization path, commit, SHA-256, and external user-approval reference;
- runner-evidence manifest SHA-256;
- every direct argv and environment record SHA-256;
- CS-0 core evidence-manifest SHA-256;
- root, fixture, inspection, finalization, and rollback-state evidence;
- repository pre/post state; and
- all four post-execution specialist findings.

## Preserved CS-0 boundary

This proposal does not amend the Accepted request. The following remain exactly as accepted:

- only the declared owner-only CS-0 evidence root may be created;
- only the declared deterministic synthetic canary may be created;
- only the six declared non-candidate collection-tool files may be read as bytes;
- `/usr/bin/stat` and `/usr/bin/codesign` remain excluded because of their candidate roles;
- no target tool is executed;
- all ownership, mode, symlink, device, containment, exclusive-write, sync, evidence-manifest, output-cap, and fail-closed checks remain mandatory;
- partial or uncertain evidence is preserved owner-only without automatic cleanup;
- rollback remains separately approved and exact-path only;
- all 25 `UNOBSERVED` occurrences remain unresolved pending accepted evidence;
- the four specialist reviews remain mandatory before and after execution; and
- no network, dependency, account, real data, packet store, watcher, service, handoff operation, route selection, downstream screening, or operational use is permitted.

## Stop conditions

Stop without retry, substitution, fallback, root creation, or cleanup if:

- the proposal, runner evidence, hash record, or execution authorization is unaccepted, uncommitted, missing, changed, or hash-mismatched;
- the user approval does not name the exact final execution-authorization SHA-256;
- a command-string or shell-capable interface is the only available runner;
- the host interface cannot prove direct executable/argv/envp invocation with `shell=false`;
- `/usr/bin/env` or `/usr/bin/perl` differs from its frozen identity;
- the runner probe cannot prove literal metacharacter handling and the exact empty environment;
- a candidate or forbidden path would be inspected during runner proof or Accepted-request hashing;
- the Accepted request would be edited to insert its own hash;
- the execution authorization would contain or depend on its own embedded hash;
- the request hash substituted into a CS-0 command differs from the accepted hash record;
- any original CS-0 command, inline source, scope, check, output, rollback rule, or specialist gate changes;
- the CS-0 root exists before execution; or
- any original Accepted-request stop condition occurs.

## Rollback

This proposal creates no runner root, CS-0 root, fixture, evidence, hash record, or execution authorization. Its planning rollback is removal of this uncommitted document only.

Every later runner probe, hash operation, or `CS-0` run must carry its own accepted rollback boundary. No rollback may modify the immutable Accepted request, this proposal after acceptance, an accepted hash record, an execution authorization, project history, a candidate path, the packet store, or another evidence root.

## Specialist reviews

Four specialists review this proposal before acceptance:

| Specialist | Required finding |
|---|---|
| Security/privacy | The direct-argv boundary excludes shells and candidates; the hash flow is non-self-referential; no authority or data scope expands |
| Operations/recovery | Exact identities, staged gates, disposable roots, failure preservation, reconciliation, and rollback remain workable and fail closed |
| Quality/independent verification | Runner proof, hash records, document relationships, substitutions, and evidence hashes are independently reproducible and non-circular |
| Governance | Request acceptance, hash recording, execution authorization, user approval, execution, and evidence acceptance remain distinct gates |

All four must review the same proposal bytes and record `Pass`, `Fail`, or `Unproved`, disagreements, residual uncertainty, and acceptance conditions. Silence or majority vote is insufficient.

## Acceptance record

Accepted on 2026-09-19 as a planning and authorization-boundary document only. Acceptance does not authorize a runner probe, hash operation, evidence-root creation, synthetic fixture, candidate inspection, network access, dependency change, packet operation, route selection, or operational use.
