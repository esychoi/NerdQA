from typing import Any

import chromadb

from app.core.settings import settings

client = chromadb.PersistentClient(path=settings.CHROMADB_PATH)


class DocumentService:
    @staticmethod
    def get_collection(
        collection_name: str,
        ids: list[str] | None,
        where: dict[str, Any] | None,
        limit: int,
        where_document: dict[str, Any] | None,
    ):
        collection = client.get_collection(name=collection_name)
        results = collection.get(ids=ids, where=where, limit=limit, where_document=where_document)
        return {k: results[k] for k in ["ids", "documents", "metadatas"]}
