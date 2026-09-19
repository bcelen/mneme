# Handoff Automation Implementation Review Package

**Status:** Accepted
**Proposal date:** 2026-09-19
**Review date:** 2026-09-19
**Implementation state:** Not started
**Execution state:** Not authorized
**Current authority:** Accepted as the frozen implementation-review scope only. Do not add the proposed implementation files, initialize a packet store, invoke the proposed runtime, create fixtures, run tests, create or consume a packet, or push.
**Governing plan:** [Local Handoff Packet Automation Implementation Plan](HANDOFF-AUTOMATION-IMPLEMENTATION-PLAN.md), Accepted 2026-09-19
**Governing-plan commit:** `a5b22d9abec0825f6bfbdcb49dbd2d7ed82af0c7`
**Governing-plan SHA-256:** `8b63002df3b06bafb20f54d476fe9d6a4428f20ab131c46004e366400486bab1`

## Purpose

This package freezes the proposed first implementation boundary for review. It identifies the exact future files, local runtime, command grammar, permissions, write protocol, validation rules, failure behavior, rollback behavior, and synthetic tests needed to implement the accepted plan.

This is not implementation authorization. No file beneath `tools/handoff/` exists or may be created under this package. No command shown below may be run merely because it is documented here.

## Preserved governing boundaries

The implementation must preserve these accepted rules without reinterpretation:

1. consuming a packet records a handoff but never authorizes or executes the packet's requested work;
2. user approval is a separate record and authority from any agent-written verdict;
3. the five-file packet core is immutable after publication;
4. stale, conflicting, malformed, unsafe, or ambiguous state fails closed;
5. verdicts, approval records, receipts, and rollbacks form an append-only history;
6. the ignored owner-only packet directory contains protocol records only and cannot be used for project code, project outputs, evidence substitutes, or hidden tracked changes;
7. all operations are manually invoked, one-shot, local, and offline; and
8. implementation, testing, first use, project-work authorization, commit, and push remain separate gates.

Any implementation detail that conflicts with one of these rules is rejected even if a test passes.

## Exact proposed repository files

A later implementation authorization may add exactly four tracked files:

| Path | Mode | Purpose | Maximum size |
|---|---:|---|---:|
| `tools/handoff/mneme-handoff.pl` | `0644` | Single production entry point and all protocol logic | 160 KiB |
| `tools/handoff/README.md` | `0644` | Operator boundary, exact commands, states, reason codes, and recovery guidance | 64 KiB |
| `tools/handoff/t/handoff.t` | `0644` | Standard-library synthetic unit and fault-injection checks | 160 KiB |
| `tools/handoff/t/fixture-cases.json` | `0644` | Canonical fictional packet, repository-state, verdict, approval, conflict, and rollback cases | 256 KiB |

No fifth path is permitted. In particular, the implementation package must not add:

- `.gitignore` changes;
- a dependency, lock, package, module, vendor, or generated file;
- an executable-bit file or installed command;
- a Git hook, agent configuration, scheduler, daemon, launch item, service, socket, or listener;
- a packet store or `.mneme-local/` content;
- a build artifact, test result, coverage file, cache, bytecode file, log, database, or temporary file;
- a copy of project source or evidence inside an ignored directory; or
- a modification to the accepted plan, current P3 proposals, or other project documents.

The test source may generate bounded synthetic state only after separate test authorization. No generated fixture is committed.

## Frozen implementation shape

`mneme-handoff.pl` is one importable Perl source file with:

- a small command dispatcher;
- closed-schema parsers and canonical encoders;
- path, permission, and containment checks;
- read-only Git-state collection through one exact Git binary;
- SHA-256 and byte-count functions;
- packet-state validation;
- atomic packet and transaction writers;
- append-only rollback recording; and
- `main()` invoked only when the file is run directly.

It has no plug-in interface, dynamic code loading, shell evaluation, template evaluation, network module, general command runner, task executor, background mode, or extension discovery.

The test file loads the source as a module and calls internal pure functions and filesystem helpers with synthetic adapters. Production command execution is not triggered by loading the source.

## Exact local runtime

The proposed runtime is the existing Apple-provided Perl binary. The exact static identity observed without executing Perl is:

| Field | Required value |
|---|---|
| Runtime path | `/usr/bin/perl` |
| File type | Regular Mach-O universal binary |
| Owner/group | `root:wheel` |
| Mode | `0755` |
| Bytes | 167,184 |
| SHA-256 | `85e5621137742a37be052f58800372b2005f91f609ad55019832214b5d9e61bc` |
| Invocation mode | Taint mode, empty environment, no external module path |

The implementation may use only these Perl core modules:

