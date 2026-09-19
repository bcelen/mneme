# Handoff Automation Security Evidence-Source Manifest

**Status:** Accepted

**Proposal date:** 2026-09-19

**Review date:** 2026-09-19

**Route-selection state:** No route selected

**Evidence-collection state:** Not authorized

**Operational-use state:** Blocked

**Current allowed command/API invocation set:** Empty

**Governing plan:** [Handoff Automation Security Route-Evidence Plan](HANDOFF-AUTOMATION-SECURITY-ROUTE-EVIDENCE-PLAN.md), Accepted 2026-09-19

**Governing-plan commit:** `22d622616dff11151f7efdddbf2b29dd6ddc9eac`

**Governing-plan SHA-256:** `9fc33128ece52b08cd9541604d7ecc9b24a30c7e7fe1f4bb0c10c527f7805798`

**Comparison record:** [ADR-007: Handoff Security Remediation Route Comparison](decisions/007-handoff-security-remediation-route-comparison.md), `Proposed`; no route selected

## Purpose

Freeze the exact executable paths, API symbols, provider paths, proposed operations, provenance requirements, permissions, and hash obligations that would be needed to evaluate Routes A through D. Listing an identity here nominates it for review only. It does not approve, allow, invoke, read, hash, inspect, load, link, build, install, or execute that identity.

This manifest is deliberately separate from:

1. identity collection;
2. route-evidence execution;
3. route scoring or selection;
4. implementation;
5. packet-store initialization; and
6. operational use.

Each later activity requires its own exact authorization. Until then, the executable and API allowlists remain empty.

## Status vocabulary

| Status | Meaning |
|---|---|
| `Accepted prior evidence` | Exact static identity was recorded in an already accepted document; no fresh invocation is allowed |
| `Proposed-unobserved` | Exact path or symbol is nominated, but local existence, bytes, hash, permissions, signature, and behavior have not been collected under this plan |
| `Not created` | Exact future repository or temporary path is nominated, but the object must remain absent |
| `Blocked` | A required exact identity is missing or cannot yet satisfy the route boundary |
| `Rejected` | The identity cannot satisfy the governing requirements and must not be substituted silently |

`Proposed-unobserved`, `Not created`, and `Blocked` are not acceptable runtime identities. A finite local artifact has no usable identity until its exact regular-file type, resolved path, owner, group, mode, byte count, SHA-256, code-signing identity where applicable, provenance, license, and immutable version are recorded and reviewed.

## Global identity and permission rules

- Every executable must be an absolute path to one regular file. PATH lookup, aliases, shell functions, shebang resolution, symlink substitution, dispatch stubs, fallbacks, and alternate binaries are prohibited.
- Apple operating-system executables and libraries must have Apple provenance and a valid platform code-signing identity. A version string alone is insufficient.
- System executable permission target: `root:wheel`, mode `0755`, no group/other write, and no unresolved symlink.
- System header and SDK-file permission target: `root:wheel`, mode `0644` or stricter, no group/other write, with the literal path and resolved immutable SDK path both recorded.
- Project source and documentation permission target: repository-tracked regular file, mode `0644`, no generated or ignored substitute.
- A future project-owned helper, if ever created, must be owner-only, mode `0700`, at the single path named below. Its source remains tracked and reviewable.
- Future synthetic roots must be newly created owner-only directories with mode `0700`; contained non-executable files must be `0600`.
- SHA-256 is the only artifact digest. `UNOBSERVED` means that hashing is not yet authorized; it is a blocker, not a wildcard.
- An API symbol inherits the hash and provenance of its accepted provider library and authoritative header. Both must be frozen before the symbol can be called.
- No identity may discover configuration, load a plug-in, invoke a helper, contact a service, prompt, write outside an exact synthetic root, or access the network.

## Common frozen identities

These identities were recorded by the accepted handoff implementation review. They are carried forward for comparison, not re-authorized for invocation.

