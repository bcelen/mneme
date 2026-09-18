# Local Handoff Packet Automation Implementation Plan

**Status:** Accepted
**Proposal date:** 2026-09-19
**Review date:** 2026-09-19
**Implementation state:** Not started
**Current authority:** Accepted as a planning document only. Do not create the packet store, add tooling, execute a handoff command, build, test, push, access the network, or read real data.

## Purpose

This plan proposes the smallest local mechanism needed to create, validate, list, and consume numbered file-based handoff packets. A packet carries a bounded review request and exact identities; it does not carry authority to perform the requested project work.

The mechanism is a manually invoked, one-shot local command. Every invocation performs one named protocol operation and exits. It is not an agent, scheduler, daemon, watcher, hook, background process, service, or project-task runner.

The first version is intentionally narrow:

- local filesystem and read-only Git-state inspection only;
- one repository and one owner-only packet store;
- immutable numbered packet cores;
- externally reviewed verdict and approval records;
- append-only consumption and rollback records;
- SHA-256 integrity identities;
- no network, accounts, credentials, correspondence, archive data, cloud service, telemetry, build, test, project execution, commit, or push capability.

## Decision boundary

Review or acceptance of this plan would approve a design only. It would not authorize implementation, packet-store creation, runtime selection, dependency acquisition, command execution, fixture creation, build, test, commit, or push.

The implementation language and runtime remain unresolved. A later implementation request must identify an already available local runtime, prove that no new dependency or network access is required, name every repository path to be added, and present the complete proposed diff before execution. If the smallest implementation cannot be delivered as one standard-library-only local entry point plus documentation and synthetic protocol fixtures, the design must return for review.

## Non-goals

Version 1 will not:

- watch the repository or packet directory;
- poll, schedule, notify, or run continuously;
- interpret packet prose as commands;
- execute project work or invoke another agent;
- edit project files, accepted records, authorization requests, or decisions;
- approve, reject, or infer a user decision;
- commit, amend, merge, rebase, tag, push, fetch, pull, or configure a remote;
- invoke a compiler, build tool, test runner, package manager, container, service, database, or project executable;
- access the network, DNS, accounts, cloud AI, telemetry, analytics, or external storage;
- read real correspondence, the live archive, credentials, keys, backups, or production data;
- repair, renumber, overwrite, delete, or silently reconcile a packet;
- provide cryptographic proof of the human identity behind an approval; or
- replace the existing staged user-approval gates.

## Accepted local boundary

### Repository code boundary

A later implementation may propose one local entry point beneath:

```text
tools/handoff/
```

The exact file list and runtime must be separately approved. No implementation file is authorized by this plan.

### Packet-store boundary

The proposed runtime store is:

```text
<repository-root>/.mneme-local/handoffs/v1/
```

`.mneme-local/` is already explicitly ignored by the repository. The packet store therefore remains local and cannot be included by ordinary Git-add behavior. Its future root must be owned by the invoking user, mode `0700`, physically contained beneath the repository root, and marked by an exact versioned sentinel. Packet files must be mode `0600`; directories must be mode `0700`.

The implementation must reject a symlink, alias, mount point, ownership mismatch, permissive mode, unexpected hard link, unsupported filesystem object, or sentinel mismatch. It must never follow a link out of the packet store or repository.

### Permitted read boundary

The mechanism may read only:

1. its own implementation and protocol-version metadata;
2. the packet store;
3. read-only Git metadata needed for repository identity and status;
4. exact repository-relative project paths declared in a packet source manifest; and
5. exact externally prepared verdict and approval-record files named to a consume operation.

Before opening a declared project path, the mechanism must prove that it is a regular file physically inside the repository and outside every prohibited root. Version 1 must deny at least:

```text
.git/
.credentials/
.mneme-secrets/
.mneme-data/
.mneme-backups/
.mneme-generated/
.mneme-tmp/
```

The initial project-file allowlist is limited to the top-level `README.md`, `AGENTS.md`, and `.gitignore` files plus regular files physically beneath `docs/`, `experiments/phase-3/`, or the later accepted `tools/handoff/` implementation directory. Exact paths must still be declared individually; the implementation must not expand a recursive glob. Adding another root requires a revised review.

