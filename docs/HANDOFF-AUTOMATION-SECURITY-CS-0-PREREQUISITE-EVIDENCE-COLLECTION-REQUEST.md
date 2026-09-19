# Handoff Automation Security CS-0 Prerequisite Evidence-Collection Request

**Status:** Accepted

**Proposal date:** 2026-09-19

**Review date:** 2026-09-19

**Current authority:** `PE-01` prerequisite evidence collection only

**Execution effect:** None

**Execution state:** `PE-01` authorized; `PE-02` and `CS-0` blocked

**Current allowed command/API invocation set:** `PE-01` only, after binding a qualifying structured process interface

**Route-selection state:** No route selected or approved

**Operational-use state:** Blocked

## Purpose

Define the evidence package required to resolve only the prerequisites that currently block the Proposed CS-0 Accepted-request hash record and the Proposed CS-0 execution authorization:

1. establish and bind one structured host process interface with a proved `shell=false` property;
2. prove literal shell-metacharacter handling and absence of shell mediation;
3. verify the pinned filesystem and byte identities of `/usr/bin/env` and `/usr/bin/perl`;
4. compute and record the final SHA-256 of the already Accepted CS-0 request; and
5. obtain security/privacy, operations/recovery, quality/independent-verification, and governance findings over the same evidence package.

This request was accepted on 2026-09-19 for prerequisite evidence collection only. The external approval authorizes `PE-01` subject to every boundary and stop condition in this document. It does not authorize `PE-02` or `CS-0`.

## Governing records

| Record | State | Effect on this request |
|---|---|---|
| [CS-0 Authorization Request](HANDOFF-AUTOMATION-SECURITY-CS-0-AUTHORIZATION-REQUEST.md) | Accepted 2026-09-19 at commit `d44935f93317ef0950cc38a4f443feed6fe7b79a` | Immutable subject whose final bytes must later be hashed |
| [CS-0 Execution-Boundary Proposal](HANDOFF-AUTOMATION-SECURITY-CS-0-EXECUTION-BOUNDARY-PROPOSAL.md) | Accepted 2026-09-19 at commit `b21734b67ed8823551d56b9c327ea64b08aaa167` | Requires a no-shell direct-argv boundary, non-self-referential hashes, staged review, and fail-closed behavior |
| [CS-0 Accepted-Request Hash Record](HANDOFF-AUTOMATION-SECURITY-CS-0-ACCEPTED-REQUEST-HASH-RECORD.md) | Proposed and unchanged | Must not be populated or edited until this evidence package is reviewed |
| [CS-0 Execution Authorization](HANDOFF-AUTOMATION-SECURITY-CS-0-EXECUTION-AUTHORIZATION.md) | Proposed and unchanged | Must not be populated or edited until this evidence package is reviewed |

Acceptance or execution of this request would not accept either Proposed record and would not authorize `CS-0`.

## Present blocker: no qualified process interface

The accepted boundary records that the currently available command interface accepts a shell command string. It does not expose a reviewed literal executable path, argv vector, environment vector, and `shell=false` field. It is therefore ineligible.

No replacement interface is identified in this request. The required binding remains:

| Interface field | Current value |
|---|---|
| Product/tool name | `UNBOUND` |
| Provider and provenance | `UNBOUND` |
| Immutable implementation identity or version | `UNBOUND` |
| Local executable, library, or service identity | `UNBOUND` |
| API operation name | `UNBOUND` |
| Structured executable field | `UNPROVED` |
| Structured argv field | `UNPROVED` |
| Structured environment field | `UNPROVED` |
| Explicit `shell=false` field and semantics | `UNPROVED` |
| Standard-input closure control | `UNPROVED` |
| Separate bounded stdout/stderr capture | `UNPROVED` |
| Pre-launch canonical request record | `UNPROVED` |

This request cannot become executable while any interface field is `UNBOUND` or `UNPROVED`. A later revision or separately reviewed interface-binding record must name the exact interface and immutable identity. A shell string, quoting convention, wrapper, terminal, successful child output, or claim that a shell probably optimized itself away is not a substitute.

## Scope boundary

