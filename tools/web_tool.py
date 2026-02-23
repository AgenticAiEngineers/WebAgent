try:
    from ddgs import DDGS
except Exception:
    from duckduckgo_search import DDGS

def web_search(query: str):
    """
    Perform web search using DuckDuckGo
    """
    results = []
    with DDGS() as ddgs:
        for row in ddgs.text(query, max_results=5):
            title = row.get("title", "")
            body = row.get("body", "")
            href = row.get("href", "")
            results.append(f"Title: {title}\nSnippet: {body}\nLink: {href}")
    return "\n\n".join(results)
