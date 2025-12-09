from typing import List

def chunk_text(texts, max_chars=1500):
    """
    Split pages into chunks respecting page boundaries.
    Each page is chunked separately to preserve document structure.
    """
    chunks = []

    for page_text in texts:
        current = ""
        lines = page_text.split("\n")
        
        for line in lines:
            # If adding this line exceeds max_chars, save current chunk and start new
            if len(current) + len(line) + 1 > max_chars and current.strip():
                chunks.append(current.strip())
                current = line
            else:
                # Add line to current chunk
                current += ("\n" if current else "") + line
        
        # Save any remaining text from this page
        if current.strip():
            chunks.append(current.strip())

    return chunks


def chunk_text_with_overlap(pages: List[str], max_chars: int = 800, overlap: int = 150) -> List[str]:
    """
    Hybrid chunker:
    - First join pages into text segments by paragraph where possible.
    - If paragraph longer than max_chars, split by sliding window with overlap.
    Returns list of chunks.
    """
    chunks = []
    for page in pages:
        # split into paragraphs by blank line or long newline runs
        paras = [p.strip() for p in page.split("\n\n") if p.strip()]
        for para in paras:
            if len(para) <= max_chars:
                # try to append to last chunk if space
                if chunks and len(chunks[-1]) + len(para) + 1 <= max_chars:
                    chunks[-1] = chunks[-1] + "\n\n" + para
                else:
                    chunks.append(para)
            else:
                # fallback sliding window on long paragraph
                start = 0
                while start < len(para):
                    end = start + max_chars
                    chunk = para[start:end].strip()
                    if chunk:
                        chunks.append(chunk)
                    start = max(end - overlap, start + 1)
    return chunks


def chunk_text_with_overlap_new(full_text, max_chars=1000, overlap=150):
    """
    Split text into overlapping chunks across entire document.
    Chunks can span multiple pages, with overlap between consecutive chunks.
    
    Args:
        full_text: Complete document text (all pages joined)
        max_chars: Maximum characters per chunk
        overlap: Number of characters to overlap between chunks
    
    Returns:
        List of text chunks with overlapping content
    """
    chunks = []
    text = full_text.strip()
    start = 0
    
    while start < len(text):
        # Calculate end position for this chunk
        end = start + max_chars
        
        # Extract chunk
        chunk = text[start:end]
        
        # Only add non-empty chunks
        if chunk.strip():
            chunks.append(chunk.strip())
        
        # Move start position with overlap
        # If this is the last chunk (end >= len(text)), we're done
        if end >= len(text):
            break
            
        start = end - overlap
    
    return chunks