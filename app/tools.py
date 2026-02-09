from tavily import TavilyClient
from app.config import TAVILY_API_KEY

tavily = TavilyClient(api_key=TAVILY_API_KEY)

def web_search(query: str):
    try:
        res = tavily.search(query=query, max_results=3)
        chunks = []
        for r in res.get("results", []):
            chunks.append(f"{r['title']}: {r['content'][:200]}")
        return " | ".join(chunks) if chunks else "No results found."
    except Exception as e:
        return f"Search error: {e}"

def calculator(expr: str):
    try:
        return str(eval(expr))
    except Exception as e:
        return f"Calc error: {e}"

def code_runner(code: str):
    if "http" in code or "requests" in code:
        return "Blocked: internet access disabled in code tool."
    try:
        local_vars = {}
        exec(code, {}, local_vars)
        return str(local_vars)
    except Exception as e:
        return f"Code error: {e}"

TOOLS = {
    "search": web_search,
    "calc": calculator,
    "code": code_runner
}
