from app.evaluation import EvalQuestion, load_questions, retrieval_status
from app.store import SearchHit


def hit(doc_id: str, section: str) -> SearchHit:
    return SearchHit(
        score=0.8,
        chunk_id=f"{doc_id}-{section}",
        doc_id=doc_id,
        title="t",
        industry="i",
        version="v",
        section=section,
        text="x",
    )


QUESTION = EvalQuestion("Q1", "问题", doc_id="doc-a", sections=(3, 4))


def test_status_strict_when_all_sections_hit() -> None:
    hits = [hit("doc-a", "3. 岗位"), hit("doc-a", "4. 应用")]
    assert retrieval_status(QUESTION, hits) == "是（2/2）"


def test_status_partial_when_one_section_hit() -> None:
    assert retrieval_status(QUESTION, [hit("doc-a", "3. 岗位")]) == "部分（1/2）"


def test_status_miss_when_wrong_document() -> None:
    assert retrieval_status(QUESTION, [hit("doc-b", "3. 岗位")]) == "否（0/2）"


def test_refusal_questions_are_not_scored() -> None:
    question = EvalQuestion("Q8", "无法回答的问题", expect_refusal=True)
    assert retrieval_status(question, []) == "—"


def test_default_question_set_has_twelve_rows() -> None:
    questions = load_questions()
    assert len(questions) == 12
    assert [q.qid for q in questions] == [f"Q{i}" for i in range(1, 13)]