The mechanism must also reject a path ignored by Git, except for its own exact packet-store paths; an absolute input path; `..`; a symlink; a device; a socket; a FIFO; a directory payload; or a path outside the reviewed project-file allowlist. Encountering a changed or referenced path outside that allowlist is a stop, not permission to inspect it.

No packet may contain real correspondence, provider export data, archive content, credentials, keys, tokens, personal identifiers, or production data. This is a protocol rule and a stop condition; the mechanism is not a content-classification system and cannot prove that arbitrary text is synthetic.

## Minimal one-shot interface

The proposed command has exactly four top-level operations:

| Operation | Purpose | Repository writes | Packet-store writes |
|---|---|---:|---:|
| `create` | Allocate the next number and freeze one packet core | None | One new immutable packet directory |
| `validate` | Check structure, identities, repository state, verdicts, receipts, conflicts, and staleness | None | None |
| `list` | Report packet number, identity, state, and blocking reason without showing payload content | None | None |
| `consume` | Record one reviewed verdict and an acknowledgement receipt; never execute packet instructions | None | Append-only verdict/approval/receipt records for one packet |

Each operation must require an explicit repository root and packet number or input path. It must not search parent directories, use an ambient repository, discover another worktree, retry, fall back, or operate on more than one repository.

`consume` may include a narrowly defined rollback mode that appends a rollback record. It must not remove or alter the packet, verdict, approval record, or original receipt.

## Packet layout

Packet numbers are six ASCII decimal digits, starting at `000001`, with no reuse. The future layout is:

```text
.mneme-local/handoffs/v1/
├── MNEME_HANDOFF_STORE.json
├── packets/
│   └── 000001/
│       ├── packet.json
│       ├── request.md
│       ├── sources.tsv
│       ├── repository-state.json
│       ├── packet-manifest.sha256
│       ├── transactions/
│       │   └── <receipt-sha256>/
│       │       ├── verdict.json
│       │       ├── approval.json
│       │       └── receipt.json
│       └── rollbacks/
│           └── <rollback-sha256>.json
└── staging/
```

The five packet-core files are immutable after atomic publication. A verdict, approval, receipt, or rollback record is never part of the packet-core identity and is never overwritten. Verdict, approval, and receipt files are published together by one same-filesystem atomic rename of their containing transaction directory. More than one terminal transaction or rollback chain for a packet is a conflict unless the exact supersession relationship was separately reviewed and is mechanically unambiguous.

The `staging/` directory may contain only a same-filesystem temporary packet being created. A stale staging entry is reported as an orphan and never resumed or deleted automatically.

## Packet schema and identity

`packet.json` must use a versioned, closed schema: unknown keys are rejected. It must contain at least:

- schema and protocol versions;
- six-digit packet number;
- packet purpose and bounded review question;
- creation time in UTC for audit only;
- repository physical root identity;
- Git `HEAD` object ID or explicit unborn state;
- symbolic branch name, if one exists;
- repository-state SHA-256;
- request SHA-256;
- sources-manifest SHA-256;
- prior packet ID, when this packet continues a chain;
- superseded packet ID, when explicitly applicable;
- declared approval gate and non-authorization boundary;
- exact permitted source-path count and aggregate byte count; and
- packet ID.

JSON identities use UTF-8, LF endings, sorted keys, no insignificant whitespace, no duplicate keys, and integers rather than floating-point values. TSV files use UTF-8, LF endings, a fixed header, tab separators, lexically ordered repository-relative paths, and no escaping ambiguity.

The packet ID is:

```text
SHA-256(
  "mneme-handoff-packet-v1" || NUL ||
  canonical packet metadata excluding packet_id || NUL ||
  request.md SHA-256 || NUL ||
  sources.tsv SHA-256 || NUL ||
  repository-state.json SHA-256
)
```

`packet-manifest.sha256` records the path, byte count, and SHA-256 of the other four core files in fixed path order. It excludes itself and every later verdict, approval, receipt, and rollback record. Validation must independently recompute every component and the packet ID.

The timestamp, packet number, and prose are included in the immutable metadata. Two otherwise similar packets are therefore distinct and cannot silently substitute for one another.

## Number allocation and atomic creation

