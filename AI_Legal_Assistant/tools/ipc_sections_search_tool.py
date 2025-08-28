from crewai.tools import tool
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

@tool("IPC Sections Search Tool")
def search_ipc_sections(query: str, persist_dir_path: str = "./chroma_vectordb", collection_name: str = "ipc_collection") -> list[dict]:
    if not os.path.exists(persist_dir_path):
        raise FileNotFoundError(f"❌ Vector DB directory not found at '{persist_dir_path}'. Build it using ipc_vectordb_builder.py")
    
    embedding_function = HuggingFaceEmbeddings()
    vector_db = Chroma(
        collection_name=collection_name,
        persist_directory=persist_dir_path,
        embedding_function=embedding_function
    )
    
    docs = vector_db.similarity_search(query, k=3)
    
    return [
        {
            "section": doc.metadata.get("section"),
            "section_title": doc.metadata.get("section_title"),
            "chapter": doc.metadata.get("chapter"),
            "chapter_title": doc.metadata.get("chapter_title"),
            "content": doc.page_content
        }
        for doc in docs
    ]
