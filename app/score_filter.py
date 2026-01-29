def filter_low_scores(results, min_score=1.05):
    """
    Filters results based on minimum similarity score.
    Returns None if no result meets the threshold.
    """
    filtered = [r for r in results if r["score"] >= min_score]

    if not filtered:
        return None
    
    return filtered