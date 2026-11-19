"""FastAPI application for the RAG Mini HK demo."""

from __future__ import annotations

from functools import lru_cache
from time import perf_counter

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app.answer import answer_question
from app.config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_MODEL,
    DEFAULT_TOP_K,
    EMBED_MODEL,
    MAX_QUESTION_CHARS,
)
from app.retrieval import Retriever
from app.store import VectorStore
from app.web import INDEX_HTML


app = FastAPI(title="RAG Mini HK", version="1.0.0")


class AskRequest(BaseModel):
    question: str = Field(min_length=2, max_length=MAX_QUESTION_CHARS)
    top_k: int = Field(default=DEFAULT_TOP_K, ge=1, le=8)


class SourceOut(BaseModel):
    rank: int
    score: float
    chunk_id: str
    doc_id: str
    title: str
    industry: str
    version: str
    section: str
    text: str


class AskResponse(BaseModel):
    answer: str
    mode: str
    sources: list[SourceOut]
    citations: list[int]
    invalid_citations: list[int]
    latency_ms: int


@lru_cache(maxsize=1)
def get_retriever() -> Retriever:
    return Retriever(VectorStore())


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return INDEX_HTML


@app.get("/api/health")
def health() -> dict[str, object]:
    retriever = get_retriever()
    count = retriever.store.count()
    return {
        "status": "ready" if count else "empty",
        "chunks": count,
        "embed_model": EMBED_MODEL,
        "llm_mode": DEEPSEEK_MODEL if DEEPSEEK_API_KEY else "retrieval-only",
    }


@app.post("/api/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    retriever = get_retriever()
    if retriever.store.count() == 0:
        raise HTTPException(
            status_code=503,
            detail="索引为空。请先运行 python scripts/build_index.py。",
        )

    started = perf_counter()
    try:
        result = answer_question(
            request.question,
            retriever,
            top_k=request.top_k,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"生成模型调用失败：{exc}") from exc

    return AskResponse(
        answer=result.answer,
        mode=result.mode,
        sources=[
            SourceOut(
                rank=index,
                score=round(hit.score, 4),
                chunk_id=hit.chunk_id,
                doc_id=hit.doc_id,
                title=hit.title,
                industry=hit.industry,
                version=hit.version,
                section=hit.section,
                text=hit.text,
            )
            for index, hit in enumerate(result.sources, start=1)
        ],
        citations=result.citations,
        invalid_citations=result.invalid_citations,
        latency_ms=round((perf_counter() - started) * 1000),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.api:app", host="127.0.0.1", port=8000, reload=False)

