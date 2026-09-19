# Handoff Automation Security Capability-Screening Request

**Status:** Accepted

**Proposal date:** 2026-09-19

**Review date:** 2026-09-19

**Authorization effect:** None

**Route-selection state:** No route selected or approved

**Capability-screening state:** Not authorized

**Current allowed command/API invocation set:** Empty

**Operational-use state:** Blocked

**Governing manifest:** [Handoff Automation Security Evidence-Source Manifest](HANDOFF-AUTOMATION-SECURITY-EVIDENCE-SOURCE-MANIFEST.md), Accepted 2026-09-19

**Governing-manifest commit:** `0e7ba7dbd54ef50d5562a9e38188ab2739a2825c`

**Governing-manifest SHA-256:** `b9ea52d9c81053ab4fd22d5694ba7bd9127f02165dc088ddb5f2e5a4a76e046f`

**Comparison record:** [ADR-007: Handoff Security Remediation Route Comparison](decisions/007-handoff-security-remediation-route-comparison.md), `Proposed`; no route selected

## Request boundary

Define—but do not authorize—the smallest read-only screening needed to replace selected `UNOBSERVED` identity and capability fields with reviewable local evidence. Screening answers only whether a nominated local path appears capable of supporting a later route evaluation. It does not prove a mandatory gate, approve an executable or API, execute a remediation route, change handoff source, create a helper, build anything, initialize the packet store, or authorize operational use.

This request preserves:

- every candidate route as unapproved;
- all `UNOBSERVED` values until an authorized command produces reviewed evidence;
- the missing Route-A Perl binding;
- Route B's lack of one conforming verifier;
- the absence of both Route-C future paths;
- Route D's disabled operational state;
- the empty current command/API allowlist; and
- separate later gates for evidence collection, route testing, scoring, selection, implementation, packet-store creation, and operational use.

Accepting this document as a plan would not execute it. A later user instruction must name exactly one screening unit and its frozen request hash before any command may run.

## Screening units

| Unit | Scope | May be authorized with |
|---|---|---|
| `CS-0` | Authenticate the proposed collection tools using the previously accepted Perl runtime identity | No other unit |
| `CS-COM` | Revalidate common frozen identities and record host identity | `CS-0` evidence accepted first |
| `CS-A` | Static inspection of Route-A provider, headers, and named symbols | `CS-0` and `CS-COM` accepted first |
| `CS-B1` | Screen `/bin/ls` alone | `CS-0` and `CS-COM` accepted first; no other Route-B unit in the same authorization |
| `CS-B2` | Screen `/usr/bin/stat` alone | Same boundary; no other Route-B unit |
| `CS-B3` | Screen `/sbin/mount` alone | Same boundary; static inspection only under this request |
| `CS-B4` | Screen `/bin/df` alone | Same boundary; no other Route-B unit |
| `CS-C` | Static toolchain and SDK capability inspection; no source or binary creation | `CS-0`, `CS-COM`, and `CS-A` evidence accepted first |
| `CS-D1` | Static and help/version screening of `/usr/bin/openssl`; no keys or attestations | `CS-0` and `CS-COM` accepted first |
| `CS-D2` | Confirm continued disablement requires no executable or API | Documentation review only; no command |

Route-B units are mutually exclusive execution objects. Their outputs may be compared only as rejected-or-incomplete alternatives; they may never be combined into a multi-executable verifier or treated as jointly satisfying Route B.

## Exact evidence roots

No root is created by this request. A later unit-specific authorization must first prove its exact root is absent, then create only that root with owner-only mode `0700` and files with mode `0600`.

