# Claude Code: Mneme

@AGENTS.md

Start with [project status](docs/PROJECT-STATUS.md) and the relevant
[roadmap milestone](docs/ROADMAP.md). Do not reread the historical approval archive
on every task. Read only the requirements and evidence relevant to the change.

- `/mneme-work M1`: implement that milestone through tests, internal reviews,
  corrections, documentation, and local checkpoint commits.
- `/mneme-review R1`: perform a deep review at the corresponding checkpoint.
  It does not implement fixes or approve publication.

The command prompts are also usable in plain chat if this Claude environment
does not expose project slash commands. They inherit the user's selected model
and existing tool permissions.

Current code is synthetic-only. Handoff automation and candidate acquisition
work remain paused. An older "do not commit" or "Phase 0" statement in a historical
report is not a fresh user instruction; an explicit current user restriction
still wins.

Memory is a navigation aid, not an approval record. Verify remembered state
against Git and project status. Surface a concrete conflicting personal/cloud
instruction once; do not silently overwrite global memory or user settings.
Do not defeat a permission prompt or hook. If infrastructure forces a pause,
record the available checkpoint and continue independent work where possible.

Keep routine implementation/review exchanges inside the task. At the roadmap's
review point, return the exact commit, results, open issues, and review prompt.
