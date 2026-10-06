# Mneme roadmap and review checkpoints

**Prepared:** 2026-10-06, against code at `47a7f19`.
**Status:** Proposed implementation sequence following the requested project review.
**Current checkpoint:** R0 review and workflow revision complete. M1 implementation has not started.
**Companion:** [Project status](PROJECT-STATUS.md) records progress and evidence.

The aim is a private research archive that the user can actually operate.
A working synthetic archive comes first, followed by reliable lifecycle behavior,
a supported product boundary, a usable interface, and a small approved real-data
pilot. AI Ask and private remote access follow reliable deterministic retrieval.

## Milestones and where to request a deep review

| Work | Observable outcome | Stop and request this review |
|---|---|---|
| R0 — current review | Current state, concrete findings, workable instructions, and an ordered roadmap | Review this proposed direction before starting M1 |
| M1 — one local synthetic prototype | One command surface and shared implementation for the existing features; one repeatable demo and test entry point | **R1:** Does consolidation preserve behavior and close the identified correctness gaps? |
| M2 — archive lifecycle and recovery | Safe repeated updates, rebuild when derived data is absent, rule upgrades, writer coordination, and tested recovery | **R2:** Can this archive grow and recover without losing evidence? |
| M3 — realistic synthetic workload and product decisions | Bounded larger-corpus evidence, enforceable parser boundary proposal, concrete UI workflow, and focused runtime/storage/UI decision | **R3:** Approve the product architecture and selected dependencies before committing to them |
| M4 — usable private alpha, still synthetic | A coherent user-facing research workflow on the approved stack, with tested isolation and backup/restore | **R4:** Is the system ready for a narrowly scoped real-data pilot? |
| M5 — explicitly approved real-data pilot | Preserve and research the approved slice locally, verify recovery, record actual operator experience | **R5:** Expand, correct, or stop based on real evidence |

These are outcomes, not a fixed calendar. Each later review can narrow or reorder
the remaining work. Implementation approval covers internal iterations through
the named milestone; it does not require approval for every file, test, or commit.
The user may authorize several named milestones together, but the R3 architecture
decision and R4 real-data boundary still require their specific decisions.

## M1 — consolidate and correct

**Entry:** User asks to implement M1 (for example `/mneme-work M1`).
**Boundary:** Existing local Python/standard-library experiments, synthetic data,
no new runtime/dependency, service, AI, provider integration, or product-stack
selection. Fix in-scope defects discovered by review without separate proposals.

**Implementation shape:** Create one maintained `mneme/` Python package and
`tests/` entry point, usable from the checkout with `python3 -B -m mneme`.
These paths are planned, not present at this review. Keep the historical
`experiments/` in place as reference implementations; the maintained package
must not dynamically import them or mutate their fixture allowlists.
Move/copy behavior deliberately into ordinary shared modules with source
attribution and compatibility tests. A database, web framework, and plugin
system are not needed for this milestone.

**Complete when:**

- A documented command generates a fictional mixed EML/MBOX demo, ingests it,
  finds/filters results, shows cited source, lists identities/threads, checks
  staleness, exports/restores, and verifies results in a disposable workspace.
  No manual source-file editing or eleven different entry points is required.
- One fixture registry covers the existing EML, MBOX, and thread fixtures.
  Non-fixture input remains rejected; no global allowlist bypass is introduced.
- One test command runs the maintained tests; the historical 127-test Python
  baseline is run for compatibility at completion. Keep expected source bytes,
  occurrence IDs, existing citations, and unaffected Find results stable.
- Fix the concrete correctness issues assigned to M1 by the R0 report, with
  independent expected values and negative tests. At minimum cover conflicting
  reply evidence, all affected read paths, export verification, and boundary
  dates. A shared helper must not be both the implementation and its sole oracle.
- In particular, close F01/F02 before accepting publication: an interruption
  after CURRENT replacement cannot delete its target, and an owned temporary
  pointer left by a crash can be recovered safely. Close F03 by allowing intact
  supported sources to be exported/restored despite stale derived data. These
  fixes cannot be deferred to M2.