```text
strict
warnings
bytes
utf8
JSON::PP
Digest::SHA
Encode
Fcntl
File::Basename
File::Spec
File::Temp
Cwd
POSIX
IO::Handle
IPC::Open3
Symbol
Getopt::Long
Time::Piece
Test::More           # test file only
```

No CPAN, package manager, local library directory, `PERL5LIB`, downloaded module, native extension added by this project, or runtime installation is permitted. If a listed module or required filesystem primitive is unavailable, the implementation stops and returns for review; it does not install or substitute anything.

The runtime's textual version and core-module inventory have not been executed under this planning authority. A later implementation authorization must either explicitly permit one identity-only preflight or accept the binary SHA-256 as the controlling runtime identity. No source invocation may occur until that choice is reviewed.

### Exact supporting binaries

| Path | Purpose | Bytes | SHA-256 |
|---|---|---:|---|
| `/usr/bin/env` | Construct an empty bounded process environment | 167,712 | `2b2a1145527f00e8369fda0d2ffc523b520201bb08dbaf4b0bded837f7652ce0` |
| `/Library/Developer/CommandLineTools/usr/bin/git` | Read-only repository identity and state | 3,837,392 | `a73bf622a2e470d5d57a4b1d5aef1e8680e67278018d4858a2f93825b7d595c7` |
| `/usr/bin/false` | Fail-closed Git askpass path | 133,184 | `ccdd13063a974daa3ffcb707ac70104fb642eaf4aab3b621e816f36e2e8b59ab` |

`/usr/bin/python3` and `/usr/bin/git` are not used because both are identically hashed Apple dispatch stubs on this host rather than the frozen implementation/runtime paths above.

## Exact process environment

Every future production or test invocation must begin with this fixed environment prefix:

```text
/usr/bin/env -i \
  PATH=/usr/bin:/bin \
  LC_ALL=C \
  TZ=UTC \
  GIT_CONFIG_NOSYSTEM=1 \
  GIT_CONFIG_GLOBAL=/dev/null \
  GIT_OPTIONAL_LOCKS=0 \
  GIT_TERMINAL_PROMPT=0 \
  GCM_INTERACTIVE=never \
  GIT_PAGER=cat \
  PAGER=cat \
  GIT_ASKPASS=/usr/bin/false \
  SSH_ASKPASS=/usr/bin/false \
  PERL5OPT= \
  PERL5LIB= \
  /usr/bin/perl -T
```

`HOME`, proxy variables, credential variables, SSH agent variables, editor variables, locale variations, user Perl configuration, user Git configuration, and every unlisted environment value are absent. The implementation sets process umask `0077` before any filesystem operation.

The source must use literal argument arrays for subprocesses. It must never invoke a shell, backticks, `system` with a scalar, `exec` with a scalar, `eval` on input, `qx`, or a PATH-resolved command.

## Exact Git command boundary

The production entry point may invoke only the frozen Command Line Tools Git binary and only these read-only forms, with the fixed environment above and the literal repository root `/Users/bogac/dev/forgejo/mneme`:

```text
/Library/Developer/CommandLineTools/usr/bin/git -C /Users/bogac/dev/forgejo/mneme -c core.fsmonitor=false -c core.untrackedCache=false -c submodule.recurse=false rev-parse --show-toplevel

/Library/Developer/CommandLineTools/usr/bin/git -C /Users/bogac/dev/forgejo/mneme -c core.fsmonitor=false -c core.untrackedCache=false -c submodule.recurse=false rev-parse --absolute-git-dir

/Library/Developer/CommandLineTools/usr/bin/git -C /Users/bogac/dev/forgejo/mneme -c core.fsmonitor=false -c core.untrackedCache=false -c submodule.recurse=false rev-parse --verify HEAD^{commit}

/Library/Developer/CommandLineTools/usr/bin/git -C /Users/bogac/dev/forgejo/mneme -c core.fsmonitor=false -c core.untrackedCache=false -c submodule.recurse=false symbolic-ref --quiet HEAD

/Library/Developer/CommandLineTools/usr/bin/git -C /Users/bogac/dev/forgejo/mneme -c core.fsmonitor=false -c core.untrackedCache=false -c submodule.recurse=false status --porcelain=v1 -z --untracked-files=all --ignore-submodules=all

/Library/Developer/CommandLineTools/usr/bin/git -C /Users/bogac/dev/forgejo/mneme -c core.fsmonitor=false -c core.untrackedCache=false -c submodule.recurse=false ls-files --stage -z -- <literal-path>...

/Library/Developer/CommandLineTools/usr/bin/git -C /Users/bogac/dev/forgejo/mneme -c core.fsmonitor=false -c core.untrackedCache=false -c submodule.recurse=false check-ignore --no-index -z --stdin
```

`<literal-path>` is documentary notation for individually validated repository-relative arguments, not a shell expansion. The source passes each path as a distinct argument after `--`.

No Git command may write an index, object, ref, configuration, lock, worktree file, commit, tag, merge, stash, or remote state. The source contains no Git subcommand other than `rev-parse`, `symbolic-ref`, `status`, `ls-files`, and `check-ignore`. It contains no URL or remote name.

Any Git stderr outside the exact documented unborn-HEAD and detached-HEAD cases is a stop. No command is retried or replaced with `/usr/bin/git`.

## Exact command grammar

The future tracked source is not executable. Every use invokes it through the exact runtime path.

### Store initialization under `create`

The accepted four-operation interface has no fifth `init` operation. The one-time store creation is therefore an explicit mode of `create`:

```text
<fixed-environment> /usr/bin/perl -T \
  /Users/bogac/dev/forgejo/mneme/tools/handoff/mneme-handoff.pl \
  create \
  --repo-root /Users/bogac/dev/forgejo/mneme \
  --initialize-store
```

This mode creates only `.mneme-local/handoffs/v1/`, its sentinel, and the exact `packets/`, `staging/`, and `locks/` protocol directories. It creates no packet. The new `locks/` directory is a proposed implementation clarification to hold atomic `mkdir` locks; it is protocol state, not project state. Acceptance of this package must explicitly accept that refinement.

Initialization fails if the store, sentinel, or a target child already exists in an unexpected or partial form. It does not inspect or alter sibling content elsewhere under `.mneme-local/`.

### Create one packet

```text
<fixed-environment> /usr/bin/perl -T \
  /Users/bogac/dev/forgejo/mneme/tools/handoff/mneme-handoff.pl \
  create \
  --repo-root /Users/bogac/dev/forgejo/mneme \
  --request-file <allowed-repository-relative-path> \
  --approval-gate <closed-token> \
  --source <role>:<allowed-repository-relative-path> \
  [--source <role>:<allowed-repository-relative-path> ...] \
  [--prior-packet-id <64-lowercase-hex>] \
  [--supersedes-packet-id <64-lowercase-hex>]
```

The request file must also appear exactly once as a `proposal` source. Sources are explicit repeated arguments; the source performs no recursive discovery or glob expansion.

`approval-gate` is one of these initial closed tokens:

```text
planning-review
implementation-review
execution-authorization
evidence-acceptance
commit-authorization
```

Adding another token requires review.

### Validate

Stored packet only:

```text
<fixed-environment> /usr/bin/perl -T \
  /Users/bogac/dev/forgejo/mneme/tools/handoff/mneme-handoff.pl \
  validate \
  --repo-root /Users/bogac/dev/forgejo/mneme \
  --packet <six-digits>
```

Read-only readiness preflight with external records:

```text
<fixed-environment> /usr/bin/perl -T \
  /Users/bogac/dev/forgejo/mneme/tools/handoff/mneme-handoff.pl \
  validate \
  --repo-root /Users/bogac/dev/forgejo/mneme \
  --packet <six-digits> \
  --review-root <literal-owner-only-review-root> \
  --verdict-file <literal-safe-path> \
  --approval-file <literal-safe-path>
```

The external paths must be regular, owner-controlled, non-linked files physically beneath the exact `--review-root`. That root must be a separately authorized literal directory, mode `0700`, outside the repository and packet store, and not a mount point. The tool never creates, searches for, or cleans it. The files may not be project source, real data, credentials, or retained experiment inputs.

### List

```text
<fixed-environment> /usr/bin/perl -T \
  /Users/bogac/dev/forgejo/mneme/tools/handoff/mneme-handoff.pl \
  list \
  --repo-root /Users/bogac/dev/forgejo/mneme \
  [--verbose]
```

List output never includes request, source, verdict-rationale, approval-statement, or project-file content.

### Consume

```text
<fixed-environment> /usr/bin/perl -T \
  /Users/bogac/dev/forgejo/mneme/tools/handoff/mneme-handoff.pl \
  consume \
  --repo-root /Users/bogac/dev/forgejo/mneme \
  --packet <six-digits> \
  --review-root <literal-owner-only-review-root> \
  --verdict-file <literal-safe-path> \
  --approval-file <literal-safe-path> \
  --approved-verdict-sha256 <64-lowercase-hex>
```

This command writes protocol transaction records only. It does not run or authorize the packet request.

### Append-only rollback

```text
<fixed-environment> /usr/bin/perl -T \
  /Users/bogac/dev/forgejo/mneme/tools/handoff/mneme-handoff.pl \
  consume \
  --repo-root /Users/bogac/dev/forgejo/mneme \
  --rollback \
  --packet <six-digits> \
  --receipt-sha256 <64-lowercase-hex> \
  --review-root <literal-owner-only-review-root> \
  --approval-file <literal-safe-path>
```

Rollback appends one rollback record. It never removes or rewrites the packet core or transaction.

Unknown options, missing required options, option repetition where not declared, positional arguments, malformed values, or incompatible modes exit before a write.

## Packet-store permissions and path rules

The future packet-store root remains:

```text
/Users/bogac/dev/forgejo/mneme/.mneme-local/handoffs/v1
```

Required modes:

| Object | Mode |
|---|---:|
| Packet-store root and protocol directories | `0700` |
| Lock directories | `0700` |
| Packet, transaction, and rollback directories | `0700` |
| Sentinel, packet files, transaction files, rollback files | `0600` |
| Tracked implementation and documentation files | `0644` |
| Separately authorized external review root | `0700` |
| External verdict and approval files | `0600` |

The invoking effective and real user IDs must match the repository and store owner. The source refuses setuid/setgid execution, elevated identity, group/world-writable protocol state, ACL uncertainty, a symlink, a hard-link count other than one for files, a mount-point protocol directory, a non-regular file, or a path outside the physical roots.

The implementation writes only beneath the exact packet store. It never changes modes or ownership outside that root.

### Preventing hidden project changes

The ignored packet store may contain only the exact sentinel, protocol directories, locks, immutable packet cores, transaction records, and rollback records. The validator rejects any other entry.

The implementation must not copy project source, diffs, binaries, test output, evidence packages, generated artifacts, or replacement documents into `.mneme-local/`. `request.md` is the only reviewed prose copy; `sources.tsv` contains identities, not source bytes.

Before packet creation and consumption, every non-ignored changed repository path must be represented in the repository-state record and must lie in the accepted project-file allowlist. A changed path outside that allowlist causes a stop before content is read. The packet store's ignored status is verified, but the source never treats another ignored path as project state or as an authorized substitute for a tracked change.

The tracked implementation is always reviewed from `tools/handoff/`; a packet-store copy can never be executed or treated as authoritative.

## Fixed resource limits

The first implementation has these hard ceilings:

| Resource | Maximum |
|---|---:|
| Packet number | `999999` |
| Declared source files | 64 |
| Request file | 262,144 bytes |
| One declared source file | 8,388,608 bytes |
| Aggregate declared source bytes | 33,554,432 bytes |
| One JSON protocol record | 262,144 bytes |
| One TSV protocol record | 262,144 bytes |
| Verdict file | 65,536 bytes |
| Approval file | 32,768 bytes |
| Receipt file | 65,536 bytes |
| Rollback file | 32,768 bytes |
| JSON nesting depth | 16 |
| Array elements in one record | 64 |
| UTF-8 path bytes | 1,024 |
| One path-segment bytes | 255 |
| Git status entries | 4,096 |
| One Git subprocess output stream | 8,388,608 bytes |
| Terminal transaction directories per packet | 1 |
| Active rollback records per transaction | 1 |

Before reading a bounded file, the source checks type, containment, ownership, mode, link count, and stat size. A changed path must also be one of the at most 64 declared sources before its content is hashed. Exceeding a limit returns exit `27`; the implementation never truncates, samples, paginates, or widens a ceiling automatically.

The accepted source roots remain exactly:

```text
README.md
AGENTS.md
.gitignore
docs/
experiments/phase-3/
tools/handoff/
```

The first three are exact top-level files. The last three are physical repository-contained prefixes, but every file beneath them must still be named individually. No recursive glob or directory payload is accepted.

## Closed record schemas

The implementation manually enforces exact key sets, key types, lengths, enums, and value syntax. JSON is accepted only when decoding and canonical re-encoding produce identical bytes. This rejects duplicate keys, alternative whitespace, ambiguous Unicode encoding, noncanonical key order, and trailing data.

### Verdict record

A verdict has exactly these keys:

```text
schema_version
record_type
status
packet_number
packet_id
packet_manifest_sha256
repository_state_sha256
sources_sha256
verdict
rationale
unresolved_concerns
reviewer_role
proposal_date
```

Required fixed values include:

```text
schema_version = 1
record_type = mneme.handoff.verdict
status = Proposed
verdict = Approve | Reject | ChangesRequested
```

An agent may write a Proposed verdict, but a verdict has no approval authority.

### User-approval record

An approval record has exactly these keys:

```text
schema_version
record_type
status
authority
packet_number
packet_id
verdict_sha256
repository_state_sha256
approval_date
decision_reference
approval_statement_sha256
```

Required fixed values include:

```text
schema_version = 1
record_type = mneme.handoff.user-approval
status = Accepted
authority = user
```

The approval record is a transcription of an external user decision. It must bind the exact Proposed verdict hash. It cannot be derived from verdict text, created by the production command, or replaced by an agent's assertion. The source can validate consistency, not human authenticity.

### Receipt record

The source creates a receipt only after all checks pass. It contains exact packet, manifest, repository-state, sources, verdict, approval, implementation, runtime, Git, transaction, timestamp, and final-state identities plus:

```text
project_work_authorized = false
project_work_executed = false
```

Both fields must be literal JSON booleans. A receipt with either `true` is invalid.

### Rollback record

The rollback record binds the exact packet, transaction, receipt, new user-approval record, original repository-state hash, current repository-state hash, reason, and date. It does not invalidate history by deletion; it changes the derived active state to `RolledBack`.

## Canonical hashing rules

- SHA-256 is the only digest algorithm.
- Hex digests are exactly 64 lowercase ASCII characters.
- Canonical JSON is UTF-8, LF-terminated, sorted-key, compact JSON with no floating-point values.
- Canonical TSV is UTF-8, LF-terminated, fixed-header, tab-delimited data with no CR, NUL, or unescaped tab/newline in a field.
- Paths are normalized repository-relative UTF-8 byte sequences and are sorted by byte value.
- The source hashes bytes, not decoded text, for project source files.
- The packet ID uses the accepted NUL-delimited formula without modification.
- The receipt directory name is the SHA-256 of canonical `receipt.json`; the receipt does not contain its own hash.
- Every manifest records path, bytes, and SHA-256.

No hash mismatch is repairable in place.

## Atomic-write protocol

All protocol writes use same-filesystem staging and fail closed.

### Locks

- Store initialization and packet-number allocation use `locks/create.lock`, acquired by atomic `mkdir`.
- Consumption and rollback use `locks/packet-<six-digits>.lock`, acquired by atomic `mkdir`.
- Lock acquisition never waits or retries.
- Each lock contains one owner-only canonical record with operation, process ID, packet if applicable, start time, repository identity, and implementation hash.
- A pre-existing lock is a conflict. It is never removed automatically, even if its process appears absent.
- Normal successful completion removes only the exact lock created by that invocation after the publication directory has been synced.
- An interruption or uncertain state preserves the lock for review.

### Packet creation

1. Validate repository, store, sentinel, all existing packets, and creation lock absence.
2. Acquire `create.lock`.
3. Repeat existing-number and repository-state checks.
4. Select `maximum + 1` and freeze the six-digit number.
5. Create exact `staging/create-<six-digits>.tmp` with `0700` and exclusive semantics.
6. Write each core file with `O_CREAT|O_EXCL|O_NOFOLLOW`, mode `0600`, bounded bytes, flush, and file sync.
7. Sync the staging directory.
8. Reopen and fully validate the staged packet.
9. Require the final packet path to be absent.
10. Atomically rename the staging directory to `packets/<six-digits>`.
11. Sync `packets/`, then remove and sync the exact lock path.

Failure before the rename publishes no packet. Failure or uncertainty after rename preserves the published bytes and lock and returns an uncertain-publication error; it never retries.

### Consumption

1. Complete read-only readiness validation.
2. Acquire the packet lock and repeat all mutable checks.
3. Recompute the current repository state and require exact packet-state equality.
4. Create `transactions/.staging-<receipt-sha256>` with exclusive `0700` semantics.
5. Copy the externally reviewed verdict and approval bytes without normalization.
6. Create canonical receipt bytes and verify the directory-name hash.
7. Sync all three files and the staging directory.
8. Reopen and validate the complete transaction.
9. Require the final transaction path to be absent.
10. Atomically rename it to `transactions/<receipt-sha256>`.
11. Sync `transactions/`, then remove and sync the exact lock path.

The three transaction records become visible together. More than one final transaction is a conflict.

### Rollback

Rollback stages one canonical file beside `rollbacks/`, syncs and validates it, then atomically renames it to `rollbacks/<rollback-sha256>.json`. It never opens the packet core or transaction for writing. Current repository drift is recorded but does not prevent revoking an erroneous protocol receipt.

### Filesystem primitive gate

The later static review must confirm that the exact runtime exposes `O_NOFOLLOW`, exclusive creation, file sync, directory sync, and atomic same-filesystem rename with the required behavior on this filesystem. If any primitive is unavailable or cannot be checked without broadening scope, implementation is blocked. No weaker silent fallback is allowed.

## Validation rules

The source follows the accepted validation order and assigns one stable reason code to every stop.

### Structural validation

- exact store sentinel, schema, physical repository root, owner, mode, and protocol version;
- exact directory and filename grammar;
- only six-digit packet numbers `000001` through `999999`;
- no unexplained gap, duplicate, alias, link, device, socket, FIFO, mount, or extra entry;
- exactly five immutable core files;
- closed canonical record schemas;
- exact byte limits, file modes, counts, manifests, and hashes; and
- no modification time used as an identity or authority signal.

### Repository validation

- exact `HEAD` commit or explicit unborn state;
- exact symbolic branch or detached state;
- exact NUL-safe status rows;
- exact staged index entries for represented paths;
- exact type, mode, byte count, and SHA-256 for changed and declared paths;
- no changed path outside the accepted allowlist;
- no ignored source path, except the exact packet store as protocol state;
- no source read before path policy and containment pass; and
- exact repository-state canonical hash.

### Identity and lineage validation

- packet number, directory, packet ID, manifest, request, sources, and repository state agree;
- predecessor and supersession identities exist and form one acyclic chain;
- a live overlapping approval gate requires an explicit predecessor relationship;
- a superseded packet is stale, never deleted;
- protocol-version incompatibility is stale or invalid according to the accepted schema rule; and
- age alone is never stale.

### Verdict and approval validation

- verdict is Proposed and uses the closed verdict enum;
- approval is Accepted, authority is `user`, and exact hashes agree;
- verdict and approval are separate files with separate identities;
- an agent role cannot satisfy the approval authority field;
- approval statement identity and durable decision reference are present;
- no approval is inferred from request, verdict, filename, packet state, or prior conversation; and
- `Approve` authorizes protocol consumption only.

### Transaction and rollback validation

- exactly zero or one terminal transaction;
- verdict, approval, and receipt agree on every controlling identity;
- receipt records no project authorization and no project execution;
- exactly zero or one valid rollback for the active receipt;
- rollback approval is distinct and exact;
- multiple, mismatched, orphaned, or partial records are conflicts; and
- history is never rewritten to derive current state.

## Closed states and precedence

Validation derives one state with this precedence:

```text
Invalid
Conflict
Stale
RolledBack
Rejected
ChangesRequested
Consumed
Pending
```

`Ready` is a transient successful result of `validate` supplied with external verdict and approval files. It is never persisted. Unsafe structure takes precedence over staleness; ambiguity takes precedence over a terminal verdict.

No code path silently downgrades `Invalid`, `Conflict`, or `Stale` to a warning.

## Stable failure classes

The proposed process exit codes are:

| Code | Class | Meaning |
|---:|---|---|
| `0` | Success | Requested protocol operation completed |
| `10` | Usage | Invalid command grammar; no write |
| `20` | Invalid | Malformed structure, schema, hash, permission, or path |
| `21` | Stale | Valid packet no longer matches required state |
| `22` | Conflict | Ambiguous numbering, lineage, transaction, rollback, lock, or publication |
| `23` | Approval | Verdict/approval separation or exact identity failed |
| `24` | Repository | Repository identity or represented state failed |
| `25` | Unsafe path | Containment, link, ignored-path, allowlist, or real-data boundary failed |
| `26` | Lock | Lock exists or cannot be acquired exactly |
| `27` | Limit | Count, bytes, depth, or field limit exceeded |
| `28` | Runtime | Required runtime/module/filesystem primitive unavailable |
| `29` | Uncertain write | Publication may have occurred; preserve state and inspect read-only |
| `30` | Internal | Unclassified internal failure; no retry |

Diagnostics contain one reason code, packet number if safely known, and protocol-relative path if safely known. They never emit payload content, source bytes, rationale, approval text, environment, credentials, or a full absolute private path beyond the already accepted repository/store roots.

## Failure and interruption handling

- No operation retries, repairs, renumbers, resumes, or falls back.
- No signal handler deletes staging, a lock, packet, transaction, or rollback record.
- A pre-publication staging directory is an orphan and a conflict until separately reviewed.
- A post-rename uncertainty is checked only with `validate`; the write is never repeated automatically.
- A missing sync, failed close, failed rename, failed directory sync, or unexpected stderr is a failure even if bytes appear present.
- A partial transaction is never interpreted as a verdict.
- A malformed packet is not skipped during allocation or listing.
- Unknown protocol files fail validation rather than being ignored.
- Source or repository drift requires a new packet; an existing core is never refreshed.
- An error after a lock is acquired preserves the lock unless successful publication is fully proven.
- Recovery never uses recursive deletion, a wildcard, Git reset/checkout, or a broad process kill.

## Rollback and recovery

The production mechanism has no destructive cleanup command.

Protocol rollback requires a new exact user-approval record and appends one rollback file. It can revoke the active consumed handoff after repository drift because it changes protocol state only. It cannot remove project work, because consumption never performs project work.

Stale locks, orphan staging paths, malformed entries, and uncertain publications require a separately reviewed recovery instruction naming exact paths and hashes. The first implementation does not automate their removal.

If the entire packet store must later be removed, that is outside this implementation. It requires separate exact-target approval and sentinel, owner, mode, realpath, mount, process, open-file, inventory, and Git-status checks.

## Synthetic test design

No test is authorized by this package. After implementation and static review, `H3` may separately authorize one local standard-library test invocation:

```text
<fixed-environment> /usr/bin/perl -T \
  /Users/bogac/dev/forgejo/mneme/tools/handoff/t/handoff.t
```

The test creates one owner-only temporary root using `File::Temp`, never touches the project packet store, never invokes Git, never opens a network path, and never commits. Repository and Git responses are fixed synthetic values from `fixture-cases.json` supplied through an internal test adapter. The production CLI exposes no adapter-selection option.

The test source must perform at least these cases:

| ID | Synthetic case | Required result |
|---|---|---|
| `HT-001` | Canonical valid packet core | Exact packet ID and `Pending` |
| `HT-002` | Repeated canonical encode | Byte-identical output |
| `HT-003` | Duplicate JSON key | `Invalid` |
| `HT-004` | Noncanonical JSON whitespace/order | `Invalid` |
| `HT-005` | CRLF or trailing JSON bytes | `Invalid` |
| `HT-006` | Malformed packet number | `Invalid` |
| `HT-007` | Duplicate number/different identity | `Conflict` |
| `HT-008` | Unexplained numbering gap | `Conflict` |
| `HT-009` | Symlinked core/source/store path | `Unsafe path` |
| `HT-010` | Prohibited or ignored source path | `Unsafe path` before content read |
| `HT-011` | Extra packet-core file | `Invalid` |
| `HT-012` | Source hash or byte mismatch | `Stale` |
| `HT-013` | `HEAD`, branch, index, or status drift | `Stale` |
| `HT-014` | Dirty unrepresented project path | `Repository` stop |
| `HT-015` | Superseded packet | `Stale` |
| `HT-016` | Predecessor cycle or fork | `Conflict` |
| `HT-017` | Agent-written Approve verdict only | Remains `Pending`; cannot consume |
| `HT-018` | Approval marked agent authority | `Approval` failure |
| `HT-019` | User approval targets different verdict hash | `Approval` failure |
| `HT-020` | Valid external verdict plus user approval | Transient `Ready` only |
| `HT-021` | Valid consume transaction | Exactly one atomic `Consumed` state |
| `HT-022` | Reject verdict transaction | `Rejected`; no replacement packet |
| `HT-023` | ChangesRequested transaction | `ChangesRequested`; no replacement packet |
| `HT-024` | Two transactions | `Conflict`; no winner selected |
| `HT-025` | Receipt claims project authority/work | `Invalid` |
| `HT-026` | Valid append-only rollback | `RolledBack`; core and transaction unchanged |
| `HT-027` | Rollback targets wrong receipt | `Conflict` |
| `HT-028` | Fault before packet rename | No published packet; orphan preserved |
| `HT-029` | Fault after rename or sync uncertainty | Exit `29`; no retry |
| `HT-030` | Fault during transaction staging | No active partial verdict |
| `HT-031` | Existing lock | Exit `26`; no wait or deletion |
| `HT-032` | File/count/depth limit | Exit `27`; no truncation |
| `HT-033` | List normal output | No payload, rationale, approval, or source content |
| `HT-034` | Packet text contains run/approve/commit instructions | Treated as inert bytes |
| `HT-035` | Unknown option, schema key, state, verdict, or gate | Fail closed |
| `HT-036` | Packet-store project file or generated artifact | `Invalid`; hidden-project-change boundary preserved |
| `HT-037` | Current repository drift during rollback | Rollback records both hashes without deleting history |
| `HT-038` | Source and transaction pre/post hashes | Immutable bytes unchanged |

Fault injection is available only through internal function arguments used by `handoff.t`. It is not controlled by an environment variable, command-line flag, packet field, or production file.

### Test evidence required

A later test evidence package must include:

