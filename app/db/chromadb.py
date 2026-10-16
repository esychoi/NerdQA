from typing import Any

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

from app.core.settings import settings


class ChromaDBClient:
    _instance = None

    def __new__(cls, collection_name: str):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, collection_name: str) -> None:
        if not hasattr(self, "embedding_function"):
            self.embedding_function = OllamaEmbeddings(
                model=settings.EMBEDDING_MODEL_NAME, base_url=settings.OLLAMA_URL
            )
            self.collection_name = None
            self.vectorstore = None

        self.switch_collection(collection_name)

    def switch_collection(self, collection_name: str) -> None:
        if self.collection_name == collection_name:
            return

        self.vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=self.embedding_function,
            persist_directory=settings.CHROMADB_PATH,
        )
        self.collection_name = collection_name

    def get_relevant_documents(self, query: str, k: int = 4, filter: dict[str, Any] | None = None) -> list[Document]:
        return self.vectorstore.similarity_search(query, k=k, filter=filter)
