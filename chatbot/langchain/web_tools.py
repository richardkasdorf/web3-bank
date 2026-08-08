from typing import Literal
from ddgs import DDGS
from tavily import TavilyClient
import os
from langchain.tools import tool


# @tool
# def internet_search(query: str) -> str:
#     """USE ESTA FERRAMENTA PARA QUALQUER PERGUNTA DO USUÁRIO. 
#     Se você não sabe o que significa uma palavra ou tecnologia como 'langgraph', chame esta função imediatamente.
#     """
#     try:
#         with DDGS() as ddgs:
#             results = [r['body'] for r in ddgs.text(query, max_results=3)]
#             return "\n\n".join(results) if results else "Nenhum resultado encontrado."
#     except Exception as e:
#         return f"Falha ao realizar a busca: {str(e)}"


tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

@tool
def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )