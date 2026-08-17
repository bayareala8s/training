# Lab 015: Architecture

## Overview

**Platform-style RAG** — ingestion, indexing, retrieval, generation as separate scalable services — not a monolithic script.

```mermaid
flowchart TB
    subgraph Ingestion
        P[Parser]
        CH[Chunker]
        E[Embedder]
        I[Index Writer]
    end
    subgraph Query
        Q[Query API]
        HR[Hybrid Retriever]
        RR[Reranker]
        GA[Context Assembler]
        GW[LLM Gateway]
    end
    subgraph Storage
        VS[(Vector Index)]
        MD[(Metadata DB)]
    end
    P --> CH --> E --> I
    I --> VS & MD
    Q --> HR
    VS --> HR
    MD --> HR
    HR --> RR --> GA --> GW
```

## Ingestion Flow

```mermaid
sequenceDiagram
    participant S as Source
    participant I as Ingest Worker
    participant E as Embedder
    participant V as Vector Store

    S->>I: document blob
    I->>I: parse + chunk
    I->>E: batch embed
    E-->>I: vectors
    I->>V: upsert(chunks, metadata)
```

## Retrieval Fusion

```
score = α * cosine_sim + (1-α) * bm25_norm
top_k → reranker → top_n for context
```

Document α tuning and per-collection overrides.

## Safety and Quality

| Concern | Mitigation |
|---------|------------|
| Tenant isolation | Metadata filter on every query |
| Hallucination | Citations required; faithfulness eval |
| Prompt injection | Delimiter wrapping retrieved chunks |
| Cost runaway | Token budget + gateway limits |

## Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| `Chunker` | Split docs with overlap |
| `EmbeddingClient` | Vectorize text |
| `VectorStore` | Similarity + metadata filter |
| `BM25Index` | Lexical search |
| `LLMGateway` | Model call with resilience |
| `EvalHarness` | recall@k stub |

## Docker Topology

`postgres` with pgvector extension (optional), `redis` for embedding cache.

## Related Documentation

- [RAG Architecture](/docs/ai-distributed-systems/rag-architecture)
- [Distributed Training and Inference](/docs/ai-distributed-systems/distributed-training-and-inference)
