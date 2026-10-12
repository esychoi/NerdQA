from fastapi import APIRouter

from .completions import completion_router

# from .documents import document_router

router = APIRouter(prefix="")

router.include_router(completion_router)
# router.include_router(document_router)
