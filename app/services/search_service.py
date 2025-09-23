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
from app.data.walrus_info import WALRUS_INFO



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
            walrus_sites = (
                "site:walruslabs.xyz OR site:github.com/mystenlabs/walrus OR site:github.com/walruslabs OR "
                "site:docs.walruslabs.xyz OR site:blog.walruslabs.xyz OR site:medium.com/@walruslabs OR "
                "site:mirror.xyz/walruslabs OR site:walrus.xyz OR site:walrus-docs.xyz OR "
                "site:walrusscan.com OR site:suiscan.xyz OR site:suiexplorer.com"
            )
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
            ddg_sites = (
                "site:walruslabs.xyz OR site:github.com/mystenlabs/walrus OR site:github.com/walruslabs OR "
                "site:docs.walruslabs.xyz OR site:blog.walruslabs.xyz OR site:medium.com/@walruslabs OR "
                "site:mirror.xyz/walruslabs OR site:walrus.xyz OR site:walrusscan.com OR site:suiscan.xyz"
                if self._is_walrus_query(query)
                else "site:docs.sui.io OR site:move-language.github.io OR site:suiscan.xyz OR site:suiexplorer.com"
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

    def _get_walrus_network_stats(self) -> Optional[str]:
        """Fetch Walrus network statistics from Walrus Scan API."""
        try:
            # Try Walrus Scan API for network stats
            stats_resp = requests.get(
                "https://api.walrusscan.com/api/v1/network/stats",
                timeout=5,
            )
            stats_resp.raise_for_status()
            stats_data = stats_resp.json()
            
            info_parts = []
            if "validators" in stats_data:
                validator_count = stats_data.get("validators", {}).get("total", 0)
                info_parts.append(f"Active Validators: {validator_count}")
            
            if "network" in stats_data:
                network_info = stats_data.get("network", {})
                if "total_stake" in network_info:
                    total_stake = network_info.get("total_stake", 0)
                    info_parts.append(f"Total Stake: {total_stake:,} WAL")
                
                if "active_nodes" in network_info:
                    active_nodes = network_info.get("active_nodes", 0)
                    info_parts.append(f"Active Nodes: {active_nodes}")
            
            if info_parts:
                return f"Walrus Network Stats (Walrus Scan): {' | '.join(info_parts)}"
            
        except Exception as e:
            self.logger.error(f"Failed to fetch Walrus network stats: {e}")
        
        # Fallback: Return basic Walrus network info if API fails
        return "Walrus Network: The Walrus network consists of distributed validators that provide data availability services. Validator count varies based on network growth and adoption. For real-time stats, visit walrusscan.com"

    def _get_sui_network_stats(self) -> Optional[str]:
        """Fetch Sui network statistics from Sui Scan API."""
        try:
            # Try Sui Scan API for network stats
            stats_resp = requests.get(
                "https://api.suiscan.xyz/api/v1/network/stats",
                timeout=5,
            )
            stats_resp.raise_for_status()
            stats_data = stats_resp.json()
            
            info_parts = []
            if "validators" in stats_data:
                validator_count = stats_data.get("validators", {}).get("total", 0)
                info_parts.append(f"Active Validators: {validator_count}")
            
            if "network" in stats_data:
                network_info = stats_data.get("network", {})
                if "total_stake" in network_info:
                    total_stake = network_info.get("total_stake", 0)
                    info_parts.append(f"Total Stake: {total_stake:,} SUI")
                
                if "tps" in network_info:
                    tps = network_info.get("tps", 0)
                    info_parts.append(f"Current TPS: {tps}")
            
            if info_parts:
                return f"Sui Network Stats (Sui Scan): {' | '.join(info_parts)}"
            
        except Exception as e:
            self.logger.error(f"Failed to fetch Sui network stats: {e}")
        
        return None

    def _search_walrus(self, query: str) -> Optional[str]:
        content = self._search_tavily(query)
        if not content:
            content = self._search_duckduckgo(query)
        
        # Add price info for price-related queries
        if re.search(r"price|worth|value|market\s*cap|how much", query, re.IGNORECASE):
            price_info = self._get_walrus_price()
            if price_info:
                content = (content + "\n\n" if content else "") + price_info
        
        # Add network stats for validator/network queries
        if re.search(r"validator|validators|network|nodes|stake|tps|stats", query, re.IGNORECASE):
            network_stats = self._get_walrus_network_stats()
            if network_stats:
                content = (content + "\n\n" if content else "") + network_stats
        
        return content

    def _check_local_info(self, query: str) -> Optional[str]:
        query = query.lower()

        # Check Walrus patterns first for faster response
        walrus_patterns = {
            "what_is_walrus": [r"what is walrus", r"walrus blockchain", r"about walrus", r"walrus overview", r"define walrus", r"walrus definition", r"walrus"],
            "walrus_da": [r"walrus da", r"data availability", r"walrus data availability", r"da solution"],
            "walrus_blobs": [r"walrus blob", r"blob storage", r"data blob", r"walrus data blob", r"blob", r"walrus.*blob"],
            "walrus_architecture": [r"walrus architecture", r"how walrus works", r"walrus design", r"walrus structure"],
            "walrus_token": [r"walrus token", r"wal token", r"wal coin", r"walrus economics", r"walrus tokenomics"],
            "walrus_sui": [r"walrus sui", r"walrus on sui", r"walrus sui integration"],
            "walrus_validators": [r"walrus validator", r"walrus validators", r"how many validator", r"walrus network", r"walrus nodes", r"validator.*walrus", r"how many.*walrus", r"validator", r"validators"]
        }

        for info_key, pattern_list in walrus_patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, query, re.IGNORECASE):
                    self.logger.info(f"Found local Walrus information for: {query}")
                    return WALRUS_INFO[info_key]

        patterns = {
            "what_is_sui": [r"what is sui", r"sui blockchain", r"about sui", r"sui overview", r"define sui", r"sui definition"],
            "sui_token": [r"sui token", r"token economics", r"tokenomics", r"sui coin"],
            "sui_architecture": [r"architecture", r"how sui works", r"sui design", r"sui structure"],
            "move_language": [r"move language", r"programming language", r"smart contract language", r"move programming"],
            "sui_objects": [r"sui objects", r"object model", r"object-centric"],
            "sui_transactions": [r"transactions", r"tx", r"how transactions work"],
            "sui_consensus": [r"consensus", r"narwhal", r"bullshark", r"proof of stake"],
            "sui_storage": [r"storage", r"data storage", r"state storage"],
            "sui_smart_contracts": [r"smart contracts", r"contracts", r"dapps", r"applications"],
            "sui_validators": [r"sui validator", r"sui validators", r"how many sui validator", r"sui network", r"sui nodes"]
        }

        for info_key, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, query, re.IGNORECASE):
                    self.logger.info(f"Found local information for: {query}")
                    return SUI_BLOCKCHAIN_INFO[info_key]
        
        return None

    def search_sui_docs(self, query: str) -> str:
        self.logger.info(f"Searching for: {query}")

        # Check local info first for fastest response
        content = self._check_local_info(query)
        if content:
            return content

        # If Walrus query, try Walrus-specific search
        if self._is_walrus_query(query):
            walrus_content = self._search_walrus(query)
            if walrus_content:
                return walrus_content
            
            # If no content found but it's a Walrus query, try to get network stats
            if re.search(r"validator|validators|network|nodes|stake|tps|stats", query, re.IGNORECASE):
                network_stats = self._get_walrus_network_stats()
                if network_stats:
                    return network_stats

        # Fallback to general search
        content = self._search_tavily(query)

        if not content:
            content = self._search_duckduckgo(query)
        
        # Add Sui network stats for Sui validator/network queries
        if re.search(r"sui.*validator|sui.*validators|sui.*network|sui.*nodes|sui.*stake|sui.*tps", query, re.IGNORECASE):
            sui_stats = self._get_sui_network_stats()
            if sui_stats:
                content = (content + "\n\n" if content else "") + sui_stats

        if not content:
            self.logger.warning("No search results found")
            raise SearchError("Could not find relevant information in Sui documentation")

        return content

