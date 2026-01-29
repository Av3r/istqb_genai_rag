from app.embedder import embed_single
from app.retrieve import retrieve_top_k
from app.score_filter import filter_low_scores
from openai import OpenAI
import textwrap

client = OpenAI()

def build_prompt(question: str, contexts: list[str]) -> str:
    """
    Creates a prompt for RAG.
    If context is missing, instruct model to answer 'INSUFFICIENT DATA'.
    """
    joined_contexts = "\n\n---\n\n".join(contexts)

    prompt = f"""
You are an exam assistant. Use ONLY the provided context to answer.
If the context is insufficient, answer exactly: "INSUFFICIENT DATA".

CONTEXT:
{joined_contexts}

QUESTION:
{question}

Answer clearly.
""".strip()

    return textwrap.dedent(prompt)

def rag_answer(question: str, top_k=5, min_score=1.05):
    """
    Full RAG pipeline:
    1. Embed question
    2. Retrieve top K chunks
    3. Filter weak scores
    4. Send to LLM
    """
    query_vec = embed_single(question)
    results = retrieve_top_k(query_vec, k=top_k)

    filtered = filter_low_scores(results, min_score=min_score)

    if filtered is None:
        return "INSUFFICIENT DATA (no good match in Elasticsearch)."

    contexts = [r["text"] for r in filtered]

    prompt = build_prompt(question, contexts)

    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message["content"]