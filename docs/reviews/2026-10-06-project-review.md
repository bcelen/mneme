# Mneme project review — R0

**Date:** 2026-10-06.
**Reviewed code:** `47a7f1965bdf5fa589674b2fc1428a7ab748ad25`.
**Review status:** Completed analysis; proposed direction and workflow edits.
**Acceptance:** This report does not record user acceptance of M1 or authorize
product implementation, commits, pushes, real-data access, or deployment.
**Current position:** [PROJECT-STATUS.md](../PROJECT-STATUS.md).
**Disposition and review schedule:** [ROADMAP.md](../ROADMAP.md).

## Judgment

Continue the project through **one consolidated, corrected local synthetic
prototype**. The preservation and retrieval experiments demonstrate useful
behavior, but the project is neither an operational personal archive nor a
coherent application yet. Starting more detached feature experiments would add
integration cost faster than product value.

The earlier branch assessment established scope and reported test coverage; it
was not a substitute for this source-level review. This review found **14
reproduced defects or validation gaps**, including publication/recovery failures.
Passing the existing tests therefore supports the tested scenarios, not a claim
that archive integrity and recovery are complete.

The first implementation work should correct the publication failures and shared
validation, then consolidate the feature paths. Do not import personal mail yet.
There is no reason to resume the unrelated Go acquisition or handoff automation
work to make this progress.

## Scope and evidence

The main review inspected the charter, requirements, preservation/acceptance
contracts, active and historical governance, candidate/no-selection records,
prototype documentation, parser/isolation/display paths, test inventory, and
Git state. Two separate review agents inspected:

- preservation, incremental generations, MBOX, export/restore, and staleness;
- filtering, identity normalization, threading, citations, and test blind spots.

They performed bounded fresh diagnostics on fictional data and returned concrete
locations and failure cases. They did not modify repository source. The main
reviewer inspected the implicated code and independently reproduced the date
overflow and quoted-address omissions. The preservation reviewer also checked
the M1/M2 scope boundary; its two clarification requests were incorporated.
The general workflow revision was self-reviewed. A requested second workflow
pass did not complete and is not counted as independent verification.

No real correspondence, private archives, `Claude outputs/`, Go execution,
dependency installation, or handoff operation was involved. Temporary diagnostic
state was removed by its owning tests/review agents. The main test run used
CPython 3.9.6 via `/usr/bin/python3 -B` with bytecode disabled.

**Baseline execution:** All **127 existing Python tests in 11 suites passed**
on this Mac; each suite exited 0. Historical Linux results were read, not rerun
in this review. No assertion of OS network isolation is made: tests patching
sockets in a parent process do not prove network denial for spawned workers.

The checked local main and origin/main were equal. Live remote equality was not
rechecked; the user had reported both pushes complete.

## Reproduced findings: storage and preservation

Experiment paths below sometimes omit the common `experiments/` prefix;
line numbers refer to the reviewed commit. P1 means a high-impact issue in the existing
archive path. P2 means a significant defect or missing validation. They are not
claims of a production security exploit.

### F01 — P1: interruption after pointer publication deletes the new generation

At `experiments/mneme-local-prototype-3/mneme.py:861–869` (also prototype 2
at 563), the rollback target remains set while `_write_current()` publishes the
pointer. A `KeyboardInterrupt` immediately after that publication enters
`except BaseException` and deletes the generation now named by CURRENT.

**Fresh diagnostic:** Wrap the real pointer writer, call it, then raise
`KeyboardInterrupt` during the second ingest. Both prototypes ended with
CURRENT naming generation-0002 and that generation absent. P3 recovery failed.
The prior generation's source bytes survived; the claim is a broken published
state, not deletion of the entire archive.

**M1 correction:** Treat pointer replacement as the commit point. Cleanup must
never remove the referenced generation. Test both sides of the pointer change.

### F02 — P1: a crash inside the pointer writer prevents recovery

`synthetic-hardening-1/hardening.py:100` stages a sibling `.CURRENT.*`.
Prototype 3's `mneme.py:509` permits only CURRENT and generations at the root.

**Fresh diagnostic:** Terminate a disposable child immediately before the
pointer writer's `os.replace()`. The temporary pointer and unpublished
generation remain; both verify and recover refuse the root before cleanup.
Existing crash tests stop at whole-function boundaries and miss this window.

