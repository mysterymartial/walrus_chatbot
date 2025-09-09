# ======================
# app/core/dependencies.py
# ======================
from functools import lru_cache
from app.services.search_service import SearchService
from app.services.ai_service import AIService
from app.services.validation_service import ValidationService

@lru_cache()
def get_search_service() -> SearchService:
    return SearchService()

@lru_cache()
def get_ai_service() -> AIService:
    return AIService()

@lru_cache()
def get_validation_service() -> ValidationService:
    return ValidationService()

