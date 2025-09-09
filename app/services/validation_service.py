# ======================
# app/services/validation_service.py
# ======================
from app.utils.exceptions import ValidationError
from app.core.config import settings


class ValidationService:
    @staticmethod
    def validate_query(query: str) -> str:
        if not query or not query.strip():
            raise ValidationError("Query cannot be empty")

        query = query.strip()
        if len(query) > settings.max_input_length:
            raise ValidationError(
                f"Query too long. Maximum {settings.max_input_length} characters allowed. "
                f"Current: {len(query)}"
            )

        return query

