from app.embedder import embed_single
from app.retrieve import retrieve_top_k


def inspect_top_k(question: str, k: int = 5, print_results: bool = True):
    """
    Inspect top K retrieved chunks for a given question.

    Args:
        question: query string
        k: number of results
        print_results: if True, prints brief preview of each result

    Returns:
        List of result dicts returned by `retrieve_top_k`.
    """
    query_vec = embed_single(question)
    results = retrieve_top_k(query_vec, k=k)

    if print_results:
        print("\n=== TOP K CHUNKS ===")
        print("QUESTION:", question)
        for i, r in enumerate(results):
            print(f"\n--- RESULT {i+1} ---")
            print(f"ID: {r.get('id')}  SCORE: {r.get('score')}")
            text = r.get("text") or ""
            print(text[:500], "...")

    return results


# backward-compatible alias
def verify_top_k(question: str, k: int = 5):
    return inspect_top_k(question, k=k, print_results=True)