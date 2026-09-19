# Handoff Automation Security CS-0 GID Compatibility Amendment

**Status:** Accepted

**Decision date:** 2026-09-19

**Review date:** 2026-09-19

**Authority:** One corrected CS-0 rerun and exact-root cleanup only

## Reason

The first CS-0 root-creation attempt stopped because macOS created the owner-only temporary directories with UID `501`, GID `0`, and mode `0700`, while the accepted command required the GID to equal the process effective group.

The GID difference does not grant group access: mode `0700` gives the group no permissions. Requiring a particular GID is therefore unnecessary for the declared single-user, owner-only boundary.

## Exact amendment

For CS-0-created directories and files only, replace checks of this form:

```perl
$s[4]==$> && $s[5]==$)
```

with:

```perl
$s[4]==$>
```

Equivalent checks using the root, fixture, or other local stat arrays receive the same substitution. The observed GID remains evidence but is not a pass/fail condition.

This applies only to:

- the CS-0 disposable root;
- its declared child directories;
- the synthetic canary;
- CS-0-created command receipts, identity records, and manifest; and
- exact-path cleanup of those objects.

The UID checks for system-owned parents and inspected non-candidate system tools remain unchanged: those paths must still be UID `0`, GID `0`, and mode `0755` where the accepted request requires it.

## Unchanged controls

All other accepted CS-0 controls remain in force:

- exact literal paths and direct argv with `shell=false`;
- accepted request SHA-256 `6876f4cdab8ab9a53a282ee492d0d87cd9c82be9e3afbe5583a2aa2c3d6b1672`;
- owner UID checks;
- directory mode `0700` and file mode `0600`;
- regular-file and directory type checks;
- final-component symlink rejection;
- physical containment and same-device checks;
- link-count, exclusive-creation, sync, byte-count, and SHA-256 checks;
- the exact synthetic canary and nine-member self-excluding manifest;
- the exact six non-candidate raw-byte inspection targets;
- no execution of an inspected target;
- no candidate path, network, email, account, real data, dependency, packet store, watcher, service, route selection, or operational handoff use; and
- exact-path, non-recursive cleanup after evidence capture.

## Authorization

This amendment authorizes one corrected CS-0 rerun. On success, capture the complete evidence in memory, remove only the exact declared files and directories, verify the root is absent, and stop for review.

If any amended or unchanged check fails, stop without retry. Clean up only the exact known CS-0 objects explicitly covered by the user's cleanup instruction; do not inspect or remove another path.

## Acceptance record

Accepted on 2026-09-19 through the user's instruction to apply this narrow fix. This amendment does not authorize PE-02 repetition, a downstream screening unit, route selection, packet-store creation, operational handoff use, or later work.
