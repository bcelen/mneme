# Handoff Automation Security CS-0 System Hard-Link Compatibility Amendment

**Status:** Accepted

**Decision date:** 2026-09-19

**Review date:** 2026-09-19

**Authority:** One corrected CS-0 rerun and exact-root cleanup only

## Reason

The corrected CS-0 run reached the first non-candidate system-tool inspection and stopped because `/usr/bin/shasum` has two hard links. The accepted command required exactly one.

Multiple hard links are valid for a protected system file and do not change its bytes. The existing exact-path, physical-path, regular-file, non-symlink, root ownership, mode, and raw-byte SHA-256 controls provide the relevant identity evidence.

## Exact amendment

For the six declared non-candidate system-tool targets only, replace:

```perl
$s[3]==1 or die "TARGET_LINKS\n";
```

with:

```perl
$s[3]>=1 or die "TARGET_LINKS\n";
```

The observed link count remains recorded in each identity record.

This amendment does not change the one-link requirement for any CS-0-created canary, receipt, identity record, or manifest file.

## Unchanged controls

All other accepted controls and the GID compatibility amendment remain in force, including:

- exact direct argv with `shell=false`;
- exact literal and physical target paths;
- regular-file and final-component non-symlink checks;
- UID `0`, GID `0`, and mode `0755` for inspected system tools;
- raw-byte SHA-256 without executing a target;
- owner UID, restrictive modes, same-device, containment, exclusive-creation, sync, and one-link checks for CS-0-created objects;
- the exact synthetic canary and nine-member self-excluding manifest;
- no candidate path, network, email, account, real data, dependency, packet store, watcher, service, route selection, or operational handoff use; and
- exact-path, non-recursive cleanup after evidence capture.

## Authorization

This amendment authorizes one corrected CS-0 rerun. On success, capture the complete evidence, remove only the exact declared files and directories, verify the root is absent, and stop for review.

If any amended or unchanged check fails, stop without retry and clean up only the exact known CS-0 objects covered by the user's instruction.

## Acceptance record

Accepted on 2026-09-19 through the user's instruction to apply this narrow fix and rerun CS-0. No downstream unit or operational handoff use is authorized.
