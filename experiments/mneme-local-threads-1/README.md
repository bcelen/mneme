# Mneme Local Threads 1 — Evidence-Only Conversation Threading

This experiment groups occurrences into conversations using only reply evidence in the preserved source bytes: `Message-ID`, `In-Reply-To`, and `References`. Subjects are never used. Prototypes 3 and 4 are loaded by path and left unchanged.

## Fixtures and the scoped allowlist

None of the accepted fixtures carry reply headers, so `thread_fixtures.py` adds nine pinned, wholly fictional fixtures: eight EML files and one single-record mbox container. Prototype 3 only ingests reviewed bytes. This experiment loads a separate copy of prototype 3 and extends that copy's allowlist with exactly these nine digests; the file on disk and the ordinary prototype 3 are unchanged, and the ordinary prototype 3 still rejects the fixtures.

| File | Role |
|---|---|
| `31-dome-repair-plan.eml` | thread root |
| `32-re-dome-repair-plan.eml` | reply to the root |
| `33-re-re-dome-repair-plan.eml` | reply to the reply, with a folded `References` header |
| `34-reply-to-missing-parent.eml` | reply to a message that is not in the archive |
| `36-malformed-references.eml` | reply headers without any message ID |
| `37-loop-a.eml`, `38-loop-b.eml` | each claims to reply to the other |
| `39-subject-only.eml` | same subject as the dome thread, no reply headers |
| `thread-replies.mbox` | an MBOX reply inside the dome thread |

## Rules

- Message IDs are the bracketed `<local@domain>` tokens in each header, case-folded. Headers are read from the preserved bytes; MBOX segments are unescaped first.
- A node is one message ID. Occurrences that share a Message-ID share one node; an occurrence without a Message-ID is its own node.
- Each `References` list links consecutive IDs as parent and child; the message's parent is the last `References` ID, or else the first `In-Reply-To` ID.
- A referenced ID with no occurrence becomes a placeholder node marked `missing_from_archive`.
- Occurrences are processed in source-ID order. The first parent assigned to a node wins; a later different explicit parent is recorded in `parent_conflicts`. A link that would make a node its own ancestor is refused and recorded in `cycles_refused`.
- Reply headers that contain no message ID are reported in `unparseable_reference_headers` and create no link.
- Children are ordered by earliest UTC date (undated and missing last), then ID; threads by the same rule. Thread IDs are `thread:` plus the root's message ID.

Everything is computed at query time from the verified current generation. No derived state changes.

## Commands

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-threads-1/mneme_threads.py ingest --incoming <dir> --state <state> --recorded-at 2026-10-05T09:00:00Z
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-threads-1/mneme_threads.py threads --state <state> [--all]
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-threads-1/mneme_threads.py thread --state <state> --source-id EML-023
PYTHONDONTWRITEBYTECODE=1 python3 -B experiments/mneme-local-threads-1/tests/test_threads.py
```