| Unit | Exact future root |
|---|---|
| `CS-0` | `/private/tmp/mneme-handoff-capability-cs0-20260919-01` |
| `CS-COM` | `/private/tmp/mneme-handoff-capability-common-20260919-01` |
| `CS-A` | `/private/tmp/mneme-handoff-capability-route-a-20260919-01` |
| `CS-B1` | `/private/tmp/mneme-handoff-capability-route-b1-ls-20260919-01` |
| `CS-B2` | `/private/tmp/mneme-handoff-capability-route-b2-stat-20260919-01` |
| `CS-B3` | `/private/tmp/mneme-handoff-capability-route-b3-mount-20260919-01` |
| `CS-B4` | `/private/tmp/mneme-handoff-capability-route-b4-df-20260919-01` |
| `CS-C` | `/private/tmp/mneme-handoff-capability-route-c-20260919-01` |
| `CS-D1` | `/private/tmp/mneme-handoff-capability-route-d1-20260919-01` |

The roots are evidence containers, not installations, caches, services, credentials, packet stores, or project state. No route unit may read another route unit's root during execution.

## Runtime identities and fixed environment

### Previously accepted bootstrap runtime

| ID | Exact path | Type and permissions | Bytes | SHA-256 | Permitted future role |
|---|---|---|---:|---|---|
| `SR-COM-01` | `/usr/bin/perl` | Regular Mach-O universal binary; `root:wheel`; `0755` | 167,184 | `85e5621137742a37be052f58800372b2005f91f609ad55019832214b5d9e61bc` | One exact identity-only bootstrap invocation per literal target in `CS-0` |
| `SR-COM-02` | `/usr/bin/env` | Regular system executable; required `root:wheel`; `0755` | 167,712 | `2b2a1145527f00e8369fda0d2ffc523b520201bb08dbaf4b0bded837f7652ce0` | Construct the fixed empty environment |

These prior hashes are controlling inputs for the proposal, not permission to invoke either path. Any pre-execution mismatch stops `CS-0`; no substitute runtime is allowed.

Every proposed process has this exact environment prefix as a direct argument array, without a shell:

```text
["/usr/bin/env", "-i", "PATH=/usr/bin:/bin", "LC_ALL=C", "LANG=C", "TZ=UTC", <absolute-executable>, <literal-arguments>]
```

No `HOME`, proxy, credential, developer-directory, module-path, locale archive, pager, editor, shell, or user configuration value may be inherited. If an executable requires one, the unit stops.

## `CS-0` — collection-tool identity bootstrap

### Exact targets

```text
/usr/bin/stat
/usr/bin/shasum
/usr/bin/codesign
/usr/bin/file
/usr/bin/otool
/usr/bin/nm
/usr/bin/sw_vers
/usr/bin/uname
```

Each target must be inspected in its own process. The only proposed bootstrap command is the following direct argv template, with `<TARGET>` replaced by exactly one path above:

```text
[
  "/usr/bin/env", "-i",
  "PATH=/usr/bin:/bin", "LC_ALL=C", "LANG=C", "TZ=UTC",
  "/usr/bin/perl", "-T", "-MDigest::SHA", "-MFcntl=:mode", "-e",
  "use strict;use warnings;use bytes;@ARGV==1 or die qq(ARG_COUNT\\n);my($p)=$ARGV[0]=~m{\\A(/[A-Za-z0-9_+./-]+)\\z} or die qq(PATH\\n);my @s=lstat($p);@s or die qq(LSTAT:$!\\n);S_ISREG($s[2]) or die qq(NOT_REGULAR\\n);open my $f,'<:raw',$p or die qq(OPEN:$!\\n);my $d=Digest::SHA->new(256);$d->addfile($f);close $f or die qq(CLOSE:$!\\n);printf qq(%s\\t%u\\t%u\\t%04o\\t%u\\t%u\\t%u\\t%s\\n),$p,$s[4],$s[5],$s[2]&07777,$s[7],$s[1],$s[3],$d->hexdigest;",
  "--", "<TARGET>"
]
```

Required stdout fields are path, numeric UID, numeric GID, mode, bytes, inode, link count, and SHA-256. Stderr must be empty and exit status must be zero. Output exceeding 1 KiB, an unexpected field count, a non-regular target, any symlink substitution, or any different target stops the unit.

