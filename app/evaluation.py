"""Retrieval-only evaluation over a fixed question set."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from app.config import QUESTIONS_FILE
from app.store import SearchHit


@dataclass(frozen=True, slots=True)
class EvalQuestion:
    qid: str
    question: str
    doc_id: str | None = None
    sections: tuple[int, ...] = ()
    expect_refusal: bool = False
    note: str = ""


@dataclass(frozen=True, slots=True)
class EvalRow:
    question: EvalQuestion
    results: list[SearchHit]
    status: str


def load_questions(path: Path = QUESTIONS_FILE) -> list[EvalQuestion]:
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    return [
        EvalQuestion(
            qid=row["qid"],
            question=row["question"],
            doc_id=row.get("doc_id"),
            sections=tuple(row.get("sections", [])),
            expect_refusal=bool(row.get("expect_refusal", False)),
            note=row.get("note", ""),
        )
        for row in rows
    ]


def section_number(section: str) -> int | None:
    match = re.match(r"\s*(\d+)\s*[.．、]", section)
    return int(match.group(1)) if match else None


def retrieval_status(question: EvalQuestion, hits: list[SearchHit]) -> str:
    if question.expect_refusal or not question.doc_id:
        return "—"

    if not question.sections:
        found = any(hit.doc_id == question.doc_id for hit in hits)
        return "是（文档命中）" if found else "否"

    matched = {
        section_number(hit.section)
        for hit in hits
        if hit.doc_id == question.doc_id
    }
    got = len(matched & set(question.sections))
    total = len(question.sections)
    if got == total:
        return f"是（{got}/{total}）"
    if got:
        return f"部分（{got}/{total}）"
    return f"否（0/{total}）"


def source_cell(hits: list[SearchHit]) -> str:
    if not hits:
        return "—"
    return "；".join(
        f"[S{index}] {hit.doc_id} §{section_number(hit.section)}"
        if section_number(hit.section) is not None
        else f"[S{index}] {hit.doc_id} {hit.section}"
        for index, hit in enumerate(hits, start=1)
    )


def evaluate_retrieval(retriever, questions: list[EvalQuestion], top_k: int = 3) -> list[EvalRow]:
    rows: list[EvalRow] = []
    for question in questions:
        hits = retriever.search(question.question, top_k=top_k)
        rows.append(
            EvalRow(
                question=question,
                results=hits,
                status=retrieval_status(question, hits),
            )
        )
    return rows


def summarize(rows: list[EvalRow]) -> dict[str, int]:
    answerable = [row for row in rows if not row.question.expect_refusal and row.question.doc_id]
    strict = sum(row.status.startswith("是") for row in answerable)
    loose = sum(not row.status.startswith("否") for row in answerable)
    return {"strict": strict, "loose": loose, "total": len(answerable)}


def to_markdown(rows: list[EvalRow], top_k: int = 3) -> str:
    summary = summarize(rows)
    lines = [
        "# Retrieval Evaluation",
        "",
        f"- Fixed `top_k={top_k}`; {len(rows)} questions.",
        f"- Strict hit@k: **{summary['strict']}/{summary['total']}**",
        f"- Loose hit@k: **{summary['loose']}/{summary['total']}**",
        "",
        "| ID | Question | Top-k sources | Status |",
        "|---|---|---|---|",
    ]
    for row in rows:
        question = row.question.question.replace("|", r"\|")
        lines.append(
            f"| {row.question.qid} | {question} | {source_cell(row.results)} | {row.status} |"
        )
    lines.extend(
        [
            "",
            "> Strict means every expected section is in top-k. Loose means at least one is.",
            "> This report evaluates retrieval only; it does not claim answer quality.",
        ]
    )
    return "\n".join(lines) + "\n"

