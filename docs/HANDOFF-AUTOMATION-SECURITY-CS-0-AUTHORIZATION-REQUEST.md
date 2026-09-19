# Handoff Automation Security CS-0 Authorization Request

**Status:** Accepted

**Proposal date:** 2026-09-19

**Review date:** 2026-09-19

**Authorization effect:** None until separately reviewed and explicitly approved

**Authorized unit if later approved:** `CS-0` only

**Route-selection state:** No route selected or approved

**Current allowed command/API invocation set:** Empty

**Operational-use state:** Blocked

**Governing screening request:** [Handoff Automation Security Capability-Screening Request](HANDOFF-AUTOMATION-SECURITY-CAPABILITY-SCREENING-REQUEST.md), Accepted 2026-09-19

**Governing-screening commit:** `35b750f5d5ea1c020e302bab7d69ac52ae7eee1e`

**Governing manifest:** [Handoff Automation Security Evidence-Source Manifest](HANDOFF-AUTOMATION-SECURITY-EVIDENCE-SOURCE-MANIFEST.md), Accepted 2026-09-19

**Manifest state:** All 25 `UNOBSERVED` occurrences remain unresolved

## Purpose

Request a later, separate authorization for `CS-0` only: create one disposable owner-only evidence root and one deterministic synthetic canary, then use the previously accepted Perl runtime to read the finite bytes and static metadata of six non-candidate collection-tool paths without executing those tools.

This request closes the earlier procedural gaps by defining:

- direct argument arrays with no shell;
- exact root and fixture creation operations;
- the only executable identities;
- owner, mode, symlink, mount-device, and containment checks;
- the complete disposable layout;
- machine evidence and self-excluding hashes;
- failure preservation and later rollback; and
- pre- and post-execution specialist review gates.

It does not authorize execution now. It does not combine `CS-0` with `CS-COM`, `CS-A`, `CS-B1` through `CS-B4`, `CS-C`, `CS-D1`, or `CS-D2`.

## No candidate-path inspection

`CS-0` may inspect only the six collection-tool paths in the allowlist below. It must not inspect any route candidate, provider, SDK header, toolchain candidate, verifier candidate, future source path, future binary path, schema, key, packet, or handoff object.

Two proposed collection tools are deliberately excluded because the same literal paths are also route candidates:

| Excluded manifest entry | Path | Reason |
|---|---|---|
| `SR-COL-01` / `SR-B-EXE-02` | `/usr/bin/stat` | Route-B candidate path; candidate inspection is forbidden during `CS-0` |
| `SR-COL-03` / `SR-C-TC-03` | `/usr/bin/codesign` | Route-C toolchain candidate path; candidate inspection is forbidden during `CS-0` |

Both paths remain `UNOBSERVED`. Their exclusion does not imply absence, failure, suitability, or rejection.

The following path classes are also expressly forbidden during `CS-0`:

```text
/usr/lib/libSystem.B.dylib
/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk
/bin/ls
/usr/bin/stat
/sbin/mount
/bin/df
/usr/bin/clang
/usr/bin/ld
/usr/bin/codesign
/usr/bin/openssl
/Users/bogac/dev/forgejo/mneme/tools/handoff/native
/Users/bogac/dev/forgejo/mneme/.mneme-local
/Users/bogac/dev/forgejo/mneme/tools/handoff/security
```

No missing or unavailable forbidden path may be probed or used to infer a capability.

## Exact executable identities

Only these two previously accepted executables may participate, in this order: `/usr/bin/env` directly replaces the empty process image with `/usr/bin/perl`; Perl performs every authorized filesystem operation internally. No shell, `mkdir`, `touch`, `rm`, `stat`, `shasum`, `codesign`, `file`, `otool`, `nm`, helper, or package command is invoked.