`CS-0` does not invoke a proposed collection tool. It only reads its finite bytes through the accepted Perl runtime. Its evidence must be independently reviewed before any later unit may invoke `SR-COL-01` through `SR-COL-08`.

## Common read-only inspection commands

After `CS-0` evidence is accepted, later units may propose the following direct argv templates for one literal target at a time. They remain unauthorized in this document.

| Command ID | Exact direct argv after the fixed environment prefix | Maximum captured output | Purpose |
|---|---|---:|---|
| `CS-CMD-STAT` | `["/usr/bin/stat", "-f", "%N\\t%HT\\t%u\\t%g\\t%Mp%Lp\\t%z\\t%d\\t%i\\t%l", "<TARGET>"]` | 4 KiB | Type, ownership, mode, bytes, device, inode, and links |
| `CS-CMD-SHA` | `["/usr/bin/shasum", "-a", "256", "<TARGET>"]` | 1 KiB | SHA-256 of one finite regular file |
| `CS-CMD-FILE` | `["/usr/bin/file", "-b", "<TARGET>"]` | 4 KiB | File and architecture classification |
| `CS-CMD-CS-VERIFY` | `["/usr/bin/codesign", "--verify", "--strict", "--verbose=4", "<TARGET>"]` | 16 KiB | Verify Apple code-signing status |
| `CS-CMD-CS-DISPLAY` | `["/usr/bin/codesign", "--display", "--verbose=4", "<TARGET>"]` | 32 KiB | Record code identifier, authority, flags, and code-directory hash |
| `CS-CMD-OTOOL` | `["/usr/bin/otool", "-L", "<TARGET>"]` | 64 KiB | Record linked-library identities |
| `CS-CMD-NM` | `["/usr/bin/nm", "-gU", "<TARGET>"]` | 2 MiB | Record exported symbols for bounded offline filtering |
| `CS-CMD-OS` | `["/usr/bin/sw_vers"]` | 4 KiB | Record macOS product version and build once |
| `CS-CMD-KERNEL` | `["/usr/bin/uname", "-mrs"]` | 4 KiB | Record kernel release and architecture once |

The executor must call the literal executable directly. Shell parsing, pipelines, redirection, globbing, command substitution, PATH lookup, retries, and fallback commands are prohibited. Captured stdout, stderr, exit status, start/end monotonic times, target identity, command-array SHA-256, and output SHA-256 must be recorded separately.

## `CS-COM` — common identity revalidation

### Exact targets

```text
/usr/bin/perl
/usr/bin/env
/usr/bin/false
/Library/Developer/CommandLineTools/usr/bin/git
```

For each target, propose `CS-CMD-STAT`, `CS-CMD-SHA`, `CS-CMD-FILE`, `CS-CMD-CS-VERIFY`, `CS-CMD-CS-DISPLAY`, and `CS-CMD-OTOOL`. `CS-CMD-OS` and `CS-CMD-KERNEL` run once for the unit. Every prior byte count and SHA-256 must match the accepted manifest. Drift stops the unit and invalidates downstream screening until reviewed.

No Git command, Perl source, handoff command, or packet operation is part of `CS-COM`.

## `CS-A` — Route-A static API capability screening

### Exact targets

```text
/usr/lib/libSystem.B.dylib
/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/sys/acl.h
/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/sys/mount.h
/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/sys/stat.h
/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/sys/fcntl.h
```

For the provider, propose `CS-CMD-STAT`, `CS-CMD-SHA`, `CS-CMD-FILE`, `CS-CMD-CS-VERIFY`, `CS-CMD-CS-DISPLAY`, `CS-CMD-OTOOL`, and `CS-CMD-NM`. If the provider is represented only through the dyld shared cache or is not a finite regular file, stop; this request does not nominate a dyld-cache extractor or alternate library path.

