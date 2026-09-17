# Mneme

Mneme is a private, intelligent archive of personal correspondence: a single-user research system for finding, understanding, and reconnecting with a lifetime of email and related documents. Sending email is explicitly out of scope.

This repository currently contains only the Phase-0 project control plane. It records the product boundary, governing principles, privacy posture, agent rules, and decisions that must guide later implementation.

## Phase-0 scope

Phase 0 deliberately excludes application code, dependencies, Docker configuration, infrastructure definitions, and implementation-stack decisions. Those belong to later, explicitly approved phases.

## Terminology and product direction

In Mneme, the **source archive** is the preserved, imported record: source messages, sent mail, attachments, documents, and provider metadata. It is byte-preserving, read-only, and the system of record. **Derived data** includes indexes, annotations, identities, classifications, embeddings, summaries, and other views that can be rebuilt. For derived data, **reversible** means either undoable through recorded history or fully reconstructible from the source archive and processing rules. Derived annotations and classifications may be created, edited, and removed by the user or authorized workflows under that definition, and must never rewrite the source archive.

- Planned source formats and corpus: Gmail/Google Workspace, Outlook, Eudora, MBOX, EML, sent mail, attachments, and provider metadata.
- Accepted product direction: a portable architecture, private remote access, deterministic Find separate from source-grounded AI Ask, ambitious historical/research assistance with citations and provenance, and controlled hybrid cloud/local AI.
- Provisional deployment context: an Ubuntu 24.04 home server with Docker and ZFS, with Tailscale as the current private-access candidate. These are not accepted implementation commitments.
- Conceptual model: people and identities, organizations, messages, conversations, attachments, documents, topics, events, relationships, and timelines.
- Retrieval: deterministic Find is separate from source-grounded AI Ask.
- Intelligence: ambitious historical and research assistance with citations and provenance.
- User experience: beautiful, fast, low-maintenance, and usable across Mac, iPhone, and iPad.

See `docs/` for the governing documents.
