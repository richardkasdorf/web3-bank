from pathlib import Path
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings

# Aponta caminho para o Crhoma
SCRIPT_DIR = Path(__file__).resolve().parent
PERSIST_DIRECTORY = SCRIPT_DIR.parent / "chroma_db"

# Inicializa Embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://127.0.0.1:11434")

# Carrega o DB existente
vector_store = Chroma(
    collection_name="rag_bank",
    embedding_function=embeddings,
    persist_directory=str(PERSIST_DIRECTORY),
)

# Busca TODOS os registros salvos dentro do banco
data = vector_store.get()

# Exibe os dados organizados no terminal
print(f"📊 Total de Chunks encontrados no banco: {len(data['documents'])}\n")

for i in range(len(data['documents'])):
    chunk_id = data['ids'][i]
    content = data['documents'][i]
    metadata = data['metadatas'][i]
    
    print(f"--- [CHUNK {i+1}] ---")
    print(f"🆔 ID no Banco: {chunk_id}")
    print(f"📂 Arquivo de Origem: {metadata.get('source')}")
    print(f"📝 Conteúdo (Primeiros 150 caracteres):\n{content[:150]}...")
    print("-" * 30 + "\n")
