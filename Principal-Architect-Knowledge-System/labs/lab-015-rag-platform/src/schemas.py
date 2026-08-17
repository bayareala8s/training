"""Pydantic schemas for Lab 015 API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class DocumentIngestRequest(BaseModel):
    doc_id: str
    tenant_id: str = "default"
    text: str | None = None
    path: str | None = None


class DocumentIngestResponse(BaseModel):
    doc_id: str
    tenant_id: str
    chunks_ingested: int


class DocumentSummary(BaseModel):
    doc_id: str
    tenant_id: str
    chunk_count: int


class DocumentsListResponse(BaseModel):
    documents: list[DocumentSummary]
    total_chunks: int


class QueryRequest(BaseModel):
    question: str
    tenant_id: str = "default"
    top_k: int = 5


class QueryCitation(BaseModel):
    chunk_id: str
    doc_id: str
    text: str
    score: float | None = None


class QueryResponse(BaseModel):
    question: str
    answer: str
    citations: list[QueryCitation]
