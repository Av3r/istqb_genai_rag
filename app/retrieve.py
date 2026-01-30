from app.elastic_client import get_es

TOP_K = 5
ES_INDEX = "rag_docs"


def retrieve_top_k(query_vector, k=5):
    """Retrieve top-k documents from Elasticsearch using a dense_vector cosine script.

    Returns a list of dicts with keys: `id`, `index`, `score`, `text`, `meta`, `page`, `chunk_id`.
    """
    es = get_es()

    body = {
        "size": k,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        },
        "_source": ["text", "page", "chunk_id", "meta"]
    }

    try:
        resp = es.search(index=ES_INDEX, body=body)
    except Exception as e:
        print(f"[WARN] Elasticsearch search failed: {e}")
        return []

    hits = resp.get("hits", {}).get("hits", [])
    results = []
    for hit in hits:
        src = hit.get("_source", {}) or {}
        text = src.get("text")
        # fallback if older clients returned fields
        if not text:
            fields = hit.get("fields", {})
            if isinstance(fields, dict) and "text" in fields:
                text = fields["text"][0] if fields["text"] else None

        results.append({
            "id": hit.get("_id"),
            "index": hit.get("_index"),
            "score": hit.get("_score"),
            "text": text,
            "meta": src.get("meta"),
            "page": src.get("page"),
            "chunk_id": src.get("chunk_id")
        })

    return results