| ID | Exact path | Required type and permissions | Bytes | SHA-256 | Provenance | Proposed later operation | Current status |
|---|---|---|---:|---|---|---|---|
| `SR-COM-01` | `/usr/bin/perl` | Regular Mach-O universal binary; `root:wheel`; `0755` | 167,184 | `85e5621137742a37be052f58800372b2005f91f609ad55019832214b5d9e61bc` | Apple-provided macOS runtime | Taint-mode execution of already accepted handoff source or separately accepted synthetic adapters only | `Accepted prior evidence`; invocation not authorized |
| `SR-COM-02` | `/usr/bin/env` | Regular system executable; required `root:wheel`; `0755` | 167,712 | `2b2a1145527f00e8369fda0d2ffc523b520201bb08dbaf4b0bded837f7652ce0` | Apple-provided macOS executable | Construct one exact empty, bounded environment for a later authorized invocation | `Accepted prior evidence`; invocation not authorized |
| `SR-COM-03` | `/usr/bin/false` | Regular system executable; required `root:wheel`; `0755` | 133,184 | `ccdd13063a974daa3ffcb707ac70104fb642eaf4aab3b621e816f36e2e8b59ab` | Apple-provided macOS executable | Fail-closed askpass identity only | `Accepted prior evidence`; invocation not authorized |
| `SR-COM-04` | `/Library/Developer/CommandLineTools/usr/bin/git` | Regular Command Line Tools executable; required `root:wheel`; `0755` | 3,837,392 | `a73bf622a2e470d5d57a4b1d5aef1e8680e67278018d4858a2f93825b7d595c7` | Apple Command Line Tools | Existing frozen read-only repository queries only | `Accepted prior evidence`; invocation by route evaluation not authorized |

The prior evidence does not establish current bytes after an operating-system or Command Line Tools update. A later collection request must either revalidate these values before any route evaluation or stop on drift.

## Proposed identity-collection tools

These tools would be needed only to establish the candidate identities below. None may run until a separate identity-collection authorization freezes its literal argument arrays, inputs, outputs, and bootstrap trust method.

| ID | Exact path | Required permissions | Required SHA-256 | Provenance | Sole proposed operation | Status |
|---|---|---|---|---|---|---|
| `SR-COL-01` | `/usr/bin/stat` | `root:wheel`; `0755`; regular file | `UNOBSERVED` | Apple macOS | Read type, owner, group, mode, bytes, device, inode, and link count for explicitly listed identities | `Proposed-unobserved` |
| `SR-COL-02` | `/usr/bin/shasum` | `root:wheel`; `0755`; regular file | `UNOBSERVED` | Apple macOS | Compute SHA-256 for explicitly listed finite local artifacts | `Proposed-unobserved` |
| `SR-COL-03` | `/usr/bin/codesign` | `root:wheel`; `0755`; regular file | `UNOBSERVED` | Apple macOS | Display and verify code-signing metadata for explicitly listed Mach-O objects | `Proposed-unobserved` |
| `SR-COL-04` | `/usr/bin/file` | `root:wheel`; `0755`; regular file | `UNOBSERVED` | Apple macOS | Identify file type and architecture without execution | `Proposed-unobserved` |
| `SR-COL-05` | `/usr/bin/otool` | `root:wheel`; `0755`; regular file | `UNOBSERVED` | Apple Command Line Tools | Display load commands and linked-library identities for explicitly listed Mach-O objects | `Proposed-unobserved` |
| `SR-COL-06` | `/usr/bin/nm` | `root:wheel`; `0755`; regular file | `UNOBSERVED` | Apple Command Line Tools | Confirm only explicitly listed exported or imported symbols | `Proposed-unobserved` |
| `SR-COL-07` | `/usr/bin/sw_vers` | `root:wheel`; `0755`; regular file | `UNOBSERVED` | Apple macOS | Record operating-system product name, version, and build once | `Proposed-unobserved` |
| `SR-COL-08` | `/usr/bin/uname` | `root:wheel`; `0755`; regular file | `UNOBSERVED` | Apple macOS | Record kernel release and machine architecture once | `Proposed-unobserved` |

The bootstrap question—how `SR-COL-01` through `SR-COL-08` are authenticated before first use—remains `Blocked`. A later authorization must choose one reviewed bootstrap method; this manifest does not choose one.

## Route A — in-process platform API identities

### Provider and header identities

