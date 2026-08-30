import uuid, os

from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from langchain.tools import tool
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from pathlib import Path
from chatbot.models import BankSupportInput



SCRIPT_DIR = Path(__file__).resolve().parent
PERSIST_DIRECTORY = SCRIPT_DIR.parent / "chroma_db"

OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://docker.internal')

if "/api/" in OLLAMA_URL:
    OLLAMA_URL = OLLAMA_URL.split("/api/")[0]


embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://127.0.0.1:11434")

vector_store = Chroma(
    collection_name="rag_bank",
    embedding_function=embeddings,
    persist_directory=str(PERSIST_DIRECTORY),
)

@tool(parse_docstring=True)
def search_documentation(query: str) -> str:
    """Busque regras e suporte no arquivo RAG.
    
    Args:
        query: O termo ou pergunta para buscar no banco de dados vetorial.
    """
    retrieved_docs = vector_store.similarity_search(query, k=1)

    if not retrieved_docs or not retrieved_docs[0].page_content.strip():
        return "No relevant content was found in the documents for this search."
        
    formatted_results = []
    
    for index, doc in enumerate(retrieved_docs, start=1):
        source = doc.metadata.get('source', 'unknown')
        chunk_text = (
            f"--- TRECHO {index} ---\n (Fonte: {source}) ---\n"
            f"{doc.page_content}\n"
        )
        formatted_results.append(chunk_text)
        
    return "\n".join(formatted_results)


CHUNK_ANALYST_INSTRUCTIONS = """# Regras de Formatação
- **Concisão**: Mantenha a resposta final com menos de 3 frases, se possível. 
- **Diretividade**: Comece a responder à pergunta logo na primeira frase. Não diga "Com base na documentação fornecida...".
- Use tópicos apenas se o usuário pedir passos ou listas."""



chunk_analyst_subagent = {
    "name": "chunk-analyst",
    "description": (
        "Analyze one retrieved documentation chunk file. "
        "Pass the user question."
    ),
    "system_prompt": CHUNK_ANALYST_INSTRUCTIONS,
}


model = init_chat_model(model="ollama:qwen2.5:3b", base_url="http://127.0.0.1:11434", temperature=0)
supervisor_agent = create_deep_agent(
    model,
    tools=[search_documentation],
    subagents=[chunk_analyst_subagent]
)


@tool("get_suport", args_schema=BankSupportInput)
def get_bank_support(request: str) -> str:
    """Suporte técnico sobre regras, políticas do banco e dúvidas em transferências.

    Use esta ferramenta sempre que o usuário tiver dúvidas sobre regras,
    políticas do banco ou precisar de suporte técnico/RAG.

    Args:
        request: A pergunta ou solicitação exata enviada pelo usuário.
    """

    result = supervisor_agent.invoke({
        "messages": [HumanMessage(content=request)]
    })

    last_message = result["messages"][-1]
    return getattr(last_message, "content", str(last_message))





