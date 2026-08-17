# Lab 015: Requirements

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Document ingestion CLI | Must |
| FR-2 | Chunking with overlap | Must |
| FR-3 | Vector upsert and search | Must |
| FR-4 | Hybrid retrieval fusion | Must |
| FR-5 | Query API with citations | Must |
| FR-6 | Tenant metadata filter | Must |
| FR-7 | LLM gateway stub | Should |
| FR-8 | Eval recall@k harness | Should |

## Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Retrieval p99 (local, 1k chunks) | < 100ms |
| NFR-2 | Ingest throughput | 100 docs/min local |
| NFR-3 | No cross-tenant leakage | 0 tolerance |

## Acceptance Criteria

### AC-1: Retrieval

Known query retrieves expected chunk in top-3.

### AC-2: Hybrid

Keyword-heavy query finds doc missed by pure vector (controlled fixture).

### AC-3: Tenant isolation

Tenant A query never returns Tenant B chunks.

## Out of Scope

- Production cross-encoder reranker training
- Multi-modal (image) ingestion
- Federated search across regions

## Related Documentation

- [LLM Serving and Model Gateways](/docs/ai-distributed-systems/llm-serving-and-model-gateways)
