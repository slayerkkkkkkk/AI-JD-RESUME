from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text: str) -> list:
    return _model.encode(text, normalize_embeddings=True).tolist()
