from fastapi import APIRouter

from .completions import completion_router

router = APIRouter(prefix="")

router.include_router(completion_router)
