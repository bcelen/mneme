# Handoff Automation Security CS-0 Accepted-Request Hash Record

**Status:** Proposed

**Record date:** 2026-09-19

**Review date:** Not reviewed

**Current authority:** Documentation and review only

**Execution effect:** None

**Execution state:** Blocked

**Hash-recording state:** Not authorized; no hash operation has run

**Route-selection state:** No route selected or approved

**Operational-use state:** Blocked

## Purpose

Provide the separate, non-self-referential record in which a later authorized direct-argv operation can record the final SHA-256 and filesystem identity of the already Accepted CS-0 request.

This Proposed record contains no observed result. It does not authorize request hashing, a runner probe, `CS-0`, evidence-root creation, synthetic-canary creation, candidate inspection, network access, a packet operation, route selection, or operational use.

## Governing records

| Record | State | Binding |
|---|---|---|
| [Handoff Automation Security CS-0 Authorization Request](HANDOFF-AUTOMATION-SECURITY-CS-0-AUTHORIZATION-REQUEST.md) | Accepted 2026-09-19 | Immutable request at commit `d44935f93317ef0950cc38a4f443feed6fe7b79a` |
| [Handoff Automation Security CS-0 Execution-Boundary Proposal](HANDOFF-AUTOMATION-SECURITY-CS-0-EXECUTION-BOUNDARY-PROPOSAL.md) | Accepted 2026-09-19 | Defines document separation, direct-argv boundary, sequence, and fail-closed controls |
| Direct-argv runner evidence | Missing and unaccepted | Must prove the exact no-shell host process interface before hashing can be authorized |
| Hash-recording authorization | Missing and unaccepted | Must freeze the literal inline source, argv, environment, outputs, and rollback for the one-file read |

The Accepted request remains unchanged. This record is populated only after the direct-argv runner evidence and a separate hash-recording authorization are reviewed and accepted.

## Subject identity

| Field | Required value or present state |
|---|---|
| Literal repository path | `/Users/bogac/dev/forgejo/mneme/docs/HANDOFF-AUTOMATION-SECURITY-CS-0-AUTHORIZATION-REQUEST.md` |
| Repository-relative path | `docs/HANDOFF-AUTOMATION-SECURITY-CS-0-AUTHORIZATION-REQUEST.md` |
| Accepted-request commit | `d44935f93317ef0950cc38a4f443feed6fe7b79a` |
| Accepted status | `Accepted` |
| Accepted review date | `2026-09-19` |
| Final Accepted-request SHA-256 | `UNRECORDED — runner evidence and hash-recording authorization are not yet accepted` |

No placeholder in the Accepted request is edited to produce this value. The final SHA-256 is recorded only here after the immutable Accepted bytes are read through the separately accepted direct-argv boundary.

## Required observed file evidence

The later one-file operation must provide every field below from the same read. None is currently observed or inferred.

| Field | Current value | Acceptance rule |
|---|---|---|
| File type | `UNOBSERVED` | Regular file |
| Numeric owner UID | `UNOBSERVED` | Current approved repository owner |
| Numeric group GID | `UNOBSERVED` | Current approved repository group |
| Mode | `UNOBSERVED` | Recorded exactly and accepted by operations review |
| Link count | `UNOBSERVED` | Exactly `1` |
| Byte count | `UNOBSERVED` | Independently recorded from the read bytes |
| Physical path | `UNOBSERVED` | Must equal the approved physical repository path and remain contained in the checkout |
| SHA-256 | `UNRECORDED` | Lowercase 64-hex digest over the exact raw bytes |
| Repository commit at observation | `UNRECORDED` | Must equal `d44935f93317ef0950cc38a4f443feed6fe7b79a` for the subject bytes |
| Working-tree status of subject | `UNOBSERVED` | Clean relative to the Accepted commit |

Any mismatch, ambiguity, symlink, additional hard link, containment failure, or subject modification stops the operation without substituting another path or revising this record in place.

## Frozen launcher and runtime identities

These static identities are inherited from the Accepted execution-boundary document. They are required but do not by themselves prove that a conforming direct runner exists.

| Role | Exact path | Bytes | SHA-256 | Required owner/group/mode |
|---|---|---:|---|---|
| Empty-environment launcher | `/usr/bin/env` | 167,712 | `2b2a1145527f00e8369fda0d2ffc523b520201bb08dbaf4b0bded837f7652ce0` | `root:wheel`, `0755`, regular non-symlink file |
| Direct-argv runner/runtime | `/usr/bin/perl` | 167,184 | `85e5621137742a37be052f58800372b2005f91f609ad55019832214b5d9e61bc` | `root:wheel`, `0755`, regular non-symlink file |

No shell, command-string interface, wrapper, helper, pipe, redirection, glob, command substitution, PATH lookup for Perl, or inherited user configuration is permitted.

## Required runner and command bindings

The final record must name the accepted evidence for each item. The unresolved fields below are deliberate blockers.

| Binding | Current value |
|---|---|
| Accepted direct-argv runner-evidence path | `UNRECORDED — no runner evidence accepted` |
| Accepted direct-argv runner-evidence commit | `UNRECORDED` |
| Direct-argv runner-evidence manifest SHA-256 | `UNRECORDED` |
| Accepted hash-recording authorization path | `UNRECORDED — no hash operation authorized` |
| Accepted hash-recording authorization commit | `UNRECORDED` |
| Exact executable/argv/environment record SHA-256 | `UNRECORDED` |
| Host process-interface identity and version | `UNOBSERVED` |
| Pre-launch proof of `shell=false` | `UNOBSERVED` |

