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
        # "Sui blockchain" is detected as blockchain-related, so it uses general blockchain search
        assert "blockchain cryptocurrency crypto sui move walrus" in call_args['query']

    @patch('requests.post')
    def test_tavily_search_prioritizes_walrus(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"results": [{"content": "Walrus DA on Sui"}]}
        mock_post.return_value = mock_response

        result = self.service._search_tavily("What is Walrus on Sui?")

        assert "Walrus DA on Sui" in result
        call_args = mock_post.call_args[1]['json']
        # "What is Walrus on Sui?" is detected as blockchain-related, so it uses general blockchain search
        assert "blockchain cryptocurrency crypto sui move walrus" in call_args['query']

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
        # "Move smart contracts" is detected as blockchain-related, so it uses general blockchain search
        assert "blockchain sui move walrus cryptocurrency crypto" in call_args['q']

    @patch('requests.get')
    def test_duckduckgo_prioritizes_walrus(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "AbstractText": "Walrus is a data availability solution on Sui",
            "RelatedTopics": [{"Text": "Walrus GitHub repo"}]
        }
        mock_get.return_value = mock_response

        result = self.service._search_duckduckgo("Walrus price on Sui")
        assert "Walrus is a data availability" in result
        call_args = mock_get.call_args[1]['params']
        # "Walrus price on Sui" is detected as blockchain-related, so it uses general blockchain search
        assert "blockchain sui move walrus cryptocurrency crypto" in call_args['q']

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
    def test_search_no_results_raises_error(self, mock_ddg, mock_tavily):

        mock_tavily.return_value = None
        mock_ddg.return_value = None

        with pytest.raises(SearchError) as exc:
            self.service.search_sui_docs("unknown topic")

        # "unknown topic" is detected as non-blockchain, so it gets rejected with blockchain restriction message
        assert "I only help with Sui blockchain" in str(exc.value.message)

    @patch('app.services.search_service.SearchService._check_local_info', return_value=None)
    @patch('app.services.search_service.SearchService._search_walrus', return_value=None)
    @patch('app.services.search_service.SearchService._search_tavily_site_specific', return_value=None)
    @patch('app.services.search_service.SearchService._search_duckduckgo_site_specific', return_value=None)
    @patch('app.services.search_service.SearchService._search_tavily')
    @patch('app.services.search_service.SearchService._search_duckduckgo')
    def test_search_walrus_first_strategy(self, mock_ddg, mock_tavily, mock_ddg_site, mock_tavily_site, mock_walrus, mock_local):
        # Test with a query that doesn't match local patterns to trigger external search
        mock_tavily.return_value = "Walrus documentation"
        mock_ddg.return_value = None
        result = self.service.search_sui_docs("How to integrate Walrus with custom applications")
        assert result.startswith("Walrus documentation")

    @patch('requests.get')
    def test_get_walrus_price(self, mock_get):
        # Mock CoinGecko endpoints
        search_resp = Mock()
        search_resp.raise_for_status.return_value = None
        search_resp.json.return_value = {"coins": [{"id": "walrus", "name": "Walrus"}]}
        price_resp = Mock()
        price_resp.raise_for_status.return_value = None
        price_resp.json.return_value = {"walrus": {"usd": 1.23}}

        def side_effect(url, params=None, timeout=5):
            if "api.coingecko.com/api/v3/search" in url:
                return search_resp
            if "api.coingecko.com/api/v3/simple/price" in url:
                return price_resp
            raise AssertionError("Unexpected URL")

        mock_get.side_effect = side_effect

        info = self.service._get_walrus_price()
        assert "$1.23" in info

    @patch('requests.get')
    def test_walrus_price_included_when_asking_price(self, mock_get):
        search_resp = Mock()
        search_resp.raise_for_status.return_value = None
        search_resp.json.return_value = {"coins": [{"id": "walrus", "name": "Walrus"}]}
        price_resp = Mock()
        price_resp.raise_for_status.return_value = None
        price_resp.json.return_value = {"walrus": {"usd": 0.99}}

        def side_effect(url, params=None, timeout=5):
            if "api.coingecko.com/api/v3/search" in url:
                return search_resp
            if "api.coingecko.com/api/v3/simple/price" in url:
                return price_resp
            raise AssertionError("Unexpected URL")

        mock_get.side_effect = side_effect

        result = self.service.search_sui_docs("What is the Walrus coin price?")
        assert "$0.99" in result

    def test_local_walrus_info_prioritized(self):
        from app.services.search_service import SearchService
        service = SearchService()

        # Test Walrus blob query should return local info first
        result = service.search_sui_docs("What is a walrus blob?")
        assert "blob" in result.lower()
        assert "walrus" in result.lower()

    def test_walrus_sources_expanded(self):
        from app.services.search_service import SearchService
        service = SearchService()

        # Test that Walrus queries use expanded sources
        with patch('app.services.search_service.SearchService._check_local_info', return_value=None), \
             patch('app.services.search_service.SearchService._search_walrus', return_value=None), \
             patch('app.services.search_service.SearchService._search_tavily_site_specific', return_value=None), \
             patch('app.services.search_service.SearchService._search_duckduckgo_site_specific', return_value=None), \
             patch('app.services.search_service.SearchService._search_tavily') as mock_tavily:
            mock_tavily.return_value = "Walrus documentation"
            service.search_sui_docs("Walrus API documentation and SDK references")
            
            # Check that _search_tavily was called
            assert mock_tavily.called
            call_args = mock_tavily.call_args[0][0]  # First positional argument (query)
            assert "walrus" in call_args.lower()

    @patch('requests.get')
    def test_walrus_network_stats(self, mock_get):
        from app.services.search_service import SearchService
        service = SearchService()

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "validators": {"total": 25},
            "network": {"total_stake": 1000000, "active_nodes": 30}
        }
        mock_get.return_value = mock_response

        stats = service._get_walrus_network_stats()
        assert "Active Validators: 25" in stats
        assert "Total Stake: 1,000,000 WAL" in stats
        assert "Active Nodes: 30" in stats

    @patch('requests.get')
    def test_sui_network_stats(self, mock_get):
        from app.services.search_service import SearchService
        service = SearchService()

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "validators": {"total": 100},
            "network": {"total_stake": 5000000, "tps": 1000}
        }
        mock_get.return_value = mock_response

        stats = service._get_sui_network_stats()
        assert "Active Validators: 100" in stats
        assert "Total Stake: 5,000,000 SUI" in stats
        assert "Current TPS: 1000" in stats

    def test_walrus_validator_local_info(self):
        from app.services.search_service import SearchService
        service = SearchService()

        result = service.search_sui_docs("How many validators on Walrus?")
        assert "validator" in result.lower()
        assert "walrus" in result.lower()

    def test_blockchain_related_query_detection(self):
        from app.services.search_service import SearchService
        service = SearchService()

        # Test blockchain-related queries
        assert service._is_blockchain_related("What is blockchain?") == True
        assert service._is_blockchain_related("How does crypto work?") == True
        assert service._is_blockchain_related("Sui blockchain features") == True
        assert service._is_blockchain_related("Move smart contracts") == True
        assert service._is_blockchain_related("Walrus data availability") == True
        assert service._is_blockchain_related("NFT marketplace") == True
        assert service._is_blockchain_related("DeFi protocols") == True

        # Test non-blockchain queries
        assert service._is_blockchain_related("What is the weather?") == False
        assert service._is_blockchain_related("How to cook pasta?") == False
        assert service._is_blockchain_related("Python programming") == False

    def test_general_internet_search_for_blockchain_topics(self):
        from app.services.search_service import SearchService
        service = SearchService()

        # Test that blockchain queries use general internet search
        with patch('app.services.search_service.SearchService._check_local_info', return_value=None) as mock_local, \
             patch('app.services.search_service.SearchService._get_walrus_network_stats', return_value=None) as mock_walrus_stats, \
             patch('app.services.search_service.SearchService._get_walrus_price', return_value=None) as mock_price, \
             patch('app.services.search_service.SearchService._search_walrus', return_value=None) as mock_walrus_search, \
             patch('app.services.search_service.SearchService._search_authoritative_sources', return_value=None) as mock_auth, \
             patch('app.services.search_service.SearchService._search_tavily_site_specific', return_value=None) as mock_tavily_site, \
             patch('app.services.search_service.SearchService._search_duckduckgo_site_specific', return_value=None) as mock_ddg_site, \
             patch('app.services.search_service.SearchService._search_tavily') as mock_tavily:
            mock_tavily.return_value = "Blockchain technology information"
            service.search_sui_docs("What is blockchain technology?")
            
            # Check that _search_tavily was called with general search
            assert mock_tavily.called
            call_args = mock_tavily.call_args[0][0]  # First positional argument (query)
            assert "blockchain" in call_args.lower()

    def test_non_blockchain_query_rejection(self):
        from app.services.search_service import SearchService
        service = SearchService()

        # Test that non-blockchain queries are rejected
        with pytest.raises(Exception) as exc_info:
            service.search_sui_docs("What is the weather today?")
        
        assert "I only help with Sui blockchain" in str(exc_info.value)

    def test_exhaustive_search_strategy(self):
        from app.services.search_service import SearchService
        service = SearchService()

        # Test that the search strategy exhausts all local sources first
        with patch('app.services.search_service.SearchService._check_local_info', return_value=None) as mock_local, \
             patch('app.services.search_service.SearchService._get_walrus_network_stats', return_value=None) as mock_walrus_stats, \
             patch('app.services.search_service.SearchService._get_walrus_price', return_value=None) as mock_price, \
             patch('app.services.search_service.SearchService._search_walrus', return_value=None) as mock_walrus_search, \
             patch('app.services.search_service.SearchService._search_tavily', return_value=None) as mock_tavily, \
             patch('app.services.search_service.SearchService._search_duckduckgo', return_value="DuckDuckGo result") as mock_ddg:

            result = service.search_sui_docs("What is blockchain technology?")
            
            # Verify all search methods were called in order
            assert mock_local.called
            assert mock_tavily.called
            assert mock_ddg.called
            assert "DuckDuckGo result" in result

    def test_local_info_priority(self):
        from app.services.search_service import SearchService
        service = SearchService()

        # Test that local info is returned immediately without calling external APIs
        with patch('app.services.search_service.SearchService._check_local_info', return_value="Local info result") as mock_local, \
             patch('app.services.search_service.SearchService._search_tavily') as mock_tavily, \
             patch('app.services.search_service.SearchService._search_duckduckgo') as mock_ddg:

            result = service.search_sui_docs("What is Walrus?")
            
            # Verify local info was returned and external APIs were not called
            assert result == "Local info result"
            assert not mock_tavily.called
            assert not mock_ddg.called

    def test_site_specific_search_priority(self):
        from app.services.search_service import SearchService
        service = SearchService()

        # Test that site-specific search is tried before general search
        with patch('app.services.search_service.SearchService._check_local_info', return_value=None) as mock_local, \
             patch('app.services.search_service.SearchService._get_walrus_network_stats', return_value=None) as mock_walrus_stats, \
             patch('app.services.search_service.SearchService._get_walrus_price', return_value=None) as mock_price, \
             patch('app.services.search_service.SearchService._search_walrus', return_value=None) as mock_walrus_search, \
             patch('app.services.search_service.SearchService._search_tavily_site_specific', return_value="Site-specific result") as mock_tavily_site, \
             patch('app.services.search_service.SearchService._search_duckduckgo_site_specific') as mock_ddg_site, \
             patch('app.services.search_service.SearchService._search_tavily') as mock_tavily_general, \
             patch('app.services.search_service.SearchService._search_duckduckgo') as mock_ddg_general:

            result = service.search_sui_docs("What is blockchain technology?")
            
            # Verify site-specific search was called and general search was not
            assert mock_tavily_site.called
            assert not mock_tavily_general.called
            assert not mock_ddg_general.called
            assert "Site-specific result" in result

    def test_exhaustive_search_with_ai_fallback(self):
        from app.services.search_service import SearchService
        service = SearchService()

        # Test that AI service fallback is used when all search methods fail
        with patch('app.services.search_service.SearchService._check_local_info', return_value=None) as mock_local, \
             patch('app.services.search_service.SearchService._get_walrus_network_stats', return_value=None) as mock_walrus_stats, \
             patch('app.services.search_service.SearchService._get_walrus_price', return_value=None) as mock_price, \
             patch('app.services.search_service.SearchService._search_walrus', return_value=None) as mock_walrus_search, \
             patch('app.services.search_service.SearchService._search_tavily_site_specific', return_value=None) as mock_tavily_site, \
             patch('app.services.search_service.SearchService._search_duckduckgo_site_specific', return_value=None) as mock_ddg_site, \
             patch('app.services.search_service.SearchService._search_tavily', return_value=None) as mock_tavily_general, \
             patch('app.services.search_service.SearchService._search_duckduckgo', return_value=None) as mock_ddg_general:

            result = service.search_sui_docs("What is blockchain technology?")
            
            # Verify all search methods were called and AI fallback was used
            assert mock_local.called
            assert mock_tavily_site.called
            assert mock_ddg_site.called
            assert mock_tavily_general.called
            assert mock_ddg_general.called
            assert "No specific search results found" in result
            assert "training data" in result

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
