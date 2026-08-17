#!/usr/bin/env python3
"""Lab 015: RAG Platform — ingestion and retrieval."""

from __future__ import annotations

import argparse
import hashlib
import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    tenant_id: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)
    embedding: list[float] | None = None


@dataclass
class Chunker:
    chunk_size: int = 512
    overlap: int = 64

    def chunk(self, doc_id: str, tenant_id: str, text: str) -> list[Chunk]:
        if not text:
            return []
        chunks: list[Chunk] = []
        step = max(1, self.chunk_size - self.overlap)
        idx = 0
        pos = 0
        while pos < len(text):
            piece = text[pos : pos + self.chunk_size]
            chunks.append(
                Chunk(
                    chunk_id=f"{doc_id}:{idx}",
                    doc_id=doc_id,
                    tenant_id=tenant_id,
                    text=piece,
                    metadata={"offset": pos},
                )
            )
            pos += step
            idx += 1
        return chunks


class EmbeddingClient:
    def embed(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for t in texts:
            vec = [0.0] * 32
            for word in re.findall(r"\w+", t.lower()):
                bucket = int(hashlib.md5(word.encode()).hexdigest(), 16) % 32
                vec[bucket] += 1.0
            norm = math.sqrt(sum(x * x for x in vec)) or 1.0
            vectors.append([x / norm for x in vec])
        return vectors


@dataclass
class VectorStore:
    chunks: dict[str, Chunk] = field(default_factory=dict)

    def upsert(self, chunks: list[Chunk]) -> int:
        for chunk in chunks:
            self.chunks[chunk.chunk_id] = chunk
        return len(chunks)

    def search(
        self,
        query_embedding: list[float],
        tenant_id: str,
        top_k: int = 5,
    ) -> list[Chunk]:
        scored: list[tuple[float, Chunk]] = []
        for chunk in self.chunks.values():
            if chunk.tenant_id != tenant_id or chunk.embedding is None:
                continue
            dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(query_embedding, chunk.embedding)))
            scored.append((dist, chunk))
        scored.sort(key=lambda x: x[0])
        return [c for _, c in scored[:top_k]]


class HybridRetriever:
    def __init__(self, vector_store: VectorStore, alpha: float = 0.7) -> None:
        self.vector_store = vector_store
        self.alpha = alpha
        self.embedder = EmbeddingClient()

    def _bm25_score(self, query: str, text: str) -> float:
        terms = set(re.findall(r"\w+", query.lower()))
        words = re.findall(r"\w+", text.lower())
        if not words:
            return 0.0
        hits = sum(1 for w in words if w in terms)
        return hits / len(words)

    def retrieve(self, query: str, tenant_id: str, top_k: int = 5) -> list[Chunk]:
        query_emb = self.embedder.embed([query])[0]
        vector_hits = self.vector_store.search(query_emb, tenant_id, top_k=top_k * 2)
        scored: list[tuple[float, Chunk]] = []
        for chunk in vector_hits:
            vec_score = 1.0 / (1.0 + math.sqrt(sum((a - b) ** 2 for a, b in zip(query_emb, chunk.embedding or []))))
            bm25 = self._bm25_score(query, chunk.text)
            scored.append((self.alpha * vec_score + (1 - self.alpha) * bm25, chunk))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in scored[:top_k]]


class LLMGateway:
    def generate(self, prompt: str, max_tokens: int = 512) -> str:
        citations = re.findall(r"\[([^\]]+)\]", prompt)
        cite_str = ", ".join(citations) if citations else "no citations"
        return f"Answer based on context. Sources: {cite_str}"[:max_tokens]


def ingest_path(path: Path, tenant_id: str, store: VectorStore | None = None) -> int:
    store = store or VectorStore()
    embedder = EmbeddingClient()
    chunker = Chunker(chunk_size=128, overlap=32)
    text = path.read_text(encoding="utf-8")
    chunks = chunker.chunk(path.stem, tenant_id, text)
    embeddings = embedder.embed([c.text for c in chunks])
    for chunk, emb in zip(chunks, embeddings):
        chunk.embedding = emb
    return store.upsert(chunks)


def run_query(query: str, tenant_id: str, store: VectorStore) -> str:
    retriever = HybridRetriever(store)
    chunks = retriever.retrieve(query, tenant_id)
    context = "\n".join(f"[{c.chunk_id}] {c.text}" for c in chunks)
    gateway = LLMGateway()
    return gateway.generate(f"Context:\n{context}\n\nQ: {query}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Lab 015: RAG Platform")
    parser.add_argument("--ingest", type=Path)
    parser.add_argument("--tenant", default="default")
    parser.add_argument("--query", type=str)
    parser.add_argument("--inject", choices=["embedding-timeout", "llm-timeout"])
    parser.add_argument("--serve", action="store_true", help="Start API on :8105")
    parser.add_argument("--port", type=int, default=8105)
    args = parser.parse_args()
    if args.inject:
        print(f"Injection {args.inject}")
        return 0
    if args.serve:
        import uvicorn

        from .api import create_app

        uvicorn.run(create_app(), host="0.0.0.0", port=args.port)
        return 0
    if args.ingest:
        print(f"Ingested {ingest_path(args.ingest, args.tenant)} chunks")
    elif args.query:
        store = VectorStore()
        print(run_query(args.query, args.tenant, store))
    else:
        print("Use --ingest, --query, or --serve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
