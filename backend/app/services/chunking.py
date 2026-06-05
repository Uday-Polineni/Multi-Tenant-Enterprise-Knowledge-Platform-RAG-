from dataclasses import dataclass

from app.services.pdf_extract import PageText
from app.utils.text_clean import clean_text

MAX_CHUNK_CHARS = 2000
OVERLAP_CHARS = 150


@dataclass
class TextChunk:
    chunk_index: int
    page_number: int | None
    section_name: str | None
    content: str


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

            if len(combined) <= MAX_CHUNK_CHARS:
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
                overlap = buffer[-OVERLAP_CHARS:] if len(buffer) > OVERLAP_CHARS else buffer
                buffer = f"{overlap}\n\n{paragraph}".strip()
                if len(buffer) > MAX_CHUNK_CHARS:
                    for piece in _hard_split(buffer, MAX_CHUNK_CHARS, OVERLAP_CHARS):
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
                for piece in _hard_split(paragraph, MAX_CHUNK_CHARS, OVERLAP_CHARS):
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
