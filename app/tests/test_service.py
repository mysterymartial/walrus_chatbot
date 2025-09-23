# ======================
# app/tests/test_service.py
# ======================
import os
import pytest
from unittest.mock import Mock, patch
from app.utils.exceptions import ValidationError, SearchError, AIServiceError



os.environ["OPENAI_API_KEY"] = "test_key"
os.environ["TAVILY_API_KEY"] = "test_key"

from app.services.search_service import SearchService
from app.services.ai_service import AIService
from app.services.validation_service import ValidationService


class TestValidationService:

    def setup_method(self):
        self.service = ValidationService()

    def test_valid_query(self):
        query = "What is Sui blockchain?"
        result = self.service.validate_query(query)
        assert result == query

    def test_empty_query_fails(self):
        with pytest.raises(ValidationError) as exc:
            self.service.validate_query("")
        assert "cannot be empty" in str(exc.value.message)

    def test_1000_char_limit_exactly(self):
        query = "a" * 1000
        result = self.service.validate_query(query)
        assert len(result) == 1000

    def test_1001_char_limit_fails(self):
        query = "a" * 1001
        with pytest.raises(ValidationError) as exc:
            self.service.validate_query(query)
        assert "too long" in str(exc.value.message)
        assert "1001" in str(exc.value.message)


class TestSearchService:

    def setup_method(self):
        from app.services.search_service import SearchService
        self.service = SearchService()



    @patch('requests.post')
    def test_tavily_search_finds_sui_docs(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "results": [
                {"content": "Sui is a Layer 1 blockchain platform"},
                {"content": "Move programming language documentation"}
            ]
        }
        mock_post.return_value = mock_response

        result = self.service._search_tavily("Sui blockchain")

        assert "Sui is a Layer 1 blockchain" in result
        assert "Move programming language" in result
        call_args = mock_post.call_args[1]['json']
        assert "site:docs.sui.io OR site:move-language.github.io OR site:move-book.com" in call_args['query']

    @patch('requests.post')
    def test_tavily_search_prioritizes_walrus(self, mock_post):
        service = self.service
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"results": [{"content": "Walrus DA on Sui"}]}
        mock_post.return_value = mock_response

        result = service._search_tavily("What is Walrus on Sui?")

        assert "Walrus DA on Sui" in result
        call_args = mock_post.call_args[1]['json']
        assert "site:walruslabs.xyz" in call_args['query']

    @patch('requests.get')
    def test_duckduckgo_search_fallback(self, mock_get):

        mock_response = Mock()
        mock_response.json.return_value = {
            "AbstractText": "Sui blockchain platform with Move language",
            "RelatedTopics": [
                {"Text": "Move smart contracts"},
                {"Text": "Sui transactions"}
            ]
        }
        mock_get.return_value = mock_response

        result = self.service._search_duckduckgo("Move smart contracts")

        assert "Sui blockchain platform" in result
        assert "Move smart contracts" in result
        call_args = mock_get.call_args[1]['params']
        assert "site:docs.sui.io OR site:move-language.github.io" in call_args['q']

    @patch('requests.get')
    def test_duckduckgo_prioritizes_walrus(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "AbstractText": "Walrus is a data availability solution on Sui",
            "RelatedTopics": [{"Text": "Walrus GitHub repo"}]
        }
        mock_get.return_value = mock_response

        from app.services.search_service import SearchService
        service = SearchService()
        result = service._search_duckduckgo("Walrus price on Sui")
        assert "Walrus is a data availability" in result
        call_args = mock_get.call_args[1]['params']
        assert "site:walruslabs.xyz" in call_args['q']

    @patch('app.services.search_service.SearchService._search_tavily')
    @patch('app.services.search_service.SearchService._search_duckduckgo')
    def test_search_fallback_strategy(self, mock_ddg, mock_tavily):

        mock_tavily.return_value = None
        mock_ddg.return_value = "Sui documentation from DuckDuckGo"

        result = self.service.search_sui_docs("Sui question")

        assert result == "Sui documentation from DuckDuckGo"
        mock_tavily.assert_called_once()
        mock_ddg.assert_called_once()

    @patch('app.services.search_service.SearchService._search_tavily')
    @patch('app.services.search_service.SearchService._search_duckduckgo')
    def test_search_walrus_first_strategy(self, mock_ddg, mock_tavily):
        from app.services.search_service import SearchService
        service = SearchService()
        mock_tavily.return_value = "Walrus documentation"
        mock_ddg.return_value = None
        result = service.search_sui_docs("Tell me about Walrus")
        assert result.startswith("Walrus documentation")

    @patch('app.services.search_service.SearchService._search_tavily')
    @patch('app.services.search_service.SearchService._search_duckduckgo')
    def test_search_no_results_raises_error(self, mock_ddg, mock_tavily):

        mock_tavily.return_value = None
        mock_ddg.return_value = None

        with pytest.raises(SearchError) as exc:
            self.service.search_sui_docs("unknown topic")


        assert "Could not find relevant information" in str(exc.value.message)

    @patch('requests.get')
    def test_get_walrus_price(self, mock_get):
        from app.services.search_service import SearchService
        service = SearchService()
        # Mock search endpoint
        search_resp = Mock()
        search_resp.raise_for_status.return_value = None
        search_resp.json.return_value = {"coins": [{"id": "walrus", "name": "Walrus"}]}
        # Mock price endpoint
        price_resp = Mock()
        price_resp.raise_for_status.return_value = None
        price_resp.json.return_value = {"walrus": {"usd": 1.23}}

        def side_effect(url, params=None, timeout=5):
            if "search" in url:
                return search_resp
            if "simple/price" in url:
                return price_resp
            raise AssertionError("Unexpected URL")

        mock_get.side_effect = side_effect

        info = service._get_walrus_price()
        assert "$1.23" in info

    @patch('requests.get')
    def test_walrus_price_included_when_asking_price(self, mock_get):
        from app.services.search_service import SearchService
        service = SearchService()

        # search services return content empty so price path is exercised
        with patch('app.services.search_service.SearchService._search_tavily', return_value=None), \
             patch('app.services.search_service.SearchService._search_duckduckgo', return_value=None):

            search_resp = Mock()
            search_resp.raise_for_status.return_value = None
            search_resp.json.return_value = {"coins": [{"id": "walrus", "name": "Walrus"}]}

            price_resp = Mock()
            price_resp.raise_for_status.return_value = None
            price_resp.json.return_value = {"walrus": {"usd": 0.99}}

            def side_effect(url, params=None, timeout=5):
                if "search" in url:
                    return search_resp
                if "simple/price" in url:
                    return price_resp
                raise AssertionError("Unexpected URL")

            mock_get.side_effect = side_effect

            result = service.search_sui_docs("What is the Walrus coin price?")
            assert "$0.99" in result

