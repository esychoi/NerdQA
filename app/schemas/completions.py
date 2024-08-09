from pydantic import BaseModel


class ChatCompletionSchema(BaseModel):
    system_prompt: str
    user_prompt: str
