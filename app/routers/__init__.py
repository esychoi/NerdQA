from fastapi import APIRouter

from app.routers.completions import completion_router
from app.routers.documents import document_router

router = APIRouter(prefix="")

router.include_router(completion_router)
router.include_router(document_router)