**M1 correction:** Recognize and validate owned pointer-write remnants, and
recover conservatively. Unknown extra entries must still fail closed.
Exercise process termination within publication steps, not only raised exceptions.

### F03 — P1: changing parser rules can make intact exports unrestorable

Prototype 3 `mneme.py:459–483,542–557` requires each retained generation's
derived records to match current rules. Export `mneme_export.py:212,262`
uses that verification before inspection/restore.

**Fresh diagnostic:** Create a valid synthetic archive/export, then change only
the in-memory MBOX rule identity. Staleness reports stale correctly, but export,
verify-export, and restore all reject intact bytes. Changing the segmenter itself
also affects preservation verification at prototype 3 `mneme.py:383`.

**M1 correction:** Separate source/format integrity from cache freshness.
Restore supported old data without asserting that its cache is current. Never
reinterpret old MBOX boundaries silently. **M2** adds rule-only generation
publication and full upgrade/recovery behavior.

### F04 — P2: output directories can overlap their input archive

Staleness `mneme_staleness.py:174` and export `mneme_export.py:133`
check that the output is new, not that the trees are disjoint.

**Fresh diagnostics:** `rederive(state, state/"rebuilt")` succeeds but makes the
archive root invalid. Export to `state/"backup"` recursively copies its own
staging tree until the path-length limit; its cleanup restores the original.

**M1 correction:** Reject overlapping/resolved-alias destinations before writes
for rebuild, rederive, export, and restore. Test input/output ancestry in both
directions and symlink aliases.

### F05 — P2: staleness can call invalid or undescribed data current

At `mneme_staleness.py:60,76,123`, some schema/semantic checks are absent
and missing identities are skipped.

**Fresh diagnostics:** A derived manifest with version 999 was called current.
Removing MBOX markers and refreshing member hashes was called current although
normal P3 verification rejected it. Removing isolation markers and refreshing
hashes was called current and guarded Find still succeeded.

**M1 correction:** Share schema/relational validation, require applicable rule
identities, and distinguish corrupt, unsupported, stale, and current data.
A known old rule is different from missing evidence of any rule.

### F06 — P2: an index can claim a source that does not exist

Hardening `hardening.py:653,695` checks member hashes but Find trusts index
references. Prototype 3 `mneme.py:473` checks message-record ordering, not
the complete index-to-source relation.

**Fresh diagnostic:** In a disposable archive, change the lantern index entries
to EML-999 with an all-zero digest and refresh derived member hashes.
Verification returned true, staleness current, and guarded Find returned EML-999.

**M1 correction:** Validate IDs, digests, locators, and duplicate relationships
against source/derived inventories before serving results. Add semantic-mutation
tests that consistently update file hashes. This is not a claim that unsigned
self-asserted manifests can resist wholesale malicious replacement.

### F07 — P2: export reports contradictory manifest metadata as complete

At `mneme_export.py:216–237`, some redundant metadata is not compared with
the exported state. Container keys are checked, but metadata values are not.

**Fresh diagnostic:** Change only EXPORT-MANIFEST.json to report source_count
-123 and false container sizes/hashes/keys/observation IDs. Verification returns
complete, including the negative count, while SHA256SUMS remains unchanged.

**M1 correction:** Recompute and compare all claimed metadata and reject
unsupported/malformed schemas. Keep the separate limitation that an independent
integrity anchor is needed against wholesale replacement.

### F08 — P2: an input FIFO blocks before type validation

Prototype 2 `mneme.py:95` and prototype 3 `mneme.py:137` open the path
before checking `fstat()`.

**Fresh diagnostic:** A fictional FIFO named with an .eml suffix and no writer
hangs both readers until the diagnostic terminates them.

**M1 correction:** Reject special files without blocking, handle replacement
races, and test the behavior in a time-bounded subprocess.

## Reproduced findings: retrieval and interpretation

The new date/address/reply-header examples below are wholly fictional.
Except F14, end-to-end probes used a process-local fixture-digest override because
ordinary ingest rejects bytes outside the fixed corpus. The repository allowlist
was not changed. These are gaps to close before broadening the synthetic corpus,
not claims that ordinary ingest currently accepts arbitrary hostile mail.