| ID | Exact path | Type and permissions | Bytes | SHA-256 | Provenance | Later role |
|---|---|---|---:|---|---|---|
| `CS0-EXE-01` | `/usr/bin/env` | Regular system executable; `root:wheel`; mode `0755` | 167,712 | `2b2a1145527f00e8369fda0d2ffc523b520201bb08dbaf4b0bded837f7652ce0` | Apple macOS; accepted prior evidence | Clear the environment and directly invoke `CS0-EXE-02` |
| `CS0-EXE-02` | `/usr/bin/perl` | Regular Mach-O universal binary; `root:wheel`; mode `0755` | 167,184 | `85e5621137742a37be052f58800372b2005f91f609ad55019832214b5d9e61bc` | Apple macOS; accepted prior evidence | Run only the four inline programs frozen below |

If either path, byte count, SHA-256, owner, group, mode, regular-file type, or prior evidence is disputed or stale, stop before root creation. This request does not authorize a fresh read of either executable to resolve that dispute.

Permitted Perl core modules are limited to:

```text
strict
warnings
bytes
Fcntl
Cwd
Digest::SHA
JSON::PP
IO::Handle
```

No module search path, downloaded module, XS extension, FFI, dynamic library call, subprocess, pipe, network API, or `system`, `exec`, backtick, or shell operation is permitted inside Perl.

## Direct-execution contract

The host executor must support a direct executable path, a literal argv vector, and a literal environment vector. It must not interpolate a command string or invoke a shell. If the available executor cannot prove this boundary, stop before root creation.

Every invocation has this exact prefix:

```text
[
  "/usr/bin/env", "-i",
  "PATH=/usr/bin:/bin",
  "LC_ALL=C",
  "LANG=C",
  "TZ=UTC",
  "/usr/bin/perl", "-T",
  <PROGRAM-MODULE-ARGUMENTS>,
  "-e", <EXACT-PROGRAM-SOURCE>,
  "--", <EXACT-PROGRAM-ARGUMENTS>
]
```

The process working directory must be `/private/tmp`. Standard input must be closed. Standard output and standard error are captured separately with 64 KiB caps and must both be empty for root creation, fixture creation, and target inspection. The finalizer may emit one newline-terminated SHA-256 for the completed core manifest, capped at 128 bytes.

The executor must record the literal argv and environment before invocation. Argument-array recording is host evidence; it may not be reconstructed later from a shell transcript.

## Exact disposable root and layout

The only writable root is:

```text
/private/tmp/mneme-handoff-capability-cs0-20260919-01
```

It must be absent before the first command. The root-creation command creates exactly:

```text
/private/tmp/mneme-handoff-capability-cs0-20260919-01/                 0700
├── evidence/                                                         0700
│   ├── commands/                                                     0700
│   │   └── CS0-ROOT.json                                             0600
│   ├── tool-identities/                                              0700
│   └── OUTPUT-MANIFEST.sha256                                        absent until finalization
└── fixture/                                                          0700
```

The fixture command then creates exactly:

```text
fixture/cs0-canary.txt                                                 0600
evidence/commands/CS0-FIXTURE.json                                    0600
```

The six target-inspection commands create exactly:

```text
evidence/tool-identities/SR-COL-02.json                                0600
evidence/tool-identities/SR-COL-04.json                                0600
evidence/tool-identities/SR-COL-05.json                                0600
evidence/tool-identities/SR-COL-06.json                                0600
evidence/tool-identities/SR-COL-07.json                                0600
evidence/tool-identities/SR-COL-08.json                                0600
```

No `STDOUT`, `STDERR`, cache, home, configuration, packet, key, credential, service, socket, log, source, binary, or installation directory is created. Captured empty output is recorded by the host executor outside the unit root and referenced in the later evidence summary; it is not synthesized into a file by these commands.

## Root, ownership, symlink, mount-device, and containment contract

Every inline program must enforce all applicable checks before writing:

