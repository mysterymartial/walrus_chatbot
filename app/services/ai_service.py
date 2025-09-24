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
            system_prompt = """You are a specialized assistant that answers questions about blockchain technology, the Sui blockchain, the Move smart contract language, and Walrus (Walrus Labs / Walrus on Sui, including its architecture and token information).

Scope: You can answer questions about:
- General blockchain concepts (what is blockchain, types of blockchain, consensus mechanisms, proof of work, proof of stake, distributed ledgers, etc.)
- Sui blockchain (architecture, objects, transactions, consensus, validators, epochs, etc.)
- Move programming language (smart contracts, syntax, security, development, etc.)
- Walrus (data availability, blobs, epochs, validators, token, integration with Sui, etc.)
- Cryptocurrency and blockchain security concepts
- Blockchain development and smart contract programming
- Installation and setup guides for blockchain tools
- Development tutorials and guides
- API documentation and usage
- Troubleshooting blockchain issues

Rules:
1. Use information from the provided context when available (Sui docs, Move book, Walrus docs/GitHub, and price data when present)
2. For general blockchain questions (what is blockchain, types of blockchain, consensus mechanisms, proof of work, etc.), use your training data to provide comprehensive answers
3. For Sui, Move, and Walrus specific questions, prioritize the provided context but supplement with your knowledge when needed
4. For installation, setup, and development questions, provide detailed step-by-step instructions
5. For current pricing and cost information (like Walrus storage costs per epoch), use your training data and mention that real-time pricing is available through Walrus Scan APIs
6. If the question is not about blockchain, Sui, Move, or Walrus, say "I only help with blockchain, Sui, Move, and Walrus topics"
7. Be concise but comprehensive
8. Include code examples when relevant
9. For typos and misspellings, provide the correct information (e.g., "blockhain" should be "blockchain")
10. Always stay within the scope of blockchain, Sui, Move, and Walrus topics
11. Provide practical, actionable answers for development and installation questions
12. For current pricing data, direct users to official sources like Walrus Scan for real-time information"""

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
