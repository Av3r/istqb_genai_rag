from elastic_client import get_es
from embedder import embed_texts
import numpy as np
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def search_es(query):
    es = get_es()
    query_vector = embed_texts([query])[0]

    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.q, 'embedding') + 1.0",
                "params": {"q": query_vector.tolist()}
            }
        }
    }

    response = es.search(
        index="rag_docs",
        query=script_query,
        size=3
    )

    docs = [hit["_source"]["text"] for hit in response["hits"]["hits"]]
    return "\n\n".join(docs)

def answer_question(question):
    context = search_es(question)

    prompt = f"""
    You are an assistant. 
    Use ONLY the context below to answer the question.

    CONTEXT:
    {context}

    QUESTION: {question}
    """

    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message["content"]

def ask_from_list(path="questions.txt"):
    with open(path, "r", encoding="utf-8") as f:
        questions = [q.strip() for q in f.readlines()]

    for q in questions:
        print("\n====================================")
        print("QUESTION:", q)
        print("ANSWER:\n", answer_question(q))