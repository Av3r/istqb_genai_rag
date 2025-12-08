import pdfplumber
import fitz
from typing import List

def load_pdf(path: str, start_page: int = 8, pages_to_skip_at_end: int = 3) -> list[str]:
    """
    Load PDF and extract text from pages.
    
    Args:
        path: Path to PDF file
        start_page: First page to read (1-indexed)
        pages_to_skip_at_end: Number of pages to skip from the end
    """
    doc = fitz.open(path)
    texts = []
    end_index = len(doc) - pages_to_skip_at_end

    for page_num in range(start_page - 1, end_index):
        page = doc[page_num]
        text = page.get_text()

        texts.append(text)
    
    doc.close()
    return texts