import math


def _cosine(a: list, b: list) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(y * y for y in b)) or 1.0
    return dot / (na * nb)


def rerank(jd: str, resumes: list) -> list:
    """Re-rank resumes by cosine similarity between JD text and resume text."""
    from embedding import generate_embedding
    jd_vec = generate_embedding(jd)
    for r in resumes:
        r_vec = generate_embedding(r.get("text", ""))
        r["rerank_score"] = _cosine(jd_vec, r_vec)
    return sorted(resumes, key=lambda x: x["rerank_score"], reverse=True)