The later hash-recording authorization must freeze one structured process request with:

```text
executable = "/usr/bin/env"
envp       = []
shell      = false
```

Its literal argv must contain `/usr/bin/env`, `-i`, exactly `PATH=/usr/bin:/bin`, `LC_ALL=C`, `LANG=C`, and `TZ=UTC`, then the absolute `/usr/bin/perl` path and the separately reviewed inline source and arguments. The current record does not supply or authorize that process request.

## Permitted future operation

If separately authorized, the hash operation may read exactly the subject file and may perform only:

- exact literal-path validation;
- `lstat` and physical-containment checks;
- regular-file, non-symlink, owner, group, mode, link-count, and byte-count recording;
- one raw read of the subject bytes;
- SHA-256 calculation through the accepted Perl core `Digest::SHA`; and
- one bounded canonical JSON record on standard output.

It may not write a file, inspect another repository or system path, invoke a subprocess, access Git, inspect a candidate, read an ignored path, inherit credentials, or use a network API. This section defines the outer boundary only; it is not an execution authorization.

## Required process receipt

After a separately authorized operation, this record must be updated with evidence from the same process attempt:

| Receipt field | Current value |
|---|---|
| Start time in UTC | `UNRECORDED` |
| End time in UTC | `UNRECORDED` |
| Process identifier | `UNRECORDED` |
| Exit status and signal status | `UNRECORDED` |
| Standard-output byte count | `UNRECORDED` |
| Standard-output SHA-256 | `UNRECORDED` |
| Standard-error byte count | `UNRECORDED` |
| Standard-error SHA-256 | `UNRECORDED` |
| Canonical output-record SHA-256 | `UNRECORDED` |
| Candidate paths read | `NONE CLAIMED; UNPROVED UNTIL RECEIPT REVIEW` |
| Other paths read or written | `NONE CLAIMED; UNPROVED UNTIL RECEIPT REVIEW` |
| Network activity | `NONE CLAIMED; UNPROVED UNTIL RECEIPT REVIEW` |

The standard output must be the single bounded canonical record permitted by the accepted hash-recording authorization. Standard error must be empty. A nonzero exit, signal, truncation, malformed output, unexpected path, or uncertain completion is a stop, not a partial success.

## Specialist reviews

All specialists must review the same final record bytes and the same runner/hash evidence. No review has occurred.

| Specialist | Current finding | Required acceptance finding |
|---|---|---|
| Security/privacy | `Unproved` | The process used a proved no-shell direct-argv boundary, read only the one non-candidate request file, inherited no credentials, and used no network |
| Operations/recovery | `Unproved` | Identity, containment, output caps, failure preservation, and no-write boundary reconcile |
| Quality/independent verification | `Unproved` | Byte count, SHA-256, canonical receipt, executable identities, and evidence-manifest hashes independently reconcile |
| Governance | `Unproved` | Hash recording remains separate from request acceptance, execution authorization, external user approval, `CS-0`, and evidence acceptance |

Disagreements and residual uncertainty must be recorded explicitly. Silence, a majority, or successful output does not satisfy a review.

## Acceptance conditions

This record may become `Accepted` only when:

1. the direct-argv runner evidence has been separately reviewed, accepted, and bound by path, commit, and manifest SHA-256;
2. the exact one-file hash operation has been separately reviewed and authorized;
3. that operation has run once without a stop condition;
4. all required observed file and process-receipt fields are populated from preserved evidence;
5. the final request SHA-256, byte count, physical path, commit, and clean subject status reconcile independently;
6. all four specialist findings address the same evidence hashes and have no unresolved blocking disagreement; and
7. the user explicitly accepts this record, after which it is dated and committed alone.

Acceptance records an identity. It does not authorize `CS-0` or any other execution.

## Stop conditions

Stop without retry, fallback, substitution, cleanup, or inference if:

- the direct-argv runner evidence or hash-recording authorization is missing, Proposed, changed, uncommitted, or hash-mismatched;
- any shell, command string, wrapper, helper, inherited environment, or unapproved executable would participate;
- the subject path, commit, status, type, owner, group, mode, link count, byte count, physical path, or containment is uncertain or differs from the accepted boundary;
- any path other than the one subject file would be read, or any file would be written;
- a candidate path, retained input, ignored path, credential, packet path, or real-data path would be inspected;
- standard output or standard error violates its accepted grammar or cap;
- the process exits nonzero, receives a signal, or has uncertain completion;
- evidence hashes do not reconcile; or
- a missing value would be inferred, waived, or treated as approval.

On a stop, preserve only already authorized evidence, keep every unresolved field unresolved, and return for review. Do not retry.

## Rollback

This Proposed document creates no runtime root, fixture, credential, key, service, packet store, or machine evidence. Before any hash operation, documentation rollback is deletion of this uncommitted draft only.

A later hash operation is required to be read-only and must have its own accepted failure and evidence-preservation boundary. It may not modify the Accepted request, this record, another project file, a candidate path, or project history.

## Review request

Review this document only as the Proposed shape of the future Accepted-request hash record. Its hash and evidence fields intentionally remain unresolved. Do not accept it or authorize hashing until the direct-argv runner evidence, exact hash-recording authorization, four specialist reviews, and external user approval are complete.