| ID | Exact path | Required permissions | Required SHA-256 | Provenance | Status |
|---|---|---|---|---|---|
| `SR-A-PRV-01` | `/usr/lib/libSystem.B.dylib` | Apple sealed-system library identity; no writable component | `UNOBSERVED`; dyld shared-cache identity and code-directory hash also required if no standalone bytes exist | Apple macOS libSystem | `Proposed-unobserved` |
| `SR-A-HDR-01` | `/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/sys/acl.h` | Resolved SDK regular file; `root:wheel`; `0644` or stricter | `UNOBSERVED` | Apple Command Line Tools SDK | `Proposed-unobserved` |
| `SR-A-HDR-02` | `/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/sys/mount.h` | Resolved SDK regular file; `root:wheel`; `0644` or stricter | `UNOBSERVED` | Apple Command Line Tools SDK | `Proposed-unobserved` |
| `SR-A-HDR-03` | `/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/sys/stat.h` | Resolved SDK regular file; `root:wheel`; `0644` or stricter | `UNOBSERVED` | Apple Command Line Tools SDK | `Proposed-unobserved` |
| `SR-A-HDR-04` | `/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/sys/fcntl.h` | Resolved SDK regular file; `root:wheel`; `0644` or stricter | `UNOBSERVED` | Apple Command Line Tools SDK | `Proposed-unobserved` |

If the literal SDK entry point resolves elsewhere, the exact resolved path must be added through review. Silent use of an Xcode SDK, another SDK version, or a copied header is prohibited.

### Exact proposed API symbols

All symbols below are proposed evidence identities only. No symbol is callable under this manifest.

| ID | Exact symbol or constant | Provider/header | Sole proposed read-only role | Status |
|---|---|---|---|---|
| `SR-A-API-01` | `acl_get_fd_np` with `ACL_TYPE_EXTENDED` | libSystem / `sys/acl.h` | Obtain the extended ACL bound to an already open synthetic descriptor | `Proposed-unobserved` |
| `SR-A-API-02` | `acl_get_entry` with `ACL_FIRST_ENTRY` and `ACL_NEXT_ENTRY` | libSystem / `sys/acl.h` | Enumerate every ACL entry without mutation | `Proposed-unobserved` |
| `SR-A-API-03` | `acl_get_tag_type` | libSystem / `sys/acl.h` | Read allow/deny and principal-tag class | `Proposed-unobserved` |
| `SR-A-API-04` | `acl_get_qualifier` | libSystem / `sys/acl.h` | Read the entry qualifier for canonical evidence | `Proposed-unobserved` |
| `SR-A-API-05` | `acl_get_flagset_np` and `acl_get_flag_np` | libSystem / `sys/acl.h` | Enumerate inheritance and ACL-entry flags | `Proposed-unobserved` |
| `SR-A-API-06` | `acl_get_permset` and `acl_get_perm_np` | libSystem / `sys/acl.h` | Enumerate permissions without mutation | `Proposed-unobserved` |
| `SR-A-API-07` | `acl_free` | libSystem / `sys/acl.h` | Release only memory returned by accepted ACL calls | `Proposed-unobserved` |
| `SR-A-API-08` | `fstat` | libSystem / `sys/stat.h` | Bind type, device, inode, owner, mode, and link count to the open synthetic descriptor | `Proposed-unobserved` |
| `SR-A-API-09` | `fstatfs` | libSystem / `sys/mount.h` | Read descriptor-bound `statfs` mount fields | `Proposed-unobserved` |
| `SR-A-API-10` | `fcntl` with `F_GETPATH` only | libSystem / `sys/fcntl.h` | Recover the bounded descriptor path solely for cross-checking canonical evidence | `Proposed-unobserved` |

No ACL setter, `chmod`, `chown`, mount mutation, path-only ACL retrieval, undocumented syscall, or hard-coded ABI is nominated.

### Binding identity blocker

The accepted `/usr/bin/perl` runtime has no accepted mechanism for calling these C symbols. No FFI package, XS extension, dynamic-loader bridge, hard-coded syscall, generated binding, or native module is nominated. Route A therefore remains `Blocked` unless a later Proposed manifest names one exact already-present, dependency-free, documented binding and proves its static identity. No informal binding substitute is allowed.

## Route B — local verifier executable identities

No single conforming verifier executable has been identified. The following exact Apple paths are nominated only for static capability screening; they are not a composite verifier and may not be combined to evade the one-executable boundary.