`create` must:

1. validate the packet-store root and sentinel;
2. acquire one exclusive, owner-only, same-filesystem creation lock without waiting;
3. enumerate valid six-digit packet directories and choose exactly `maximum + 1`;
4. reject malformed names, duplicate numbers, gaps caused by unexplained existing state, or overflow;
5. validate the proposed request and exact source manifest before reading source content;
6. capture the repository state and source identities;
7. write all core files into one new owner-only staging directory;
8. validate that staged packet as if it were published;
9. atomically rename the staged directory to its numbered final path; and
10. release the lock and print only the number, packet ID, manifest hash, and state.

There is no automatic retry. A lock collision, final-path collision, unexpected directory, failed write, failed sync, validation error, or uncertain rename stops creation. A packet number is not reused after a published packet exists, even if it is later rejected, consumed, rolled back, or superseded.

The mechanism must not alter Git state or the input request/source files. The ignored packet store is the only writable location.

## Repository-state contract

The mechanism must establish repository state without reading undeclared file content. The state record includes:

- physical repository root and Git directory identity;
- `HEAD` object ID or unborn state;
- symbolic branch or detached state;
- exact, NUL-safe Git status entries, including all untracked non-ignored paths;
- index mode, object ID, and stage for each changed or declared path;
- worktree type, mode, byte count, and SHA-256 for each changed or declared regular file inside the allowlist;
- explicit deletion state where a worktree file is absent;
- packet-store exclusion; and
- a canonical repository-state SHA-256.

Git status may identify a prohibited or unapproved path by repository-relative name, but the mechanism must stop before opening or hashing that path. Unchanged tracked content is represented by `HEAD`; changed, staged, and untracked safe files are represented individually. This records staged and unstaged differences without generating or storing a full repository diff.

Creation is permitted from a dirty worktree only when every status path is inside the explicit project-file allowlist and every changed path is represented in the state record. A dirty but unrepresented path is a stop. The packet request must clearly say that the recorded state is dirty.

Immediately before `consume` writes anything, it must recapture the same state fields. Any difference is stale state, even if the changed path appears unrelated. The user may then request a new packet; the mechanism must not refresh an existing packet in place.

## Source manifest and hashes

`sources.tsv` identifies only the exact files relevant to the handoff. Each row contains:

```text
relative_path	type	mode	bytes	sha256	role
```

Version 1 accepts only regular files. `role` is one of `proposal`, `evidence`, `governing-input`, or `supporting-record`. Unknown roles are rejected.

The packet request may summarize source content but must not embed an unchecked recursive diff, archive, binary, generated cache, database, secret, or real-data excerpt. File-size and aggregate-size ceilings must be frozen in the later implementation request. Exceeding either ceiling is a stop requiring a revised plan, not automatic truncation.

Validation recomputes every source identity. Missing, extra, changed, moved, linked, ignored, prohibited, or out-of-root source paths make the packet stale or invalid as defined below.

## Packet states

`list` and `validate` use these closed states:

| State | Meaning |
|---|---|
| `Pending` | Core is valid, repository state matches, and no terminal verdict exists |
| `Ready` | A `validate` preflight over the core plus exact external verdict and approval files succeeds; this transient result is not stored before consumption |
| `Consumed` | One valid verdict, approval record, and receipt agree on the exact packet and current repository state |
| `Rejected` | A user-approved `Reject` verdict has been consumed |
| `ChangesRequested` | A user-approved `ChangesRequested` verdict has been consumed; a new numbered packet is required |
| `RolledBack` | A valid user-approved rollback record supersedes the one receipt without deleting history |
| `Stale` | The packet was valid when created but a required current identity no longer matches |
| `Conflict` | Two individually parseable records make the packet's controlling state ambiguous |
| `Invalid` | Structure, containment, schema, hash, permission, or identity validation fails |

`list` displays no request body or source content. It prints the packet number, abbreviated packet ID, stored state, verdict if any, creation time, base `HEAD`, and a stable reason code. Before a transaction is consumed, ordinary listing reports a valid packet as `Pending`; `Ready` is available only from an explicit read-only `validate` preflight supplied with the external verdict and approval files. A verbose listing may show exact hashes and repository-relative project paths but no file contents.