For each header, propose only `CS-CMD-STAT`, `CS-CMD-SHA`, and `CS-CMD-FILE`. The literal SDK path and its physically resolved target must be identical to a later accepted SDK identity; this request does not authorize a resolver or alternate Xcode SDK.

Offline review of the bounded outputs must confirm declarations or exports for exactly:

```text
acl_get_fd_np
ACL_TYPE_EXTENDED
acl_get_entry
ACL_FIRST_ENTRY
ACL_NEXT_ENTRY
acl_get_tag_type
acl_get_qualifier
acl_get_flagset_np
acl_get_flag_np
acl_get_permset
acl_get_perm_np
acl_free
fstat
fstatfs
fcntl
F_GETPATH
```

No API call is proposed. Finding the symbols does not resolve the missing Perl binding, prove semantics, or pass a route gate.

## Route-B mutually exclusive screening units

Each unit receives a separate request hash, root, specialist review, and later user authorization. No unit may read another unit's output during execution, and no result may be treated as permission to invoke another candidate.

### `CS-B1` — `/bin/ls` only

Identity inspection proposes `CS-CMD-STAT`, `CS-CMD-SHA`, `CS-CMD-FILE`, `CS-CMD-CS-VERIFY`, `CS-CMD-CS-DISPLAY`, and `CS-CMD-OTOOL` for `/bin/ls`.

The sole proposed capability invocation, after a separately authorized synthetic fixture exists, is:

```text
["/bin/ls", "-lde@", "/private/tmp/mneme-handoff-capability-route-b1-ls-20260919-01/fixture/object"]
```

The fixture must contain no real data. This invocation may screen ACL output only; it cannot be combined with mount evidence from another executable. Path-only or locale-sensitive output is a recorded blocker, not a reason to broaden argv.

### `CS-B2` — `/usr/bin/stat` only

Identity inspection proposes `CS-CMD-STAT`, `CS-CMD-SHA`, `CS-CMD-FILE`, `CS-CMD-CS-VERIFY`, `CS-CMD-CS-DISPLAY`, and `CS-CMD-OTOOL` for `/usr/bin/stat`.

The sole proposed capability invocation is:

```text
["/usr/bin/stat", "-f", "%N\\t%HT\\t%u\\t%g\\t%Mp%Lp\\t%z\\t%d\\t%i\\t%l", "/private/tmp/mneme-handoff-capability-route-b2-stat-20260919-01/fixture/object"]
```

This invocation may screen descriptor-independent metadata formatting only. It must not be combined with `/bin/ls`, `/sbin/mount`, or `/bin/df`. Absence of complete ACL and mount-instance evidence is a blocker.

### `CS-B3` — `/sbin/mount` only

Identity inspection proposes `CS-CMD-STAT`, `CS-CMD-SHA`, `CS-CMD-FILE`, `CS-CMD-CS-VERIFY`, `CS-CMD-CS-DISPLAY`, and `CS-CMD-OTOOL` for `/sbin/mount`.

No executable invocation is proposed. The ordinary no-argument command would enumerate real host mount metadata and violate the synthetic-only boundary. Unless a later reviewed, literal, synthetic-only argv is demonstrated for this exact executable, `CS-B3` remains `Blocked` after static inspection.

### `CS-B4` — `/bin/df` only

Identity inspection proposes `CS-CMD-STAT`, `CS-CMD-SHA`, `CS-CMD-FILE`, `CS-CMD-CS-VERIFY`, `CS-CMD-CS-DISPLAY`, and `CS-CMD-OTOOL` for `/bin/df`.

The sole proposed capability invocation is:

```text
["/bin/df", "-P", "/private/tmp/mneme-handoff-capability-route-b4-df-20260919-01/fixture/object"]
```

This invocation may screen filesystem output for the one synthetic path only. It must not be combined with another Route-B candidate. Path-oriented, incomplete, or alias-insensitive evidence is a blocker.