| ID | Exact path | Required permissions | Required SHA-256 | Provenance | Sole proposed screening question | Status |
|---|---|---|---|---|---|---|
| `SR-B-EXE-01` | `/bin/ls` | `root:wheel`; `0755`; regular file | `UNOBSERVED` | Apple macOS | Whether bounded ACL output is complete, canonical, locale-independent, and object-bound | `Proposed-unobserved`; not approved |
| `SR-B-EXE-02` | `/usr/bin/stat` | `root:wheel`; `0755`; regular file | `UNOBSERVED` | Apple macOS | Whether one bounded operation exposes mount-instance identity stronger than device equality and remains descriptor-bound | `Proposed-unobserved`; not approved |
| `SR-B-EXE-03` | `/sbin/mount` | `root:wheel`; `0755`; regular file | `UNOBSERVED` | Apple macOS | Whether mount-table output is complete, canonical, side-effect-free, and bindable to the exact object | `Proposed-unobserved`; not approved |
| `SR-B-EXE-04` | `/bin/df` | `root:wheel`; `0755`; regular file | `UNOBSERVED` | Apple macOS | Whether bounded filesystem output distinguishes same-device mount aliases and closes replacement races | `Proposed-unobserved`; not approved |

The proposed later operation for each screening candidate is read-only help/man-page and static binary inspection first; synthetic invocation would require another authorization with one literal argv per candidate. No argv is approved here. If no one executable independently provides complete ACL and mount-instance evidence with object binding, Route B must be marked `Fail`; multiple executables, parsing their combined output, or introducing an unlisted executable requires a new proposal.

## Route C — native helper identities

### Future project paths

| ID | Exact path | Required permissions | Required SHA-256 | Provenance | Sole proposed role | Status |
|---|---|---|---|---|---|---|
| `SR-C-SRC-01` | `/Users/bogac/dev/forgejo/mneme/tools/handoff/native/mneme_handoff_security_verify.c` | Tracked regular file; `0644` | Not applicable until separately authorized creation; then mandatory | Project-owned source derived only from accepted API contracts | Minimal helper source | `Not created` |
| `SR-C-BIN-01` | `/Users/bogac/dev/forgejo/mneme/.mneme-local/bin/mneme-handoff-security-verify` | Owner-only regular file; `0700`; parent `0700` | Not applicable until two separately authorized reproducible builds agree; then mandatory | Deterministic output of the frozen source and toolchain | One-shot synthetic ACL/mount evidence emitter | `Not created` |

The ignored owner-only path may hold only the derived helper binary after explicit authorization. It may never conceal source, manifests, test definitions, findings, or project changes; all of those must remain tracked.

### Proposed toolchain identities

| ID | Exact path | Required permissions | Required SHA-256 | Provenance | Sole proposed operation | Status |
|---|---|---|---|---|---|---|
| `SR-C-TC-01` | `/usr/bin/clang` | `root:wheel`; `0755`; regular file | `UNOBSERVED` | Apple Command Line Tools dispatcher or compiler; exact behavior must be resolved | Compile the one frozen C source with one literal argument array | `Proposed-unobserved` |
| `SR-C-TC-02` | `/usr/bin/ld` | `root:wheel`; `0755`; regular file | `UNOBSERVED` | Apple Command Line Tools linker | Link only the one frozen helper with Apple system libraries | `Proposed-unobserved` |
| `SR-C-TC-03` | `/usr/bin/codesign` | `root:wheel`; `0755`; regular file | `UNOBSERVED` | Apple macOS | Inspect signing; signing itself is not nominated or authorized | `Proposed-unobserved` |
| `SR-C-SDK-01` | `/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk` | Exact resolved SDK tree; no writable component | Tree manifest and per-input SHA-256 values `UNOBSERVED` | Apple Command Line Tools SDK | Supply only the four headers and system-library metadata named for Route A | `Proposed-unobserved` |

Route C proposes the same API symbols `SR-A-API-01` through `SR-A-API-10`; it adds no API. Compiler-driver expansion, implicit linker inputs, SDK resolution, and every generated artifact must be captured before a build can be proposed. If `/usr/bin/clang` is a dispatcher or requires an unlisted tool, the route stops until every transitive identity is added by review.

## Route D — attestation or continued-disablement identities

Route D has two mutually exclusive evaluation branches. `D1` evaluates a strong offline attestation verifier. `D2` preserves continued disablement and has no executable or API identity.

### D1 proposed verifier and data identities

