import json
import faiss
import numpy as np
from crewai.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings

INDEX_PATH = "./ipc_vectordb.faiss"
METADATA_PATH = "./ipc_vectordb_meta.json"

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

@tool("IPC Sections Search Tool")
def search_ipc_sections(query: str, top_k: int = 3):
    embed_model = HuggingFaceEmbeddings()
    query_embedding = np.array(embed_model.embed_query(query), dtype=np.float32).reshape(1, -1)

    index = faiss.read_index(INDEX_PATH)
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    distances, indices = index.search(query_embedding, top_k)
    results = []
    for i in indices[0]:
        results.append(metadata[i])

    return results
