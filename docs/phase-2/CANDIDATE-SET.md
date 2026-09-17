# Neutral Candidate Set

**Status:** Accepted
**Review date:** 2026-09-17
**Evidence cutoff:** 2026-09-17
**Decision state:** Comparison candidates only; no candidate is selected.

## Framing principles

The candidates are coherent architecture archetypes, not a popularity list and not a component-by-component tournament. Each represents a materially different answer to Mneme's central product and operating tradeoff: low-maintenance web delivery versus richer platform-native clients, and minimal single-user persistence versus a separate database service.

The set is neutral in the following sense:

- every candidate covers the complete boundary required by the accepted Phase-2 plan;
- every candidate is evaluated against the same source families, security controls, target devices, workload assumptions, and evidence cutoff;
- common preservation and privacy obligations are mandatory architecture, not points awarded to a favored stack;
- material variants receive separate rejection or revisit records rather than being silently substituted during scoring;
- software popularity, developer familiarity, and speculative future ecosystem benefits are not scored unless tied to reviewable evidence.

## Common workload and product assumptions

- One private user researches a historical personal-correspondence corpus.
- Planned source families are Gmail/Google Workspace, Outlook, Eudora, MBOX/EML, sent mail, attachments, and provider metadata.
- The preserved source archive is read-only after an approved package is sealed. Reversible annotations and classifications live outside it.
- Sending email, public sharing, multi-user collaboration, and source mutation are out of scope.
- Mac is the primary deep-research surface; iPhone and iPad must support useful Find, reading, citation navigation, annotation, and status workflows.
- A private home-server deployment is expected, but Ubuntu 24.04, Docker, ZFS, and Tailscale remain provisional context.
- No cloud model, hosted database, external identity service, or telemetry service is assumed.
- Corpus size, write concurrency, offline depth, recovery objectives, and exact hardware remain unknown and are recorded in the registers.

## Common architecture contract

These elements are identical requirements for all candidates.

### Source archive and acquisition boundary

Approved source packages enter a quarantine/staging boundary and are sealed only after byte length, package membership, and approved cryptographic hashes are recorded. The application receives read-only access to sealed source packages. Filenames, provider identifiers, source-item identifiers, derived identifiers, and user-visible entity identifiers remain separate namespaces. Exact hash, manifest serialization, identifier format, and storage layout remain deferred.

### Derived state and provenance

The candidate's database holds parsed metadata, entities, conversations, messages, organizations, topics, events, relationships, timelines, annotations, classifications, processing generations, and lineage. Machine-derived state is disposable and rebuildable from source plus recorded rules. User-authored state uses append-only history sufficient for undo and export. Nondeterministic outputs retain model, configuration, context, citations, and generation identity.

### Deterministic Find

Find is lexical and structured retrieval over a named derived-data generation. Identical query, filters, and generation must return stable results and source references. Search reports stale, incomplete, or quarantined inputs. Embeddings may later supplement Ask, but never replace deterministic Find.

### Import and parser isolation

Import adapters and content parsers run as disposable workers behind a narrow file-and-manifest interface. The service gives a worker read-only access to one staged source item, an empty scratch/output area, no source-archive write access, no credentials, no administrative capability, and no outbound network. An operating-system-enforced isolation adapter must provide process, filesystem, network, time, memory, file-count, and expansion limits; a Linux implementation may use namespaces, resource controls, and syscall restrictions, but no container runtime is selected here. Crashes, limit hits, malformed output, path escapes, and unsupported content quarantine the item and do not mark it successful. Parser and extractor implementations remain replaceable and unselected.

### Safe content presentation

Original HTML and attachments remain evidence, never trusted application UI. The client receives a safe derived representation with scripts, forms, event handlers, active content, and remote resources disabled. Opening original or risky material requires a separate, explicit, isolated action. Source-controlled URLs cannot trigger background network traffic.

### AI Ask and routing

Ask consumes retrieval results and lineage records through a separate model-routing interface. Local-only operation is meaningful. External transfer is default-deny; no provider, model, data class, or fallback is enabled without separate approval. Archive content has no authority to call tools, change policy, reveal credentials, mutate source, or route data. Answers distinguish quotation, supported synthesis, inference, and insufficient evidence and carry source citations. Exact models, embedding stores, and providers remain unselected.

### Export, backup, restore, and compromise recovery

Every candidate must emit an application-independent export containing source bytes, manifests, provenance, documented user-controlled state, and explicit omissions. Backups cover source packages, integrity evidence, durable history, configuration needed for interpretation, and a separately protected secret-recovery process. Clean restore verifies source integrity before rebuilding machine-derived state. Exact backup topology, encryption mechanism, retention, RPO, and RTO remain separate operational decisions.

