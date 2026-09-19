# Mneme Local Handoff Packets

This directory contains the frozen first implementation of Mneme's local file-based handoff protocol.

The tool is not an agent and does not execute project work. Consuming a packet records a reviewed handoff only. It never turns the packet request, an agent verdict, or a receipt into authority to act.

## Current operating boundary

The implementation and its 38-case synthetic result were accepted on 2026-09-19. Acceptance does not authorize operational use. Until the security qualification below receives an explicit reviewed disposition and a later first-use gate is approved:

- do not initialize `.mneme-local/handoffs/v1/`;
- do not create, validate, list, consume, reject, or roll back a real packet;
- do not use the tool to authorize project work;
- do not push.

The tool has no network, watcher, daemon, scheduler, service, project runner, package manager, build, commit, push, or remote capability.

## Files

The complete tracked implementation object is exactly:

```text
tools/handoff/mneme-handoff.pl
tools/handoff/README.md
tools/handoff/t/handoff.t
tools/handoff/t/fixture-cases.json
```

No installed command, executable bit, dependency, lockfile, generated source, cache, result, or fifth file is part of the implementation.

## Runtime identity

The source is invoked explicitly through the existing local runtime:

```text
/usr/bin/perl
```

Frozen identity:

```text
bytes:  167184
sha256: 85e5621137742a37be052f58800372b2005f91f609ad55019832214b5d9e61bc
```

Supporting identities:

```text
/usr/bin/env
  bytes:  167712
  sha256: 2b2a1145527f00e8369fda0d2ffc523b520201bb08dbaf4b0bded837f7652ce0

/usr/bin/false
  bytes:  133184
  sha256: ccdd13063a974daa3ffcb707ac70104fb642eaf4aab3b621e816f36e2e8b59ab

/Library/Developer/CommandLineTools/usr/bin/git
  bytes:  3837392
  sha256: a73bf622a2e470d5d57a4b1d5aef1e8680e67278018d4858a2f93825b7d595c7
```

No CPAN or other dependency acquisition is allowed. A missing core module or primitive is a stop.

## Fixed environment

Every future production or test invocation must use this prefix:

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

`HOME`, proxy variables, credentials, SSH-agent variables, editor settings, and user Perl/Git configuration are absent.

The source is mode `0644`, not executable. Packet text is always inert data.

## Exact command grammar

The examples below document syntax. They are not currently authorized for operational use.

### Initialize the local store

```text
<fixed-environment> /usr/bin/perl -T \
  /Users/bogac/dev/forgejo/mneme/tools/handoff/mneme-handoff.pl \
  create \
  --repo-root /Users/bogac/dev/forgejo/mneme \
  --initialize-store
```

Initialization creates only the ignored owner-only protocol store, its sentinel, and `packets/`, `staging/`, and `locks/`. It creates no packet.

### Create a numbered packet

```text
<fixed-environment> /usr/bin/perl -T \
  /Users/bogac/dev/forgejo/mneme/tools/handoff/mneme-handoff.pl \
  create \
  --repo-root /Users/bogac/dev/forgejo/mneme \
  --request-file <allowed-repository-relative-path> \
  --approval-gate <closed-token> \
  --source <role>:<allowed-repository-relative-path> \
  [--source <role>:<allowed-repository-relative-path> ...] \
  [--prior-packet-id <sha256>] \
  [--supersedes-packet-id <sha256>]
```

The request file must also be a `proposal` source. Source paths are explicit and never globbed or recursively discovered.

### Validate a stored packet

```text
<fixed-environment> /usr/bin/perl -T \
  /Users/bogac/dev/forgejo/mneme/tools/handoff/mneme-handoff.pl \
  validate \
  --repo-root /Users/bogac/dev/forgejo/mneme \
  --packet <six-digits>
```

### Validate proposed verdict and approval records

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

This may report transient `Ready`; it writes nothing.

### List packets

```text
<fixed-environment> /usr/bin/perl -T \
  /Users/bogac/dev/forgejo/mneme/tools/handoff/mneme-handoff.pl \
  list \
  --repo-root /Users/bogac/dev/forgejo/mneme \
  [--verbose]
```

Listing never prints request bodies, source content, verdict rationale, or approval text.

### Consume a verdict