1. `/private` and `/private/tmp` are existing directories, not symlinks at their final components, owned by numeric UID `0` and GID `0`, and not group/other writable except the expected sticky world-writable mode on `/private/tmp`;
2. `Cwd::abs_path('/private/tmp')` is exactly `/private/tmp`;
3. the exact unit root is absent before creation;
4. process effective UID and effective GID are recorded, and no elevation is attempted;
5. `umask(0077)` is set before any creation;
6. root and all child directories are created with mode `0700` and files with mode `0600` using exclusive creation;
7. no created final component is a symlink or has link count other than one for files;
8. `Cwd::abs_path` for every created object begins with the exact root plus `/`, except the root itself, which must equal the literal root;
9. the root and `/private/tmp` have equal `st_dev`, with both device values recorded;
10. every created child has the same `st_dev` as the root;
11. root parent identity, root identity, and every created object's device and inode are recorded before finalization; and
12. equality of `st_dev` is explicitly labeled a disposable-root containment check only, not evidence for same-device mount-alias safety or any route gate.

If mount-instance identity stronger than `st_dev` would be required to proceed safely, stop. `CS-0` must not inspect a mount candidate or call a mount API to close that uncertainty.

## Exact root-creation command

The direct argv is the fixed prefix plus:

```text
<PROGRAM-MODULE-ARGUMENTS> =
["-MFcntl=:DEFAULT,:mode,O_NOFOLLOW", "-MCwd=abs_path", "-MJSON::PP", "-MIO::Handle"]

<EXACT-PROGRAM-ARGUMENTS> =
[
  "/private/tmp/mneme-handoff-capability-cs0-20260919-01",
  "<ACCEPTED-CS0-REQUEST-SHA256>"
]
```

`<ACCEPTED-CS0-REQUEST-SHA256>` must be replaced by the lowercase 64-hex SHA-256 of the final Accepted bytes of this document, explicitly named by the later user authorization. No other substitution is allowed.

`<EXACT-PROGRAM-SOURCE>` is the exact UTF-8 text below, passed as one argv element:

```perl
use strict;use warnings;use bytes;
@ARGV==2 or die "ARG_COUNT\n";
my($root)=$ARGV[0]=~m{\A(/private/tmp/mneme-handoff-capability-cs0-20260919-01)\z} or die "ROOT\n";
my($request_sha)=$ARGV[1]=~m{\A([0-9a-f]{64})\z} or die "REQUEST_SHA\n";
for my $p ('/private','/private/tmp') { my @s=lstat($p); @s or die "PARENT_LSTAT\n"; S_ISDIR($s[2]) or die "PARENT_TYPE\n"; S_ISLNK($s[2]) and die "PARENT_SYMLINK\n"; $s[4]==0 && $s[5]==0 or die "PARENT_OWNER\n"; }
(((lstat('/private/tmp'))[2])&01777)==01777 or die "TMP_MODE\n";
abs_path('/private/tmp') eq '/private/tmp' or die "TMP_REALPATH\n";
my @pre=lstat($root); @pre and die "ROOT_EXISTS\n";
umask 0077;
mkdir($root,0700) or die "MKDIR_ROOT\n";
for my $d ("$root/evidence","$root/evidence/commands","$root/evidence/tool-identities","$root/fixture") { mkdir($d,0700) or die "MKDIR_CHILD\n"; }
my @ps=stat('/private/tmp'); my @rs=lstat($root); @ps && @rs or die "ROOT_STAT\n"; S_ISDIR($rs[2]) or die "ROOT_TYPE\n"; S_ISLNK($rs[2]) and die "ROOT_SYMLINK\n"; ($rs[2]&07777)==0700 or die "ROOT_MODE\n"; $rs[4]==$> && $rs[5]==$) or die "ROOT_OWNER\n"; $rs[0]==$ps[0] or die "ROOT_DEVICE\n"; abs_path($root) eq $root or die "ROOT_REALPATH\n";
for my $d ("$root/evidence","$root/evidence/commands","$root/evidence/tool-identities","$root/fixture") { my @s=lstat($d); @s or die "CHILD_LSTAT\n"; S_ISDIR($s[2]) or die "CHILD_TYPE\n"; S_ISLNK($s[2]) and die "CHILD_SYMLINK\n"; ($s[2]&07777)==0700 or die "CHILD_MODE\n"; $s[4]==$> && $s[5]==$) or die "CHILD_OWNER\n"; $s[0]==$rs[0] or die "CHILD_DEVICE\n"; index(abs_path($d),"$root/")==0 or die "CHILD_CONTAINMENT\n"; }
my $record=JSON::PP->new->canonical->utf8->encode({unit=>'CS-0',operation=>'root-create',request_sha256=>$request_sha,root=>$root,euid=>$>,egid=>$),parent_device=>$ps[0],root_device=>$rs[0],root_inode=>$rs[1],root_mode=>sprintf('%04o',$rs[2]&07777),mount_claim=>'st_dev containment only; not route evidence'})."\n";
my $out="$root/evidence/commands/CS0-ROOT.json";
sysopen(my $fh,$out,O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW,0600) or die "RECEIPT_OPEN\n";
print {$fh} $record or die "RECEIPT_WRITE\n"; $fh->sync or die "RECEIPT_SYNC\n"; close($fh) or die "RECEIPT_CLOSE\n";
```

