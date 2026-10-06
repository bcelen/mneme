---
description: Deep-review a Mneme milestone and its next step
argument-hint: "[review checkpoint, e.g. R1; optional focus]"
disable-model-invocation: true
---

Perform the deep review requested in: $ARGUMENTS

Read AGENTS.md, docs/PROJECT-STATUS.md, docs/ROADMAP.md and the previous review.
If no checkpoint is named, review the current completed milestone or current
project state; do not invent completion.

Inspect the exact commit, branch, working diff including relevant untracked
files, and applicable instructions. Record that review object. Review actual
code and tests alongside the report, not just the implementer's summary.
Do not inspect unrelated private files or real correspondence.

Evaluate:
- preservation and source/container/occurrence identities;
- independent integrity, provenance, citation binding and inert source display;
- transactions, interrupted updates, staleness, rebuild, export and restore;
- parser entry points, privilege/resource boundaries and hostile input;
- integration, compatibility, test oracles, portability and performance;
- product usefulness, maintenance cost and whether the roadmap needs narrowing;
- current versus historical instructions and evidence.

Delegate focused read-only reviews where useful and available. Reproduce material
findings with bounded synthetic diagnostics. Run appropriate installed-runtime
tests, record actual results, and avoid unrelated Go/handoff work or downloads.
Do not claim full assurance from a test count or from reviewing your own work.

Write one dated report in docs/reviews/ and link it from project status. Preserve
previous reports; distinguish a new revision from acceptance. Include reviewed
source state, scope, prioritized findings with exact locations and failure cases,
evidence actually collected, limitations, and a continue/correct/hold recommendation.
Assign each open issue a milestone or explain why it blocks progression.

This is a review: do not implement product fixes, mark a decision user-Accepted,
commit, push, merge, or start the next milestone. If the user also explicitly
requests documentation/roadmap changes, make those reviewable edits separately.
End with the next concrete user decision, if any, not another approval protocol.