| ID | Exact path | Required permissions | Required SHA-256 | Provenance | Sole proposed role | Status |
|---|---|---|---|---|---|---|
| `SR-D-EXE-01` | `/usr/bin/openssl` | `root:wheel`; `0755`; regular file | `UNOBSERVED` | Apple macOS cryptographic executable; exact implementation and license must be recorded | Offline verification of one frozen synthetic detached signature; no key generation or network | `Proposed-unobserved`; not approved |
| `SR-D-SCHEMA-01` | `/Users/bogac/dev/forgejo/mneme/tools/handoff/security/attestation-schema.json` | Tracked regular file; `0644` | Not applicable until separately authorized creation; then mandatory | Project-owned canonical schema | Define signed object, ACL, mount, policy, issue-time, expiry, and nonce fields | `Not created` |
| `SR-D-KEY-01` | `/Users/bogac/dev/forgejo/mneme/tools/handoff/security/synthetic-route-d-public-key.pem` | Tracked synthetic public key only; `0644` | Not applicable until separately authorized creation; then mandatory | Disposable synthetic test trust root; no private key in repository | Verify synthetic attestations only | `Not created` |
| `SR-D-FIX-01` | `/private/tmp/mneme-handoff-route-d-evidence-<authorization-id>/` | Fresh owner-only directory; `0700`; files `0600` | Per-file manifest required after authorized creation | Disposable synthetic-only evidence root | Hold synthetic attestations, signatures, and outputs for one authorized run | `Not created` |

No real host attestation, real signing key, credential, Keychain identity, production trust root, packet-store record, or operational authorization is nominated. The future private synthetic key, if separately authorized, must remain only in the exact disposable root and must be destroyed under reviewed rollback after evidence preservation.

### D2 continued disablement

`D2` requires no executable, API, key, schema, service, or packet store. Its exact operation is the absence of operational handoff use. Selecting continued disablement would still require an explicit user decision; this manifest does not select it.

## Proposed operations register

The table records the only operation classes that a later authorization may instantiate. It is not an active allowlist.

| Operation ID | Candidate identities | Proposed future scope | Explicitly excluded |
|---|---|---|---|
| `SR-OP-01` | `SR-COL-01` through `SR-COL-08` | One identity-only collection over the literal paths in this manifest | Candidate execution, network, writes outside a fresh evidence root, discovery, fallback |
| `SR-OP-02` | `SR-A-API-01` through `SR-A-API-10` | Calls against already open synthetic fixture descriptors only | Real repository objects, path-only ACL calls, mutation, installation, FFI acquisition |
| `SR-OP-03` | One of `SR-B-EXE-01` through `SR-B-EXE-04` | One literal read-only synthetic screening invocation after static review | Combining candidates, shell, PATH lookup, helper/configuration discovery, real paths |
| `SR-OP-04` | `SR-C-TC-01` and transitive accepted toolchain only | Two isolated reproducible builds of one frozen source after separate build approval | Installation, package acquisition, undeclared tools, real data |
| `SR-OP-05` | `SR-C-BIN-01` | One-shot read-only execution against synthetic descriptors after build acceptance | Packet operations, service mode, watcher mode, real paths, network |
| `SR-OP-06` | `SR-D-EXE-01` | Offline verification of frozen synthetic attestations and signatures | Key generation, Keychain access, real attestations, network, operational authorization |

Every row remains `Proposed`. A later authorization must replace the operation class with literal argv or exact function-call contracts, a fixed empty environment, input/output paths, byte and time caps, expected exit/error states, and a unique rollback boundary.

## Synthetic-only scope

Any later evaluation must use only deliberately synthetic objects under one fresh authorization-specific root beneath `/private/tmp`. It may model:

- no ACL, allow, deny, inherited, unknown, unreadable, reordered, oversized, and changing ACL states;
- ordinary directories, true mount points, same-device alias models, differing mount identities, and mount-change races;
- descriptor/path replacement, symlink, hard-link, wrong-owner, wrong-mode, and unsupported-host cases;
- malformed, contradictory, duplicate, truncated, localized, and oversized command or helper output;
- signed, unsigned, stale, expired, replayed, revoked, wrong-key, and substituted synthetic attestations; and
- interruption, timeout, uncertain completion, and rollback evidence.

It must not read or write the live repository beyond the separately reviewed source diff, create `.mneme-local/handoffs/v1`, consume a packet, access correspondence, use a real account, use a real credential or key, contact a network endpoint, or exercise an operational path.

