# ======================
# app/models/chat.py
# ======================
from pydantic import BaseModel, Field, validator
from typing import Optional
from app.core.config import settings


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=settings.max_input_length)

    @validator('query')
    def validate_query(cls, v):
        if not v.strip():
            raise ValueError('Query cannot be empty or whitespace only')
        return v.strip()


class ChatResponse(BaseModel):
    success: bool
    response: str
    query: Optional[str] = None
    context_found: bool = False
    processing_time: Optional[float] = None


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    status_code: int


class HealthResponse(BaseModel):
    status: str = "healthy"
    app_name: str = settings.app_name
    version: str = settings.version
    timestamp: str

