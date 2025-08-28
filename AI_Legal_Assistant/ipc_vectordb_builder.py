import json
import faiss
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings

INDEX_PATH = "./ipc_vectordb.faiss"
METADATA_PATH = "./ipc_vectordb_meta.json"

def load_ipc_data(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_ipc_vectordb():
    ipc_data = load_ipc_data("./ipc.json")
    embed_model = HuggingFaceEmbeddings()

    embeddings = []
    metadata = []

    for entry in ipc_data:
        content = f"Section {entry['Section']}: {entry['section_title']}\n\n{entry['section_desc']}"
        emb = np.array(embed_model.embed_query(content), dtype=np.float32)
        embeddings.append(emb)
        metadata.append({
            "chapter": entry["chapter"],
            "chapter_title": entry["chapter_title"],
            "section": entry["Section"],
            "section_title": entry["section_title"],
            "content": entry["section_desc"]
        })

    embeddings = np.vstack(embeddings)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)

    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f)

    print("✅ FAISS IPC Vector DB built successfully.")
