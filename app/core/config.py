# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "Sui Chatbot API"
    version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000

    openai_api_key: str
    tavily_api_key: Optional[str] = None
    max_input_length: int = 1000
    ai_model: str = "gpt-4o-mini"
    ai_max_tokens: int = 500
    ai_temperature: float = 0.2


    log_level: str = "INFO"


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