The future evidence collection is limited to two executable units separated by a mandatory evidence-review gate:

| Unit | Purpose | May run when |
|---|---|---|
| `PE-01` | Prove the structured process interface, literal metacharacter delivery, fixed environment, and absence of shell mediation | Only after the interface identity is bound and this exact unit receives separate explicit approval |
| `PE-02` | Verify `/usr/bin/env` and `/usr/bin/perl` and hash the one Accepted CS-0 request file | Only after `PE-01` evidence and four specialist findings are separately accepted, and `PE-02` receives separate explicit approval |

The units may not be combined, reordered, retried, or treated as one approval. `PE-01` must stop for review before `PE-02` is eligible.

## Exact non-CS-0 evidence root

If and only if a later authorization permits evidence persistence, both units use this separate disposable prerequisite root:

```text
/private/tmp/mneme-handoff-cs0-prerequisites-20260919-01
```

This is not the CS-0 root. The following CS-0 path remains forbidden and absent:

```text
/private/tmp/mneme-handoff-capability-cs0-20260919-01
```

The prerequisite root must be absent before `PE-01`. Its creation, if later authorized, must use the qualified structured interface and a separately frozen direct-argv operation. The root and directories are mode `0700`; regular evidence files are mode `0600`; all are owned by the current unprivileged user and group, reside on the `/private/tmp` device, are non-symlink final components, and are physically contained beneath the literal root.

No fixture directory or CS-0 canary is permitted. The only planned evidence layout is:

```text
/private/tmp/mneme-handoff-cs0-prerequisites-20260919-01/
└── evidence/                                      0700
    ├── PE-01-HOST-INTERFACE.json                  0600
    ├── PE-01-PROCESS-REQUEST.json                 0600
    ├── PE-01-RUNNER-PROBE.json                    0600
    ├── PE-01-PROCESS-RECEIPT.json                 0600
    ├── PE-02-PROCESS-REQUEST.json                 0600
    ├── PE-02-IDENTITIES-AND-REQUEST-HASH.json     0600
    ├── PE-02-PROCESS-RECEIPT.json                 0600
    └── PREREQUISITE-EVIDENCE-MANIFEST.sha256      0600
```

The exact root-creation and evidence-persistence mechanism is intentionally unresolved with the process-interface binding. No root or evidence file may be created from this Proposed request.

## Frozen launcher and runtime claims to verify

`PE-02` must verify, not assume, these Accepted claims:

| ID | Exact path | Required type and permissions | Expected bytes | Expected SHA-256 |
|---|---|---|---:|---|
| `CS0-EXE-01` | `/usr/bin/env` | Regular non-symlink system file; `root:wheel`; mode `0755`; link count `1` | 167,712 | `2b2a1145527f00e8369fda0d2ffc523b520201bb08dbaf4b0bded837f7652ce0` |
| `CS0-EXE-02` | `/usr/bin/perl` | Regular non-symlink system file; `root:wheel`; mode `0755`; link count `1` | 167,184 | `85e5621137742a37be052f58800372b2005f91f609ad55019832214b5d9e61bc` |

The evidence for each path must include the literal path, physical path, file type, final-component symlink result, numeric UID and GID, symbolic owner and group where independently available, mode, link count, device, inode, byte count, SHA-256 over raw bytes, observation time, and the canonical evidence-record SHA-256.

A mismatch is a stop. It must not be repaired, reinterpreted as a platform update, or bypassed with an alternate executable.

## Structured process contract

Both executable units require the same reviewed host process request:

```text
executable = "/usr/bin/env"
argv       = [literal ordered values frozen for the unit]
envp       = []
shell      = false
cwd        = "/private/tmp"
stdin      = closed
stdout     = separately captured and capped
stderr     = separately captured and capped
```

The argv prefix is:

```text
[
  "/usr/bin/env", "-i",
  "PATH=/usr/bin:/bin",
  "LC_ALL=C",
  "LANG=C",
  "TZ=UTC",
  "/usr/bin/perl", "-T",
  <UNIT-MODULE-ARGUMENTS>,
  "-e", <EXACT-UNIT-PROGRAM-SOURCE>,
  "--", <EXACT-UNIT-PROGRAM-ARGUMENTS>
]
```

