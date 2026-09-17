# Product Requirements

## Users and mode

- The system has one intended user.
- The user researches their own correspondence and related documents.
- The product is read-only with respect to the preserved source archive. Derived annotations, identity links, and classifications may be user-controlled when reversible; reversible means either undoable through recorded history or fully reconstructible from the source archive and processing rules.
- Sending email, editing source messages, and acting as a mail client are out of scope.
- Remote use is private; the current Tailscale idea is provisional deployment context, not an implementation commitment.

## Corpus and source formats

The planned corpus includes Gmail/Google Workspace, Outlook, Eudora, MBOX, and EML. It includes received and sent mail, attachments, and provider metadata. Import support, provider APIs, OAuth flows, and parser choices require later approval.

## Evidence model and terminology

- The **source archive** is the preserved, byte-faithful imported record of messages, sent mail, attachments, documents, and provider metadata. It is read-only and the system of record.
- **Derived data** includes indexes, annotations, identity links, classifications, embeddings, summaries, relationships, and other computed views. It may be changed reversibly and must be rebuildable. Here, reversible means either undoable through recorded history or fully reconstructible from the source archive and processing rules.
- Every source item and derived representation must have hashes or equivalent integrity evidence, manifests, provenance, and a traceable relationship to its inputs and processing history.
- The source archive must support application-independent export, backups, restore verification, and rebuild of derived data.
- People and identities are distinct concepts: one person may have multiple addresses or identifiers, and an identity must not be silently treated as a person.
- The conceptual model includes people, identities, organizations, messages, conversations, attachments, documents, topics, events, relationships, and timelines.
- Conversations, attachments, and documents are independently addressable and linked to their evidence.

## Retrieval

- Find provides deterministic, inspectable retrieval and filtering.
- Find results must identify the underlying source items and relevant fields.
- AI Ask is a separate experience, not a replacement for deterministic retrieval.
- AI Ask answers must be grounded in retrieved source material and expose citations/provenance.
- When evidence is insufficient, the system should say so rather than inventing an answer.

## Research intelligence

- The system should support historical and longitudinal questions across correspondence.
- It should help with chronology, themes, people, relationships, documents, and changes over time.
- Interpretive or inferential output must be distinguishable from directly supported facts.
- Users must be able to move from an answer back to its sources.

## Experience

- The experience should be beautiful, fast, calm, and low-maintenance for one user.
- Core workflows should work well across Mac, iPhone, and iPad, with appropriate layouts and interaction patterns for each.
- Performance, synchronization, offline behavior, accessibility, and responsive research navigation are requirements to validate in later design work.

## AI execution

- Cloud and local models may coexist in a controlled hybrid design.
- Routing, data exposure, retention, cost, and model identity must be explicit and reviewable.
- No external AI service is assumed or selected in Phase 0.

## Operational qualities

- The system must be portable beyond the Ubuntu/Docker/ZFS production target.
- Rebuilding indexes and derived classifications must be a supported recovery operation.
- Security and privacy defaults must be conservative.
