import os

from pydantic_settings import BaseSettings, SettingsConfigDict

env = os.getenv("ENV", "dev")
env_file = ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=env_file,
        env_file_encoding="utf-8",
    )

    DEVICE: str

    OPENAI_API_KEY: str

    LANGCHAIN_TRACING_V2: str
    LANGCHAIN_API_KEY: str


settings = Settings()
