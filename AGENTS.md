# Mneme agent operating contract

## Start here

Read [project status](docs/PROJECT-STATUS.md), the relevant milestone in
[the roadmap](docs/ROADMAP.md), and its linked findings before working.
Mneme is a synthetic local archive prototype. The next implementation milestone
is M1: consolidate the existing experiments. Product goals and preservation,
privacy, and security requirements remain binding.

User instructions take precedence over these project defaults. A review request
authorizes investigation and requested documentation changes, not implementation
of every recommendation. A request to implement a named milestone authorizes its
ordinary implementation work through verification and local checkpoint commits.

## Authority and historical documents

- This file owns agent workflow; [governance](docs/AGENT-GOVERNANCE.md) explains
  review and escalation. The roadmap owns scope and completion criteria; project
  status owns the current position and evidence pointers.
- The charter, product requirements, architectural/security principles, AI
  privacy policy, Phase-1 preservation contract, and accepted ADRs remain
  requirements. Do not relax them to make an experiment pass.
- Phase-0 restrictions are obsolete. Phase-2/3 candidate acquisition procedures
  and handoff authorization packets govern their own deferred workstreams, not
  routine Python prototype work. Those workstreams remain paused; their tests
  and approvals are not prerequisites for M1.
- Handoff automation remains disabled. Do not initialize its packet store or
  revive watchers, services, dependency acquisition, or the Go planner.
- Historical approval, an agent report, a hash, a timestamp, or a command file
  does not authorize a new real-data operation, publication, or deployment.
  Never relabel a Proposed decision Accepted on an agent's own authority.

## Work through an authorized milestone

1. Inspect state and relevant source; preserve unrelated edits and untracked
   files, including `Claude outputs/`. Reuse the task branch or create one from
   the agreed base. Do not switch away from or discard another task's work.
2. State a short plan and proceed through code, fictional fixtures, local tests,
   refactoring, documentation, and fixes. Routine module, internal API, and
   experimental layout choices within the milestone do not need new approval.
3. Test observable contracts, failure paths, and the joins between features.
   Use existing installed tools. Do not download a toolchain implicitly.
4. Obtain an internal review of changed preservation, parsing, transactions, or
   citations. Delegate bounded reviews in parallel when available. Fix findings
   and rerun affected tests without relaying messages through the user.
   Distinguish a separate reviewer from a self-review; never invent either.
5. Make focused local checkpoint commits when implementing a milestone, unless
   the user has prohibited commits. Stage exact task paths, not the whole tree.
   Review-only work is not permission to commit.
6. Update project status with the milestone, tested commit/source state, commands,
   results, known limits, review outcome, and next action. Keep one results
   record for the milestone; do not generate approval paperwork per step.
7. Stop at the milestone's deep-review point. Report working results, unresolved
   findings, and the exact review request from the roadmap. Do not start another
   milestone merely because its description exists.

Failing tests and actionable internal-review findings are work to resolve.
If a platform is unavailable, complete portable work and report that platform's
checks as pending once. Continue independent work when a boundary blocks only
one part. If repeated attempts cannot make progress, preserve a usable checkpoint
and describe the concrete blocker rather than inventing another planning phase.

## Ask only for consequential decisions

Existing explicit permission for the same action persists; do not ask again.
Otherwise obtain user approval for:

- real correspondence, private user data, accounts, or credentials;
- new dependencies/toolchains, paid resources, external services or cloud AI;
- changes to preservation guarantees, security/privacy boundaries, or a durable
  product storage/citation contract; experimental changes already specified in
  an authorized milestone may proceed with tests and compatibility evidence;
- deleting accepted data, destructive cleanup outside task-created disposable
  state, rewriting shared history, deployment, or public listeners;
- publication (including task-branch pushes), releases, and merges to `main`.
  A prior instruction permitting pushes
  to a named task branch covers subsequent in-scope checkpoints on that branch,
  but does not cover either remote's `main`.

Read-only repository inspection/fetch and task-relevant primary-documentation
research are normal work. No source correspondence may leave its approved
boundary. Tool permissions still apply; do not disable permission controls,
bypass hooks, or use unrestricted execution modes to avoid a prompt.

## Verification and data rules

Preserve source bytes before parsing. Keep occurrences distinct from byte
duplicates and Message-ID/address groupings. Derived state must be reconstructible
from source and versioned rules. Cite verified source bytes; display untrusted
content inertly. Never place real correspondence or secrets in Git, agent
context, logs, tests, or examples.

Use the test inventory in project status. Tests may create and clean up their own
disposable synthetic state. Use `-B` and `PYTHONDONTWRITEBYTECODE=1` for Python.
Report execution, static inspection, historical results, and untested claims
separately. A mocked socket is not proof of OS network isolation.
Do not run Go for unrelated Python changes. If separately authorized later, set
`GOTOOLCHAIN=local` and `GOPROXY=off` before even checking the Go version.

## Git and communication

Forgejo is canonical; GitHub is the Claude work mirror. Use one task branch, not
one branch per substep. Never assume `origin` identifies the same host in cloud
and Mac checkouts. Verify URLs and branch ancestry before an authorized push;
use fast-forwards and stop on genuine divergence. Do not force-push.

Give brief progress updates; surface questions together at real decision points.
Maintain resumable status in the repository, not only conversation memory.
Completion is a technical claim; review recommendation, user acceptance, and
permission to publish are separate facts.