Any compile-time, constant, ownership, mode, filesystem, path, write, or sync error stops the unit. A partially created root is preserved owner-only for review; no automatic cleanup follows.

## Exact synthetic-fixture creation command

The direct argv is the fixed prefix plus:

```text
<PROGRAM-MODULE-ARGUMENTS> =
["-MFcntl=:DEFAULT,:mode,O_NOFOLLOW", "-MCwd=abs_path", "-MDigest::SHA=sha256_hex", "-MJSON::PP", "-MIO::Handle"]

<EXACT-PROGRAM-ARGUMENTS> =
[
  "/private/tmp/mneme-handoff-capability-cs0-20260919-01",
  "<ACCEPTED-CS0-REQUEST-SHA256>"
]
```

The exact fixture bytes are the UTF-8/ASCII bytes of:

```text
MNEME-CS0-SYNTHETIC-CANARY-v1
```

including one terminal line feed and no other bytes.

`<EXACT-PROGRAM-SOURCE>` is:

```perl
use strict;use warnings;use bytes;
@ARGV==2 or die "ARG_COUNT\n";
my($root)=$ARGV[0]=~m{\A(/private/tmp/mneme-handoff-capability-cs0-20260919-01)\z} or die "ROOT\n";
my($request_sha)=$ARGV[1]=~m{\A([0-9a-f]{64})\z} or die "REQUEST_SHA\n";
my @rs=lstat($root); @rs or die "ROOT_LSTAT\n"; S_ISDIR($rs[2]) or die "ROOT_TYPE\n"; S_ISLNK($rs[2]) and die "ROOT_SYMLINK\n"; ($rs[2]&07777)==0700 or die "ROOT_MODE\n"; $rs[4]==$> && $rs[5]==$) or die "ROOT_OWNER\n"; abs_path($root) eq $root or die "ROOT_REALPATH\n";
my $content="MNEME-CS0-SYNTHETIC-CANARY-v1\n";
my $fixture="$root/fixture/cs0-canary.txt";
sysopen(my $fh,$fixture,O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW,0600) or die "FIXTURE_OPEN\n";
print {$fh} $content or die "FIXTURE_WRITE\n"; $fh->sync or die "FIXTURE_SYNC\n"; close($fh) or die "FIXTURE_CLOSE\n";
my @fs=lstat($fixture); @fs or die "FIXTURE_LSTAT\n"; S_ISREG($fs[2]) or die "FIXTURE_TYPE\n"; S_ISLNK($fs[2]) and die "FIXTURE_SYMLINK\n"; ($fs[2]&07777)==0600 or die "FIXTURE_MODE\n"; $fs[4]==$> && $fs[5]==$) or die "FIXTURE_OWNER\n"; $fs[3]==1 or die "FIXTURE_LINKS\n"; $fs[0]==$rs[0] or die "FIXTURE_DEVICE\n"; abs_path($fixture) eq $fixture or die "FIXTURE_REALPATH\n";
my $record=JSON::PP->new->canonical->utf8->encode({unit=>'CS-0',operation=>'fixture-create',request_sha256=>$request_sha,path=>$fixture,bytes=>length($content),sha256=>sha256_hex($content),device=>$fs[0],inode=>$fs[1],mode=>sprintf('%04o',$fs[2]&07777),synthetic_only=>JSON::PP::true})."\n";
my $out="$root/evidence/commands/CS0-FIXTURE.json";
sysopen(my $rf,$out,O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW,0600) or die "RECEIPT_OPEN\n";
print {$rf} $record or die "RECEIPT_WRITE\n"; $rf->sync or die "RECEIPT_SYNC\n"; close($rf) or die "RECEIPT_CLOSE\n";
```

