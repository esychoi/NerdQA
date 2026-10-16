from pydantic import BaseModel


class SimpleChatSchema(BaseModel):
    system_prompt: str = ""
    user_prompt: str = ""


class RagChatSchema(BaseModel):
    system_prompt: str = ""
    user_prompt: str = ""
    k: int = 4
    filter: dict | None = None