## `CS-C` — Route-C static toolchain screening

### Exact existing targets

```text
/usr/bin/clang
/usr/bin/ld
/usr/bin/codesign
/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk
```

For each executable, propose `CS-CMD-STAT`, `CS-CMD-SHA`, `CS-CMD-FILE`, `CS-CMD-CS-VERIFY`, `CS-CMD-CS-DISPLAY`, and `CS-CMD-OTOOL`. The SDK receives only a non-recursive metadata check at its literal entry point plus the already listed Route-A header checks. No tree walk, SDK manifest, compiler-driver expansion, or transitive tool discovery is authorized by this request.

The only proposed capability invocations are:

```text
["/usr/bin/clang", "--version"]
["/usr/bin/ld", "-v"]
```

No source file, object, binary, directory under `.mneme-local`, compile, preprocess, assemble, link, sign, install, or execute operation is proposed. Any helper or developer-directory resolution stops the unit rather than expanding it.

The following paths must remain absent and must not be inspected through discovery:

```text
/Users/bogac/dev/forgejo/mneme/tools/handoff/native/mneme_handoff_security_verify.c
/Users/bogac/dev/forgejo/mneme/.mneme-local/bin/mneme-handoff-security-verify
```

## `CS-D1` — Route-D verifier screening

Identity inspection proposes `CS-CMD-STAT`, `CS-CMD-SHA`, `CS-CMD-FILE`, `CS-CMD-CS-VERIFY`, `CS-CMD-CS-DISPLAY`, and `CS-CMD-OTOOL` for `/usr/bin/openssl`.

The only proposed capability invocations are:

```text
["/usr/bin/openssl", "version", "-a"]
["/usr/bin/openssl", "dgst", "-help"]
```

No key, schema, signature, attestation, credential, Keychain identity, random input, configuration file, provider module, engine, network operation, or verification is created or used. If the executable loads configuration, providers, engines, or another helper under the fixed empty environment, stop.

The following paths remain absent:

```text
/Users/bogac/dev/forgejo/mneme/tools/handoff/security/attestation-schema.json
/Users/bogac/dev/forgejo/mneme/tools/handoff/security/synthetic-route-d-public-key.pem
```

## `CS-D2` — continued-disablement screening

No command, API, executable, key, schema, fixture, service, or store is required. The sole finding is that operational use remains blocked. This unit is documentation-only and cannot select Route D.

## Evidence requirements

Every later authorized unit must produce an owner-only evidence package containing:

```text
REQUEST-SHA256.txt
RUNTIME-IDENTITIES.tsv
COMMANDS.jsonl
TARGET-IDENTITIES.tsv
STDOUT/
STDERR/
OUTPUT-MANIFEST.sha256
STOP-RECORD.md
ROLLBACK-STATE.md
SPECIALIST-REVIEW-INPUT.md
```

Each command record must include the literal argv array, fixed environment, executable pre-run identity, target pre-run identity, monotonic start/end times, exit status or signal, stdout/stderr byte counts and SHA-256 values, and post-run target identity. Every output is capped as specified. Truncation is a stop, not acceptable evidence.

For finite target files, record exact literal path, resolved path, file type, numeric owner/group, mode, byte count, device, inode, link count, SHA-256, code-signing evidence where applicable, linked libraries where applicable, provenance, and license source. A missing value remains `UNOBSERVED` and prevents acceptance.

No screening result changes an `UNOBSERVED` value in the accepted manifest. Results belong in a separate evidence record and require specialist review and user acceptance before the manifest can later be superseded.

## Synthetic-only and permission boundary