The fixture proves only that deterministic bytes can be created and hashed inside the disposable root. It is not an ACL, mount, packet, attestation, correspondence, or route fixture.

## Exact non-candidate inspection allowlist

| Manifest ID | Exact path | Required precondition | Evidence output |
|---|---|---|---|
| `SR-COL-02` | `/usr/bin/shasum` | Regular file; UID `0`; GID `0`; mode `0755`; final component not a symlink | `evidence/tool-identities/SR-COL-02.json` |
| `SR-COL-04` | `/usr/bin/file` | Same | `evidence/tool-identities/SR-COL-04.json` |
| `SR-COL-05` | `/usr/bin/otool` | Same | `evidence/tool-identities/SR-COL-05.json` |
| `SR-COL-06` | `/usr/bin/nm` | Same | `evidence/tool-identities/SR-COL-06.json` |
| `SR-COL-07` | `/usr/bin/sw_vers` | Same | `evidence/tool-identities/SR-COL-07.json` |
| `SR-COL-08` | `/usr/bin/uname` | Same | `evidence/tool-identities/SR-COL-08.json` |

The tools are opened as raw bytes by Perl and are never invoked. Their observed hashes remain evidence awaiting review; this request does not update the accepted manifest or clear an `UNOBSERVED` blocker.

## Exact target-inspection command

Run the following command once per allowlist row, sequentially in table order. No retry is permitted.

```text
<PROGRAM-MODULE-ARGUMENTS> =
["-MFcntl=:DEFAULT,:mode,O_NOFOLLOW", "-MCwd=abs_path", "-MDigest::SHA", "-MJSON::PP", "-MIO::Handle"]

<EXACT-PROGRAM-ARGUMENTS> =
[
  "/private/tmp/mneme-handoff-capability-cs0-20260919-01",
  "<ACCEPTED-CS0-REQUEST-SHA256>",
  "<MANIFEST-ID>",
  "<EXACT-TARGET-PATH>"
]
```

The only legal substitutions are the six exact `(MANIFEST-ID, EXACT-TARGET-PATH)` pairs in the table.

`<EXACT-PROGRAM-SOURCE>` is:

