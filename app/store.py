"""Chroma-backed vector store with lazy model loading."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from app.chunking import Chunk
from app.config import CHROMA_DIR, COLLECTION_NAME, EMBED_DEVICE, EMBED_MODEL


@dataclass(frozen=True, slots=True)
class SearchHit:
    score: float
    chunk_id: str
    doc_id: str
    title: str
    industry: str
    version: str
    section: str
    text: str


class VectorStore:
    """A small, persistent Chroma collection.

    The embedding model is loaded lazily so health checks and unit tests do
    not need to pay the model-loading cost.
    """

    def __init__(
        self,
        path: Path = CHROMA_DIR,
        collection_name: str = COLLECTION_NAME,
        model_name: str = EMBED_MODEL,
        device: str = EMBED_DEVICE,
    ) -> None:
        import chromadb

        self._path = Path(path)
        self._collection_name = collection_name
        self._model_name = model_name
        self._device = device
        self._client = chromadb.PersistentClient(path=str(self._path))
        self._collection = self._open_collection()
        self._model = None

    def _open_collection(self):
        return self._client.get_or_create_collection(
            name=self._collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    @property
    def model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self._model_name, device=self._device)
        return self._model

    def count(self) -> int:
        return self._collection.count()

    def reset(self) -> None:
        try:
            self._client.delete_collection(self._collection_name)
        except Exception:
            pass
        self._collection = self._open_collection()

    def build(self, chunks: Iterable[Chunk]) -> int:
        rows = list(chunks)
        if not rows:
            raise ValueError("No chunks to index. Check the data directory.")

        vectors = self.model.encode(
            [chunk.embedding_text for chunk in rows],
            batch_size=16,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        self._collection.upsert(
            ids=[chunk.chunk_id for chunk in rows],
            embeddings=[vector.tolist() for vector in vectors],
            documents=[chunk.text for chunk in rows],
            metadatas=[
                {
                    "chunk_id": chunk.chunk_id,
                    "doc_id": chunk.doc_id,
                    "title": chunk.title,
                    "industry": chunk.industry,
                    "version": chunk.version,
                    "section": chunk.section,
                }
                for chunk in rows
            ],
        )
        return self.count()

    def search(self, query: str, top_k: int = 3) -> list[SearchHit]:
        count = self.count()
        if count == 0:
            return []

        query_vector = self.model.encode(
            [query],
            normalize_embeddings=True,
        )[0].tolist()
        result = self._collection.query(
            query_embeddings=[query_vector],
            n_results=min(top_k, count),
            include=["documents", "metadatas", "distances"],
        )

        hits: list[SearchHit] = []
        for chunk_id, document, metadata, distance in zip(
            result["ids"][0],
            result["documents"][0],
            result["metadatas"][0],
            result["distances"][0],
        ):
            metadata = metadata or {}
            hits.append(
                SearchHit(
                    score=1.0 - float(distance),
                    chunk_id=chunk_id,
                    doc_id=metadata.get("doc_id", "unknown"),
                    title=metadata.get("title", "unknown"),
                    industry=metadata.get("industry", "unknown"),
                    version=metadata.get("version", "unknown"),
                    section=metadata.get("section", "unknown"),
                    text=document or "",
                )
            )
        return hits

