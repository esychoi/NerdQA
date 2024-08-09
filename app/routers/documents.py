from fastapi import APIRouter, HTTPException

from services.documents import DocumentService

document_router = APIRouter(prefix="/documents", tags=["Documents"])


@document_router.get("")
def read_document(db, file):
    return "read_document"


@document_router.post("")
def create_document(type: str, name: str):
    try:
        return DocumentService.create(type, name)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error occured when creating document: {e}"
        )


@document_router.put("")
def update_document(db, file):
    return "update_document"


@document_router.delete("")
def delete_document(db, file):
    return "delete_document"
