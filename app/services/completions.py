import ollama

from app.core.settings import Prompts, settings
from app.db.chromadb import ChromaDBClient


class ChatService:
    @staticmethod
    def simple_chat(system_prompt: str = "", user_prompt: str = ""):
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

    @staticmethod
    def rag_chat(collection_name: str, system_prompt: str = "", user_prompt: str = "", k: int = 4, filter: dict = {}):
        messages = [
            {
                "role": "system",
                "content": (
                    Prompts.RAG_SYSTEM_PROMPT + "\n\n" + system_prompt if system_prompt else Prompts.RAG_SYSTEM_PROMPT
                ),
            }
        ]

        # Retrieval
        chromadb_client = ChromaDBClient(collection_name)
        documents = chromadb_client.get_relevant_documents(query=user_prompt, k=k, filter=filter)

        # LLM Call
        if user_prompt:
            messages.append(
                {
                    "role": "user",
                    "content": Prompts.RAG_USER_PROMPT.format(
                        context=Prompts.format_context_documents(documents), user_prompt=user_prompt
                    ),
                }
            )

        response_stream = ollama.chat(model=settings.LLM_NAME, messages=messages, stream=True)
        for chunk in response_stream:
            content = chunk["message"]["content"]
            if content:
                yield content
