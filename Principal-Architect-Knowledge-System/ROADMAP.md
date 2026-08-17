# Roadmap

## Phase 0: Foundation (Complete)

- [x] Repository structure
- [x] Docusaurus documentation site
- [x] Cursor rules and templates
- [x] Validation scripts and CI
- [x] Curriculum and progress metadata
- [x] Start Here section and 12-week learning path
- [x] Comprehensive sidebar navigation across all domains

## Phase 1: Distributed Systems Core (Complete)

- [x] What is a distributed system?
- [x] Partial failure
- [x] Safety and liveness
- [x] System models
- [x] Time and clocks (physical and logical time, Lamport/vector clocks, ordering)
- [x] CAP theorem and PACELC
- [x] Consistency models (linearizability through eventual)
- [x] Quorums and replication (primary-secondary, multi-leader, leaderless, CRDTs)
- [x] Raft, Paxos, leader election, and production consensus systems
- [x] Transactions, 2PC, sagas, MVCC, transactional outbox
- [x] Idempotency and failure detection
- [x] Computer architecture, operating systems, and networking foundations

## Phase 2: Data Systems (Complete)

- [x] Storage engines (B-trees, LSM trees, WAL, fundamentals)
- [x] Distributed databases (Dynamo, DynamoDB, Cassandra, Spanner, CockroachDB, MongoDB, Snowflake, Kafka, Redis)
- [x] Messaging and streaming (delivery semantics, Kafka, event-driven architecture)
- [x] Caching (fundamentals, invalidation, distributed caching)

## Phase 3: Production Architecture (Complete)

- [x] Microservices (decomposition, resilience, service mesh)
- [x] API and integration architecture (REST/gRPC/GraphQL, versioning)
- [x] Cloud architecture (AWS fundamentals, multi-region)
- [x] Kubernetes and platform engineering (K8s architecture, GitOps)
- [x] Reliability and resilience (SLOs, DR, chaos engineering)
- [x] Observability (fundamentals, distributed tracing)
- [x] Security (architecture fundamentals, zero trust)

## Phase 4: AI and Leadership (Complete)

- [x] Data platforms (lakehouse, stream/batch, governance)
- [x] Distributed inference, LLM serving, and RAG architecture
- [x] Agentic AI platform architecture and governance
- [x] Architecture strategy, ADRs, governance, and executive communication
- [x] Cost and FinOps (cloud cost optimization)
- [x] Production failures (analysis methodology, postmortem culture)
- [x] Hands-on labs for AI platform patterns (labs 015–016)

## Phase 5: Interview System (Complete)

- [x] Company guides (Adobe, Amazon/AWS, Google, Microsoft, NVIDIA, Snowflake/Databricks, OpenAI/Anthropic)
- [x] Behavioral and leadership (STAR framework, leadership principles, domain stories)
- [x] Mock interviews and scoring rubrics
- [x] System design exercises (25 principal-level designs)
- [x] Question bank (520 principal-level questions across 14 domains)
- [x] Flashcards auto-generated from curriculum (`scripts/build_flashcards.py`)
- [x] Real-world scenario walkthroughs (12 production-grounded interview guides in Domain 32)
- [x] STEP interview framework and 12-week scenario integration

## Phase 6: Labs and Case Studies (Complete)

- [x] 16 hands-on labs with implementations and unit tests
- [x] 16 production case studies
- [x] Flashcards (1,600+ cards) and cheat sheets

## Long-Term Enhancements

- Readiness dashboard and progress tracking UI
- AI-powered semantic search
- Personalized study recommendations
- Automated flashcard scheduling (Anki export)
- Mock-interview scoring automation
- Local RAG assistant for private notes
- Expand case studies to 20+

## Current Coverage (July 2026)

| Area | Domains | Chapters |
|------|---------|----------|
| Foundations | 01–04 | 15 |
| Core distributed systems | 05–09 | 36 |
| Data systems | 10–13 | 19 |
| Production architecture | 14–20 | 16 |
| Data platforms & AI | 21–23 | 8 |
| System design | 24 | 25 |
| Leadership & operations | 25–27 | 8 |
| Interview preparation | 28–30 | 13 |
| Real-world scenarios | 32 | 12 |
| **Total curriculum** | **32 domains** | **152 chapters** |

| Asset | Count |
|-------|-------|
| Interview questions | 520 |
| Flashcards | 1,600+ |
| Mermaid diagrams | 549 |
| Labs (implemented) | 16 |
| Case studies | 16 |
| Real-world scenarios | 12 |
