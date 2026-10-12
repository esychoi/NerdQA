from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.schemas.completions import ChatCompletionSchema
from app.services.completions import CompletionService

completion_router = APIRouter(prefix="/completion", tags=["Completion"])


@completion_router.post("")
def chat_completion(request: ChatCompletionSchema):
    system_prompt = request.system_prompt
    user_prompt = request.user_prompt
    response = CompletionService.chat_completion(system_prompt, user_prompt)
    return JSONResponse(status_code=200, content={"response": response})
