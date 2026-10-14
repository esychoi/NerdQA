import ollama

from app.core.settings import settings


class CompletionService:
    @staticmethod
    def chat_completion(system_prompt: str = "", user_prompt: str = ""):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if user_prompt:
            messages.append({"role": "user", "content": user_prompt})
        response_stream = ollama.chat(model=settings.LLM_NAME, messages=messages, stream=True)
        for chunk in response_stream:
            content = chunk["message"]["content"]
            if content:
                yield content
