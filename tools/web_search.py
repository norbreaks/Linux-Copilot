from duckduckgo_search import DDGS

def search_errors(query: str, max_results=3) -> str:
    """Uses DuckDuckGo to find answers from web without leaving terminal."""
    print(f"Searching DuckDuckGo for: {query}...")
    try:
        results = DDGS().text(query, max_results=max_results)
        res_strings = []
        for r in results:
            res_strings.append(f"Title: {r['title']}\nSnippet: {r['body']}\nLink: {r['href']}")
        return "\n\n".join(res_strings)
    except Exception as e:
        return f"Web search failed: {e}"
