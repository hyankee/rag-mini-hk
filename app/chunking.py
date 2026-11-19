"""Turn Markdown documents into section-level chunks with metadata."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from app.config import DATA_DIR


@dataclass(frozen=True, slots=True)
class Chunk:
    chunk_id: str
    doc_id: str
    title: str
    industry: str
    version: str
    section: str
    text: str

    @property
    def embedding_text(self) -> str:
        """Text used for semantic embedding.

        Identifiers stay in metadata instead of the embedding text so that
        exact IDs do not become noise in the dense vector.
        """

        return "\n".join([self.title, self.section, self.text]).strip()

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    """Parse the simple key/value YAML front matter used in this corpus."""

    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    metadata: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata, parts[2]


def split_sections(body: str):
    """Yield (heading, section text) for each level-2 Markdown heading."""

    current_section = "开头"
    buffer: list[str] = []

    for line in body.splitlines():
        if line.startswith("## "):
            text = "\n".join(buffer).strip()
            if text and current_section != "开头":
                yield current_section, text
            current_section = line[3:].strip()
            buffer = []
        else:
            buffer.append(line)

    text = "\n".join(buffer).strip()
    if text and current_section != "开头":
        yield current_section, text


def chunk_documents(data_dir: Path = DATA_DIR) -> list[Chunk]:
    """Read all Markdown files in a directory and return section-level chunks."""

    chunks: list[Chunk] = []
    for path in sorted(Path(data_dir).glob("*.md")):
        text = path.read_text(encoding="utf-8")
        metadata, body = parse_front_matter(text)
        doc_id = metadata.get("doc_id", path.stem)

        for index, (section, section_text) in enumerate(split_sections(body), start=1):
            if len(section_text) < 20:
                continue
            chunks.append(
                Chunk(
                    chunk_id=f"{doc_id}-{index:02d}",
                    doc_id=doc_id,
                    title=metadata.get("title", path.stem),
                    industry=metadata.get("industry", "unknown"),
                    version=metadata.get("version", "unknown"),
                    section=section,
                    text=section_text,
                )
            )
    return chunks

