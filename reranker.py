from sentence_transformers import CrossEncoder

_cross_encoder = None

def _get_model():
    global _cross_encoder
    if _cross_encoder is None:
        _cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    return _cross_encoder

def rerank(jd: str, resumes: list) -> list:
    pairs = [(jd, r.get("text", "")) for r in resumes]
    scores = _get_model().predict(pairs).tolist()
    for r, score in zip(resumes, scores):
        r["rerank_score"] = score
    return sorted(resumes, key=lambda x: x["rerank_score"], reverse=True)
