from fastapi import APIRouter

from schemas.completions import ChatCompletionSchema
from services.completions import CompletionService

completion_router = APIRouter(prefix="/completion", tags=["Completion"])


@completion_router.post("")
def chat_completion(request: ChatCompletionSchema):
    system_prompt = request.system_prompt
    user_prompt = request.user_prompt
    response = CompletionService.chat_completion(system_prompt, user_prompt)
    return response
