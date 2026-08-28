from typing import BinaryIO

from PyPDF2 import PdfReader


def extract_text_from_pdf(file_stream: BinaryIO) -> str:
    """Extract raw text from an uploaded PDF file stream."""
    reader = PdfReader(file_stream)
    text_parts = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text)
    return "\n".join(text_parts).strip()
