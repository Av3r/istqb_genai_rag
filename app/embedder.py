from sentence_transformers import SentenceTransformer

def get_embedder():
    return SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts):
    model = get_embedder()
    vectors = model.encode(texts, show_progress_bar=True)
    return vectors