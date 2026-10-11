from pathlib import Path
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings

SCRIPT_DIR = Path(__file__).resolve().parent
PERSIST_DIRECTORY = SCRIPT_DIR.parent / "chroma_db"

embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://127.0.0.1:11434")

vector_store = Chroma(
    collection_name="rag_bank",
    embedding_function=embeddings,
    persist_directory=str(PERSIST_DIRECTORY),
)

data = vector_store.get()

print(f"📊 Total Chunks found in the DB: {len(data['documents'])}\n")

for i in range(len(data['documents'])):
    chunk_id = data['ids'][i]
    content = data['documents'][i]
    metadata = data['metadatas'][i]
    
    print(f"--- [CHUNK {i+1}] ---")
    print(f"🆔 ID inside DB: {chunk_id}")
    print(f"📂 Source File: {metadata.get('source')}")
    print(f"📝 Content (First 150 characters):\n{content[:150]}...")
    print("-" * 30 + "\n")

# Test RUN:
# python chatbot/langchain/view_db.py