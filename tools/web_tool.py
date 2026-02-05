from langchain_community.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()

def web_search(query: str):
    """
    Perform web search using DuckDuckGo
    """
    return search_tool.run(query)
