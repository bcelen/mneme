# Synthetic Hardening Experiment: Proposed Plan

**Status:** Accepted
**Prepared:** 2026-09-20
**Review date:** 2026-09-20
**Governing boundary:** `SYNTHETIC-VERTICAL-SLICE-DECISION-NOTE.md`

## Decision requested

Approve one bounded extension of the accepted first synthetic slice to test the highest-value format, hostile-content, failure, rebuild, and recovery gaps listed below. Approval would authorize implementation and focused synthetic tests only. It would not select a production stack or authorize real data, deployment, or follow-on work.

## Experiment boundary

The experiment remains local, offline, synthetic-only, disposable, and reversible. It should reuse the first slice's already-installed experimental runtime and standard library, with the exact runtime identity recorded again before implementation. If a required check cannot be implemented with the standard library, stop and report the gap; do not acquire a dependency.

All implementation, fixtures, and tests must be isolated under `experiments/synthetic-hardening-1/`. A later evidence record may be added as `docs/SYNTHETIC-HARDENING-EXPERIMENT-RESULTS.md`. Runtime archives, indexes, exports, restores, and logs must remain in fresh temporary directories outside the repository and be removed after evidence capture.

## Synthetic corpus

Create only wholly fictional EML fixtures using reserved addresses and URLs. The bounded corpus should include:

| Set | Coverage |
|---|---|
| Format and encoding | LF and CRLF messages; `7bit`, `8bit`, quoted-printable, and base64 bodies; folded headers and encoded words |
| Unicode and headers | Unicode names, subjects, and bodies; repeated, missing, malformed, and undecodable headers with declared expected outcomes |
| Duplicates | Exact duplicate bytes in separate source occurrences and a message-ID duplicate whose bytes differ; no source occurrence may be deleted or overwritten |
| Attachments | Small text and inert binary attachments, duplicate filenames, suspicious filenames, missing names, and declared content types that disagree with filename extensions |
| Hostile HTML | Inert script, event-handler, form, CSS concealment, deceptive link, tracking-pixel, and remote-resource examples using reserved targets |
| Malformed messages | Broken MIME boundaries, truncated transfer encoding, invalid charset labels, excessive nesting descriptors, and an input that causes a controlled parser failure |

Every fixture must have a stable ID, fixed bytes and SHA-256, expected preservation membership, expected parse status, warnings or quarantine outcome, expected derived facts, and prohibited side effects.

## Required behavior

1. Preserve every EML occurrence byte-for-byte before parsing. Record source-package membership, byte count, SHA-256, provenance, and processing version in an application-independent manifest.
2. Treat duplicate detection as reversible derived data. Preserve and cite every source occurrence even when bytes or message IDs match.
3. Decode supported transfer encodings into derived representations without changing source bytes. Unsupported or invalid encodings must produce deterministic warnings or quarantine, never silent repair.
4. Record attachments as derived MIME-part metadata and bytes with source digest, part locator, filename treatment, media type, size, and SHA-256. Never execute an attachment or trust its filename as a write path.
5. Treat HTML as untrusted evidence. Preserve the original message, block all remote fetches and active behavior, and provide only escaped or plain inert display with an explicit source citation.
6. Give each message a deterministic outcome: indexed, indexed with warnings, or quarantined. Parser exceptions, malformed structures, and limit failures must leave source preservation intact, create no partial trusted index, and record a stable failure reason.
7. Rebuild all derived metadata, attachment derivatives, duplicate relations, indexes, results, and citations from the preserved sources and recorded rules. Two clean rebuilds must produce byte-identical deterministic artifacts.
8. Require every Find result and source display to identify the preserved source occurrence, SHA-256, provenance event, processing generation, and unambiguous header, line, byte, or MIME-part locator.
9. Export preserved source bytes, manifests, provenance, deterministic derived state, and format documentation to a plain directory structure readable without the experiment code.
10. Restore into a fresh temporary root, independently verify every exported member, reproduce the same Find results and citations, then delete and rebuild derived state to confirm the same deterministic hashes. Missing, changed, or extra export members must fail closed.

## Focused acceptance evidence

The result must include the complete implementation diff, fixture catalog and hashes, runtime identity, exact test command, test inventory, and temporary-root cleanup. Tests must show:

- original and restored source bytes match their fixture hashes exactly;
- all declared encodings and Unicode cases have deterministic expected outcomes;
- malformed headers and messages warn or quarantine as declared without source loss or process escape;
- exact and message-ID duplicates retain distinct source occurrences and provenance;
- attachment names cannot escape the temporary root and attachment bytes are never executed;
- hostile HTML remains inert and causes no network attempt;
- parser failure cannot create a trusted partial index or prevent unrelated fixtures from completing;
- repeated clean rebuilds produce identical derived hashes, Find ordering, and citations; and
- complete export/restore passes, while changed, missing, and extra members are rejected.

The preservation/corpus, security/privacy, and quality/review perspectives must review the combined result before it can be accepted. Passing this experiment is evidence only for its bounded synthetic corpus.

## Exclusions and stop conditions

This plan does not permit accounts, network access, real correspondence, provider authentication, cloud AI, embeddings, containers, databases, persistent services, production configuration, deployment, mobile clients, handoff automation, stack selection, commit, or push.

Stop without workaround if implementation would require a new dependency, network access, execution of source content, writes outside the authorized repository paths or temporary root, source mutation, an unexplained parser crash, nondeterministic output, missing provenance, unsupported citation, incomplete cleanup, or contact with real data. Return the evidence and unresolved gap for review.

No implementation or test execution is authorized while this document remains Proposed.
