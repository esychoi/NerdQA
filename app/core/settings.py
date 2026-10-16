from langchain_core.documents import Document
from pydantic_settings import BaseSettings, SettingsConfigDict

env_file = ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=env_file, env_file_encoding="utf-8")

    OLLAMA_URL: str = "http://localhost:11434"
    LLM_NAME: str = "qwen3:8b"

    EMBEDDING_MODEL_NAME: str = "qwen3-embedding:0.6b"

    CHROMADB_PATH: str


class Prompts:
    RAG_SYSTEM_PROMPT = """You are a helpful, accurate, and natural conversational assistant.

    You will receive context documents under the "# CONTEXT DOCUMENTS" tag and the user's question under the "# USER QUESTION" tag.

    # INSTRUCTIONS

    1. Answer the user's question using only information explicitly supported by the provided context documents. Do not use outside knowledge, assumptions, or speculation.
    2. If the answer is not available in the context, respond exactly with: "Sorry, I cannot find the answer in my knowledge base."
    3. If only part of the question can be answered from the context, answer the supported part directly. If the missing information prevents a complete answer, clearly state that you cannot find the answer in your knowledge base rather than guessing.
    3. Respond directly and naturally, as if you were answering the user in a normal conversation.
    4. Never mention the context documents, retrieved documents, provided context, knowledge base contents, or the process used to find information in your answer. *DO NOT USE PHRASES* such as:
        - "The provided context states...", "According to the documents...", "Based on the available information...", "in the provided context..."
        - "The context does not mention...", "The provided context does not include..."
"""

    RAG_USER_PROMPT = """# CONTEXT DOCUMENTS
    
{context}
    
# USER QUESTION
    
{user_prompt}
"""

    @staticmethod
    def format_context_documents(documents: list[Document]) -> str:
        context = ""
        for document in documents:
            title = document.metadata["title"]
            content = document.page_content
            context += f"## {title}\n\n{content}\n\n"
        return context


settings = Settings()
