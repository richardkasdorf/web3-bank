import uuid, os

from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from langchain.tools import tool
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from pathlib import Path
from chatbot.models import BankSupportInput
from pydantic import BaseModel, Field



SCRIPT_DIR = Path(__file__).resolve().parent
PERSIST_DIRECTORY = SCRIPT_DIR.parent / "chroma_db"

OLLAMA_URL = os.getenv('OLLAMA_URL', "http://127.0.0.1:11434")

if "/api/" in OLLAMA_URL:
    OLLAMA_URL = OLLAMA_URL.split("/api/")[0]

model = init_chat_model(model="ollama:qwen2.5:3b", base_url="http://127.0.0.1:11434", temperature=0)

embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_URL)

vector_store = Chroma(
    collection_name="rag_bank",
    embedding_function=embeddings,
    persist_directory=str(PERSIST_DIRECTORY),
)

@tool("get_support", parse_docstring=True)
def search_documentation(query: str) -> str:
    """Search the bank's documentation for fees, charges, limits, rules, policies and support.
    Use for ANY question about bank fees, maintenance fees, tariffs, rules or policies.

    Args:
        query: The question to search for, in English.
    """
    print(f"[RAG] query={query!r}")
    docs = vector_store.similarity_search(query, k=3)
    print(f"[RAG] {len(docs)} chunks")

    retrieved_docs = vector_store.similarity_search(query, k=1)

    if not retrieved_docs or not retrieved_docs[0].page_content.strip():
        return "No relevant content was found in the documents for this search."
        
    formatted_results = []
    
    for index, doc in enumerate(retrieved_docs, start=1):
        source = doc.metadata.get('source', 'unknown')
        chunk_text = (
            f"--- TRECHO {index} (Fonte: {source}) ---\n{doc.page_content}\n"
        )
        formatted_results.append(chunk_text)
        
    return "\n".join(formatted_results)


# CHUNK_ANALYST_INSTRUCTIONS = """# Formatting Rules
# - **Conciseness**: Keep the final answer under 3 sentences, if possible. 
# - **Directness**: Start answering the question right in the very first sentence. Do not say "Based on the provided documentation...".
# - Use bullet points only if the user asks for steps or lists."""

# rag_subagent = {
#     "name": "support-subagent",
#     "description": (
#         "Analyze policy and rules information in documentation."
#         "Pass the user question."
#     ),
#     "system_prompt": CHUNK_ANALYST_INSTRUCTIONS,
#     "tools": [search_documentation],
#     "model": model,
# }