```text
<fixed-environment> /usr/bin/perl -T \
  /Users/bogac/dev/forgejo/mneme/tools/handoff/mneme-handoff.pl \
  consume \
  --repo-root /Users/bogac/dev/forgejo/mneme \
  --packet <six-digits> \
  --review-root <literal-owner-only-review-root> \
  --verdict-file <literal-safe-path> \
  --approval-file <literal-safe-path> \
  --approved-verdict-sha256 <sha256>
```

An agent-written verdict remains `Proposed`. A separate `Accepted` user-approval record must bind its exact SHA-256. The tool cannot authenticate a human; it can only validate the local records' consistency.

Consumption appends one transaction containing the exact verdict, approval, and receipt. The receipt always records:

```text
project_work_authorized = false
project_work_executed = false
```

### Append a rollback record

```text
<fixed-environment> /usr/bin/perl -T \
  /Users/bogac/dev/forgejo/mneme/tools/handoff/mneme-handoff.pl \
  consume \
  --repo-root /Users/bogac/dev/forgejo/mneme \
  --rollback \
  --packet <six-digits> \
  --receipt-sha256 <sha256> \
  --review-root <literal-owner-only-review-root> \
  --approval-file <literal-safe-path>
```

Rollback creates one new record. It never changes or deletes the immutable packet core, verdict, approval, receipt, or transaction.

## States

State precedence is:

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

`Ready` is a transient validation result and is never stored.

Malformed, stale, conflicting, ambiguous, linked, escaped, oversized, permission-mismatched, or hash-mismatched state fails closed. The tool never picks a winner or repairs a packet.

## Repository and source boundary

The literal repository root is:

```text
/Users/bogac/dev/forgejo/mneme
```

Allowed project source roots are only:

```text
README.md
AGENTS.md
.gitignore
docs/
experiments/phase-3/
tools/handoff/
```

Every file is named individually. A changed non-ignored path outside this set, or a changed path absent from the packet source manifest, stops creation or consumption before its content is read.

The ignored packet store contains protocol records only. It cannot hold project source, project outputs, evidence substitutes, binaries, test results, or generated artifacts. Tracked project changes remain in their tracked locations and visible to Git.

## Git boundary

Only the direct Command Line Tools Git binary is permitted. Its only subcommands are:

```text
rev-parse
symbolic-ref
status
ls-files
check-ignore
```

Arguments are literal arrays. There is no shell and no remote or write command. Hooks, user/system configuration, fsmonitor, untracked cache, submodule recursion, prompts, pagers, and optional locks are disabled or bypassed.

## Permissions and atomic writes

Tracked files are `0644`. Future protocol directories are `0700`; future protocol files are `0600`. The process uses umask `0077` and refuses links, unsafe types, permissive protocol modes, owner mismatch, path escape, and unexpected entries.

Packet publication and consumption use:

1. one exact atomic `mkdir` lock;
2. repeated state validation under the lock;
3. same-filesystem owner-only staging;
4. exclusive no-follow file creation;
5. bounded writes and file sync;
6. staging-directory sync and revalidation;
7. final-path absence checks;
8. one atomic rename; and
9. parent-directory sync before successful lock release.

There is no wait, retry, fallback, overwrite, or automatic orphan cleanup. An uncertain write preserves the lock and bytes for review.

## Failure classes

```text
0   success
10  usage
20  invalid
21  stale
22  conflict
23  approval
24  repository
25  unsafe path
26  lock
27  limit
28  runtime
29  uncertain write
30  internal
```

Diagnostics emit reason codes, not payload content.

## Synthetic tests

The frozen synthetic suite contains exactly `HT-001` through `HT-038`. It uses an owner-only disposable directory, fixed fictional records, and internal adapters. It does not invoke Git, the production CLI, project code, a shell, or the network.

The separately authorized test command is:

```text
<fixed-environment> /usr/bin/perl -T \
  /Users/bogac/dev/forgejo/mneme/tools/handoff/t/handoff.t
```

Test execution does not authorize packet-store initialization or operational use.

## Accepted synthetic verification record

**Status:** Accepted within the declared synthetic scope

**Review date:** 2026-09-19

**Operational-use state:** Blocked

The accepted test object had these SHA-256 identities before and after the run:

```text
tools/handoff/mneme-handoff.pl
  b276ae4f81e749a50f9f15383043e3e68d67ff6382bcee4c69583e5055afecdc
tools/handoff/README.md
  cec752c315eddc111eb90644f22860760bc1133015f4478d601240f2e3c60b20
tools/handoff/t/handoff.t
  db5d04ff775f9d66f654866837e904eefa226140b7bd142cb7ba5285beee0a15
tools/handoff/t/fixture-cases.json
  51593d986bc61a709911d52cb7867906f06f670f86abdf16eab13c9f1177412d
```

The README hash above is the accepted pre-record identity. This section is the later user-authorized evidence-only update; it does not change executable behavior, fixtures, or tests.

The accepted runtime and supporting identities were:

```text
/usr/bin/perl
  bytes:  167184
  sha256: 85e5621137742a37be052f58800372b2005f91f609ad55019832214b5d9e61bc
/usr/bin/env
  bytes:  167712
  sha256: 2b2a1145527f00e8369fda0d2ffc523b520201bb08dbaf4b0bded837f7652ce0
/usr/bin/false
  bytes:  133184
  sha256: ccdd13063a974daa3ffcb707ac70104fb642eaf4aab3b621e816f36e2e8b59ab
/Library/Developer/CommandLineTools/usr/bin/git
  bytes:  3837392
  sha256: a73bf622a2e470d5d57a4b1d5aef1e8680e67278018d4858a2f93825b7d595c7
```

The exact frozen invocation exited successfully with `1..38` and `ok 1` through `ok 38`. It exercised canonical identities; malformed and noncanonical records; unsafe paths; stale repository and source state; numbering, lineage, transaction, and rollback conflicts; agent/user authority separation; receipt non-authorization; redaction; inert instruction text; closed schemas; limits; append-only rollback; and implementation immutability.

Fault injection produced the required fail-closed evidence:

| Case | Injection or condition | Accepted result |
|---|---|---|
| `HT-028` | Failure before packet rename | No published packet; owner-only orphan stage preserved |
| `HT-029` | Failure after rename | Published bytes preserved as an uncertain write; no retry |
| `HT-030` | Failure during transaction staging | No active transaction; partial stage preserved |
| `HT-031` | Existing exact lock | Lock failure; no wait, deletion, or replacement |
| `HT-026`, `HT-027`, `HT-037`, `HT-038` | Valid, mismatched, drifted, and immutable rollback cases | Append-only history and controlling bytes preserved |

The final accepted disposable root was `/private/tmp/mneme-handoff-test-CFr7mcem`, mode `0700`. Its complete pre-removal inventory was:

```text
ht009/                         directory 0700
ht009/link                     symlink -> /private/tmp/mneme-handoff-test-CFr7mcem/ht009/target
ht009/target                   regular 0600 10 bytes
  sha256 18c4f85a180cf29ddc1f8e3a3143ff54d643d1c306dbe610f4f70482632071d4
ht028.stage/                   directory 0700
ht028.stage/packet.json        regular 0600 3 bytes
ht029.final/                   directory 0700
ht029.final/packet.json        regular 0600 3 bytes
ht030.stage/                   directory 0700
ht030.stage/approval.json      regular 0600 3 bytes
ht030.stage/receipt.json       regular 0600 3 bytes
ht030.stage/verdict.json       regular 0600 3 bytes
```

Every three-byte synthetic JSON file had SHA-256 `ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356`. The harness verified the complete temporary root was absent after rollback. No implementation file changed during the run. The suite invoked no production command, implementation-owned Git subprocess, shell, project command, service, watcher, or network path.

### Qualified security finding

The synthetic and static evidence passes for ownership, modes, link counts, realpaths, containment, device boundaries, taint mode, the empty environment, closed command arguments, and frozen binary identities. Operational use remains blocked because the accepted core-only implementation does not yet have a reviewed mechanism to enumerate macOS ACLs or conclusively exclude a same-device mount alias. This qualification must not be converted into a warning, silently waived, or addressed with an undeclared command or dependency. It requires a separate reviewed security-remediation decision.

## Recovery

The production tool has no cleanup command. A stale lock, orphan stage, uncertain publication, malformed entry, or rejected implementation remains in place for exact-path review.

Implementation rollback and packet-store removal require separate explicit authorization. Never use Git reset, checkout, clean, a wildcard, a broad recursive removal, or an unrelated-process kill.
