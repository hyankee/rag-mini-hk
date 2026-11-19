from pathlib import Path

from app.chunking import chunk_documents, parse_front_matter, split_sections


SAMPLE = """---
doc_id: demo-001
title: 演示文档
industry: demo
version: 2026-11-19
---

# 演示文档

## 1. 背景

这是第一段正文，长度足够通过最小长度检查。

## 2. 方法

这是第二段正文，也足够长，用于验证切片和元数据。
"""


def test_parse_front_matter() -> None:
    metadata, body = parse_front_matter(SAMPLE)
    assert metadata["doc_id"] == "demo-001"
    assert metadata["industry"] == "demo"
    assert body.lstrip().startswith("# 演示文档")


def test_split_sections() -> None:
    _, body = parse_front_matter(SAMPLE)
    sections = list(split_sections(body))
    assert [heading for heading, _ in sections] == ["1. 背景", "2. 方法"]


def test_chunk_documents(tmp_path: Path) -> None:
    (tmp_path / "demo.md").write_text(SAMPLE, encoding="utf-8")

    chunks = chunk_documents(tmp_path)

    assert len(chunks) == 2
    assert chunks[0].chunk_id == "demo-001-01"
    assert chunks[0].doc_id == "demo-001"
    assert chunks[0].title == "演示文档"
    assert chunks[0].section == "1. 背景"
    assert "演示文档" in chunks[0].embedding_text
    assert "这是第一段正文" in chunks[0].embedding_text
