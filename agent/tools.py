from ddgs import DDGS


def calculator_tool(expression: str):
    try:
        result = eval(expression)
        return str(result)
    except Exception:
        return "Invalid calculation."


def search_tool(query: str):
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)
            output = ""

            for r in results:
                output += f"Title: {r['title']}\n"
                output += f"Snippet: {r['body']}\n"
                output += f"Link: {r['href']}\n\n"

            return output

    except Exception as e:
        return f"Search error: {str(e)}"
import requests

def time_tool(text=""):
    try:
        url = "https://timeapi.io/api/Time/current/zone?timeZone=Asia/Kolkata"
        res = requests.get(url).json()
        return res["time"]
    except:
        return "Time not available"
def smart_query_rewrite(query: str):
    query_lower = query.lower()

    # News queries
    if "news" in query_lower:
        return f"latest world news headlines today site:bbc.com OR site:reuters.com OR site:apnews.com"

    # Weather queries
    if "weather" in query_lower:
        return f"current weather report {query}"

    # Time queries
    if "time" in query_lower:
        return f"current time {query}"

    # Default
    return query
