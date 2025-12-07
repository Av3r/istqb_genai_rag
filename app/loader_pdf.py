import pdfplumber
import fitz
from typing import List

def load_pdf(path: str, start_page: int = 8, end_page: int = 3) -> list[str]:
    doc = fitz.open(path)
    texts = []
    end_index = len(doc) - end_page

    for page_num in range(start_page - 1, end_index):
        page = doc[page_num]
        text = page.get_text()

        texts.append(text)
    
    doc.close()
    return texts