```perl
use strict;use warnings;use bytes;
@ARGV==4 or die "ARG_COUNT\n";
my($root)=$ARGV[0]=~m{\A(/private/tmp/mneme-handoff-capability-cs0-20260919-01)\z} or die "ROOT\n";
my($request_sha)=$ARGV[1]=~m{\A([0-9a-f]{64})\z} or die "REQUEST_SHA\n";
my($id)=$ARGV[2]=~m{\A(SR-COL-(?:02|04|05|06|07|08))\z} or die "ID\n";
my %allowed=('SR-COL-02'=>'/usr/bin/shasum','SR-COL-04'=>'/usr/bin/file','SR-COL-05'=>'/usr/bin/otool','SR-COL-06'=>'/usr/bin/nm','SR-COL-07'=>'/usr/bin/sw_vers','SR-COL-08'=>'/usr/bin/uname');
my($target)=$ARGV[3]=~m{\A(/[A-Za-z0-9_+./-]+)\z} or die "TARGET\n";
$allowed{$id} eq $target or die "PAIR\n";
my @rs=lstat($root); @rs or die "ROOT_LSTAT\n"; S_ISDIR($rs[2]) or die "ROOT_TYPE\n"; S_ISLNK($rs[2]) and die "ROOT_SYMLINK\n"; ($rs[2]&07777)==0700 or die "ROOT_MODE\n"; $rs[4]==$> && $rs[5]==$) or die "ROOT_OWNER\n"; abs_path($root) eq $root or die "ROOT_REALPATH\n";
my @s=lstat($target); @s or die "TARGET_LSTAT\n"; S_ISREG($s[2]) or die "TARGET_TYPE\n"; S_ISLNK($s[2]) and die "TARGET_SYMLINK\n"; $s[4]==0 && $s[5]==0 or die "TARGET_OWNER\n"; ($s[2]&07777)==0755 or die "TARGET_MODE\n"; $s[3]==1 or die "TARGET_LINKS\n"; abs_path($target) eq $target or die "TARGET_REALPATH\n";
open(my $fh,'<:raw',$target) or die "TARGET_OPEN\n"; my $d=Digest::SHA->new(256); $d->addfile($fh); close($fh) or die "TARGET_CLOSE\n";
my $record=JSON::PP->new->canonical->utf8->encode({unit=>'CS-0',operation=>'static-byte-inspection',request_sha256=>$request_sha,manifest_id=>$id,path=>$target,uid=>$s[4],gid=>$s[5],mode=>sprintf('%04o',$s[2]&07777),bytes=>$s[7],device=>$s[0],inode=>$s[1],links=>$s[3],sha256=>$d->hexdigest,executed=>JSON::PP::false,candidate_path=>JSON::PP::false})."\n";
my $out="$root/evidence/tool-identities/$id.json";
sysopen(my $rf,$out,O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW,0600) or die "OUTPUT_OPEN\n";
print {$rf} $record or die "OUTPUT_WRITE\n"; $rf->sync or die "OUTPUT_SYNC\n"; close($rf) or die "OUTPUT_CLOSE\n";
```

## Exact core-evidence finalization command

Finalization runs only after the root, fixture, and all six identity records pass structural checks. It hashes an explicit list; it performs no directory walk, glob, discovery, or candidate read.

```text
<PROGRAM-MODULE-ARGUMENTS> =
["-MFcntl=:DEFAULT,:mode,O_NOFOLLOW", "-MCwd=abs_path", "-MDigest::SHA", "-MIO::Handle"]

<EXACT-PROGRAM-ARGUMENTS> =
[
  "/private/tmp/mneme-handoff-capability-cs0-20260919-01"
]
```

`<EXACT-PROGRAM-SOURCE>` is:

