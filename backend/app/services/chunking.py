from dataclasses import dataclass

from app.core.config import get_settings
from app.services.pdf_extract import PageText
from app.utils.text_clean import clean_text


@dataclass
class TextChunk:
    chunk_index: int
    page_number: int | None
    section_name: str | None
    content: str


def _chunk_limits() -> tuple[int, int]:
    settings = get_settings()
    return settings.ingest_chunk_max_chars, settings.ingest_chunk_overlap_chars


def _looks_like_heading(text: str) -> bool:
    line = text.split("\n", 1)[0].strip()
    return len(line) <= 100 and not line.endswith((".", ",", ";"))


def _split_paragraphs(text: str) -> list[str]:
    return [part.strip() for part in text.split("\n\n") if part.strip()]


def _hard_split(text: str, max_chars: int, overlap: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]

    pieces: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        pieces.append(text[start:end].strip())
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return [piece for piece in pieces if piece]


def chunk_pages(pages: list[PageText]) -> list[TextChunk]:
    max_chars, overlap_chars = _chunk_limits()
    chunks: list[TextChunk] = []
    chunk_index = 0

    for page in pages:
        text = clean_text(page.text)
        if not text:
            continue

        section_name: str | None = None
        buffer = ""

        for paragraph in _split_paragraphs(text):
            if _looks_like_heading(paragraph):
                section_name = paragraph.split("\n", 1)[0][:255]

            combined = f"{buffer}\n\n{paragraph}".strip() if buffer else paragraph

            if len(combined) <= max_chars:
                buffer = combined
                continue

            if buffer:
                chunks.append(
                    TextChunk(
                        chunk_index=chunk_index,
                        page_number=page.page_number,
                        section_name=section_name,
                        content=buffer,
                    )
                )
                chunk_index += 1
                overlap = buffer[-overlap_chars:] if len(buffer) > overlap_chars else buffer
                buffer = f"{overlap}\n\n{paragraph}".strip()
                if len(buffer) > max_chars:
                    for piece in _hard_split(buffer, max_chars, overlap_chars):
                        chunks.append(
                            TextChunk(
                                chunk_index=chunk_index,
                                page_number=page.page_number,
                                section_name=section_name,
                                content=piece,
                            )
                        )
                        chunk_index += 1
                    buffer = ""
            else:
                for piece in _hard_split(paragraph, max_chars, overlap_chars):
                    chunks.append(
                        TextChunk(
                            chunk_index=chunk_index,
                            page_number=page.page_number,
                            section_name=section_name,
                            content=piece,
                        )
                    )
                    chunk_index += 1

        if buffer:
            chunks.append(
                TextChunk(
                    chunk_index=chunk_index,
                    page_number=page.page_number,
                    section_name=section_name,
                    content=buffer,
                )
            )
            chunk_index += 1

    return chunks
