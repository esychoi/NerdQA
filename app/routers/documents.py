import json
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.services.documents import DocumentService

document_router = APIRouter(prefix="/documents", tags=["Documents"])


@document_router.get("/{collection_name}")
def get_collection(
    collection_name: str,
    ids: list[str] | None = Query(default=None),
    where: str | None = Query(default=None),
    limit: int | None = Query(default=None),
    where_document: str | None = Query(default=None),
):
    try:
        where_filter = json.loads(where) if where else None
        where_document_filter = json.loads(where_document) if where_document else None
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="where and where_document must be valid JSON",
        )

    result = DocumentService.get_collection(collection_name, ids, where_filter, limit, where_document_filter)
    return JSONResponse(status_code=200, content={"response": result})