No other environment entry is permitted. `/usr/bin/env` must directly replace itself with the absolute `/usr/bin/perl` path. No PATH lookup for Perl, shell, command string, wrapper, pipe, redirection, glob, variable expansion, command substitution, subprocess, retry, resume, fallback, or helper is permitted.

The exact process-interface identity, complete argv byte strings, environment, working directory, standard-stream controls, output caps, and `shell=false` value must be serialized canonically and hashed before each launch. Host evidence may not be reconstructed later from a transcript.

## `PE-01`: structured-interface and no-shell probe

### Exact inert metacharacter argument

The probe passes the following UTF-8/ASCII text as one literal argv element:

```text
MNEME-RUNNER-PROBE-v1 space ; $ ( ) * ? [ ] ' " & | < >
```

The terminal line feed shown by Markdown is not part of the argument. The argument names no real command or filesystem path. It is data only and must not be evaluated.

The child must compare the received byte string directly with the frozen literal. It must report the expected and received byte counts and SHA-256 values, plus an exact-match Boolean. It must also report all environment keys and values and fail unless they are exactly:

```text
LANG=C
LC_ALL=C
PATH=/usr/bin:/bin
TZ=UTC
```

### Required host evidence

Before launch, `PE-01-HOST-INTERFACE.json` and `PE-01-PROCESS-REQUEST.json` must establish:

- exact product/tool/provider identity and immutable version or implementation hash;
- the API operation used and its primary documentation or local source identity;
- literal `executable`, each argv byte string, empty `envp`, `shell=false`, `cwd`, closed stdin, and independent output caps;
- a statement of whether any broker, launcher, terminal, wrapper, or helper exists between the API and `/usr/bin/env`;
- the operating-system process-creation primitive used by the interface;
- proof that no command-string field, shell option, expansion pass, or fallback path is reachable for this request;
- the canonical serialization rules and SHA-256 of the complete pre-launch request; and
- current unprivileged UID/GID and the absence of elevation or identity switching.

### Required child and receipt evidence

`PE-01-RUNNER-PROBE.json` and `PE-01-PROCESS-RECEIPT.json` must record:

- exact receipt of the metacharacter argument as one unchanged argv element;
- expected and received byte counts and SHA-256 values;
- exact-match result;
- exactly the four fixed environment entries and no others;
- child effective UID/GID;
- start and end times, process identifiers, exit and signal status;
- stdout and stderr byte counts and SHA-256 values under their approved caps;
- the pre-launch process-request SHA-256;
- no shell, helper, subprocess, pipe, redirection, glob, expansion, command substitution, or second child in the process evidence;
- no unexpected path creation beneath the prerequisite root; and
- absence of the forbidden CS-0 root before and after the unit.

Successful child output is supporting evidence only. `shell=false` must also be proved from the bound host interface and pre-launch request. If the host cannot provide both forms of evidence, `PE-01` remains `Unproved`.

## Mandatory review stop after `PE-01`

After `PE-01`, stop. Preserve the prerequisite root owner-only and present the complete evidence. Do not run `PE-02` until:

1. all four specialists review the same `PE-01` evidence-manifest SHA-256;
2. every specialist records `Pass`, `Fail`, or `Unproved`, evidence, disagreement, residual uncertainty, and acceptance conditions;
3. no blocking disagreement remains;
4. the user explicitly accepts the `PE-01` evidence; and
5. a separate hash-bound authorization for `PE-02` is reviewed and approved.

Acceptance of this request or successful `PE-01` output is not `PE-02` authorization.

## `PE-02`: executable identities and Accepted-request hash

`PE-02` may read exactly three paths as raw bytes:

```text
/usr/bin/env
/usr/bin/perl
/Users/bogac/dev/forgejo/mneme/docs/HANDOFF-AUTOMATION-SECURITY-CS-0-AUTHORIZATION-REQUEST.md
```

