"""Run the fixed 12-question retrieval evaluation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.config import DEFAULT_TOP_K, QUESTIONS_FILE
from app.evaluation import evaluate_retrieval, load_questions, to_markdown
from app.retrieval import Retriever
from app.store import VectorStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate retrieval only")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--questions", type=Path, default=QUESTIONS_FILE)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    retriever = Retriever(VectorStore())
    if retriever.store.count() == 0:
        raise SystemExit("Index is empty. Run: python scripts/build_index.py")

    rows = evaluate_retrieval(retriever, load_questions(args.questions), top_k=args.top_k)
    report = to_markdown(rows, top_k=args.top_k)
    print(report)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()

