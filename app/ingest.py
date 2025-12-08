from .elastic_client import get_es
from .embedder import embed_texts

def ingest_to_es(chunks):
    """
    Ingest text chunks to Elasticsearch with embeddings.
    
    Args:
        chunks: List of text chunks to index
    """
    es = get_es()

    # Create index if it doesn't exist
    try:
        if not es.indices.exists(index="rag_docs"):
            es.indices.create(index="rag_docs", mappings={
                "properties": {
                    "text": {"type": "text"},
                    "embedding": {"type": "dense_vector", "dims": 384}
                }
            })
    except Exception as e:
        print(f"Warning: Could not check/create index: {e}")

    vectors = embed_texts(chunks)

    for i, (text, vector) in enumerate(zip(chunks, vectors)):
        es.index(index="rag_docs", id=i, document={
            "text": text,
            "embedding": vector.tolist(),
        })

    print("DONE: documents stored.")