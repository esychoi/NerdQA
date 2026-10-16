from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.completions import RagChatSchema, SimpleChatSchema
from app.services.completions import ChatService

completion_router = APIRouter(prefix="/completion", tags=["Completion"])


@completion_router.post("/chat")
def simple_chat(request: SimpleChatSchema):
    return StreamingResponse(
        ChatService.simple_chat(request.system_prompt, request.user_prompt), media_type="text/plain; charset=utf-8"
    )


@completion_router.post("/ragchat/{collection_name}")
def rag_chat(collection_name: str, request: RagChatSchema):
    return StreamingResponse(
        ChatService.rag_chat(collection_name, request.system_prompt, request.user_prompt, request.k, request.filter),
        media_type="text/plain; charset=utf-8",
    )
