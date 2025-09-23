# ======================
# app/services/search_service.py
# ======================
import requests
import re
from typing import Optional
from app.core.config import settings
from app.utils.exceptions import SearchError
from app.utils.logger import get_logger
from app.data.sui_info import SUI_BLOCKCHAIN_INFO
from urllib.parse import quote_plus


class SearchService:
    def __init__(self):
        self.logger = get_logger(__name__)

    def _is_walrus_query(self, query: str) -> bool:
        q = query.lower()
        walrus_terms = [
            r"walrus", r"walrus labs", r"walrus sui", r"walrus da", r"walrus coin",
            r"wal token", r"wal price", r"wal ticker"
        ]
        return any(re.search(term, q, re.IGNORECASE) for term in walrus_terms)

    def _search_tavily(self, query: str) -> Optional[str]:
        if not settings.tavily_api_key:
            return None

        try:
            url = "https://api.tavily.com/search"
            # Prioritize Walrus sources when query is about Walrus
            walrus_sites = "site:walruslabs.xyz OR site:github.com/mystenlabs/walrus OR site:github.com/walruslabs"
            sui_sites = "site:docs.sui.io OR site:move-language.github.io OR site:move-book.com"
            query_filter = f"{walrus_sites} OR {sui_sites}" if self._is_walrus_query(query) else sui_sites

            payload = {
                "api_key": settings.tavily_api_key,
                "query": f"{query} {query_filter}",
                "search_depth": "basic",
                "max_results": 5
            }

            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()

            content_pieces = []
            if "results" in data:
                for result in data["results"][:3]:
                    if "content" in result:
                        content_pieces.append(result["content"])

            content = " ".join(content_pieces)
            if content:
                self.logger.info("Found results via Tavily")
            return content or None

        except Exception as e:
            self.logger.error(f"Tavily search failed: {e}")
            return None

    def _search_duckduckgo(self, query: str) -> Optional[str]:
        try:
            search_url = "https://api.duckduckgo.com/"
            # Prioritize Walrus sources when relevant
            ddg_sites = (
                "site:walruslabs.xyz OR site:github.com/mystenlabs/walrus OR site:github.com/walruslabs"
                if self._is_walrus_query(query)
                else "site:docs.sui.io OR site:move-language.github.io"
            )
            params = {
                'q': f"{query} {ddg_sites}",
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }

            response = requests.get(search_url, params=params, timeout=5)
            data = response.json()

            content = ""
            if 'AbstractText' in data and data['AbstractText']:
                content += data['AbstractText'] + " "

            if 'RelatedTopics' in data:
                for topic in data['RelatedTopics'][:2]:
                    if isinstance(topic, dict) and 'Text' in topic:
                        content += topic['Text'] + " "

            content = content.strip()
            if content:
                self.logger.info("Found results via DuckDuckGo")
            return content or None

        except Exception as e:
            self.logger.error(f"DuckDuckGo search failed: {e}")
            return None

    def _get_walrus_price(self) -> Optional[str]:
        """Fetch Walrus token price via CoinGecko public API.
        Strategy: search for coin id by query 'walrus', then request simple price.
        """
        try:
            search_resp = requests.get(
                "https://api.coingecko.com/api/v3/search",
                params={"query": "walrus"},
                timeout=5,
            )
            search_resp.raise_for_status()
            data = search_resp.json() or {}
            coins = (data.get("coins") or [])
            if not coins:
                return None
            # pick the most relevant coin (first match)
            coin_id = coins[0].get("id")
            if not coin_id:
                return None
            price_resp = requests.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={"ids": coin_id, "vs_currencies": "usd"},
                timeout=5,
            )
            price_resp.raise_for_status()
            price_json = price_resp.json() or {}
            usd_price = (price_json.get(coin_id) or {}).get("usd")
            if usd_price is None:
                return None
            return f"Current {coins[0].get('name', 'Walrus')} price (CoinGecko): ${usd_price}"
        except Exception as e:
            self.logger.error(f"Failed to fetch Walrus price: {e}")
            return None

    def _search_walrus(self, query: str) -> Optional[str]:
        """Walrus-focused search combining docs, GitHub, and optional price."""
        # Try Tavily first with Walrus filters
        content = self._search_tavily(query)
        # Fallback to DuckDuckGo
        if not content:
            content = self._search_duckduckgo(query)
        # Optionally append price info when query asks about price/value/market cap
        if re.search(r"price|worth|value|market\s*cap|how much", query, re.IGNORECASE):
            price_info = self._get_walrus_price()
            if price_info:
                content = (content + "\n\n" if content else "") + price_info
        return content

    def _check_local_info(self, query: str) -> Optional[str]:
        query = query.lower()

        patterns = {
            "what_is_sui": [r"what is sui", r"sui blockchain", r"about sui", r"sui overview", r"define sui", r"sui definition"],
            "sui_token": [r"sui token", r"token economics", r"tokenomics", r"sui coin"],
            "sui_architecture": [r"architecture", r"how sui works", r"sui design", r"sui structure"],
            "move_language": [r"move language", r"programming language", r"smart contract language", r"move programming"],
            "sui_objects": [r"sui objects", r"object model", r"object-centric"],
            "sui_transactions": [r"transactions", r"tx", r"how transactions work"],
            "sui_consensus": [r"consensus", r"narwhal", r"bullshark", r"proof of stake"],
            "sui_storage": [r"storage", r"data storage", r"state storage"],
            "sui_smart_contracts": [r"smart contracts", r"contracts", r"dapps", r"applications"]
        }

        for info_key, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, query, re.IGNORECASE):
                    self.logger.info(f"Found local information for: {query}")
                    return SUI_BLOCKCHAIN_INFO[info_key]
        
        return None

    def search_sui_docs(self, query: str) -> str:
        self.logger.info(f"Searching for: {query}")

        # Walrus-first: if the query is about Walrus, prioritize Walrus sources
        if self._is_walrus_query(query):
            walrus_content = self._search_walrus(query)
            if walrus_content:
                return walrus_content

        content = self._check_local_info(query)
        if content:
            return content

        content = self._search_tavily(query)

        if not content:
            content = self._search_duckduckgo(query)

        if not content:
            self.logger.warning("No search results found")
            raise SearchError("Could not find relevant information in Sui documentation")

        return content