class TestAIService:


    def setup_method(self):
        self.service = AIService()

    @patch('app.services.ai_service.OpenAI')
    def test_generate_response_with_sui_context(self, mock_openai_class):
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = (
            "Sui is a blockchain platform that uses Move for smart contracts."
        )
        mock_client.chat.completions.create.return_value = mock_response

        with patch('app.services.ai_service.settings') as mock_settings:
            mock_settings.openai_api_key = "test_key"
            self.service = __import__("app.services.ai_service", fromlist=["AIService"]).AIService()

        query = "What is Sui?"
        context = "Sui is a Layer 1 blockchain platform designed for high throughput."

        result = self.service.generate_response(query, context)

        assert "Sui is a blockchain platform" in result
        call_args = mock_client.chat.completions.create.call_args[1]
        system_message = call_args['messages'][0]['content']
        assert "Sui blockchain, the Move smart contract language, and Walrus" in system_message
        assert "Context (Sui/Move/Walrus):" in call_args['messages'][1]['content']

    @patch('openai.OpenAI')
    def test_ai_service_handles_errors(self, mock_openai_class):
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        with pytest.raises(AIServiceError) as exc:
            self.service.generate_response("tests query", "tests context")

        assert "Failed to generate response" in str(exc.value.message)

    def test_ai_service_no_api_key(self):
        with patch('app.services.ai_service.settings') as mock_settings:
            mock_settings.openai_api_key = None
            with pytest.raises(AIServiceError) as exc:
                AIService()
            assert "OpenAI API key not configured" in str(exc.value.message)
