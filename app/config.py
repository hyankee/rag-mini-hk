"""Project configuration, loaded from environment variables when present."""

from __future__ import annotations

import os
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - dependency is optional for tests
    load_dotenv = None

if load_dotenv is not None:
    load_dotenv(ROOT_DIR / ".env")


DATA_DIR = Path(os.getenv("DATA_DIR", str(ROOT_DIR / "data" / "docs")))
QUESTIONS_FILE = Path(os.getenv("QUESTIONS_FILE", str(ROOT_DIR / "data" / "questions.json")))
CHROMA_DIR = Path(os.getenv("CHROMA_DIR", str(ROOT_DIR / "chroma_db")))

COLLECTION_NAME = os.getenv("COLLECTION_NAME", "rag_docs")
EMBED_MODEL = os.getenv("EMBED_MODEL", "BAAI/bge-small-zh-v1.5")
EMBED_DEVICE = os.getenv("EMBED_DEVICE", "cpu")
DEFAULT_TOP_K = int(os.getenv("TOP_K", "3"))
MAX_QUESTION_CHARS = 500

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

