# Mneme

Mneme is a private research archive for personal correspondence: preserve the
record, find relevant material deterministically, and follow every claim back to
its sources. Sending email is out of scope.

The code currently consists of local Python experiments using fictional EML and
mboxrd messages. They demonstrate preservation, incremental ingestion, Find and
filters, address identities, threads, staleness detection, citations, and
export/restore. They are not yet one usable application. The current review
identified correctness and recovery defects that must be addressed during
consolidation.

## Start here

- [Project status and test inventory](docs/PROJECT-STATUS.md): what exists,
  evidence, limitations, and current task.
- [Roadmap and deep-review checkpoints](docs/ROADMAP.md): M1–M5 outcomes and R1–R5
  review points. The next implementation is **M1: one local synthetic prototype**.
- [Latest project review](docs/reviews/2026-10-06-project-review.md): findings and
  their planned disposition.
- [Agent operating contract](AGENTS.md): autonomy, review, and consequential
  approval boundaries. [CLAUDE.md](CLAUDE.md) loads it for Claude Code.

In Claude, `/mneme-work M1` runs a user-authorized milestone through tests and
internal review. `/mneme-review R1` requests a deep review. The prompts in
[.claude/commands/](.claude/commands/) also work as plain task instructions.
These are agent commands; a unified Mneme application command is an M1 deliverable
and does not exist yet.

To inspect the existing filtered-search experiment's CLI without ingesting data:

```sh
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B experiments/mneme-local-prototype-4/mneme.py --help
```

On Linux use an already installed Python interpreter appropriate to the tests.
Use the commands in project status for verification; no package installation is
required for these Python experiments. Experiments accept reviewed synthetic
fixtures only, not the user's mail.

## Structure

| Location | Purpose |
|---|---|
| `experiments/` | Existing reference implementations, fixtures, tests, and historical results |
| `docs/PROJECT-STATUS.md` and `docs/ROADMAP.md` | Current state and one implementation sequence |
| `docs/reviews/` | Dated project/milestone reviews |
| `docs/decisions/` | Durable decisions, with acceptance distinct from proposals |
| `docs/phase-1/` | Preservation, threat, corpus, and acceptance requirements |
| `docs/phase-2/`, `docs/phase-3/` | Historical/deferred candidate evaluation and acquisition evidence |
| `tools/handoff/` | Disabled handoff experiment; not required for development |
| `.claude/commands/` | Reusable work/review prompts |

A maintained `mneme/` package and top-level `tests/` are planned for M1.
Historical paths remain intact for reproducibility. Local archives, private
exports, credentials, and runtime state do not belong in Git.

## Product and preservation commitments

The **source archive** is the immutable record: source packages, messages,
attachments, containers, sidecars, and provider metadata as supplied.
**Derived data** includes indexes, classifications, identity links, annotations,
threads, embeddings, and summaries. Machine-derived state must rebuild from
source plus versioned rules; user-authored changes require reversible history.

Planned sources include Gmail/Google Workspace, Outlook, Eudora, MBOX, and EML,
including sent mail and attachments. Tested LF mboxrd support does not establish
support for every provider export or legacy mailbox.

Find remains independent of AI Ask. People and addresses are distinct; inferred
relationships must remain distinguishable from evidence. The intended experience
is a calm, fast, low-maintenance private research workspace across Mac, iPhone,
and iPad. AI, remote access, real-data ingestion, and deployment remain future
scoped work.

An Ubuntu home server, Docker, ZFS, and Tailscale are provisional deployment
context, not accepted stack choices. Python is the current experiment runtime,
not an automatic production decision.

See the [charter](docs/PROJECT-CHARTER.md),
[product requirements](docs/PRODUCT-REQUIREMENTS.md),
[preservation contract](docs/phase-1/PRESERVATION-CONTRACT.md),
[security principles](docs/SECURITY-PRINCIPLES.md), and
[AI privacy policy](docs/AI-PRIVACY-POLICY.md) for the governing requirements.

Forgejo is canonical; GitHub is the Claude work mirror. Check the actual remote
URLs in each checkout before publishing.
