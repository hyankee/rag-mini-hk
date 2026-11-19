from fastapi.testclient import TestClient

from app import api
from app.answer import AnswerResult
from app.store import SearchHit


def make_hit() -> SearchHit:
    return SearchHit(
        score=0.88,
        chunk_id="demo-001-01",
        doc_id="demo-001",
        title="演示文档",
        industry="demo",
        version="2026-11-19",
        section="3. 常见岗位",
        text="示例证据。",
    )


class FakeStore:
    def __init__(self, count: int) -> None:
        self._count = count

    def count(self) -> int:
        return self._count


class FakeRetriever:
    def __init__(self, count: int) -> None:
        self.store = FakeStore(count)


def test_health(monkeypatch) -> None:
    monkeypatch.setattr(api, "get_retriever", lambda: FakeRetriever(1))
    client = TestClient(api.app)

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"
    assert response.json()["chunks"] == 1


def test_ask_returns_sources(monkeypatch) -> None:
    def fake_answer(question: str, retriever, top_k: int):
        return AnswerResult(
            answer="答案：示例。[S1]",
            sources=[make_hit()],
            mode="generated",
            citations=[1],
        )

    monkeypatch.setattr(api, "get_retriever", lambda: FakeRetriever(1))
    monkeypatch.setattr(api, "answer_question", fake_answer)
    client = TestClient(api.app)

    response = client.post("/api/ask", json={"question": "示例问题", "top_k": 3})

    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == "答案：示例。[S1]"
    assert body["sources"][0]["chunk_id"] == "demo-001-01"
    assert body["sources"][0]["rank"] == 1


def test_ask_rejects_empty_index(monkeypatch) -> None:
    monkeypatch.setattr(api, "get_retriever", lambda: FakeRetriever(0))
    client = TestClient(api.app)

    response = client.post("/api/ask", json={"question": "示例问题"})

    assert response.status_code == 503


def test_ask_validates_top_k(monkeypatch) -> None:
    monkeypatch.setattr(api, "get_retriever", lambda: FakeRetriever(1))
    client = TestClient(api.app)

    response = client.post("/api/ask", json={"question": "示例问题", "top_k": 99})

    assert response.status_code == 422
