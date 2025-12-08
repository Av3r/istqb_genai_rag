from elasticsearch import Elasticsearch

def get_es():
    return Elasticsearch(
        hosts=["http://localhost:9200"]
    )