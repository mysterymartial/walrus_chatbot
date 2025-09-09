# ======================
# app/api/routes/chat.py
# ======================
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
import time
from typing import Dict, Any

from app.models.chat import ChatRequest, ChatResponse, ErrorResponse, HealthResponse
from app.services.search_service import SearchService
from app.services.ai_service import AIService
from app.services.validation_service import ValidationService
from app.core.dependencies import get_search_service, get_ai_service, get_validation_service
from app.utils.exceptions import SuiBotException, ValidationError, SearchError, AIServiceError
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        timestamp=datetime.utcnow().isoformat()
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(
        request: ChatRequest,
        search_service: SearchService = Depends(get_search_service),
        ai_service: AIService = Depends(get_ai_service),
        validation_service: ValidationService = Depends(get_validation_service)
):

    start_time = time.time()

    try:
        logger.info(f"Received chat request: {request.query[:50]}...")

        validated_query = validation_service.validate_query(request.query)


        context = search_service.search_sui_docs(validated_query)


        ai_response = ai_service.generate_response(validated_query, context)

        processing_time = time.time() - start_time

        logger.info(f"Successfully processed request in {processing_time:.2f}s")

        return ChatResponse(
            success=True,
            response=ai_response,
            query=validated_query,
            context_found=True,
            processing_time=round(processing_time, 2)
        )

    except ValidationError as e:
        logger.warning(f"Validation error: {e.message}")
        raise HTTPException(
            status_code=e.status_code,
            detail={"error": "Validation Error", "message": e.message}
        )
    except SearchError as e:
        logger.error(f"Search error: {e.message}")
        return ChatResponse(
            success=False,
            response="I couldn't find information about your question in the Sui docs or Move book. Please try rephrasing your question.",
            query=request.query,
            context_found=False,
            processing_time=round(time.time() - start_time, 2)
        )
    except AIServiceError as e:
        logger.error(f"AI service error: {e.message}")
        raise HTTPException(
            status_code=e.status_code,
            detail={"error": "AI Service Error", "message": "Failed to generate response"}
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Internal Server Error", "message": "An unexpected error occurred"}
        )


@router.get("/info")
async def get_api_info() -> Dict[str, Any]:
    return {
        "name": "Sui Chatbot API",
        "version": "1.0.0",
        "description": "Ask questions about Sui blockchain and Move smart contracts",
        "usage": {
            "endpoint": "/chat",
            "method": "POST",
            "max_query_length": 1000,
            "supported_topics": [
                "Sui blockchain",
                "Move smart contracts",
                "Sui objects",
                "Move modules",
                "Sui transactions",
                "Move programming language"
            ]
        },
        "example_request": {
            "query": "How do I create a Move module on Sui?"
        }
    }