- exact source/test/fixture/runtime hashes;
- exact environment and command bytes;
- owner-only temporary root identity and inventory;
- 38 case results and reason codes;
- pre/post hashes proving the repository and implementation files unchanged;
- zero Git subprocesses during synthetic tests;
- zero network requests, connections, listeners, external processes, project commands, commits, or pushes;
- complete temporary-root rollback scope; and
- specialist findings.

Tests prove protocol behavior only. They do not authorize operational use or project work.

## Static implementation review checklist

Before any test or packet-store creation, four specialists review the same frozen four-file implementation object.

### Orchestrator / governance

- Every command exits after one operation.
- No consumed packet authorizes work.
- Verdict and user approval remain separate.
- Approval gates and non-authorizations are visible in CLI output and README.
- No operation commits, pushes, invokes an agent, or continues to another phase.

### Security / privacy

- Imports and subprocesses match the closed allowlists.
- Input text cannot become code, shell, path traversal, or command arguments without validation.
- Permissions, taint mode, empty environment, no-network design, and output redaction are complete.
- Prohibited roots and real-data boundaries fail before file-content reads.
- Packet-store contents cannot hide project source or generated evidence.

### Quality / independent verification

- Schemas, canonicalization, hash formulas, state precedence, and reason codes match this package.
- Repository-state capture is exact for staged, unstaged, untracked, deleted, unborn, and detached cases.
- All stale, conflict, approval, atomicity, and rollback cases map to tests.
- No test-only bypass is reachable from production CLI.

### Operations / recovery

- Locks, exclusive creation, sync order, atomic rename, interruption behavior, and uncertain-publication handling are correct.
- No automatic cleanup or broad deletion exists.
- Rollback is append-only and preserves every controlling byte.
- Store initialization and the `locks/` clarification remain bounded protocol operations.

Any non-`Pass` finding, runtime uncertainty, missing filesystem primitive, test gap, or reviewer disagreement blocks execution.

## Approval gates

| Gate | Decision required | Current state |
|---|---|---|
| `H1-A` Package review | Accept or revise this exact implementation boundary | Accepted 2026-09-19 |
| `H1-B` Implementation authorization | Authorize adding only the four exact tracked files | Blocked |
| `H2` Static review | Freeze hashes and run four source-review passes | Blocked |
| `H3` Synthetic test authorization | Authorize the one exact local test command | Blocked |
| `H4-A` Store initialization | Authorize only `create --initialize-store` | Blocked |
| `H4-B` First synthetic packet trial | Authorize exact create/validate/list/consume records | Blocked |
| `H5` Operational acceptance | Decide whether the mechanism may be used for later handoffs | Blocked |

Acceptance of `H1-A` is a planning decision only. It does not authorize `H1-B`. No gate implies the next.

Before `H1-B`, the implementation request must repeat:

- the four exact paths and size ceilings;
- runtime and supporting-binary identities;
- core-module availability decision;
- complete proposed diff;
- rollback for the four tracked paths; and
- confirmation that no packet store, command execution, test, commit, or push is included.

## Explicit non-authorization

This Accepted review package does not authorize:

- adding `tools/handoff/` or any implementation/test/fixture file;
- changing `.gitignore`, the accepted plan, P3 proposals, or other project files;
- choosing a different runtime, adding a dependency, or installing a module;
- invoking Perl, the proposed source, the test, or a runtime/module preflight;
- invoking any proposed Git subprocess through the implementation;
- initializing `.mneme-local/handoffs/v1/` or creating protocol state;
- creating, validating, listing, consuming, approving, rejecting, or rolling back a packet;
- creating a fixture, temporary test root, lock, staging path, transaction, receipt, or generated artifact;
- running continuously, watching the filesystem, executing project work, or invoking another agent;
- building, testing, committing, pushing, accessing the network, or configuring a remote;
- reading real correspondence, retained experiment inputs, accounts, credentials, keys, the live archive, or production data; or
- beginning P3 execution, planner execution, R3-O1, Checkpoint B, stack selection, deployment, or real-data work.

## Review request

Review is requested on:

1. the exact four-file implementation object;
2. the frozen Perl, Git, and environment identities;
3. the four-operation command grammar and `create --initialize-store` clarification;
4. owner-only permissions and prevention of hidden project changes;
5. record schemas, identity rules, Git-state capture, and closed states;
6. atomic locks, staging, sync, rename, interruption, and uncertain-write behavior;
7. verdict/user-approval separation and no-project-authority receipts;
8. append-only rollback and manual recovery boundary;
9. the 38 synthetic test cases and evidence requirements; and
10. the staged implementation, review, test, initialization, trial, and operational gates.

Until a later implementation request is separately accepted and explicitly authorized, no implementation file or packet-store path may be created and no handoff command may run.
