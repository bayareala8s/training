"""Tests for Lab 015: RAG Platform."""

import sys
from pathlib import Path

from fastapi.testclient import TestClient

LAB_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(LAB_ROOT))

from src.api import create_app  # noqa: E402
from src.main import Chunk, Chunker, EmbeddingClient, HybridRetriever, LLMGateway, VectorStore  # noqa: E402
from src.service import RagService  # noqa: E402


def test_chunking_overlap():
    chunker = Chunker(chunk_size=20, overlap=5)
    chunks = chunker.chunk("doc1", "t1", "abcdefghijklmnopqrstuvwxyz")
    assert len(chunks) >= 2
    assert chunks[0].text != chunks[1].text


def test_vector_search():
    store = VectorStore()
    embedder = EmbeddingClient()
    from src.main import Chunk

    c1 = Chunk("c1", "d1", "t1", "quorum systems", embedding=embedder.embed(["quorum"])[0])
    c2 = Chunk("c2", "d1", "t1", "unrelated topic", embedding=embedder.embed(["weather"])[0])
    store.upsert([c1, c2])
    hits = store.search(embedder.embed(["quorum replication"])[0], "t1", top_k=1)
    assert hits[0].chunk_id == "c1"


def test_hybrid_fusion():
    store = VectorStore()
    embedder = EmbeddingClient()
    from src.main import Chunk

    c1 = Chunk("c1", "d1", "t1", "distributed quorum", embedding=embedder.embed(["quorum"])[0])
    store.upsert([c1])
    retriever = HybridRetriever(store)
    hits = retriever.retrieve("quorum", "t1")
    assert hits


def test_tenant_filter():
    store = VectorStore()
    embedder = EmbeddingClient()
    from src.main import Chunk

    c1 = Chunk("c1", "d1", "tenant-a", "data", embedding=embedder.embed(["data"])[0])
    store.upsert([c1])
    assert store.search(embedder.embed(["data"])[0], "tenant-b", top_k=5) == []


def test_citation_in_response():
    gateway = LLMGateway()
    response = gateway.generate("Context [chunk-1] [chunk-2]\nQ: test")
    assert "chunk-1" in response


def test_embedding_client_deterministic():
    client = EmbeddingClient()
    v1 = client.embed(["hello"])
    v2 = client.embed(["hello"])
    assert v1 == v2


def test_chunker_defaults():
    c = Chunker()
    assert c.chunk_size == 512
    assert c.overlap == 64


def test_rag_service_ingest_and_query():
    rag = RagService()
    count = rag.ingest_text("doc1", "t1", "distributed quorum replication systems")
    assert count >= 1
    result = rag.query("quorum", "t1")
    assert "quorum" in result["answer"].lower() or result["citations"]


def test_api_ingest_list_query():
    client = TestClient(create_app())
    assert client.get("/health").json()["status"] == "ok"
    ingest = client.post(
        "/v1/documents",
        json={
            "doc_id": "quorum",
            "tenant_id": "default",
            "text": "Quorum replication requires overlapping read and write sets.",
        },
    )
    assert ingest.status_code == 201
    docs = client.get("/v1/documents").json()
    assert docs["total_chunks"] >= 1
    query = client.post(
        "/v1/query",
        json={"question": "What is quorum replication?", "tenant_id": "default"},
    )
    assert query.status_code == 200
    data = query.json()
    assert data["answer"]
    assert len(data["citations"]) >= 1