```perl
use strict;use warnings;use bytes;
@ARGV==1 or die "ARG_COUNT\n";
my($root)=$ARGV[0]=~m{\A(/private/tmp/mneme-handoff-capability-cs0-20260919-01)\z} or die "ROOT\n";
my @rs=lstat($root); @rs or die "ROOT_LSTAT\n"; S_ISDIR($rs[2]) or die "ROOT_TYPE\n"; S_ISLNK($rs[2]) and die "ROOT_SYMLINK\n"; ($rs[2]&07777)==0700 or die "ROOT_MODE\n"; $rs[4]==$> && $rs[5]==$) or die "ROOT_OWNER\n"; abs_path($root) eq $root or die "ROOT_REALPATH\n";
my @rel=('evidence/commands/CS0-ROOT.json','evidence/commands/CS0-FIXTURE.json','fixture/cs0-canary.txt','evidence/tool-identities/SR-COL-02.json','evidence/tool-identities/SR-COL-04.json','evidence/tool-identities/SR-COL-05.json','evidence/tool-identities/SR-COL-06.json','evidence/tool-identities/SR-COL-07.json','evidence/tool-identities/SR-COL-08.json');
my @lines;
for my $rel (@rel) { my $path="$root/$rel"; index(abs_path($path),"$root/")==0 or die "CONTAINMENT\n"; my @s=lstat($path); @s or die "INPUT_LSTAT\n"; S_ISREG($s[2]) or die "INPUT_TYPE\n"; S_ISLNK($s[2]) and die "INPUT_SYMLINK\n"; ($s[2]&07777)==0600 or die "INPUT_MODE\n"; $s[4]==$> && $s[5]==$) or die "INPUT_OWNER\n"; $s[3]==1 or die "INPUT_LINKS\n"; $s[0]==$rs[0] or die "INPUT_DEVICE\n"; open(my $fh,'<:raw',$path) or die "INPUT_OPEN\n"; my $d=Digest::SHA->new(256); $d->addfile($fh); close($fh) or die "INPUT_CLOSE\n"; push @lines,$d->hexdigest."  ".$rel."\n"; }
my $manifest=join('',@lines);
my $out="$root/evidence/OUTPUT-MANIFEST.sha256";
sysopen(my $mf,$out,O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW,0600) or die "MANIFEST_OPEN\n";
print {$mf} $manifest or die "MANIFEST_WRITE\n"; $mf->sync or die "MANIFEST_SYNC\n"; close($mf) or die "MANIFEST_CLOSE\n";
my $core=Digest::SHA::sha256_hex($manifest); print $core,"\n";
```

`OUTPUT-MANIFEST.sha256` is self-excluding and contains exactly nine sorted-in-declared-order records. The finalizer's one-line stdout is the SHA-256 of the manifest bytes, not an additional manifest member.

## Evidence package and hashes

The complete review package after a later authorized run must contain:

| Evidence | Hash requirement |
|---|---|
| Accepted CS-0 request | Exact SHA-256 named in the user authorization and every command receipt |
| Direct argv/environment records | One SHA-256 per canonical record, captured before invocation |
| `CS0-ROOT.json` | Included in `OUTPUT-MANIFEST.sha256` |
| `CS0-FIXTURE.json` | Included in `OUTPUT-MANIFEST.sha256`; contains fixture byte count and SHA-256 |
| `cs0-canary.txt` | Included in `OUTPUT-MANIFEST.sha256` |
| Six tool-identity JSON files | Each records target bytes and SHA-256 and is included in `OUTPUT-MANIFEST.sha256` |
| `OUTPUT-MANIFEST.sha256` | Self-excluding SHA-256 reported by finalizer stdout |
| Captured stdout/stderr/exit records | SHA-256 and byte count from the direct executor; outputs must meet the caps |
| `CS0-STOP-RECORD.md` | Required on any deviation; SHA-256 recorded in the review summary |
| `CS0-ROLLBACK-STATE.md` | Records preserved-root state and later disposition; SHA-256 recorded in the review summary |
| `CS0-SPECIALIST-FINDINGS.md` | Four findings over the same evidence hash; remains separate from machine evidence |

The six observed collection-tool hashes are evidence only. Every one of the accepted manifest's 25 `UNOBSERVED` occurrences remains unresolved until the evidence package is independently reviewed and the user separately approves a superseding record.

## Specialist reviews

Before execution, all four specialists must review the same Accepted request SHA-256:

| Specialist | Required pre-execution finding |
|---|---|
| Security/privacy | Only `/usr/bin/env` and `/usr/bin/perl` execute; six non-candidate targets are read as bytes; no candidate, network, credential, real-data, API, packet, or operational path exists |
| Operations/recovery | Exact root, permissions, partial-failure preservation, direct argv, evidence layout, output caps, and rollback boundary are complete |
| Quality/independent verification | Inline programs, allowlist pairs, deterministic fixture, explicit manifest members, and self-excluding hashes are internally consistent and independently reproducible |
| Governance | `CS-0` is isolated; all 25 `UNOBSERVED` markers remain unresolved; no downstream unit, route gate, selection, implementation, or operational approval is implied |

After execution, the same four specialists must review the same core-manifest hash and record `Pass`, `Fail`, or `Unproved`, disagreements, residual uncertainty, and acceptance conditions. No majority vote or silence closes a finding.

## Stop conditions

Stop before root creation unless the user explicitly approves `CS-0` under the SHA-256 of the final Accepted bytes of this request.

Stop immediately without retry, substitution, fallback, cleanup, or downstream work if:

- direct no-shell argv and exact environment execution cannot be proven;
- either executable's accepted path, bytes, SHA-256, ownership, mode, type, or provenance is disputed;
- `/private`, `/private/tmp`, the unit root, or any created object fails an owner, mode, type, symlink, realpath, device, inode, link-count, or containment check;
- the root already exists or any authorized output path already exists;
- `O_NOFOLLOW`, exclusive creation, sync, canonical JSON, SHA-256, or a required core module is unavailable;
- any command emits unexpected stdout or stderr, exceeds a cap, exits nonzero, receives a signal, or has uncertain completion;
- an allowlist path or ID differs, a target is absent, or its type, UID, GID, mode, link count, or realpath differs;
- a candidate path, forbidden prefix, mount API, ACL API, route executable, helper, SDK, source, binary, schema, key, packet, packet store, account, correspondence, credential, network endpoint, service, watcher, listener, build, test, or operational path would be read, created, or invoked;
- `/usr/bin/stat` or `/usr/bin/codesign` would be inspected despite their dual candidate roles;
- a hash or missing path is interpreted as route capability, gate success, or route rejection; or
- repository state changes other than a separately authorized later evidence document.

On stop, preserve any created root owner-only, record the exact last completed operation and observed state, leave all 25 `UNOBSERVED` occurrences unresolved, and return for review.

## Rollback

This request does not authorize rollback execution. Before `CS-0`, rollback is unnecessary because no root exists.

After a complete or stopped run:

1. preserve the exact root unchanged through evidence review;
2. record every existing authorized path, type, mode, owner, device, inode, byte count, and SHA-256;
3. prepare a separate rollback authorization naming the root and every existing child explicitly;
4. remove files before directories using direct argv and no recursive, wildcard, shell, or discovery operation;
5. stop if any unexpected child, symlink, mount change, ownership change, or containment discrepancy exists; and
6. prove the exact root absent afterward without touching another path.

No repository file, packet store, handoff history, system path, candidate path, source path, or other evidence root may be modified by rollback.

## Definition of complete `CS-0` evidence

`CS-0` is complete only if:

- the root and fixture commands succeed once under exact direct argv;
- exactly six non-candidate tool identities are recorded without executing them;
- `/usr/bin/stat` and `/usr/bin/codesign` remain uninspected;
- the exact nine-member core manifest reconciles;
- no candidate or forbidden path was accessed;
- all repository and system paths remain unchanged;
- the four post-execution specialist findings review the same hash; and
- the result is presented to the user without changing the accepted manifest.

Completion does not accept the evidence, resolve an `UNOBSERVED` marker, authorize `CS-COM`, authorize any Route-B unit, pass a mandatory gate, select a route, create the packet store, or permit operational use.

## Review request

Review this `CS-0`-only request as a proposed execution boundary. Do not execute it until it is separately marked `Accepted`, dated, committed alone, assigned its final Accepted-file SHA-256, reviewed by all four specialists, and explicitly authorized by the user under that exact hash.
