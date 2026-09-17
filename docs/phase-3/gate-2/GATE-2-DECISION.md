# Gate-2 Safety-Baseline Decision

**Status:** Accepted
**Review date:** 2026-09-18
**Decision:** Gate 2 remains open and not passed.

## Finding

The repository is at the intended clean documentation-only starting point. The Gate-1 design is accepted and committed, useful future artifacts are visible to Git, the experiment tree does not exist, no proposed external runtime/dependency is present, and no external account, real data, production state, model service, or public endpoint has been used.

That evidence is necessary but not sufficient. Twelve controls remain Blocked because verifying them would require acquired artifacts or an empty runtime harness, both deliberately paused for this review. Thirteen more controls are Designed but have no enforcing implementation. Claiming a Gate-2 pass now would contradict the accepted rule that unexecuted evidence is not pass.

## Accepted conclusions preserved

- No stack has been selected.
- `EXP-C001` and `EXP-C003` remain comparison references only.
- The Phase-2 no-selection finding remains in force.
- Ubuntu, Docker, ZFS, and Tailscale remain provisional deployment context, not Phase-3 selections.
- The source archive remains byte-preserving and read-only; reversible derived state is separate.
- Sending email and source-system mutation remain out of scope.
- No real-data dry run is authorized.

## Actions still prohibited

Until this package is reviewed, do not:

- download or install Phase-3 dependencies;
- initialize or start Podman, PostgreSQL, a database, a candidate service, a listener, or a container;
- create `experiments/phase-3/`, fixture bytes, a synthetic release, generated manifests, credentials, keys, caches, SBOMs, or build outputs;
- add prototype, harness, generator, parser, renderer, schema, test, or infrastructure code;
- run an acceptance test, candidate behavior, fault injection, migration, rebuild, backup, restore, rendering, or citation/search experiment;
- access an account, inspect real correspondence, touch the live archive, call cloud AI, enable telemetry, deploy, expose a public service, send email, mutate source data, select a stack, create a stack-selection ADR, commit, or push.

## Review request

The user is asked to review:

1. the current evidence and `Verified`/`Designed`/`Blocked` calibration;
2. the exact allowlisted acquisition and integrity checkpoint;
3. the empty safety-harness checkpoint;
4. the continued pause before fixture generation and prototype work.

If approved, work proceeds only through Checkpoint A and returns with exact acquisition/integrity evidence before any build or service startup. Checkpoint B remains separately reviewable, preserving the user's instruction to see evidence before services start.

This decision record requests no permission to select a stack, create fixtures, build prototypes, run tests, access real data, or push.
