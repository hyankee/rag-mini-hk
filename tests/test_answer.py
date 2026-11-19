from app.answer import (
    REFUSAL_TEXT,
    answer_question,
    build_evidence,
    extract_citations,
)
from app.store import SearchHit


def make_hit(index: int, section: str = "3. 常见岗位") -> SearchHit:
    return SearchHit(
        score=0.9 - index * 0.01,
        chunk_id=f"doc-{index:02d}",
        doc_id="demo-001",
        title="演示文档",
        industry="demo",
        version="2026-11-19",
        section=section,
        text=f"第 {index} 段证据。",
    )


class FakeRetriever:
    def __init__(self, hits: list[SearchHit]) -> None:
        self.hits = hits

    def search(self, question: str, top_k: int = 3) -> list[SearchHit]:
        return self.hits[:top_k]


def test_build_evidence_numbers_sources() -> None:
    evidence = build_evidence([make_hit(1), make_hit(2)])
    assert "[S1]" in evidence
    assert "[S2]" in evidence
    assert "doc_id=demo-001" in evidence


def test_extract_citations_deduplicates() -> None:
    assert extract_citations("结论 [S1]，补充 [S2]，重复 [S1]。") == [1, 2]


def test_answer_question_returns_generated_answer_and_sources() -> None:
    result = answer_question(
        "演示问题",
        FakeRetriever([make_hit(1)]),
        model_call=lambda messages: "答案：有证据。[S1]",
    )

    assert result.mode == "generated"
    assert result.citations == [1]
    assert result.invalid_citations == []
    assert result.sources[0].chunk_id == "doc-01"


def test_answer_question_refuses_without_hits() -> None:
    result = answer_question("演示问题", FakeRetriever([]))

    assert result.mode == "refusal"
    assert result.answer.startswith(REFUSAL_TEXT)
    assert result.sources == []


def test_answer_question_can_run_without_llm() -> None:
    result = answer_question(
        "演示问题",
        FakeRetriever([make_hit(1)]),
        force_retrieval_only=True,
    )

    assert result.mode == "retrieval_only"
    assert result.sources
