# Mneme Local Staleness 1 — Results

**Status:** Successful within the declared local, offline, synthetic-only experimental scope; committed on a feature branch, awaiting review.
**Run date:** 2026-10-05.

## Runtime

- Linux container: CPython 3.11.15 and 3.10.20.
- macOS (reported 2026-10-06): passed on the accepted runtime, CPython 3.9.6 via `/usr/bin/python3 -B`, on commit `416be0c` fetched from GitHub into a local review branch: 8 tests in 33.5 s.
- Python standard library only; no network access.

## Verification

`tests/test_staleness.py`: 8 tests pass. Stale state is produced for real, by ingesting under an older MBOX rule identity (`synthetic-mboxrd-segmentation-v0`) and then examining it with the current code. Engine-rule and isolation-profile changes are simulated by changing the current value at check time.

The tests cover: a current state with no stale component and no stale records; an old MBOX rule reported with exactly the 12 MBOX records; an engine-rule change marking all 26 records stale; an isolation-profile change marking only records that were parsed in a worker; corrupt derived bytes reported as `corrupt` rather than `stale`; a rederive report that is complete, leaves the state untouched, and changes only `derived-manifest.json` and `messages.json`; and a rederive that is deterministic, publishes nothing on failure, and refuses an existing output. The strongest check: re-deriving the stale archive under the current rules reproduces, byte for byte, the derived state of the same archive ingested under those rules.

Five deliberate mutations were each caught and reverted: skipping the integrity check, disabling the Find guard, listing every record as stale, giving unparsed records an isolation profile, and skipping cleanup after a failed rederive. The third one initially survived because no test checked that non-stale components list no records; that assertion was added.

## CLI evidence

State: the 14 accepted EML fixtures, then `MBOX-001` and `MBOX-004` ingested under `synthetic-mboxrd-segmentation-v0`: `generation-0002`, 26 sources, derived tree `88c3fffb9ff89fb74901234868c47bee2c977cadc471c4fe468119ad909abcf1`.

| Command | Result |
|---|---|
| prototype 3 `find` | exit 2: `derived MBOX record has a stale or missing rule: EML-015` |
| `check` | exit 3; `stale`; only `mbox-rule` stale, recorded `synthetic-mboxrd-segmentation-v0`, 12 records |
| guarded `find` | exit 2: `derived state is stale (mbox-rule); run rederive and review the rebuild report` |
| `rederive` | exit 0; changed `derived-manifest.json`, `messages.json`; 7 members unchanged; 10 failures (quarantines); derived tree `833237ba60fcd80af9cfa2d0a3d1969fef49dec4ef3d40d789df11e4301dbc15`; report SHA-256 `413bf17249b972ec452653dc65249ffe7b864e4a0164ef5e473bb3d14e29a71e` |

## Limitations

- Re-derived state is not published into the state; that needs a reviewed generation-convention change.
- Only the four listed rule identities are compared. The index normalization text and the parser's internal behavior are not separately versioned; a behavior change without a rule-identity change cannot be detected.
- An engine-rule change cannot be simulated end to end in tests, because parsing runs in spawned workers that load the unmodified engine.
- Only the current generation is checked; earlier generations are retained as history and not re-derived.
