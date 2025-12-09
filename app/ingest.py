from .elastic_client import get_es
from .embedder import embed_texts
import math


INDEX_NAME = "rag_docs"
EMBED_DIMS = 384 # for all-MiniLM-L6-v2

def ensure_index(es):
    if es.indices.exists(index=INDEX_NAME):
        return
    mapping = {
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "page": {"type": "integer"},
                "chunk_id": {"type": "integer"},
                "embedding": {"type": "dense_vector", "dims": EMBED_DIMS}
            }
        }
    }
    es.indices.create(index=INDEX_NAME, body=mapping)

def ingest_to_es(chunks, batch_size=32):
    es = get_es()
    ensure_index(es)

    # batch embeddings
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        vectors = embed_texts(batch)  # expect numpy array or list of vectors
        for j, (text, vec) in enumerate(zip(batch, vectors)):
            doc_id = i + j
            es.index(index=INDEX_NAME, id=doc_id, document={
                "text": text,
                "embedding": vec.tolist()
            })
    print("DONE: documents stored.")


# def ingest_to_es(chunks):
#     """
#     Ingest text chunks to Elasticsearch with embeddings.
    
#     Args:
#         chunks: List of text chunks to index
#     """
#     es = get_es()

#     # Create index if it doesn't exist
#     try:
#         if not es.indices.exists(index="rag_docs"):
#             es.indices.create(index="rag_docs", mappings={
#                 "properties": {
#                     "text": {"type": "text"},
#                     "embedding": {"type": "dense_vector", "dims": 384}
#                 }
#             })
#     except Exception as e:
#         print(f"Warning: Could not check/create index: {e}")

#     vectors = embed_texts(chunks)

#     for i, (text, vector) in enumerate(zip(chunks, vectors)):
#         es.index(index="rag_docs", id=i, document={
#             "text": text,
#             "embedding": vector.tolist(),
#         })

#     print("DONE: documents stored.")