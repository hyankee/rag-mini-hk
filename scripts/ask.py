"""Ask one question from the command line."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.answer import answer_question
from app.config import DEFAULT_TOP_K
from app.retrieval import Retriever
from app.store import VectorStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask the RAG Mini HK index")
    parser.add_argument("question", nargs="+", help="Question text")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--retrieval-only", action="store_true", help="Skip the LLM call")
    args = parser.parse_args()

    question = " ".join(args.question)
    result = answer_question(
        question,
        Retriever(VectorStore()),
        top_k=args.top_k,
        force_retrieval_only=args.retrieval_only,
    )
    print(f"Mode: {result.mode}")
    print(f"\n{result.answer}\n")
    for index, hit in enumerate(result.sources, start=1):
        print(f"[S{index}] cosine={hit.score:.4f} | {hit.doc_id} | {hit.section}")


if __name__ == "__main__":
    main()