- Fixtures contain generated names and empty or bounded synthetic bytes only.
- No fixture may contain correspondence, repository content, packet content, personal identifiers, credentials, tokens, real keys, real attestations, or copied host configuration.
- The only writes are evidence files and synthetic fixture objects inside the unit's exact `/private/tmp` root.
- No packet-store directory, `.mneme-local/handoffs/v1`, helper path, source path, schema path, public-key path, service, socket, listener, cache, log, or configuration is created.
- No command runs with elevation, entitlements, inherited environment, network permission, package-manager access, or a writable working directory outside the exact evidence root.
- Candidate APIs are never called. Candidate binaries receive only the literal argv shown for their own unit.
- The existing handoff automation is not invoked and no packet is created, validated, listed, consumed, or rolled back.

## Rollback and failure handling

Before a unit runs, record repository status and prove the unit root absent. On the first deviation:

1. stop without retry, substitution, fallback, broader argv, or another screening unit;
2. preserve the exact owner-only evidence root and write `STOP-RECORD.md` without altering prior files;
3. mark the unit `Incomplete` and keep all associated manifest entries `UNOBSERVED`;
4. record whether any target identity or repository state changed;
5. do not clean uncertain state automatically; and
6. return for review.

After review, rollback may be separately approved to remove only the exact unit root. It must not modify the repository, accepted documents, system paths, packet history, packet store, candidate executable, SDK, helper path, keys, or another unit's evidence. If root removal cannot be proven complete, preserve it owner-only and record the uncertainty.

## Specialist reviews

Each unit requires four reviews of the same request hash before execution and again of the same evidence hash afterward.

| Specialist | Pre-screening finding | Post-screening finding |
|---|---|---|
| Security/privacy | Literal paths and argv are read-only, least-privilege, synthetic-only, non-networked, and non-operational | No hidden helper/configuration/network path, real-data exposure, mutation, or boundary escape occurred |
| Operations/recovery | Runtime, permissions, roots, output caps, stop behavior, and rollback are exact | Target and repository state are unchanged; interruption and residual roots are accounted for |
| Quality/independent verification | Hash bootstrap, command records, expected fields, and evidence schema are reproducible | Hashes, byte counts, outputs, failures, and `UNOBSERVED` dispositions reconcile independently |
| Governance | One screening unit only; Route-B candidates remain separate; no route or operational authority is implied | Evidence is screening-only; no gate, route, implementation, packet-store, or operational status was silently advanced |

A `Fail`, `Unproved`, disagreement, changed request hash, or different evidence object blocks execution or acceptance. Majority vote and silence are insufficient.

## Stop conditions

Stop before or during a later screening unit if:

- its exact request hash and unit name are not explicitly approved by the user;
- `CS-0` or required predecessor evidence is absent, incomplete, or unaccepted;
- an exact root already exists, permissions differ, or a write would escape it;
- a literal executable or target differs by path, resolution, type, owner, group, mode, bytes, SHA-256, signature, link count, or provenance;
- an executable invokes a shell, helper, dispatcher, plug-in, provider, engine, configuration, pager, service, network path, or unlisted library behavior;
- output is malformed, localized, contradictory, missing, oversized, truncated, or non-deterministic;
- a Route-B unit would inspect, invoke, read, or combine another Route-B candidate;
- Route A would require an API call or a Perl binding;
- Route C would create source, compile, link, sign, install, or create the future helper path;
- Route D would create or use a key, schema, attestation, credential, Keychain item, or real host evidence;
- a packet store, packet operation, watcher, service, listener, build, test, dependency, account, correspondence, or operational handoff path is encountered; or
- any network access is attempted or observed.

## Review and later approval gate

Review whether this request completely and narrowly defines capability screening without granting it. If accepted as planning, it must still remain non-executable until the user later names one exact screening unit and the SHA-256 of the unchanged request.

A valid later authorization must say, in substance:

> I authorize capability-screening unit `<EXACT-UNIT>` only under request SHA-256 `<EXACT-HASH>`. No other unit, route execution, route selection, implementation, packet-store creation, or operational use is authorized.

No such authorization is present now.
