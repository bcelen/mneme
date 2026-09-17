# Architectural Principles

1. **Source immutability.** The source archive is the byte-preserving system of record and is never rewritten as a side effect of indexing, cleanup, classification, annotation, or AI use.
2. **Reconstructible derivation.** Indexes, embeddings, classifications, annotations, summaries, relationships, and other derived data are disposable, reversibly editable where user-controlled, and reproducible from source plus versioned rules. For derived data, reversible means either undoable through recorded history or fully reconstructible from the source archive and processing rules.
3. **Logical, not physical, cleanup.** Deduplication and junk handling are classifications or relationships over source items, never destructive deletion.
4. **Explicit entities.** People and identities, organizations, messages, conversations, attachments, documents, topics, events, relationships, and timelines have distinct conceptual identities and relationships.
5. **Deterministic foundations.** Find is independent of probabilistic AI and remains useful, testable, and inspectable on its own.
6. **Grounded intelligence.** AI Ask operates over retrieved evidence and carries citations/provenance through to the user.
7. **Portable boundaries.** Deployment context must not dictate the product architecture; Ubuntu 24.04, Docker, ZFS, and Tailscale are provisional context, not accepted implementation choices.
8. **Minimal privilege.** Components and agents receive only the access needed for the current operation.
9. **Recoverability.** Hashes, manifests, provenance, application-independent export, backups, restore verification, rebuilds, and failure modes must preserve the source archive and make derived state replaceable.
10. **Observable uncertainty.** The system should make provenance, confidence, ambiguity, and missing evidence visible where they affect interpretation.
11. **No outbound mail.** Sending email and modifying source messages are outside the product boundary.
12. **Human-scale experience.** The single-user experience should be beautiful, fast, low-maintenance, and coherent across Mac, iPhone, and iPad.
