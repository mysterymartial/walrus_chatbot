# ======================
# tests/test_integration.py
# ======================
import os


os.environ.setdefault("OPENAI_API_KEY", "tests-openai-key")
os.environ.setdefault("TAVILY_API_KEY", "tests-tavily-key")

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from app.core.config import settings

client = TestClient(app)


class TestIntegration:


    def test_complete_sui_question_workflow(self):
        """Test complete workflow: input validation → search → AI → response"""

        with patch('app.services.search_service.SearchService.search_sui_docs') as mock_search, \
                patch('app.services.ai_service.AIService.generate_response') as mock_ai:

            mock_search.return_value = (
                "Sui is a next-generation smart contract platform with high throughput, "
                "low latency, and an asset-oriented programming model powered by the Move programming language."
            )


            mock_ai.return_value = (
                "Based on the Sui documentation, Sui is a Layer 1 blockchain that uses Move programming language "
                "for smart contracts. It's designed for high performance applications."
            )

            response = client.post(
                "/api/v1/chat",
                json={"query": "What is Sui blockchain and how does it work?"}
            )

            assert response.status_code == 200
            data = response.json()


            assert data["success"] is True
            assert data["context_found"] is True
            assert "Sui" in data["response"]
            assert "Move" in data["response"]
            assert data["query"] == "What is Sui blockchain and how does it work?"
            assert isinstance(data["processing_time"], float)


            mock_search.assert_called_once_with("What is Sui blockchain and how does it work?")
            mock_ai.assert_called_once()

    def test_move_programming_question_workflow(self):

        with patch('app.services.search_service.SearchService.search_sui_docs') as mock_search, \
                patch('app.services.ai_service.AIService.generate_response') as mock_ai:
            mock_search.return_value = (
                "Move is a resource-oriented programming language for writing smart contracts. "
                "It provides safety and expressiveness for high-value digital assets."
            )
            mock_ai.return_value = (
                "Move is the programming language used for Sui smart contracts. "
                "It's designed with safety features to prevent common blockchain vulnerabilities."
            )

            response = client.post(
                "/api/v1/chat",
                json={"query": "How do I create a Move module for Sui?"}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "Move" in data["response"]

    def test_1000character_limit_integration(self):

        max_len = settings.max_input_length


        query_max = ("What is Sui blockchain? " * 50)[:max_len]  # build a long-ish string, then trim

        with patch('app.services.search_service.SearchService.search_sui_docs') as mock_search, \
                patch('app.services.ai_service.AIService.generate_response') as mock_ai:
            mock_search.return_value = "Sui documentation content"
            mock_ai.return_value = "Response about Sui"

            response = client.post(
                "/api/v1/chat",
                json={"query": query_max}
            )

            assert response.status_code == 200
            assert len(response.json()["query"]) == max_len

        query_over = query_max + "a"
        response = client.post(
            "/api/v1/chat",
            json={"query": query_over}
        )
        assert response.status_code == 422

    def test_no_results_fallback(self):

        with patch('app.services.search_service.SearchService.search_sui_docs') as mock_search:
            from app.utils.exceptions import SearchError
            mock_search.side_effect = SearchError("No results found")

            response = client.post(
                "/api/v1/chat",
                json={"query": "Some unrelated question"}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is False
            assert data["context_found"] is False
            assert "couldn't find information" in data["response"]
