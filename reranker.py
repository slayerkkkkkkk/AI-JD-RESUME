import os
import math

_cross_encoder = None

def _get_model():
    global _cross_encoder
    if _cross_encoder is None:
        from sentence_transformers import CrossEncoder
        _cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    return _cross_encoder

def _cosine(a: list, b: list) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(y * y for y in b)) or 1.0
    return dot / (na * nb)

def rerank(jd: str, resumes: list) -> list:
    if os.environ.get("RENDER") == "true":
        from embedding import generate_embedding
        jd_vec = generate_embedding(jd)
        for r in resumes:
            r["rerank_score"] = _cosine(jd_vec, generate_embedding(r.get("text", "")))
        return sorted(resumes, key=lambda x: x["rerank_score"], reverse=True)

    pairs = [(jd, r.get("text", "")) for r in resumes]
    scores = _get_model().predict(pairs).tolist()
    for r, score in zip(resumes, scores):
        r["rerank_score"] = score
    return sorted(resumes, key=lambda x: x["rerank_score"], reverse=True)
