# Mneme Local Threads 1 — Results

**Status:** Successful within the declared local, offline, synthetic-only experimental scope; committed on a feature branch, awaiting review.
**Run date:** 2026-10-05.

## Runtime

- Linux container: CPython 3.11.15 and 3.10.20.
- macOS (reported 2026-10-06): passed on the accepted runtime, CPython 3.9.6 via `/usr/bin/python3 -B`, on commit `416be0c` fetched from GitHub into a local review branch: 10 tests in 10.2 s.
- Python standard library only; no network access.

## Fixtures

| Fixture | File | Bytes | SHA-256 |
|---|---|---:|---|
| `THR-301` | `31-dome-repair-plan.eml` | 343 | `c00c8c74894e18e25fd21f0a179887313652cee4bbaf8f4d3f165ec6444597ca` |
| `THR-302` | `32-re-dome-repair-plan.eml` | 417 | `154462eeea08aea8005ab55f6dd5811eedcdd6e61b66975e2074cedd8bb484f7` |
| `THR-303` | `33-re-re-dome-repair-plan.eml` | 450 | `adfaf78c379898ae7f76210dcf967e54df8f13a97c453c7d873d89a2d1af40ef` |
| `THR-304` | `34-reply-to-missing-parent.eml` | 454 | `2819e8286c70f64afaf48011329dcb59e83119e38b43dc04f7cc987d8d69b7f5` |
| `THR-306` | `36-malformed-references.eml` | 387 | `02c13f60532b5bc2384996b5920eacc9e3e3f6c01d20c05d7df77d664ee868a9` |
| `THR-307` | `37-loop-a.eml` | 349 | `04819bfbd0898710cb1b4b7e2a10cc08363df7bb5c60a30eec23591c473100e3` |
| `THR-308` | `38-loop-b.eml` | 349 | `92b5435f51a9d81ed08c452692b5ad1ccc611f464cbd41ca3aa0a71f67a85373` |
| `THR-309` | `39-subject-only.eml` | 346 | `d252f30243619f3bec87b6d94b11da413d8b33a3c63b1819a4c755e7e80c0bae` |
| `THR-MBOX` | `thread-replies.mbox` | 509 | `98295f7a7136e2636aae0f86b34c8d6b32dd321f04ab0a2605860b2b4118eabc` |

## Verification

`tests/test_threads.py`: 10 tests pass. Expected trees were worked out by hand from the fixture headers. They cover message-ID extraction; pinned, synthetic fixtures; the scoped allowlist (the ordinary prototype 3 still rejects the fixtures); the reply chain with a folded header, a missing parent placeholder, and a cross-family MBOX reply; no links from subjects or malformed headers; a refused loop; one node for a shared Message-ID and a separate thread for a missing one; list ordering, with every non-quarantined occurrence in exactly one thread; resolving citations and read-only behavior; and the CLI.

Five deliberate mutations were each caught and reverted: disabling the loop check, not linking `References` chains, not case-folding IDs, not reporting unparseable headers, and splitting a shared Message-ID per occurrence.

Two mutations are equivalent for these fixtures and are recorded as untested behavior:

- Skipping mboxrd unescaping before header parsing: the header parser treats the envelope line as a Unix-from line, and escaping only affects body lines.
- Preferring `In-Reply-To` over the last `References` ID: every fixture's two headers agree.

`parent_conflicts` (two occurrences of one Message-ID claiming different parents) has no fixture and is likewise untested.

## CLI evidence

State: the 14 accepted EML fixtures, then the nine threading fixtures: `generation-0002`, 23 sources, source manifest `20a1a8dfcbf2e255e566a3570e67948aa65e814a6f9a6f9d1ab105169c36e549`, derived tree `a26f8076420b0027b64d1b65a7e562a23e51b4a7e45833f7c2ab9119fe831443`. The ordinary prototype 3 stops with exit 2: `incoming member is not a reviewed synthetic eml fixture: 31-dome-repair-plan.eml`.

```text
- <dome-repair-301@example.test> [EML-015]
  - <dome-repair-302@example.test> [EML-016]
    - <dome-repair-303@example.test> [EML-017]
    - <dome-repair-305@example.test> [EML-023]   (MBOX)
  - <dome-repair-399@example.test> []  MISSING
    - <dome-repair-304@example.test> [EML-018]
```

| Output | Result |
|---|---|
| `threads` | `duplicate-anchor` (3 occurrences), `dome-repair-301` (5), `loop-b-308` (2); SHA-256 `410fca73df81ae4b57bebca70035ed0c1772773084bf39cd73c9591ce44ba1a9` |
| missing messages | `<dome-repair-399@example.test>` |
| refused loop | `loop-b-308` would become a child of `loop-a-307` (`EML-021`) |
| unparseable reply headers | `EML-019` |
| `thread --source-id EML-023` | SHA-256 `510edbddf2b63c9a41952fb8ce94520d6db96794d19c207c7b4acaae90d30552` |

## Limitations

- Reply headers are parsed in the main process with the standard library's header parser, not in the isolated parser worker. Only non-quarantined occurrences are read.
- Message-ID comparison is case-folded, which treats IDs differing only in local-part case as the same.
- First-parent-wins and loop refusal depend on source-ID order, so a different ingest order can produce a different, equally valid tree. The result is deterministic for a given archive.
- No subject-based grouping, so replies whose clients dropped reply headers stay separate.
- Rebuilt on every call by reading every non-quarantined source; fine only at synthetic scale.
