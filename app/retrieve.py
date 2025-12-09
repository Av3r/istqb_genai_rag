from elasticsearch import Elasticsearch


TOP_K = 5
ES_INDEX = "rag_docs"

es = Elasticsearch("http://localhost:9200")

def retrieve_top_k(query_vector, k=5):
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
        "_source": False,
        "fields": ["text"]
    }

    resp = es.search(index=ES_INDEX, body=body)
    results = [
        {"text": hit["fields"]["text"][0], "score": hit["_score"]}
        for hit in resp["hits"]["hits"]
    ]

    return results