It may additionally inspect only the parent components required to prove literal-path and physical containment for those three paths and the already accepted prerequisite root. It may not enumerate a directory, walk a tree, follow a final-component symlink, inspect another executable, access Git internals, read an ignored path, or inspect any candidate path.

For the Accepted request, the evidence must record:

| Field | Required result |
|---|---|
| Literal path | `/Users/bogac/dev/forgejo/mneme/docs/HANDOFF-AUTOMATION-SECURITY-CS-0-AUTHORIZATION-REQUEST.md` |
| Repository-relative path | `docs/HANDOFF-AUTOMATION-SECURITY-CS-0-AUTHORIZATION-REQUEST.md` |
| Accepted commit binding | `d44935f93317ef0950cc38a4f443feed6fe7b79a` |
| Accepted review date | `2026-09-19` |
| Type | Regular non-symlink file |
| Link count | `1` |
| Owner, group, and mode | Observed exactly and reviewed |
| Physical path and containment | Observed exactly; contained in the approved checkout |
| Byte count | Independently observed from the same raw read |
| SHA-256 | Lowercase 64-hex digest over the exact raw bytes |

The one process must emit one bounded canonical JSON object containing the two executable identity records and the Accepted-request identity record. Standard error must be empty. The host receipt must bind the output to the exact pre-launch request SHA-256, runner evidence-manifest SHA-256, byte counts, output hashes, exit status, signal status, start/end times, and process identifiers.

No result may be copied into either existing Proposed record before the full prerequisite package and specialist findings are reviewed by the user.

## Evidence manifest

After `PE-02`, the self-excluding `PREREQUISITE-EVIDENCE-MANIFEST.sha256` must list exactly these seven evidence records in the declared order:

1. `evidence/PE-01-HOST-INTERFACE.json`
2. `evidence/PE-01-PROCESS-REQUEST.json`
3. `evidence/PE-01-RUNNER-PROBE.json`
4. `evidence/PE-01-PROCESS-RECEIPT.json`
5. `evidence/PE-02-PROCESS-REQUEST.json`
6. `evidence/PE-02-IDENTITIES-AND-REQUEST-HASH.json`
7. `evidence/PE-02-PROCESS-RECEIPT.json`

Each line contains lowercase SHA-256, two spaces, and the root-relative path with one terminal line feed. The evidence summary must record the manifest's byte count and SHA-256 separately. The manifest does not include itself.

If evidence persistence cannot be achieved without an unapproved writer, shell, helper, or additional path, stop and return the captured output for review; do not improvise a file-writing route.

## Specialist findings

Two review rounds are mandatory: one after `PE-01` and one after the complete package. The complete-package findings must all bind the same final evidence-manifest SHA-256.

| Specialist | Required complete-package finding |
|---|---|
| Security/privacy | The bound interface proves direct structured invocation and `shell=false`; metacharacters remained inert; only the three allowed files were raw-read; no candidate, credential, network, real-data, packet, or operational path was accessed |
| Operations/recovery | Exact identities, root boundary, permissions, process receipts, output caps, partial-failure preservation, stop behavior, and later rollback are complete and workable |
| Quality/independent verification | Interface identity, pre-launch request hashes, metacharacter bytes, environment, executable bytes and hashes, Accepted-request byte count and SHA-256, and manifest all reconcile independently |
| Governance | `PE-01`, its evidence acceptance, `PE-02`, the prerequisite-package review, record updates, CS-0 authorization, CS-0 execution, and CS-0 evidence acceptance remain distinct gates |

Each finding records its status, evidence paths and hashes, disagreements, residual uncertainty, and conditions for acceptance. Silence, majority vote, expected output, or lack of observed harm does not close a finding.

## Evidence-package acceptance conditions

The prerequisite evidence package may be accepted only if:

- the exact process interface and immutable identity are bound and independently reviewable;
- `shell=false` is proved by the host request and supported by literal metacharacter delivery;
- the fixed environment and no-helper/no-subprocess boundaries are proved;
- `/usr/bin/env` and `/usr/bin/perl` exactly match every pinned identity field;
- the immutable Accepted-request path, byte count, physical containment, and final SHA-256 reconcile;
- both process receipts and all seven evidence records reconcile to the self-excluding manifest;
- the forbidden CS-0 root remained absent and no CS-0 command or fixture ran;
- no candidate or excluded path was inspected;
- all four specialist findings bind the same evidence-manifest SHA-256 with no unresolved blocker; and
- the user explicitly accepts the package.