## Stale-packet rules

A packet is `Stale` when its immutable core remains valid but any of these conditions holds:

- current `HEAD`, branch state, Git status set, index identity, or represented worktree identity differs;
- a declared source path is missing, moved, changed, or no longer permitted;
- its declared predecessor or superseded packet no longer has the recorded identity;
- a newer valid packet explicitly supersedes it;
- a verdict or approval record targets an earlier packet hash or repository-state hash; or
- the accepted protocol version no longer permits the packet schema.

Age alone does not make a packet stale in version 1. There is no hidden expiry interval. A future expiry policy requires separate review.

Stale packets remain immutable and visible. They cannot be refreshed, consumed, or silently discarded. Replacement requires a new number that names the stale packet as its predecessor or superseded packet.

## Conflict rules

A packet is `Conflict` when validation finds any of the following:

- two packet directories or aliases claim the same number with different identities;
- a number, directory name, internal packet number, or packet ID disagrees;
- two terminal transactions with different verdict identities exist for one packet;
- verdict and approval records disagree about packet ID, manifest hash, repository-state hash, scope, or decision;
- more than one active transaction or receipt exists;
- a rollback targets no receipt, the wrong receipt, or an already rolled-back receipt;
- predecessor or supersession relationships form a fork, loop, or contradictory chain;
- two live packets claim the same exclusive approval gate and overlapping project paths without an explicit predecessor relationship; or
- a partial publication, uncertain atomic operation, or unexpected protocol file makes controlling state ambiguous.

The mechanism does not pick a winner. `create` and `consume` stop while any relevant conflict exists. Conflict resolution requires a separately reviewed record and, normally, a new numbered packet.

## Verdict and user-approval contract

Allowed verdicts are exactly:

- `Approve`;
- `Reject`; and
- `ChangesRequested`.

A verdict is an externally prepared, immutable canonical JSON file. It names the packet number, packet ID, packet-manifest hash, repository-state hash, reviewed source-manifest hash, verdict, bounded rationale, unresolved concerns, reviewer role, and proposal date. It has its own SHA-256 and remains untrusted until the user explicitly reviews that exact hash.

The mechanism must never create an `Approve` verdict, infer approval from prose, treat a document's `Accepted` status as packet approval, or infer approval from a prior conversation. Before `consume`, a separate canonical approval record must name:

- the exact packet ID;
- exact verdict SHA-256;
- exact repository-state SHA-256;
- approval date;
- approval authority `user`;
- a durable reference to the user decision; and
- SHA-256 of the exact approval statement when that statement is retained outside the packet store.

The user must explicitly authorize consumption of the named packet and verdict hash. An agent's creation of an approval record is transcription, not approval. The mechanism can validate internal consistency and local file integrity, but version 1 cannot cryptographically authenticate the user's identity or the external conversation. This limitation must appear in every consumption receipt.

An `Approve` verdict authorizes only recording the verdict as consumed. It does not authorize the project work described by the packet. Any architecture, privacy/security, external-service, destructive, deployment, real-data, implementation, build, test, commit, or push action still requires its ordinary explicit gate.

## Consume transaction

`consume` must take one packet number, one exact verdict file, one exact approval-record file, and the user-approved verdict SHA-256. It must:

1. validate the store, packet core, source identities, predecessor chain, verdict, and approval record;
2. require the supplied verdict hash to match both the file and approval record;
3. require the current repository state to match the packet exactly;
4. reject stale, conflicting, invalid, already consumed, or rolled-back state;
5. acquire one packet-specific owner-only lock without waiting;
6. repeat every mutable-state and repository-state check after acquiring the lock;
7. copy the exact verdict and approval records without modification into a new owner-only transaction staging directory beneath `transactions/`;
8. create one canonical receipt in that directory naming all identities, the decision, the tool identity, and the fact that no project work was executed;
9. atomically rename the complete transaction directory to `transactions/<receipt-sha256>/`; and
10. release the lock and print only the packet number, final state, and record hashes.

If the verdict is `Reject` or `ChangesRequested`, consumption records that decision and closes the packet. It does not modify the request or create the replacement packet automatically.

No consume operation may run a command found in the packet, alter the repository, invoke a project tool, or continue to another stage.

