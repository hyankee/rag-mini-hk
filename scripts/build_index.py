"""Build the Chroma index from Markdown documents."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.chunking import chunk_documents
from app.config import CHROMA_DIR, COLLECTION_NAME, DATA_DIR, EMBED_MODEL
from app.store import VectorStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the RAG Mini HK index")
    parser.add_argument("--data-dir", type=Path, default=DATA_DIR)
    parser.add_argument("--chroma-dir", type=Path, default=CHROMA_DIR)
    parser.add_argument("--collection", default=COLLECTION_NAME)
    parser.add_argument("--model", default=EMBED_MODEL)
    parser.add_argument("--reset", action="store_true", help="Delete the old collection first")
    args = parser.parse_args()

    chunks = chunk_documents(args.data_dir)
    store = VectorStore(
        path=args.chroma_dir,
        collection_name=args.collection,
        model_name=args.model,
    )
    if args.reset:
        store.reset()

    count = store.build(chunks)
    print(f"Indexed {len(chunks)} chunks into {args.chroma_dir} ({count} rows in collection)")


if __name__ == "__main__":
    main()

