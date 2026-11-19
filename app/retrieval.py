"""Thin retriever interface used by the answer and evaluation layers."""

from __future__ import annotations

from app.config import DEFAULT_TOP_K
from app.store import SearchHit, VectorStore


class Retriever:
    def __init__(self, store: VectorStore) -> None:
        self.store = store

    def search(self, question: str, top_k: int = DEFAULT_TOP_K) -> list[SearchHit]:
        return self.store.search(question, top_k=top_k)

