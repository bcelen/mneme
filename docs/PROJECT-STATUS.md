# Mneme project status

**Snapshot:** 2026-10-06.
**Reviewed code:** `47a7f1965bdf5fa589674b2fc1428a7ab748ad25` on local `main`.
Before publishing this review package, local `main`, Forgejo `main`, and GitHub
`main` were checked directly and all matched that reviewed code commit.

**Current checkpoint:** R0 project review and agent/workflow revision complete.
The user authorized committing and publishing this documentation/workflow package
to Forgejo and GitHub on 2026-10-06. This does not start M1 implementation.
**Next:** M1 consolidation and correctness fixes, awaiting an implementation
instruction. No product code was changed during R0.
**Latest review:** [2026-10-06 project review](reviews/2026-10-06-project-review.md).
**Scope and review points:** [ROADMAP.md](ROADMAP.md).

## What works, and how far the claims go

| Area | Existing evidence | Important boundary |
|---|---|---|
| Preservation and parsing | Fictional EML bytes, hashes, provenance, quarantine, parser process/resource tests | Process separation is not a complete security sandbox |
| Incremental archive | Stable occurrences, idempotency, staged generations, deterministic rebuild comparisons | Crash-window defects; no writer coordination; rebuild is not general recovery |
| MBOX | LF mboxrd segments and byte-exact container reconstruction | Filename/offset keys; rewrites rejected; other dialects/provider packages unproved |
| Retrieval | Deterministic Find/filtering and source-bound display | Extreme dates, address syntax, and semantic index validation need correction |
| Identities and threads | Address evidence and header-derived thread views | No people model; relationship diagnostics/evidence and graph bounds need work |
| Staleness and export | Rule comparison, side rebuild, generations exported/restored | Stale caches can block restore; missing-rule/manifest validation defects |
| Product | Several separate CLIs | No unified UI, operational backup, deployment, AI, real-data pilot, or selected production stack |

The baseline is valuable experimental evidence, not readiness for personal mail.
The review assigns **14 reproduced defects/validation gaps** to M1 and broader
lifecycle/security/product gaps to later milestones. Keep experiments as reference
evidence; do not hide failing edge cases behind the passing baseline.

## Python regression inventory

Run each file as `PYTHONDONTWRITEBYTECODE=1 <installed-python> -B <path>`
from the repository root. macOS baseline uses `/usr/bin/python3` (3.9.6).
Run sequentially when resource-limit tests are involved. M1 will add one maintained
test entry point; the table also remains the reference compatibility inventory.

| Suite | File | Tests |
|---|---|---:|
| Vertical slice | `experiments/vertical-slice-1/tests/test_vertical_slice.py` | 10 |
| Hardening | `experiments/synthetic-hardening-1/tests/test_hardening.py` | 16 |
| Isolation | `experiments/synthetic-hardening-1/tests/test_isolation.py` | 6 |
| Prototype 1 | `experiments/mneme-local-prototype-1/tests/test_mneme.py` | 5 |
| Incremental EML | `experiments/mneme-local-prototype-2/tests/test_incremental.py` | 16 |
| MBOX | `experiments/mneme-local-prototype-3/tests/test_mbox.py` | 22 |
| Filters | `experiments/mneme-local-prototype-4/tests/test_filters.py` | 14 |
| Export/restore | `experiments/mneme-local-export-1/tests/test_export.py` | 13 |
| Staleness | `experiments/mneme-local-staleness-1/tests/test_staleness.py` | 8 |
| Identities | `experiments/mneme-local-identities-1/tests/test_identities.py` | 7 |
| Threads | `experiments/mneme-local-threads-1/tests/test_threads.py` | 10 |
| **Total** | **11 separately executable suites** | **127** |

**R0 fresh execution:** All **127 tests across 11 suites passed** on this Mac with
CPython 3.9.6 on 2026-10-06. Every suite exited 0; code remained at the reviewed
commit. Historical Linux results remain in experiment records and were not rerun
here. New synthetic diagnostics are reported separately; a green baseline does
not cover an edge case absent from its tests.

## Deferred work and evidence interpretation

- Handoff automation remains disabled. Its historical 38-case Perl result does
  not authorize operational use, and its suite is not part of the Python baseline.
- The Go checksum/planner and candidate-acquisition route remains paused.
  [The correction record](SYNTHETIC-HARDENING-EXPERIMENT-RESULTS.md) records a
  successful offline Go 1.27.1 run on 2026-09-20. Later feature reports say Go was
  not run in those sessions. Neither statement means the current Go suite was
  executed in R0; it was not, and it does not block M1.
- Phase-1 requirements and accepted ADR-001–006 remain binding. Phase-2's
  no-selection finding remains historical evidence; no product stack is selected.
- Some historical results still say "uncommitted" or "awaiting review" although
  their code is now on main. Use the recorded commit and this status page for
  current position; preserve historical results rather than silently rewriting
  their test claims.
- `Claude outputs/` is existing untracked material, excluded from this review and
  any future task commit unless the user explicitly includes it.

## Maintaining this page

At a checkpoint record the milestone, current code commit (plus relevant working
diff), completed/in-progress work, checks actually run, unresolved findings, and
next review ID. Link one evidence/report file rather than duplicating it here.
An agent may record technical completion or readiness for review; user acceptance
and push/merge permission need an attributable user instruction.

Review schedule: **R1** integrated prototype; **R2** lifecycle/recovery;
**R3** architecture choice; **R4** before real-data use; **R5** pilot results.
The roadmap contains the reusable independent-review request.
