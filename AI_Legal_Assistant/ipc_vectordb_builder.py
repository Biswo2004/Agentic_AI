import json
import os
import sqlite3
from langchain_huggingface import HuggingFaceEmbeddings
import numpy as np

DB_PATH = "./ipc_vectordb.sqlite"

def load_ipc_data(file_path: str) -> list[dict]:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def build_ipc_vectordb():
    """
    Build SQLite3 database for IPC sections with embeddings.
    """
    ipc_json_path = "./ipc.json"
    ipc_data = load_ipc_data(ipc_json_path)

    # Initialize embedding model
    embed_model = HuggingFaceEmbeddings()

    # Create DB and table
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS ipc_sections (
            id INTEGER PRIMARY KEY,
            chapter TEXT,
            chapter_title TEXT,
            section TEXT,
            section_title TEXT,
            section_desc TEXT,
            embedding BLOB
        )
    """)
    conn.commit()

    # Insert IPC entries with embeddings
    for entry in ipc_data:
        content = f"Section {entry['Section']}: {entry['section_title']}\n\n{entry['section_desc']}"
        embedding = embed_model.embed_query(content)
        embedding_blob = np.array(embedding, dtype=np.float32).tobytes()

        c.execute("""
            INSERT INTO ipc_sections 
            (chapter, chapter_title, section, section_title, section_desc, embedding)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            entry["chapter"], entry["chapter_title"],
            entry["Section"], entry["section_title"],
            entry["section_desc"], embedding_blob
        ))

    conn.commit()
    conn.close()
    print(f"✅ SQLite IPC Vector DB built at '{DB_PATH}'")

if __name__ == "__main__":
    build_ipc_vectordb()