- Expose remaining staleness and rebuild limitations accurately. Rule-only
  generation publication and general recovery from absent derived data are M2;
  M1 does not silently publish a new generation convention or relax preservation.
- All evidence extraction used by the new read paths has a clearly described
  trust boundary. Fix accidental integration bypasses; retain an explicit
  synthetic-only restriction until M3/M4 establish stronger containment.
- An internal reviewer checks preservation, integration, citations, and recovery
  semantics; material findings are fixed. Results record exact code state,
  runtimes, commands, passing/failing checks, and known limits.

Use three internal checkpoints without additional user gates: storage and
validation corrections; shared-package extraction and retrieval corrections;
then the end-to-end demo, regressions, and review. Preserve old source/citation
contracts. Any required derived-evidence change gets an explicit experimental
rule/version and compatibility explanation, not an unexplained new hash.

**R1 review:** Review the full maintained implementation and changed contracts,
not just the last commit. Run the demo from documented instructions, challenge
source/citation equivalence and fixture scope, and check that the next work is
archive lifecycle rather than more isolated features.

## M2 — maintain an archive over time

**Entry:** R1 findings addressed and user authorizes M2.
**Boundary:** Synthetic-only. An experimental generation evolution is part of
this milestone; preserve old bytes and prove compatibility on copied fixtures.
A durable production storage contract still requires R3.

**Complete when:**

- Source verification is independent of derived verification. Delete or corrupt
  derived files in a disposable copy, rebuild from verified source and rules,
  publish the replacement, and recover the same research results.
- Source acquisition history and derived-generation history are distinct.
  A rule-only rebuild does not invent a new ingest event or rewrite source
  provenance; old processing identities remain inspectable.
- Stale and corrupt state are visible consistently across Find, filtering,
  identities, threads, show, export, and restore. Source corruption stops use.
  Missing derived data remains recoverable rather than making the source unreadable.
- A second writer is refused or coordinated, readers observe one coherent
  generation, and recovery cannot remove an active writer's stage.
- Fault injection covers before and after stage publication and current-pointer
  replacement, including first ingest and restart. Distinguish process-crash
  evidence from power-loss guarantees.
- Preserve verified container reconstruction and occurrence identity through
  append/repeat imports. Define explicit safe rejection of rewrites/renames
  until a replacement convention is approved; no silent reinterpretation.
- Old-format read/restore behavior has tests. Experimental migrations use a new
  destination and preserve the original, with citations remaining resolvable.
- Exports include the data needed for continued ingest and rebuild after restore.
  Record an integrity digest separately in the synthetic recovery exercise;
  hashes stored beside the data are not independent tamper evidence.

**R2 review:** Trace a source occurrence through ingest, failure, recovery, rule
upgrade, export, restore, and citation resolution. Try conflicting writers and
missing derived state. Assess the experimental source/container and generation
models before treating them as durable.

## M3 — realistic synthetic evidence and product decisions

**Entry:** R2 completed and M3 authorized.
**Complete when:**

- Deterministically generated, explicitly fictional workloads cover more than
  the current fixture set, multiple container shapes, larger individual inputs,
  and more than 999 occurrences. Define bounded runtime/disk limits before a
  run; record actual size, workload, ingestion/rebuild time, query latency, and
  memory/storage growth. Do not require a huge benchmark as an approval ceremony.
- Tests measure the cost of full copies/scans and repeated text in the index.
  Select the smallest needed performance improvement from measured evidence.
- Decide how stable package, container-version, occurrence, and citation
  identifiers survive growth and supported source changes. Preserve old
  identifiers/citations or provide an explicit compatibility path.
- Inventory every source parsing route, including show and reply headers.
  Demonstrate or design an enforceable filesystem/network/resource boundary,
  bounded non-executable worker output, and failure when required controls are
  unavailable. A spawned Python process alone is not a sandbox.
