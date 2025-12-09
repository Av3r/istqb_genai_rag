from elasticsearch import Elasticsearch
from typing import List, Dict, Any

def get_es():
    return Elasticsearch(
        hosts=["http://localhost:9200"]
    )

INDEX_NAME = "rag_docs"
es = Elasticsearch("http://localhost:9200")

def create_index_if_not_exists(dims: int = 384):
    if es.indices.exists(index=INDEX_NAME):
        return
    mapping = {
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "meta": {"type": "object"},
                "embedding": {"type": "dense_vector", "dims": dims}
            }
        }
    }
    es.indices.create(index=INDEX_NAME, body=mapping)

def index_documents(docs: List[Dict[str, Any]]):
    """
    docs = [{"id": id, "text": text, "embedding": embedding, "meta": {...}}, ...]
    """
    for d in docs:
        es.index(index=INDEX_NAME, id=d.get("id"), document=d)