## Rollback

Packet cores, verdicts, approval records, and receipts are never deleted or rewritten. A consumed packet may be rolled back only after a separate explicit user instruction names the packet ID and receipt hash.

Rollback is an append-only mode of `consume`. It validates the store, immutable packet core, exact transaction and receipt, new user approval, and lock conditions. It records the current repository-state hash but does not require that current state to equal the packet's original state; repository drift must not make an erroneous protocol receipt impossible to revoke. It then writes one `rollback` record that names the exact receipt, reason, approval reference, original repository-state hash, and current repository-state hash. The resulting state is `RolledBack`.

Rollback does not undo project work because the mechanism never performs project work. It only reverses the protocol assertion that the packet's verdict is the active consumed handoff. A replacement requires a new numbered packet. A rollback mismatch or ambiguous receipt is a conflict and stops without change.

## Failure handling

The mechanism is fail-closed and performs no automatic repair, cleanup, retry, or fallback.

| Failure point | Required result |
|---|---|
| Before a staging or consume lock | No write |
| After lock but before staging write | Release lock; no packet change |
| During packet staging | Preserve or report the owner-only orphan; do not publish it |
| Before final packet rename | Existing numbered packets remain unchanged |
| During verdict/approval/receipt staging | No record becomes active until the complete transaction directory is atomically published |
| Uncertain publish result | Re-run read-only validation only; never repeat consumption automatically |
| Hash, schema, permission, path, or repository mismatch | Mark result invalid or stale and stop |
| Multiple records or chain ambiguity | Mark conflict and stop |
| Output or write outside packet store | Stop, preserve evidence, and require security review |

Diagnostics must contain reason codes and repository-relative protocol paths only. They must not print request bodies, source contents, verdict rationale, approval text, secrets, or real-data-like payloads.

Exit status classes must distinguish success, invalid packet, stale packet, conflict, approval failure, repository-state mismatch, unsafe path, lock contention, and internal failure. Exact numeric values belong in the later implementation request.

## Validation order

`validate` must perform checks in this order and stop at the first unsafe boundary while still reporting independently safe structural findings:

1. repository-root and packet-store containment;
2. owner, mode, sentinel, file type, link, and mount checks;
3. packet directory naming and unique numbering;
4. closed-schema and canonical-encoding checks;
5. packet-core byte counts and hashes;
6. packet-ID recomputation;
7. source-manifest path-policy checks before source reads;
8. source identities;
9. repository-state identity;
10. predecessor and supersession chain;
11. verdict and approval identities;
12. receipt and rollback identities;
13. stale-state determination;
14. conflict determination; and
15. final state.

Validation is read-only. It must not normalize line endings, modes, JSON, manifests, stale records, or numbering.

## Security and privacy controls

- Run with the invoking user's existing privileges; never request elevation.
- Use an empty or explicitly bounded environment; ignore proxy, credential, editor, pager, hook, and Git external-command settings.
- Disable Git hooks, external diff/textconv, smudge/clean filters, pager, and credential helpers for every read-only Git invocation.
- Use literal argument arrays and fixed command paths; never evaluate packet text, shell fragments, templates, substitutions, aliases, or globbed input.
- Enforce owner-only packet-store permissions and refuse permissive inherited state.
- Apply fixed file-count and byte ceilings before hashing content.
- Reject symlinks and path traversal before opening files.
- Do not log payload content.
- Never place secrets, real data, approval text, or full diffs in the packet store.
- Make no network call and expose no listener.
- Record the implementation-file SHA-256 and protocol version in every packet and receipt.

Packet content is untrusted data. Text such as "approve," "run," "commit," or an apparent instruction has no control authority.

## Required evidence for later implementation review

A later implementation package must present, before any execution:

1. exact implementation paths, line counts, byte counts, and SHA-256 values;
2. runtime/compiler identity and proof that no dependency acquisition is needed;
3. complete command interface and closed schemas;
4. source-path allowlist, prohibited roots, size ceilings, and command-path allowlist;
5. proof that there is no daemon, watcher, scheduler, hook, network, commit, push, project execution, build, or test path;
6. packet identity and canonicalization review;
7. Git-state capture and dirty-worktree review;
8. stale, conflict, verdict, approval, receipt, and rollback state-transition review;
9. atomic-publication and lock behavior;
10. failure-mode and diagnostic inventory;
11. synthetic-only protocol fixtures for valid, invalid, stale, conflicting, rejected, changes-requested, consumed, and rolled-back cases; and
12. test-to-requirement traceability for the handoff tool itself.