| ID / priority | Evidence at reviewed commit | Reproduction and consequence | M1 correction |
|---|---|---|---|
| F09 / P2 | `mneme-local-prototype-4/mneme.py:77` | `Fri, 31 Dec 9999 23:30:00 -0100` overflows UTC conversion outside the handler; filtering, identities and threads crash after successful ingest | Guard conversion/serialization as well as parsing; report invalid dates |
| F10 / P2 | `mneme-local-threads-1/mneme_threads.py:168–201` | A 12,665-byte message with 600 folded reference IDs is indexed but recursive tree rendering fails; placeholders bypass the occurrence cap | Bound graph expansion/depth and use iterative traversals; include serialization limits |
| F11 / P2 | `mneme-local-prototype-4/mneme.py:49,81`; `mneme-local-identities-1/mneme_identities.py:52` | Quoted addresses such as `"a b"@example.test` and `"a@b"@example.test` disappear or are refused as filters | Share parser-based normalization; retain raw evidence and diagnose unsupported syntax |
| F12 / P2 | `mneme-local-threads-1/mneme_threads.py:98` | Repeated References fields `<a@example.test>`, garbage, `<b@example.test>` become an inferred a→b→leaf chain with no malformed-header warning | Retain header ordinals; validate fields separately and define duplicate-header handling |
| F13 / P2 | `mneme-local-threads-1/mneme_threads.py:137` | A self-reply is silently omitted from cycles_refused | Record a refused self-cycle, separately from an already recorded edge |
| F14 / P2 | `mneme-local-threads-1/mneme_threads.py:214–218` | The existing THR-307/308 cycle is reported by the thread list but omitted from the selected-thread response | Carry relevant conflict/cycle diagnostics into each thread view |

The accepted tests already identify missing parent-conflict and contradictory
In-Reply-To/References cases. Add those along with F09–F14. Message-ID
case-folding and first-parent-wins are declared experimental policies; do not
call a different preference a defect. Preserve originals, show ambiguity, and
review durable grouping semantics before real data.

## Architecture and requirement gaps

**Shared implementation.** Features dynamically import experimental files,
private helpers, and global fixture modules. Threads modifies the allowlist on a
second in-memory copy of prototype 3. This was a practical experiment technique,
but it leaves no single supported application or consistent verification
boundary. M1 establishes ordinary modules and a single fixture registry; it does
not need a distributed architecture or a framework rewrite.

**Derived recovery.** Prototype 3 `rebuild()` at line 892 first resolves a
currently valid derived generation and demands equality with it. Staleness
`rederive()` at line 167 compares against old derived files and only publishes
a side directory. The generation convention at prototype 3 line 448 requires
one new ingest batch per generation. Demonstrated deterministic rebuild is
therefore not the full PRES-028/031 recovery obligation. M2 must rebuild from
source when old derived state is absent, and publish without inventing an ingest.

**Isolation includes readers.** Ingestion uses a bounded spawned worker, but
EML display at `synthetic-hardening-1/hardening.py:777`, MBOX display at
prototype 3 line 940, and thread headers at `mneme_threads.py:73` parse in the
caller. Worker output uses Python object deserialization
(`isolation.py:272`). The memory probe can return no reading. M1 makes all
entry points explicit and fixes accidental bypasses in the maintained code;
M3/M4 must establish OS-enforced privileges/egress, bounded non-executable output,
resource fail-closed behavior, and compromise containment before real data.
No test here establishes safety after arbitrary parser compromise.

**Evidence for relationships.** Identity/thread citations currently resolve to
subjects, not the From/References headers supporting the relation. Accepted
thread edges discard their supporting header/occurrence. Correct-source links
are useful but weaker than claim-level lineage (PRES-014). M1 retains header
ordinals, source digest, processing rule, and diagnostics for relationship
evidence, with a source inspection path; durable citation/version evolution is
reviewed at R2/R3.

**Format and scale.** Filename/offset keys survive appends, not general mailbox
rewrites or renames. EML-NNN caps occurrences at 999. Sources and derived data
are recopied for every generation; queries repeatedly scan/verify whole trees;
index entries repeat whole text per token. These are documented synthetic limits.
M2 addresses lifecycle/coordination, M3 measures costs and resolves bounded
scale/identity evolution. Do not optimize speculatively or silently remove caps.

