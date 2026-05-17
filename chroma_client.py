import chromadb
import os

CHROMA_PATH = os.path.join(os.path.dirname(__file__), "data", "chromadb")
os.makedirs(CHROMA_PATH, exist_ok=True)

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

def get_collection(name: str):
    return chroma_client.get_or_create_collection(name)

def delete_collection(name: str):
    try:
        chroma_client.delete_collection(name)
    except Exception:
        pass
