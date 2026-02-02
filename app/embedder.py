from sentence_transformers import SentenceTransformer
from typing import List

# Module-level cached model to avoid re-loading on every call
_MODEL: SentenceTransformer | None = None

def get_embedder() -> SentenceTransformer:
    global _MODEL
    if _MODEL is None:
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