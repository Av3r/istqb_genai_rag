from typing import List, Any, Optional

# Module-level cached model to avoid re-loading on every call
_MODEL: Optional[Any] = None

def get_embedder() -> Any:
    """Lazily import and return the SentenceTransformer model.

    Delays importing heavy libraries (torch/transformers/torchvision)
    until an embedding is actually requested so the Streamlit app
    can start without requiring those packages at import time.
    """
    global _MODEL
    if _MODEL is None:
        from sentence_transformers import SentenceTransformer

        _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return _MODEL

def embed_texts(texts: List[str]):
    """Embed whole list of texts for indexing."""
    model = get_embedder()
    vectors = model.encode(texts, show_progress_bar=True)
    return vectors

def embed_single(text: str):
    """Embed a single query for search."""
    model = get_embedder()
    vec = model.encode([text], convert_to_numpy=True)[0]
    try:
        return vec.tolist()
    except Exception:
        return list(vec)