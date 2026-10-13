from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.schemas.completions import ChatCompletionSchema
from app.services.completions import CompletionService

completion_router = APIRouter(prefix="/completion", tags=["Completion"])


@completion_router.post("")
def chat_completion(request: ChatCompletionSchema):
    response = CompletionService.chat_completion(request.system_prompt, request.user_prompt)
    return JSONResponse(status_code=200, content={"response": response})
