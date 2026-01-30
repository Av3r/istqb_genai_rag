from typing import List
import textwrap

from openai import OpenAI

from app.embedder import embed_single
from app.retrieve import retrieve_top_k
from app.score_filter import filter_low_scores
from app.config import Settings


class RAGService:
    """Encapsulates RAG logic and dependencies.

    Use dependency injection to pass an OpenAI client and settings.
    """

    def __init__(self, openai_client: OpenAI, settings: Settings):
        self.client = openai_client
        self.settings = settings

    def build_prompt(self, question: str, contexts: List[str]) -> str:
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

    def answer(self, question: str) -> str:
        query_vec = embed_single(question)
        results = retrieve_top_k(query_vec, k=self.settings.RAG_TOP_K)

        filtered = filter_low_scores(results, min_score=self.settings.RAG_MIN_SCORE)
        if filtered is None:
            return "INSUFFICIENT DATA (no good match in Elasticsearch)."

        contexts = [r["text"] for r in filtered]
        prompt = self.build_prompt(question, contexts)

        resp = self.client.chat.completions.create(
            model=self.settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )

        choice = resp.choices[0]
        msg = getattr(choice, "message", None) or (choice.get("message") if isinstance(choice, dict) else None)
        if msg is None:
            return str(resp)

        content = getattr(msg, "content", None)
        if content is None and isinstance(msg, dict):
            content = msg.get("content")
        return content


# convenience factory for backwards compatibility
def rag_answer(question: str, openai_client: OpenAI = None, settings: Settings | None = None):
    """Simple helper: create client/settings if not provided and return answer."""
    import os
    from openai import OpenAI as _OpenAI

    if settings is None:
        settings = Settings()

    if openai_client is None:
        openai_client = _OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    service = RAGService(openai_client, settings)
    return service.answer(question)