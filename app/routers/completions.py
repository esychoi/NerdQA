from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.completions import ChatCompletionSchema
from app.services.completions import CompletionService

completion_router = APIRouter(prefix="/completion", tags=["Completion"])


@completion_router.post("")
def chat_completion(request: ChatCompletionSchema):
    return StreamingResponse(
        CompletionService.chat_completion(request.system_prompt, request.user_prompt),
        media_type="text/plain; charset=utf-8",
    )
