def calculator_tool(expression: str):
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception:
        return "Invalid calculation"


def search_tool(query: str):
    return f"Search result for '{query}' (mocked response)"
