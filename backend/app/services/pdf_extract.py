from dataclasses import dataclass

import fitz


@dataclass
class PageText:
    page_number: int
    text: str


def extract_text_from_pdf(data: bytes) -> list[PageText]:
    doc = fitz.open(stream=data, filetype="pdf")
    pages: list[PageText] = []
    try:
        for index, page in enumerate(doc):
            text = page.get_text("text")
            pages.append(PageText(page_number=index + 1, text=text))
    finally:
        doc.close()
    return pages
