from pydantic_settings import BaseSettings, SettingsConfigDict

env_file = ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=env_file, env_file_encoding="utf-8")

    LLM_NAME: str = "qwen3:8b"

    EMBEDDING_MODEL_NAME: str = "qwen3-embedding:0.6b"

    CHROMADB_PATH: str


settings = Settings()