Package acceptance would permit a later proposed update to the two existing records. It would not itself edit those records, authorize `CS-0`, resolve any of the 25 `UNOBSERVED` route entries, select a route, or permit operational use.

## Stop conditions

Stop without retry, fallback, substitution, automatic cleanup, or downstream work if:

- this request or the unit-specific authorization is Proposed, uncommitted, missing, changed, or hash-mismatched;
- the structured process interface remains unbound or cannot prove literal executable/argv/envp invocation with `shell=false`;
- a shell string, shell executable, terminal, wrapper, helper, pipe, redirection, expansion, subprocess, retry, or fallback would participate;
- an executable, request file, process request, evidence record, or manifest differs from its reviewed identity;
- the metacharacter argument is split, transformed, evaluated, expanded, or not reported exactly;
- the environment contains anything other than the four fixed entries;
- either executable differs from its pinned path, type, owner, group, mode, link count, byte count, physical path, or SHA-256;
- the Accepted request differs from its literal path, Accepted commit binding, type, link count, physical containment, or reviewed bytes;
- an output exceeds its cap, standard error is nonempty, a process exits nonzero, receives a signal, or has uncertain completion;
- the prerequisite root or any output path already exists before its authorized exclusive creation;
- the CS-0 root or CS-0 canary would be created or read;
- a candidate path, forbidden path, retained input, credential, real-data path, network endpoint, dependency, packet path, watcher, service, listener, build, test, or operational path would be accessed;
- evidence persistence requires an unapproved writer or path;
- a specialist finding is missing, hash-mismatched, disputed, or `Fail`; or
- any missing fact would be inferred or treated as approval.

On stop, preserve only already authorized prerequisite evidence owner-only, record the exact last completed action, leave both Proposed records unchanged, and return for review. Do not retry.

## Rollback

This Proposed document creates no runtime root, fixture, process, or evidence. Its current rollback is deletion of this uncommitted draft only.

A later prerequisite root must remain preserved through evidence review. Removal requires a separate explicit rollback authorization naming every existing path. Files must be removed before directories through the accepted direct-argv interface, without a shell, recursive operation, wildcard, directory walk, or discovery. Stop on any unexpected child, symlink, owner, mode, device, or containment discrepancy.

Rollback may not touch the CS-0 root, either existing Proposed record, another repository file, project history, a candidate path, packet store, handoff history, or another evidence root.

## Explicit exclusions

This request does not authorize:

- creation or inspection of `/private/tmp/mneme-handoff-capability-cs0-20260919-01`;
- creation of the CS-0 synthetic canary or any CS-0 evidence member;
- execution of the Accepted request's root, fixture, target-inspection, or finalization commands;
- inspection or execution of candidate paths, including `/usr/bin/stat` and `/usr/bin/codesign`;
- `CS-COM`, `CS-A`, `CS-B1` through `CS-B4`, `CS-C`, `CS-D1`, or `CS-D2`;
- network access, dependencies, installation, package management, account access, correspondence, retained-input access, or real-data access;
- packet-store creation, packet consumption, watcher, service, listener, or operational handoff use;
- route selection, mandatory-gate closure, implementation, build, test, deployment, infrastructure, or production work;
- modification of either existing Proposed record before package review; or
- commit, push, retry, substitution, or automatic cleanup.

## Acceptance record

Accepted on 2026-09-19 for prerequisite evidence collection only. The accompanying external approval authorizes only `PE-01`. Before a child process may launch, the exact structured process-interface identity must replace the `UNBOUND` fields and satisfy the fail-closed checks above. `PE-02`, `CS-0`, evidence-root creation, candidate inspection, operational handoff use, commit of evidence, and push remain unauthorized. Keep the two existing Proposed records unchanged until the complete evidence package and specialist findings are reviewed.
