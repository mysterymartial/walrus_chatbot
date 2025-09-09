# ======================
# app/utils/exceptions.py
# ======================
from fastapi import HTTPException, status

class SuiBotException(Exception):

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ValidationError(SuiBotException):

    def __init__(self, message: str):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)

class SearchError(SuiBotException):
    """Search service error"""
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_503_SERVICE_UNAVAILABLE)

class AIServiceError(SuiBotException):

    def __init__(self, message: str):
        super().__init__(message, status.HTTP_503_SERVICE_UNAVAILABLE)

