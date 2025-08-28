from crewai.tools import tool
import sqlite3
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings

DB_PATH = "./ipc_vectordb.sqlite"

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

@tool("IPC Sections Search Tool")
def search_ipc_sections(query: str, top_k: int = 3) -> list[dict]:
    embed_model = HuggingFaceEmbeddings()
    query_embedding = np.array(embed_model.embed_query(query), dtype=np.float32)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT chapter, chapter_title, section, section_title, section_desc, embedding FROM ipc_sections")
    rows = c.fetchall()
    conn.close()

    results = []
    for row in rows:
        chapter, chapter_title, section, section_title, section_desc, embedding_blob = row
        embedding = np.frombuffer(embedding_blob, dtype=np.float32)
        score = cosine_similarity(query_embedding, embedding)
        results.append({
            "chapter": chapter,
            "chapter_title": chapter_title,
            "section": section,
            "section_title": section_title,
            "content": section_desc,
            "score": score
        })

    # Sort by similarity
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]
