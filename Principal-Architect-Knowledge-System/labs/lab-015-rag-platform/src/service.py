"""RAG platform service layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .main import (
    Chunker,
    EmbeddingClient,
    HybridRetriever,
    LLMGateway,
    VectorStore,
)


@dataclass
class DocumentRecord:
    doc_id: str
    tenant_id: str
    chunk_count: int


@dataclass
class RagService:
    store: VectorStore = field(default_factory=VectorStore)
    chunker: Chunker = field(default_factory=lambda: Chunker(chunk_size=128, overlap=32))
    embedder: EmbeddingClient = field(default_factory=EmbeddingClient)
    retriever: HybridRetriever | None = None
    gateway: LLMGateway = field(default_factory=LLMGateway)
    documents: dict[str, DocumentRecord] = field(default_factory=dict)
    lab_root: Path = field(default_factory=lambda: Path(__file__).resolve().parent.parent)

    def _ensure_retriever(self) -> HybridRetriever:
        if self.retriever is None:
            self.retriever = HybridRetriever(self.store)
        return self.retriever

    def ingest_text(self, doc_id: str, tenant_id: str, text: str) -> int:
        chunks = self.chunker.chunk(doc_id, tenant_id, text)
        embeddings = self.embedder.embed([c.text for c in chunks])
        for chunk, emb in zip(chunks, embeddings):
            chunk.embedding = emb
        count = self.store.upsert(chunks)
        self.documents[doc_id] = DocumentRecord(doc_id, tenant_id, count)
        return count

    def ingest_from_path(self, doc_id: str, tenant_id: str, path: Path) -> int:
        text = path.read_text(encoding="utf-8")
        return self.ingest_text(doc_id, tenant_id, text)

    def ingest_document(self, doc_id: str, tenant_id: str, text: str | None, path: str | None) -> int:
        if text is not None:
            return self.ingest_text(doc_id, tenant_id, text)
        if path is not None:
            file_path = Path(path)
            if not file_path.is_absolute():
                file_path = self.lab_root / path
            if not file_path.exists():
                raise FileNotFoundError(f"path not found: {path}")
            return self.ingest_from_path(doc_id, tenant_id, file_path)
        raise ValueError("provide text or path")

    def list_documents(self) -> list[DocumentRecord]:
        return list(self.documents.values())

    def query(self, question: str, tenant_id: str, top_k: int = 5) -> dict[str, Any]:
        retriever = self._ensure_retriever()
        chunks = retriever.retrieve(question, tenant_id, top_k=top_k)
        context = "\n".join(f"[{c.chunk_id}] {c.text}" for c in chunks)
        answer = self.gateway.generate(f"Context:\n{context}\n\nQ: {question}")
        citations = [
            {
                "chunk_id": c.chunk_id,
                "doc_id": c.doc_id,
                "text": c.text,
            }
            for c in chunks
        ]
        return {
            "question": question,
            "answer": answer,
            "citations": citations,
        }

    def stats(self) -> dict[str, Any]:
        return {
            "documents": len(self.documents),
            "total_chunks": len(self.store.chunks),
        }