**Packages and backups.** Segment concatenation reproduces tested containers;
it does not establish preservation of arbitrary provider export structure,
Eudora sidecars, PST, folders/flags, or missing remote attachments. Export hashes
are stored with the export. Encryption, independent copies, retention, keys,
and clean recovery are not a completed backup system. Source-package completeness
(PRES-003), independent integrity (PRES-008), and backup requirements remain open
outside the tested scope.

**Product.** There is no unified user workflow or UI. Find is token matching;
identities are addresses, not people; threads are interpretations. Annotations,
organizations/topics/timelines, AI Ask, account integration, and cross-device
operation remain future work. M1 must deliver a runnable demo; M3/M4 reconnect
engineering work to the actual research experience rather than treating more
CLI experiments as the finished product.

## Governance findings and changes in this working diff

The committed AGENTS.md and README still described Phase 0. Agent governance
also separately prohibited commits and required broad per-step approval. The
initial autonomy draft removed those stops, but indiscriminately dismissed
historical restrictions and permitted task-branch pushes without enough scope.

This revision supplies:

- one agent contract with milestone autonomy, attributable approval, local
  checkpoint commits for implementation, internal review and persistent status;
- a narrow historical distinction: preservation/privacy/accepted ADR obligations
  remain; unrelated candidate-acquisition gates are paused rather than universal;
- continued disablement of handoff operations and no default permission for
  publication, real data, external services, or production commitments;
- a CLAUDE.md import of AGENTS.md instead of relying on prose telling Claude to
  open it; two small work/review commands inheriting normal permissions;
- a current status/test index, one roadmap, and named major review checkpoints;
- review-only scope distinct from permission to fix code, accept results, or
  publish, so an agent-written report cannot expand its own authority.

The code/experiment directories were not moved during this review. M1's proposed
`mneme/` and `tests/` are future implementation paths; existing paths remain
available for reproduction. The review does not silently select Python or a
particular UI/database as the production architecture.

No project CLAUDE.md or .claude command directory existed before the preceding
draft. The Mac parent/global CLAUDE.md paths checked in this review were absent.
Claude's cloud-session memory, managed policy, and stop-hook configuration were
not accessible here. Project instructions can remove repository ambiguity; they
cannot guarantee removal of infrastructure permission prompts.

The command/import formats were checked against the
[Claude Code command documentation](https://code.claude.com/docs/en/skills) and
[instruction import documentation](https://code.claude.com/docs/en/memory).
The actual Claude cloud session was not launched to test command discovery.

## Verification record

The [status test inventory](../PROJECT-STATUS.md#python-regression-inventory)
lists the exact 11 test files. Each ran sequentially with
`PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B <test-file>`.

| Suite | Passed | Elapsed seconds |
|---|---:|---:|
| Vertical slice | 10 | 0.096 |
| Hardening | 16 | 0.990 |
| Isolation | 6 | 7.553 |
| Prototype 1 | 5 | 18.284 |
| Incremental EML | 16 | 104.145 |
| MBOX | 22 | 183.194 |
| Filters | 14 | 16.758 |
| Export/restore | 13 | 64.849 |
| Staleness | 8 | 34.042 |
| Identities | 7 | 16.258 |
| Threads | 10 | 10.471 |

The 14 diagnostic findings are separate from this baseline count. These probes
demonstrate missing assertions; they are not new tests committed by this review.
Git whitespace checks and local-link/simple command-frontmatter checks passed.
Application sources, fixtures, and tests remain unchanged. No Go or Perl rerun
was needed because their code and dependencies were not changed.

Historical evidence needs careful interpretation. The 2026-09-20 correction
record reports a successful offline Go run; the later feature sessions report
that they did not run it. Calling it "never tested" would be wrong. Conversely,
an old pass is not proof of a fresh run. Several result files also retain
pre-commit status language. Current state is recorded centrally rather than
rewriting historic execution claims.

## Recommended next decision

Authorize **M1 only** when this revised scope is accepted: first correct F01–F14
and establish consistent validation, then assemble the shared package and one
end-to-end demo. Internal reviews and fixes continue without per-step approval.
At **R1**, request another deep review against this report and the actual code.

Do not add UI, AI, provider access, or real mail to M1. Those have meaningful
later outcomes in the roadmap. The next deep reviews are R2 (lifecycle/recovery),
R3 (product architecture), R4 (real-data readiness), and R5 (pilot evidence).
