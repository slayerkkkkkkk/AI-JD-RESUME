import hashlib
import math


def _tokenize(text: str) -> list[str]:
    return text.lower().split()


def _hash_token(token: str, dim: int) -> int:
    return int(hashlib.md5(token.encode()).hexdigest(), 16) % dim


def generate_embedding(text: str, dim: int = 384) -> list:
    """Produce a deterministic sparse-hashing embedding without any ML deps."""
    vec = [0.0] * dim
    tokens = _tokenize(text)
    if not tokens:
        return vec
    for token in tokens:
        idx = _hash_token(token, dim)
        vec[idx] += 1.0
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]
