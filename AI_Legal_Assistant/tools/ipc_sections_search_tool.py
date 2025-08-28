import os
from crewai.tools import tool
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

@tool("IPC Sections Search Tool")
def search_ipc_sections(query: str) -> list[dict]:
    """
    Search IPC vector database for sections relevant to the input query.

    Args:
        query (str): User query in natural language.

    Returns:
        list[dict]: List of matching IPC sections with metadata and content.
    """
    # Resolve vector DB path from environment variables
    persist_dir_path = os.getenv("PERSIST_DIRECTORY_PATH", "./chroma_vectordb")
    collection_name = os.getenv("IPC_COLLECTION_NAME", "ipc_collection")

    # Ensure vector DB directory exists
    if not os.path.exists(persist_dir_path):
        raise FileNotFoundError(f"❌ Vector DB directory not found at '{persist_dir_path}'. "
                                "Make sure it exists or build it using ipc_vectordb_builder.py")

    embedding_function = HuggingFaceEmbeddings()

    # Load vectorstore
    vector_db = Chroma(
        collection_name=collection_name,
        persist_directory=persist_dir_path,
        embedding_function=embedding_function
    )

    top_k = 3  # can be passed as an argument for flexibility

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

# Example usage (uncomment to test locally)
# query = "What is the IPC section for Theft?"
# results = search_ipc_sections.func(query)
# for r in results:
#     print(r)
