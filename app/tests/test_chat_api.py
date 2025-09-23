# ======================
# tests/test_chat_api.py
# ======================
import pytest
import os


os.environ.setdefault("OPENAI_API_KEY", "tests-openai-key")
os.environ.setdefault("TAVILY_API_KEY", "tests-tavily-key")

from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app


client = TestClient(app)


class TestChatAPI:

    def test_health_endpoint(self):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data

    def test_info_endpoint(self):
        response = client.get("/api/v1/info")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Sui Chatbot API"
        assert "usage" in data
        assert data["usage"]["max_query_length"] == 1000

    @patch('app.services.search_service.SearchService.search_sui_docs')
    @patch('app.services.ai_service.AIService.generate_response')
    def test_chat_endpoint_success(self, mock_ai, mock_search):
        mock_search.return_value = "Sui is a Layer 1 blockchain platform designed for high throughput and low latency."
        mock_ai.return_value = "Sui is a Layer 1 blockchain platform that uses the Move programming language for smart contracts."

        response = client.post(
            "/api/v1/chat",
            json={"query": "What is Sui blockchain?"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "Sui" in data["response"]
        assert data["context_found"] is True
        assert data["query"] == "What is Sui blockchain?"
        assert "processing_time" in data

    @patch('app.services.search_service.SearchService.search_sui_docs')
    @patch('app.services.ai_service.AIService.generate_response')
    def test_chat_endpoint_move_question(self, mock_ai, mock_search):
        mock_search.return_value = "Move is a programming language for writing smart contracts on Sui blockchain."
        mock_ai.return_value = "Move is a resource-oriented programming language designed for blockchain applications."

        response = client.post(
            "/api/v1/chat",
            json={"query": "How do I write a Move module?"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "Move" in data["response"]
        assert data["context_found"] is True

    def test_chat_empty_query(self):
        response = client.post(
            "/api/v1/chat",
            json={"query": ""}
        )
        assert response.status_code == 422  # Validation error

    def test_chat_too_long_query(self):
        from app.core.config import settings
        long_query = "a" * (settings.max_input_length + 1)

        response = client.post(
            "/api/v1/chat",
            json={"query": long_query}
        )

        assert response.status_code == 422

    def test_chat_exactly_1000_chars(self):
        exact_query = "a" * 1000

        with patch('app.services.search_service.SearchService.search_sui_docs') as mock_search, \
                patch('app.services.ai_service.AIService.generate_response') as mock_ai:
            mock_search.return_value = "Some Sui documentation content"
            mock_ai.return_value = "Response about the query"

            response = client.post(
                "/api/v1/chat",
                json={"query": exact_query}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True

    @patch('app.services.search_service.SearchService.search_sui_docs')
    def test_chat_no_search_results(self, mock_search):
        from app.utils.exceptions import SearchError
        mock_search.side_effect = SearchError("Could not find relevant information")

        response = client.post(
            "/api/v1/chat",
            json={"query": "Some random question"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert data["context_found"] is False
        assert "couldn't find information" in data["response"]

    def test_chat_whitespace_query(self):
        response = client.post(
            "/api/v1/chat",
            json={"query": "   "}
        )
        assert response.status_code == 422

    @patch('app.services.search_service.SearchService.search_sui_docs')
    @patch('app.services.ai_service.AIService.generate_response')
    def test_chat_endpoint_walrus_query(self, mock_ai, mock_search):
        mock_search.return_value = (
            "Walrus is a data availability solution on Sui. Current Walrus price (CoinGecko): $1.00"
        )
        mock_ai.return_value = "Walrus provides DA on Sui. Price info included."

        response = client.post(
            "/api/v1/chat",
            json={"query": "What is Walrus on Sui and what's the price?"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["context_found"] is True
        assert "Walrus" in data["response"]
