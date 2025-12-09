from retriever import retrieve_top_k_by_text
from reranker import rerank
from openai import OpenAI  # or your preferred OpenAI wrapper
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

def build_prompt(contexts: list, question: str) -> str:
    context_text = "\n\n---\n\n".join(contexts)
    prompt = f"""You are an exam assistant. Use ONLY the context below to answer the question.
If the answer is not in the context, reply exactly: "Syllabus does not contain this information."

CONTEXT:
{context_text}

QUESTION:
{question}

Answer concisely:
"""
    return prompt

def answer_rag(question: str, top_k: int = 5, use_rerank: bool = True):
    hits = retrieve_top_k_by_text(question, top_k=top_k)
    contexts = [h["text"] for h in hits]
    if use_rerank:
        # rerank top_k with cross-encoder
        candidates = [(h["text"], h["id"]) for h in hits]
        ranked = rerank(question, candidates)
        contexts = [r[0] for r in ranked][:top_k]
    prompt = build_prompt(contexts, question)
    if client:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512
        )
        return resp.choices[0].message["content"]
    else:
        return prompt  # for testing without OpenAI