# First Synthetic Vertical Slice: Evidence Boundary

**Status:** Accepted
**Prepared:** 2026-09-20
**Review date:** 2026-09-20
**Evidence commit:** `cb024f9171f6fd37558210a6981d44fe591781f6`

## Proposed decision

Accept the first synthetic vertical slice as evidence that Mneme's central preservation-to-retrieval path is feasible within the tested experimental boundary. Do not treat it as stack selection, production readiness, or authorization for another implementation phase.

## What the experiment established

For one wholly fictional, UTF-8, non-multipart, plain-text EML, a local standard-library implementation can:

- preserve the original bytes before parsing and independently verify their byte count and SHA-256 against an application-independent JSON manifest;
- stop derivation and Find when the source is missing, its size changes, a same-size byte changes, or the manifest digest is wrong;
- derive minimal metadata and a disposable index with recorded source and processing provenance;
- return deterministic Find results with stable citations that resolve to inert source lines and preservation evidence;
- delete and reproduce the deterministic derived state from the preserved source and recorded rule version; and
- run without accounts, network use, external dependencies, services, containers, cloud AI, real correspondence, or retained execution state.

The seven focused synthetic tests and the complete end-to-end run passed. This is positive feasibility evidence for the tested slice, not proof beyond it.

## What remains unproved

The experiment did not establish:

- preservation or parsing across Gmail/Google Workspace, Outlook, Eudora, MBOX, provider metadata, multiple messages, attachments, HTML, malformed MIME, hostile content, duplicates, or junk classification;
- parser-worker isolation, resource limits, safe rich rendering, prompt-injection defenses, credential handling, operating-system-level network denial, or compromise recovery;
- corpus-scale performance, concurrent use, durable storage, migration, full application-independent export, backup, restore, or disaster recovery;
- the Mac, iPhone, and iPad experience, accessibility, synchronization, offline product behavior, or low-maintenance operation;
- nondeterministic AI behavior, cloud/local model routing, external embeddings, research-quality synthesis, or citation behavior beyond deterministic Find;
- production portability, deployment, observability, maintenance, licensing, cost, or any mandatory stack-selection gate; or
- safety or correctness with real correspondence.

## Consequence

The experiment supports continuing from a working preservation, provenance, Find, and citation seam. It does not resolve the Phase-2 no-selection finding or select Python, a storage engine, a service architecture, or any deployment technology.

Review of this note records the evidence boundary only. No additional implementation, dependency, account access, real-data work, service, deployment, or stack decision is authorized until a separate user-approved next step is defined.
