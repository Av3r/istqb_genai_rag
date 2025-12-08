from sentence_transformers import SentenceTransformer

def get_embedder():
    return SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts):
    model = get_embedder()
    vectors = model.encode(texts, show_progress_bar=True)
    return vectors

def embed_single(text: str):
    """Embed a single query for search."""
    model = get_embedder()
    vector = model.encode([text], convert_to_numpy=True)[0].tolist()
    return vector