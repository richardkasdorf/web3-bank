from pathlib import Path
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_classic.indexes import SQLRecordManager


SCRIPT_DIR = Path(__file__).resolve().parent
DOCS_BASE = SCRIPT_DIR.parent / "data"
DOC_PATHS = ["rag.md"]
PERSIST_DIRECTORY = SCRIPT_DIR.parent / "chroma_db"
RECORD_DB = SCRIPT_DIR.parent / "record_manager.sql"


def load_local_docs(doc_paths: list[str] | None = None) -> list[Document]:
    """Fetch and load local markdown files with no external dependencies."""
    if doc_paths is None:
        paths = [p.name for p in DOCS_BASE.glob("*.md")]
    else:
        paths = doc_paths

    docs: list[Document] = []
    
    for path in paths:
        full_path = DOCS_BASE / path.lstrip("/")
        try:
            content = full_path.read_text(encoding="utf-8")
            docs.append(
                Document(page_content=content, metadata={"source": str(full_path)})
            )
        except FileNotFoundError:
            print(f"⚠️ Aviso: Arquivo não encontrado em {full_path}")
            continue
    return docs


docs = load_local_docs()
print(f"Loaded {len(docs)} documentation pages.")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)
print(f"Split documentation into {len(all_splits)} chunks.")

embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://127.0.0.1:11434")


record_manager = SQLRecordManager(
    namespace="chroma/rag_bank", 
    db_url=f"sqlite:///{RECORD_DB}"
)
vector_store = Chroma(
    collection_name="rag_bank",
    embedding_function=embeddings,
    persist_directory=str(PERSIST_DIRECTORY),
)
vector_store.add_documents(documents=all_splits)
print(f"Indexed {len(all_splits)} chunks.")




