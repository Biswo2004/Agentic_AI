from crewai.tools import tool
from tavily import TavilyClient

LEGAL_SOURCES = ["indiankanoon.org"]

def _is_legal_source(url: str) -> bool:
    return any(domain in url for domain in LEGAL_SOURCES)

@tool("Legal Precedent Search Tool")
def search_legal_precedents(query: str, tavily_api_key: str) -> list[dict]:
    if not tavily_api_key:
        raise ValueError("❌ Tavily API key is required as a function argument.")
    
    client = TavilyClient(api_key=tavily_api_key)
    search_query = f"site:{' OR site:'.join(LEGAL_SOURCES)} {query}"
    response = client.search(query=search_query, max_results=10)
    
    raw_results = response.get("results", [])
    legal_results = [
        {
            "title": item.get("title"),
            "summary": item.get("content"),
            "link": item.get("url")
        }
        for item in raw_results
        if _is_legal_source(item.get("url", ""))
    ]
    
    return legal_results if legal_results else [{
        "title": "No relevant legal precedents found",
        "summary": "No matching results found from trusted Indian legal sources.",
        "link": None
    }]