Preparation of fixtures or execution of the handoff tool's own tests requires a separate authorization. The runtime mechanism must never invoke Mneme project builds or tests.

## Required specialist reviews

| Review | Required finding before implementation authorization |
|---|---|
| Orchestrator / governance | Packets do not confer project authority; exact user gates, supersession, and non-authorization wording are preserved |
| Security / privacy | Path confinement, no-real-data boundary, untrusted-text handling, permissions, environment, no-network behavior, and diagnostics fail closed |
| Quality / independent verification | Canonical identities, repository-state capture, state machine, stale/conflict cases, atomic operations, and evidence are deterministic and testable |
| Operations / recovery | One-shot lifecycle, locks, partial-write handling, append-only rollback, and orphan behavior cannot silently lose or overwrite a packet |

Any non-`Pass` finding or unresolved disagreement blocks implementation.

## Implementation stages and gates

| Gate | Scope | Current state |
|---|---|---|
| `H0` Plan review | Review this document | Accepted 2026-09-19 |
| `H1` Implementation package | Exact runtime, paths, schemas, source, fixtures, and traceability presented as a complete diff | Blocked |
| `H2` Static specialist review | Four reviews over the frozen implementation object | Blocked |
| `H3` Synthetic tool verification | Separately authorized local tests over protocol-only synthetic fixtures | Blocked |
| `H4` First packet trial | Separately authorized creation/validation/list/consume cycle containing no project execution | Blocked |
| `H5` Operational acceptance | User accepts evidence and defines whether the mechanism may be used | Blocked |

No gate implies the next. Plan acceptance does not authorize implementation. Implementation review does not authorize execution. Synthetic verification does not authorize consuming a real project handoff. Consuming a packet does not authorize its requested project work.

## Definition of done

The first version is complete only when:

- the exact implementation object and runtime have been separately approved;
- all four operations are one-shot, local, offline, and confined to the packet store plus declared read-only inputs;
- packet numbering and identity are deterministic and immutable;
- dirty repository state is exactly represented or rejected;
- stale and conflicting packets fail closed;
- verdict and approval records bind to exact packet and repository hashes;
- consumption writes only append-only protocol records and executes no project work;
- rollback preserves the full history;
- all failure paths are bounded and reviewable;
- synthetic protocol checks and specialist reviews pass under separate authorization; and
- the user explicitly accepts the evidence.

## Explicit non-authorization

This Accepted planning document does not authorize:

- creating `.mneme-local/handoffs/v1/` or its sentinel;
- choosing or invoking an implementation runtime;
- adding code, dependencies, fixtures, generated files, hooks, services, or configuration;
- creating, validating, listing, consuming, approving, rejecting, rolling back, or repairing a packet;
- running continuously or watching the filesystem;
- executing project work, a build, a test, a planner, Go, a verifier, a key operation, or another agent;
- reading retained inputs, real correspondence, the live archive, accounts, credentials, secrets, or production data;
- accessing the network, cloud AI, telemetry, databases, containers, or external services;
- modifying the existing P3-01, synthetic test-run, or planner-execution proposals;
- changing Git state, committing, pushing, or configuring a remote; or
- beginning P3 execution, R3-O1, Checkpoint B, stack selection, deployment, or real-data work.

## Review request

Review is requested on:

1. the one-shot four-operation boundary;
2. the ignored owner-only packet store and prohibited read/write paths;
3. packet numbering, layout, canonical identity, and immutable core;
4. exact repository-state and source-hash model;
5. stale, conflict, verdict, approval, consume, and rollback rules;
6. atomicity, failure handling, and diagnostic limits;
7. specialist reviews and staged gates; and
8. the rule that a consumed packet records a handoff only and never authorizes or executes project work.

Until a later complete implementation package is separately reviewed and explicitly authorized, no handoff automation may be implemented or run.