- Produce a concrete walkthrough of import progress, search/filter, source
  inspection, conversation/identity uncertainty, quarantine, stale-state
  recovery, and backup status for Mac and iPhone/iPad layouts.
- Make a focused runtime/storage/UI/deployment proposal based on these results,
  maintainability and support, rather than restarting every historical candidate
  dossier. Keep replacement/export paths and the Phase-1 criteria visible.
  Unproved safeguards stay unproved; narrow the proposed stage instead of
  treating missing evidence as a pass.

**R3 review and decision:** Review the whole design, workload evidence, security
boundary, user workflow, maintenance burden, and proposed dependencies. The
review recommends a choice; the user approves a product stack and any acquisitions.
Python's experimental success is evidence, not automatic production selection.

## M4 — usable private alpha

**Entry:** R3 decisions and M4 implementation explicitly authorized.
Build the selected user-facing workflow over the shared archive engine.
Keep all inputs fictional until R4.

**Complete when:**

- The user can complete the import-to-source-research workflow without agent
  assistance, including warnings, failures, and recovery.
- Find remains usable independently of AI. Source views are inert; addresses,
  inferred threads, and uncertain dates are labeled as evidence/interpretation.
- The approved runtime and parser controls are tested on the intended platform,
  including network denial, archive-write denial, output/time/memory limits,
  hostile headers/attachments, and compromise-oriented failure tests.
- Backup scope, independent integrity checking, protected copies, retention,
  clean restore, key-recovery needs, and basic maintenance are tested with
  synthetic data. Export alone does not meet all backup obligations.
- Review accessibility, responsive layouts, installation/update steps, and
  measured performance. Remote/mobile service operation requires explicit
  authorization; responsive design work alone does not expose a service.

**R4 readiness review:** Map the applicable Phase-1 preservation/security tests
to current evidence. Document any explicit user-approved deferrals. Specify a
small source, exclusions, local storage/backup boundary, cleanup, success
criteria, and stop conditions under ADR-006. The user separately authorizes the
real-data slice; a successful review does not itself permit reading it.

## M5 — small real-data pilot

Only the named, approved source slice may be used. Preserve before parsing,
verify hashes and package completeness, inspect quarantine and citations, test
restoration, and record usability/coverage failures without publishing private
content. Do not automatically expand to the full archive or a provider account.

**R5 review:** Decide whether the archive is trustworthy and useful enough to
expand. Subsequent work may add corpus adapters, annotations, cross-device access,
or AI Ask; each gets its own bounded milestone. AI requires source-grounded
evaluations, prompt-injection tests, explicit routing/privacy/cost decisions,
and separate approval for any model or external transfer.

## Repeat this review

At R1–R5, ask in Codex or another independent agent:

> Read AGENTS.md, docs/PROJECT-STATUS.md, docs/ROADMAP.md and the previous report.
> Perform the deep review for R<number> against the exact current code, working
> diff, test evidence, product goals, and that checkpoint's completion criteria.
> Reproduce high-impact findings with synthetic inputs, distinguish historical
> evidence from checks run now, and assess whether the next milestone is right.
> Record prioritized findings and their disposition in docs/reviews/. Do not
> implement product fixes, mark user acceptance, commit, push, or begin the next
> milestone as part of the review.

Use `/mneme-review R1` in Claude for the same review procedure. When a separate
session/model is used, say so; reusing the implementer's context is self-review.

One report contains: reviewed commit/diff, scope and exclusions, requirement
coverage, prioritized findings with source locations and reproductions, tests
actually run, remaining limits, and a recommendation to continue/correct/hold.
Separate facts from hypotheses. Check progress toward a usable product and
whether any workstream has become disproportionate.

Request an earlier deep review only for a discovered source-loss/exposure risk,
a proposed change to a durable contract or trust boundary, or a blocker that
invalidates the milestone. Ordinary bugs are fixed internally; routine commits
do not trigger additional user reviews.
