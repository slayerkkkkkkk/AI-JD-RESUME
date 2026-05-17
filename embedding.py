import os
import hashlib
import math

_model = None

def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def _hash_embedding(text: str, dim: int = 384) -> list:
    vec = [0.0] * dim
    tokens = text.lower().split()
    if not tokens:
        return vec
    for token in tokens:
        idx = int(hashlib.md5(token.encode()).hexdigest(), 16) % dim
        vec[idx] += 1.0
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]

def generate_embedding(text: str) -> list:
    if os.environ.get("RENDER") == "true":
        return _hash_embedding(text)
    return _get_model().encode(text, normalize_embeddings=True).tolist()