### Network and operations

The service binds only to a private interface selected at deployment, requires its own authentication and session boundary, emits content-minimized operational events, and exposes integrity, backup, rebuild, quarantine, and update status. Tailscale may be evaluated as transport but does not replace application authorization. Dependency inventory, lock files, vulnerability response, reviewed updates, rollback, and compromise recovery are mandatory. There is no public listener requirement.

## CAND-001 — Python web monolith

### Boundary summary

A supported Python and Django release provides one private application/service process and responsive server-rendered interface with progressive enhancement and a PWA shell. SQLite stores durable derived state and FTS5 supplies deterministic text search. Background imports are serialized through an internal job queue to respect SQLite's single-writer characteristics. The source archive, parser workers, exports, and backups remain separate filesystem boundaries.

| Category | Declared boundary |
|---|---|
| Client | Responsive HTML/CSS with limited JavaScript enhancement and installable PWA metadata; Safari on Mac, iPhone, and iPad; no sensitive offline cache by default |
| Runtime | Django over a production WSGI or ASGI server; one private service; serialized background writer; no public exposure |
| Source archive | Common read-only package boundary; never stored as mutable database blobs |
| Derived/provenance | SQLite transactional database with append-only history conventions and generation identifiers |
| Find | SQLite FTS5 plus structured relational filters; FTS tables are rebuildable |
| Parsers | Replaceable external workers launched through the common isolation adapter; parser language not constrained to Python |
| Ask | Server-side retrieval and model-routing adapter; local-only default; no provider selected |
| Export/recovery | Portable export plus SQLite online backup or clean consistent copy procedure; source backup remains independent |
| Operations | One application service and filesystem archive; database is embedded; supported Python/Django security branches only |

### Strengths and risks

The candidate minimizes always-on services and deployment surfaces, has a mature security process, and places AI/research integrations near Python's broad tooling ecosystem. The important risk is SQLite contention between interactive use and sustained ingestion/rebuild work. Django's documentation explicitly warns that SQLite cannot support high concurrency. The candidate is therefore bounded to one user, short write transactions, and serialized heavy writers; corpus-scale and latency evidence must validate that assumption before implementation acceptance.

### Replaceability and exit

Source packages, manifests, export bundles, parser-worker protocol, and model-routing protocol are database-independent. Replacing SQLite with another store is a new material candidate and requires a later ADR; it is not an automatic fallback hidden inside `CAND-001`.

## CAND-002 — TypeScript web application

### Boundary summary

A supported Next.js release on a supported Node.js LTS release provides a self-hosted responsive application and PWA. PostgreSQL stores derived state and supplies built-in full-text search. Background jobs run in a distinct worker process. The candidate retains one web language across client and application service but introduces a separate database service and a larger JavaScript dependency surface.

| Category | Declared boundary |
|---|---|
| Client | Responsive Next.js PWA for Safari on Mac, iPhone, and iPad; no sensitive offline cache by default |
| Runtime | Self-hosted Node.js service plus separate background worker; private reverse-proxy boundary expected but not selected |
| Source archive | Common read-only package boundary outside PostgreSQL |
| Derived/provenance | PostgreSQL transactions, append-only history conventions, and generation identifiers |
| Find | PostgreSQL full-text search and structured filters; search structures rebuild from derived records |
| Parsers | Replaceable external workers through the common isolation adapter; parsers never execute in the request process |
| Ask | Server-side retrieval/model-routing interface; local-only default; no provider selected |
| Export/recovery | Portable export plus PostgreSQL logical/physical backup path; source backup remains independent |
| Operations | Application process, worker, PostgreSQL, and private ingress; supported Node LTS and supported Next.js releases only |

### Strengths and risks

The candidate provides a richer single-codebase web client than a mostly server-rendered monolith, strong self-hosting documentation, and a durable database with mature backup options. Its principal disadvantages are an additional database service, a broader transitive dependency graph, framework and runtime upgrade cadence, and more cache/build behavior to understand and secure. Native-quality interaction remains an empirical UX question.

### Replaceability and exit

PostgreSQL is not the preservation authority. Source packages and exports remain independent. The client can be replaced over a versioned private API, while parser and model adapters remain out of process.

## CAND-003 — Apple-native clients with Go service

### Boundary summary

SwiftUI supplies separate but shared-design Mac, iPhone, and iPad applications. A supported Go release provides a small private service/API and background orchestration. PostgreSQL stores derived state and supplies full-text search. Client devices cache only explicitly bounded derived records and thumbnails; source bytes remain on the server unless the user explicitly opens or exports an item.

