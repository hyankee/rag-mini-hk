"""Build evidence-grounded answers with citations and a no-key fallback."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from app.config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    DEEPSEEK_MODEL,
    DEFAULT_TOP_K,
)
from app.store import SearchHit


REFUSAL_TEXT = "资料中无法确认"

SYSTEM_PROMPT = (
    "你是一个严谨的资料问答助手。"
    "只能使用 <evidence> 中的内容回答，不得使用外部知识。"
    "每个事实性结论后必须标注证据编号，例如 [S1]；不要编造证据编号。"
    "如果证据不足以回答，第一行必须写“资料中无法确认”，然后说明缺少什么证据。"
    "检索到了相关片段，不代表片段回答了问题。"
)


@dataclass(slots=True)
class AnswerResult:
    answer: str
    sources: list[SearchHit] = field(default_factory=list)
    mode: str = "generated"
    citations: list[int] = field(default_factory=list)
    invalid_citations: list[int] = field(default_factory=list)


def build_evidence(hits: list[SearchHit]) -> str:
    blocks: list[str] = []
    for index, hit in enumerate(hits, start=1):
        blocks.append(
            "\n".join(
                [
                    f"[S{index}]",
                    f"doc_id={hit.doc_id}",
                    f"title={hit.title}",
                    f"industry={hit.industry}",
                    f"version={hit.version}",
                    f"section={hit.section}",
                    f"text={hit.text}",
                ]
            )
        )
    return "\n\n".join(blocks)


def build_messages(question: str, evidence: str) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"<evidence>\n{evidence}\n</evidence>\n\n"
                f"<question>\n{question}\n</question>\n\n"
                "请按以下格式回答：\n答案：...\n引用：..."
            ),
        },
    ]


def extract_citations(answer: str) -> list[int]:
    return sorted({int(number) for number in re.findall(r"\[S(\d+)\]", answer)})


def create_deepseek_model_call():
    if not DEEPSEEK_API_KEY:
        raise RuntimeError("未配置 DEEPSEEK_API_KEY")

    from openai import OpenAI

    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

    def model_call(messages: list[dict[str, str]]) -> str:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=messages,
            stream=False,
        )
        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("模型没有返回文本内容")
        return content

    return model_call


def answer_question(
    question: str,
    retriever,
    top_k: int = DEFAULT_TOP_K,
    model_call=None,
    force_retrieval_only: bool = False,
) -> AnswerResult:
    hits = retriever.search(question, top_k=top_k)
    if not hits:
        return AnswerResult(
            answer="资料中无法确认：知识库中没有找到相关片段。",
            sources=[],
            mode="refusal",
        )

    if force_retrieval_only or (model_call is None and not DEEPSEEK_API_KEY):
        return AnswerResult(
            answer=(
                "当前未配置 DEEPSEEK_API_KEY，下面只展示检索到的证据，未调用生成模型。"
                "配置密钥后，同一套证据会交给模型生成带引用的回答。"
            ),
            sources=hits,
            mode="retrieval_only",
        )

    if model_call is None:
        model_call = create_deepseek_model_call()

    answer = model_call(build_messages(question, build_evidence(hits)))
    citations = extract_citations(answer)
    invalid = [number for number in citations if number < 1 or number > len(hits)]
    return AnswerResult(
        answer=answer,
        sources=hits,
        mode="generated",
        citations=citations,
        invalid_citations=invalid,
    )

