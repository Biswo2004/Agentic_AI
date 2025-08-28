import os
from crewai.tools import tool
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Default relative paths
PERSIST_DIRECTORY_PATH = "./chroma_vectordb"
IPC_COLLECTION_NAME = "ipc_collection"


@tool("IPC Sections Search Tool")
def search_ipc_sections(query: str) -> list[dict]:
    """
    Search IPC vector database for sections relevant to the input query.
    Args:
        query (str): User query in natural language.
    Returns:
        list[dict]: List of matching IPC sections with metadata and content.
    """
    if not os.path.exists(PERSIST_DIRECTORY_PATH):
        raise FileNotFoundError(f"❌ Vector DB not found at {PERSIST_DIRECTORY_PATH}. Please run ipc_vectordb_builder.py first.")

    embedding_function = HuggingFaceEmbeddings()

    # Load vectorstore
    vector_db = Chroma(
        collection_name=IPC_COLLECTION_NAME,
        persist_directory=PERSIST_DIRECTORY_PATH,
        embedding_function=embedding_function
    )

    top_k = 3  # can be made dynamic

    # Perform similarity search
    docs = vector_db.similarity_search(query, k=top_k)

    # Format results
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
