# ======================
# app/services/ai_service.py
# ======================
from openai import OpenAI
from app.core.config import settings
from app.utils.exceptions import AIServiceError
from app.utils.logger import get_logger


class AIService:
    def __init__(self):
        if not settings.openai_api_key:
            raise AIServiceError("OpenAI API key not configured")

        self.client = OpenAI(api_key=settings.openai_api_key)
        self.logger = get_logger(__name__)

    def generate_response(self, query: str, context: str) -> str:
        """Generate AI response with context"""
        try:
            system_prompt = """You are a specialized assistant that ONLY answers questions about the Sui blockchain, the Move smart contract language, and Walrus (Walrus Labs / Walrus on Sui, including its architecture and token information).

Rules:
1. Only use information from the provided context (Sui docs, Move book, Walrus docs/GitHub, and price data when present)
2. If the context doesn't contain relevant information, say "I don't have information about this in the Sui/Walrus documentation"
3. If the question is not about Sui, Move, or Walrus, say "I only help with Sui blockchain, Move language, and Walrus"
4. Be concise but comprehensive
5. Include code examples when relevant
6. Never make up information not in the context"""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context (Sui/Move/Walrus): {context}\n\nQuestion: {query}"}
            ]

            response = self.client.chat.completions.create(
                model=settings.ai_model,
                messages=messages,
                max_tokens=settings.ai_max_tokens,
                temperature=settings.ai_temperature
            )

            return response.choices[0].message.content

        except Exception as e:
            self.logger.error(f"AI service error: {e}")
            raise AIServiceError(f"Failed to generate response: {str(e)}")
