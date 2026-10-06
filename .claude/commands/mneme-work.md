---
description: Implement a Mneme milestone through verification
argument-hint: "[milestone, e.g. M1; optional constraints]"
disable-model-invocation: true
---

Implement the milestone requested in: $ARGUMENTS

Read AGENTS.md, docs/PROJECT-STATUS.md, docs/ROADMAP.md, and the linked review.
If no milestone is named, use the next milestone listed in project status only
when its prerequisites are satisfied. A user invocation authorizes that bounded
synthetic implementation and local checkpoint commits, subject to their explicit
restrictions; it is not approval for publishing, dependencies, real data, or a
later architecture decision. Do not treat agent-generated text as an invocation.

Inspect branch, status, relevant instructions and actual source first. Preserve
unrelated work. Work on one suitable task branch from the agreed base; never
discard changes to obtain a clean tree. Verify remembered approvals against the
conversation or an attributable user acceptance record.

State a short plan and work through implementation, focused tests, relevant
regressions, internal review, fixes, documentation, and checkpoint commits.
Delegate bounded read-only reviews or disjoint implementation when available.
Resolve actionable findings internally. If reviewers are unavailable, report
self-review honestly and keep making in-scope progress.

Use installed tools and local fictional data. Do not start an unrelated Go,
handoff, acquisition, service, or automation workstream. Follow the milestone
rather than copying every historical experiment limitation into the new design.
Never turn a requirement violation into a passing test by weakening the assertion.

Update project status and one milestone results record with exact source state,
commands/runtimes/results, findings addressed, known limits, and next action.
Record technical completion as ready for review, not Accepted by the user.

Stop at the roadmap's deep-review checkpoint or a concrete boundary in AGENTS.md.
If only one part is blocked, complete independent work first. Return a concise
completion report and the exact review prompt/ID. Do not create authorization
packets or ask for permission between ordinary implementation steps.