| Category | Declared boundary |
|---|---|
| Client | SwiftUI applications for macOS, iOS, and iPadOS; Apple-native navigation, accessibility, and platform integration; bounded encrypted cache |
| Runtime | Go private API/service and background worker; explicit versioned client API; no public exposure |
| Source archive | Common read-only package boundary on the server |
| Derived/provenance | PostgreSQL transactions, append-only history conventions, and generation identifiers |
| Find | PostgreSQL full-text search and structured filters exposed through a deterministic API |
| Parsers | Replaceable external workers through the common isolation adapter; not embedded in clients or Go request handlers |
| Ask | Server-side retrieval/model-routing interface; citations returned as structured source references |
| Export/recovery | Portable export plus PostgreSQL backup path; clients are disposable and recover from server state |
| Operations | Go service, PostgreSQL, three Apple application targets, signing/update process, and private transport |

### Strengths and risks

The candidate offers the strongest documented route to polished Apple-platform behavior, accessibility integration, and responsive device-specific interaction. Go has a strong compatibility promise and clear security process. Costs are higher engineering and release complexity, two principal language ecosystems, PostgreSQL operations, and Apple signing/distribution constraints. App Store or broad signed distribution may require an annual developer-program fee; personal on-device development can begin without that membership but is operationally limited.

### Replaceability and exit

The versioned API separates clients from the service, and all authoritative preserved and user-controlled data remain exportable from the server. SwiftUI is Apple-specific, so replacing the client on a non-Apple platform requires new client work even though data ownership is portable.

## CAND-004 — Shared native clients with Rust service

### Boundary summary

Flutter supplies one shared client codebase targeting macOS, iPhone, and iPad. A supported Rust release with Axum provides the private service/API and background orchestration. PostgreSQL stores derived state and supplies full-text search. The boundary otherwise matches `CAND-003`, but trades deeper Apple-native integration for greater client-code reuse and uses Rust's memory-safety model in the service.

| Category | Declared boundary |
|---|---|
| Client | Flutter applications for macOS, iOS, and iPadOS; shared UI code with bounded encrypted cache |
| Runtime | Rust/Axum private API/service and background worker; explicit versioned client API; no public exposure |
| Source archive | Common read-only package boundary on the server |
| Derived/provenance | PostgreSQL transactions, append-only history conventions, and generation identifiers |
| Find | PostgreSQL full-text search and structured filters exposed through a deterministic API |
| Parsers | Replaceable external workers through the common isolation adapter; not embedded in clients or request handlers |
| Ask | Server-side retrieval/model-routing interface; citations returned as structured source references |
| Export/recovery | Portable export plus PostgreSQL backup path; clients are disposable and recover from server state |
| Operations | Rust service, PostgreSQL, Flutter toolchain, Apple signing/update process, and private transport |

### Strengths and risks

The candidate combines native packaging and one shared client codebase, while Rust and Axum provide a strong memory-safety posture and a relatively thin server framework. Flutter officially supports current iOS and macOS targets and supplies accessibility facilities. Risks include two fast-moving non-system toolchains, third-party crate security ownership, platform-fidelity gaps, macOS Intel deprecation, and the maintenance cost of Rust plus Flutter for a single-user product.

### Replaceability and exit

The versioned API and portable server export preserve data ownership. Flutter can be replaced without reinterpreting the archive. Axum and PostgreSQL remain replaceable behind the service/export boundaries, but replacement is not cost-free.

## Candidate completeness check

| Required category | CAND-001 | CAND-002 | CAND-003 | CAND-004 |
|---|---|---|---|---|
| Mac/iPhone/iPad client | Web/PWA | Web/PWA | SwiftUI native | Flutter native |
| Service/runtime | Django/Python | Next.js/Node.js | Go | Rust/Axum |
| Source preservation | Common file/package contract | Common | Common | Common |
| Derived/provenance | SQLite | PostgreSQL | PostgreSQL | PostgreSQL |
| Deterministic Find | SQLite FTS5 | PostgreSQL FTS | PostgreSQL FTS | PostgreSQL FTS |
| Parser isolation | Common replaceable worker contract | Common | Common | Common |
| AI Ask/routing | Common controlled adapter | Common | Common | Common |
| Export/backup/recovery | Portable export + SQLite backup | Portable export + PostgreSQL backup | Same as CAND-002 | Same as CAND-002 |
| Operations | App + embedded DB | App + worker + DB | API + worker + DB + native releases | API + worker + DB + native releases |

No candidate includes a selected parser library, model, cloud provider, deployment technology, manifest serialization, backup product, authentication product, or real-data acquisition route.
