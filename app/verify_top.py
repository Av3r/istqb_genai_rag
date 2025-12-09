from app.embedder import embed_single
from app.retrieve import retrieve_top_k

def verify_top_k(question: str, k: int = 5):
    """
    Manual verification of top K retrieved chunks for a given question.
    """
    print("\n=== VERIFY TOP K CHUNKS ===")
    print("QUESTION:", question)
    
    query_vec = embed_single(question)
    results = retrieve_top_k(query_vec, k=k)

    for i, r in enumerate(results):
        print(f"\n--- RESULT {i+1} ---")
        print(f"SCORE: {r['score']}")
        print(r['text'][:500], "...")

    return results