## Rollback boundary

Planning rollback is deletion of the uncommitted manifest only. No other artifact is created by this proposal.

A later evidence-collection or synthetic-run authorization must define rollback before execution:

1. stop on the first deviation without retry or substitution;
2. preserve documentation evidence and uncertainty records;
3. revoke the affected proposed identity;
4. remove only the exact disposable synthetic root or derived helper path named by that authorization;
5. never delete, rewrite, or clean the append-only handoff history;
6. never create or remove the packet store as part of route rollback; and
7. return the repository to the exact pre-run tracked state, with any inability recorded as `Incomplete`.

## Specialist review requirements

All reviewers must review the same byte-identical manifest and later evidence object.

| Specialist | Required findings before identity collection can be proposed |
|---|---|
| Security/privacy | API and executable least privilege; ACL completeness; descriptor binding; mount-alias semantics; code-signing and bootstrap trust; no network, credential, or real-data path |
| Operations/recovery | Exact ownership and modes; update drift; binary replacement; temporary-root isolation; interruption; cleanup; compromise recovery; continued-disablement behavior |
| Quality/independent verification | Completeness of hashes and provenance; reproducible identity collection; literal operation contracts; parser/schema closure; synthetic test traceability; independent rebuild where applicable |
| Governance | No route selection; empty current allowlist; separate collection, execution, selection, implementation, packet-store, and operational gates; explicit disposition of every `UNOBSERVED` and blocker |

Each review must record `Pass`, `Fail`, or `Unproved`, evidence hashes, disagreements, residual uncertainty, and an acceptance condition. Silence, majority vote, or review of different bytes cannot close `SR-G10`.

## Stop conditions

Stop without retry, substitution, or broader inspection if:

- any literal path is absent, resolves elsewhere, is not a regular file where required, or has unexpected owner, group, mode, link count, bytes, hash, signature, or provenance;
- a hash remains `UNOBSERVED` when invocation is requested;
- the bootstrap trust for an identity-collection tool is unresolved;
- an executable is a dispatcher, loads an unlisted helper, plug-in, configuration, localization source, pager, SDK, library, or runtime;
- an API symbol, constant, layout, ownership rule, or error contract is undocumented or differs from the frozen header/provider;
- the runtime needs FFI, XS, a native extension, a downloaded module, a package manager, or an undocumented ABI;
- a Route-B candidate requires another executable or cannot independently provide complete ACL and mount-instance evidence;
- the compiler expands to an unlisted tool or SDK input, or reproducible outputs differ;
- an attestation verifier requires a real key, Keychain, service, network, mutable trust root, or real host attestation;
- an operation touches a real repository object for security evidence, correspondence, account, credential, packet, packet store, watcher, service, or operational path;
- a candidate mutates ACLs, mounts, files, configuration, logs, caches, or external state; or
- any requested identity or operation is not literally present in an Accepted manifest and separately Accepted execution authorization.

## Acceptance and later authorization gates

Acceptance of this manifest freezes only the candidate identity list and its blockers. It does not activate an identity, command, API, hash tool, helper, compiler, SDK, verifier, fixture, or operation.

The next permissible step after manifest acceptance would be a separate `Proposed` identity-collection authorization request. That request must:

1. resolve the bootstrap trust method;
2. name the exact subset of identities to inspect;
3. give literal commands or API calls and a fixed environment;
4. define output files, byte/time limits, and an owner-only synthetic evidence root;
5. prohibit all candidate execution not essential to identity collection;
6. define rollback and stop conditions; and
7. require the four specialist reviews before execution.

Route evidence, scoring, selection, implementation, packet-store creation, and operational use remain later independent user gates.

## Review request

Review whether this manifest:

1. identifies every executable, API, provider, header, toolchain, helper, verifier, schema, and trust-root path needed to evaluate all four routes;
2. keeps every current command and API invocation unauthorized;
3. distinguishes accepted prior identities from unobserved or nonexistent candidates;
4. makes hashes, permissions, provenance, allowed operations, synthetic scope, rollback, and specialist reviews explicit;
5. records Route A's binding blocker and Route B's lack of a conforming single executable without selecting a route; and
6. preserves ADR-007 as `Proposed`, the packet-store block, and the operational-use block.
