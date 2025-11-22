"""
pdf_utils.py

PDF reading and text chunking helpers.

For kids:
- "Python reads each page of the book."
- "We cut the text into smaller knowledge cards (chunks)."
"""

from typing import List, Tuple, Dict, Any
from pypdf import PdfReader


def extract_pages_from_pdf(pdf_path: str) -> List[Tuple[int, str]]:
    """
    Read the PDF and return a list of (page_number, text).

    pdf_path: path to the PDF file as a string.

    page_number starts at 1 for human-friendliness.
    """
    # Make sure we pass a plain string into PdfReader
    reader = PdfReader(str(pdf_path))
    pages: List[Tuple[int, str]] = []

    for idx, page in enumerate(reader.pages):
        page_num = idx + 1
        text = page.extract_text() or ""
        text = text.strip()
        if text:
            pages.append((page_num, text))

    return pages


def split_page_into_chunks(page_text: str, max_chars: int = 400) -> List[str]:
    """
    Cut one page of text into smaller chunks.

    Simple strategy:
    - Split by blank lines into paragraphs.
    - Keep adding paragraphs to the current chunk.
    - If it would be too long, start a new chunk.
    """
    paragraphs = [p.strip() for p in page_text.split("\n\n") if p.strip()]
    chunks: List[str] = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 > max_chars:
            if current:
                chunks.append(current.strip())
            current = para
        else:
            if current:
                current += "\n\n" + para
            else:
                current = para

    if current:
        chunks.append(current.strip())

    return chunks


def build_knowledge_cards(
    pages: List[Tuple[int, str]],
    max_chars: int = 400
) -> List[Dict[str, Any]]:
    """
    Build a list of knowledge cards from PDF pages.

    Each card has:
    - id: "card_1", "card_2", ...
    - page: original page number
    - text: chunk text
    """
    cards: List[Dict[str, Any]] = []
    card_id = 1

    for page_num, page_text in pages:
        chunks = split_page_into_chunks(page_text, max_chars=max_chars)
        for chunk in chunks:
            cards.append(
                {
                    "id": f"card_{card_id}",
                    "page": page_num,
                    "text": chunk,
                    # "embedding" will be added later
                }
            )
            card_id += 1

    return cards
