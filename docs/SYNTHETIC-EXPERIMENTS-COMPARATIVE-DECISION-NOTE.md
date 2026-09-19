# Synthetic Experiments: Comparative Evidence Decision

**Status:** Accepted
**Prepared:** 2026-09-20
**Reviewed:** 2026-09-20
**First-slice evidence:** `cb024f9171f6fd37558210a6981d44fe591781f6`
**Hardening evidence:** `ff1c11df59c7cd687fa0df7fc28264658b394183`

## Decision

Accept the first vertical slice and the synthetic hardening experiment as cumulative evidence that Mneme's preservation-to-retrieval seam is feasible for the tested EML boundary. The hardening result materially broadens the evidence, but it does not establish production readiness or select an implementation stack.

## What is now established

Within local, offline, standard-library experiments using wholly fictional data:

- original EML bytes can be preserved before parsing, independently hashed, manifested, traced through provenance, cited, exported, restored, and verified without source mutation;
- deterministic metadata, indexes, Find ordering, citations, duplicate relations, attachment derivatives, and inert HTML representations can be deleted and rebuilt byte-for-byte from preserved sources and recorded rules;
- the tested path handles LF and CRLF, `7bit`, `8bit`, quoted-printable, base64, Unicode, folded encoded headers, selected malformed headers, exact duplicates, message-ID duplicates, attachments, and hostile HTML;
- malformed MIME boundaries, controlled parser failure, excessive MIME depth, and invalid base64 can be quarantined while unrelated messages continue and no partial trusted index is created;
- source occurrences remain distinct even when their bytes or message IDs match;
- deterministic Find citations resolve to inert source display with source hash and preservation provenance; and
- a plain-directory export can be independently inventoried, restored, queried, and rebuilt, while changed, missing, or extra members fail closed.

These conclusions are supported by one passing seven-test slice and one passing thirteen-test hardening suite. They apply only to the reviewed synthetic fixtures and runtime.

## What remains unproved

The experiments do not prove parser process isolation, operating-system network denial, CPU or memory limits, timeouts, decompression controls, browser-renderer safety, malware handling, or compromise recovery. They do not cover MBOX, Eudora, Gmail/Google Workspace, Outlook, provider metadata, large corpora, durable concurrent storage, encrypted backups, key recovery, migration across versions, Mac/iPhone/iPad UX, AI behavior, production deployment, maintenance, licensing, cost, or real correspondence.

The plain-directory export is useful feasibility evidence, not a complete backup, migration, retention, or disaster-recovery design. Python and its standard library remain experimental tools, not a selected product stack.

## Recommended next step

Before broadening the corpus or choosing a stack, prepare a separate evidence review for parser isolation and enforceable resource boundaries. It should identify the minimum synthetic evidence needed for process separation, read-only source access, denied network access, bounded CPU/memory/time/output, crash containment, cleanup, and independent verification on the intended development and provisional deployment platforms.

That review should determine whether a bounded experiment is justified and what platform mechanisms or dependencies it would require. It must return for explicit approval before implementation or execution. No next step is authorized by this note.
