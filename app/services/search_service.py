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

    def _is_blockchain_related(self, query: str) -> bool:
        """Check if query is related to blockchain, Sui, Move, or Walrus topics."""
        q = query.lower()
        blockchain_terms = [
            r"blockchain", r"crypto", r"cryptocurrency", r"defi", r"nft", r"dapp",
            r"sui", r"move", r"walrus", r"smart contract", r"token", r"coin",
            r"validator", r"consensus", r"staking", r"gas", r"transaction",
            r"proof of work", r"proof of stake", r"pow", r"pos", r"mining", r"miners",
            r"distributed ledger", r"ledger", r"hash", r"block", r"epoch",
            r"decentralized", r"decentralization", r"peer to peer", r"p2p",
            r"wallet", r"address", r"private key", r"public key", r"signature",
            r"bitcoin", r"ethereum", r"solana", r"cardano", r"polkadot",
            r"blockhain", r"blockhchain", r"cryptocurreny", r"cryptocurrencty",
            r"install", r"setup", r"blockchain.*development", r"smart contract.*development", r"dapp.*development", r"blockchain.*programming", r"smart contract.*programming", r"move.*programming", r"tutorial",
            r"guide", r"how to.*blockchain", r"how to.*sui", r"how to.*walrus", r"how to.*move", r"how to.*crypto", r"getting started", r"beginner", r"api",
            r"walrus labs", r"walruslabs", r"walruss", r"walruss labs"
        ]
        return any(re.search(term, q, re.IGNORECASE) for term in blockchain_terms)

    def _search_tavily_site_specific(self, query: str) -> Optional[str]:
        """Search using our configured authoritative sources first"""
        if not settings.tavily_api_key:
            return None

        try:
            url = "https://api.tavily.com/search"
            
            # Use our configured authoritative sources
            walrus_sites = (
                "site:walruslabs.xyz OR site:github.com/mystenlabs/walrus OR site:github.com/walruslabs OR "
                "site:docs.walruslabs.xyz OR site:blog.walruslabs.xyz OR site:medium.com/@walruslabs OR "
                "site:mirror.xyz/walruslabs OR site:walrus.xyz OR site:walrus-docs.xyz OR "
                "site:walrusscan.com OR site:suiscan.xyz OR site:suiexplorer.com"
            )
            sui_sites = "site:docs.sui.io OR site:move-language.github.io OR site:move-book.com"
            query_filter = f"{walrus_sites} OR {sui_sites}" if self._is_walrus_query(query) else sui_sites
            search_query = f"{query} {query_filter}"

            payload = {
                "api_key": settings.tavily_api_key,
                "query": search_query,
                "search_depth": "basic",
                "max_results": 5
            }

            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()

            content = ""
            for result in data.get("results", []):
                content += f"{result.get('title', '')}\n{result.get('content', '')}\n\n"

            return content.strip() if content else None

        except Exception as e:
            self.logger.error(f"Tavily site-specific search failed: {e}")
            return None

    def _search_authoritative_sources(self, query: str) -> Optional[str]:
        """Search the most authoritative sources first: Sui docs, Walrus docs, Scans, Labs"""
        try:
            search_url = "https://api.duckduckgo.com/"
            
            # Prioritize the most authoritative sources
            authoritative_sites = (
                "site:docs.sui.io OR site:docs.walruslabs.xyz OR site:walrusscan.com OR site:suiscan.xyz OR "
                "site:walruslabs.xyz OR site:github.com/mystenlabs/walrus OR site:github.com/walruslabs OR "
                "site:blog.walruslabs.xyz OR site:medium.com/@walruslabs OR site:mirror.xyz/walruslabs"
            )
            params = {
                'q': f"{query} {authoritative_sites}",
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }

            response = requests.get(search_url, params=params, timeout=5)
            data = response.json()

            content = ""
            for result in data.get("results", []):
                content += f"{result.get('title', '')}\n{result.get('abstract', '')}\n\n"

            return content.strip() if content else None

        except Exception as e:
            self.logger.error(f"Authoritative sources search failed: {e}")
            return None

    def _search_duckduckgo_site_specific(self, query: str) -> Optional[str]:
        """Search using our configured authoritative sources first"""
        try:
            search_url = "https://api.duckduckgo.com/"
            
            # Use our configured authoritative sources
            ddg_sites = (
                "site:walruslabs.xyz OR site:github.com/mystenlabs/walrus OR site:github.com/walruslabs OR "
                "site:docs.walruslabs.xyz OR site:blog.walruslabs.xyz OR site:medium.com/@walruslabs OR "
                "site:mirror.xyz/walruslabs OR site:walrus.xyz OR site:walrusscan.com OR site:suiscan.xyz"
                if self._is_walrus_query(query)
                else "site:docs.sui.io OR site:move-language.github.io OR site:suiexplorer.com"
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
            for result in data.get("results", []):
                content += f"{result.get('title', '')}\n{result.get('abstract', '')}\n\n"

            return content.strip() if content else None

        except Exception as e:
            self.logger.error(f"DuckDuckGo site-specific search failed: {e}")
            return None

    def _search_tavily(self, query: str) -> Optional[str]:
        if not settings.tavily_api_key:
            return None

        try:
            url = "https://api.tavily.com/search"
            
            # For blockchain-related queries, use general internet search
            if self._is_blockchain_related(query):
                # General internet search with blockchain focus for broader results
                blockchain_keywords = "blockchain cryptocurrency crypto sui move walrus"
                search_query = f"{query} {blockchain_keywords}"
            else:
                # Use site-specific search for focused results
                walrus_sites = (
                    "site:walruslabs.xyz OR site:github.com/mystenlabs/walrus OR site:github.com/walruslabs OR "
                    "site:docs.walruslabs.xyz OR site:blog.walruslabs.xyz OR site:medium.com/@walruslabs OR "
                    "site:mirror.xyz/walruslabs OR site:walrus.xyz OR site:walrus-docs.xyz OR "
                    "site:walrusscan.com OR site:suiscan.xyz OR site:suiexplorer.com"
                )
                sui_sites = "site:docs.sui.io OR site:move-language.github.io OR site:move-book.com"
                query_filter = f"{walrus_sites} OR {sui_sites}" if self._is_walrus_query(query) else sui_sites
                search_query = f"{query} {query_filter}"

            payload = {
                "api_key": settings.tavily_api_key,
                "query": search_query,
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
            
            # For blockchain-related queries, use general search with blockchain keywords
            if self._is_blockchain_related(query):
                # General internet search with blockchain focus
                blockchain_terms = "blockchain sui move walrus cryptocurrency crypto"
                params = {
                    'q': f"{query} {blockchain_terms}",
                    'format': 'json',
                    'no_html': '1',
                    'skip_disambig': '1'
                }
            else:
                # Use site-specific search for focused results
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
            "what_is_walrus": [r"what is walrus", r"walrus blockchain", r"about walrus", r"walrus overview", r"define walrus", r"walrus definition", r"walrus", r"what is walruss", r"walruss", r"what.*walruss"],
            "walrus_da": [r"walrus da", r"data availability", r"walrus data availability", r"da solution"],
            "walrus_blobs": [r"walrus blob", r"blob storage", r"data blob", r"walrus data blob", r"blob", r"walrus.*blob"],
            "walrus_architecture": [r"walrus architecture", r"how walrus works", r"walrus design", r"walrus structure"],
            "walrus_token": [r"walrus token", r"wal token", r"wal coin", r"walrus economics", r"walrus tokenomics"],
            "walrus_sui": [r"walrus sui", r"walrus on sui", r"walrus sui integration"],
            "walrus_validators": [r"walrus validator", r"walrus validators", r"how many validator", r"walrus network", r"walrus nodes", r"validator.*walrus", r"how many.*walrus", r"validator", r"validators", r"how many.*validator", r"walrus.*validator", r"validator.*exist", r"validator.*count"],
            "walrus_epochs": [r"walrus epoch", r"walrus epochs", r"walrus epoch.*", r"epoch.*walrus", r"walrus.*epoch", r"how many.*day.*epoch", r"epoch.*day", r"walrus.*day", r"how long.*epoch", r"epoch.*duration", r"walrus.*duration", r"how long.*walrus.*epoch", r"walrus.*epoch.*duration", r"walrus.*epoch.*length", r"walrus.*epoch.*time", r"walrus.*epoch.*period"],
            "walrus_blob_ids": [r"walrus blob id", r"walrus blob ids", r"blob id", r"blob ids", r"walrus.*blob.*id", r"blob.*id.*walrus"],
            "walrus_storage_costs": [r"walrus storage cost", r"walrus storage price", r"walrus cost", r"walrus price", r"how much.*walrus", r"walrus.*cost", r"walrus.*price", r"storage.*cost.*walrus", r"walrus.*storage.*cost", r"how much.*store.*walrus", r"walrus.*fee", r"walrus.*billing"],
            "walrus_economics": [r"walrus economics", r"walrus tokenomics", r"walrus economy", r"walrus revenue", r"walrus income", r"walrus profit", r"walrus business", r"walrus financial", r"walrus economic", r"walrus.*economic", r"walrus.*financial"]
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
            "sui_objects": [r"sui objects", r"object model", r"object-centric", r"sui object", r"sui.*object", r"object.*sui"],
            "sui_transactions": [r"transactions", r"tx", r"how transactions work", r"sui transaction", r"sui.*transaction", r"transaction.*sui"],
            "sui_consensus": [r"consensus", r"narwhal", r"bullshark", r"proof of stake", r"sui consensus", r"sui.*consensus", r"consensus.*sui"],
            "sui_storage": [r"storage", r"data storage", r"state storage"],
            "sui_smart_contracts": [r"smart contracts", r"contracts", r"dapps", r"applications"],
            "sui_validators": [r"sui validator", r"sui validators", r"how many sui validator", r"sui network", r"sui nodes"],
            "sui_epochs": [r"sui epoch", r"sui epochs", r"epoch.*sui", r"sui.*epoch", r"epoch"],
            "move_smart_contracts": [r"move smart contract", r"move smart contracts", r"move contract", r"move contracts", r"smart contract", r"smart contracts", r"move.*contract", r"contract.*move"],
            "what_is_blockchain": [r"what is blockchain", r"blockchain", r"about blockchain", r"blockchain overview", r"define blockchain", r"blockchain definition", r"what.*blockchain", r"what is blockhain", r"blockhain", r"what.*blockhain"],
            "types_of_blockchain": [r"types of blockchain", r"blockchain types", r"kinds of blockchain", r"blockchain categories", r"different blockchain", r"blockchain classification", r"types of blockhain", r"blockhain types"],
            "distributed_ledger": [r"distributed ledger", r"distributed database", r"ledger technology", r"distributed system", r"what.*distributed.*ledger"],
            "proof_of_work": [r"proof of work", r"pow", r"mining", r"miners", r"what.*proof.*work", r"how.*mining.*work"],
            "sui_blockchain_type": [r"what type.*sui", r"sui.*type", r"what.*blockchain.*sui", r"sui.*blockchain.*type", r"type.*sui.*blockchain"],
            "blockchain_consensus": [r"consensus mechanism", r"consensus algorithm", r"blockchain consensus", r"how.*consensus.*work", r"consensus.*blockchain"],
            "blockchain_security": [r"blockchain security", r"crypto security", r"blockchain.*secure", r"security.*blockchain", r"blockchain.*attack"]
        }

        for info_key, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, query, re.IGNORECASE):
                    self.logger.info(f"Found local information for: {query}")
                    return SUI_BLOCKCHAIN_INFO[info_key]
        
        return None

    def search_sui_docs(self, query: str) -> str:
        self.logger.info(f"Searching for: {query}")

        # Check if query is blockchain-related, if not, reject it
        if not self._is_blockchain_related(query):
            raise SearchError("I only help with Sui blockchain, Move language, and Walrus topics. Please ask about blockchain, crypto, Sui, Move, or Walrus.")

        # STEP 1: Try to get real-time data first (price, network stats) for specific queries
        if re.search(r"price|worth|value|market\s*cap|how much", query, re.IGNORECASE):
            if self._is_walrus_query(query):
                price_info = self._get_walrus_price()
                if price_info:
                    self.logger.info("Found Walrus price info - returning immediately")
                    return price_info

        # STEP 2: Try to get real-time network stats for validator/network queries
        if re.search(r"validator|validators|network|nodes|stake|tps|stats|how many|count|exist", query, re.IGNORECASE):
            # Try Walrus network stats first
            if self._is_walrus_query(query):
                network_stats = self._get_walrus_network_stats()
                if network_stats:
                    self.logger.info("Found Walrus network stats - returning immediately")
                    return network_stats
            
            # Try Sui network stats
            if re.search(r"sui.*validator|sui.*validators|sui.*network|sui.*nodes|sui.*stake|sui.*tps", query, re.IGNORECASE):
                sui_stats = self._get_sui_network_stats()
                if sui_stats:
                    self.logger.info("Found Sui network stats - returning immediately")
                    return sui_stats

        # STEP 3: Check local info for general queries (after real-time data)
        content = self._check_local_info(query)
        if content:
            self.logger.info("Found local information - returning immediately")
            return content

        # STEP 4: Try Walrus-specific external search (if Walrus query)
        if self._is_walrus_query(query):
            walrus_content = self._search_walrus(query)
            if walrus_content:
                self.logger.info("Found Walrus-specific content - returning")
                return walrus_content

        # STEP 5: Try authoritative sources first (Sui docs, Walrus docs, Scans, Labs)
        content = self._search_authoritative_sources(query)
        if content:
            self.logger.info("Found content via authoritative sources - returning")
            return content

        # STEP 6: Try Tavily with site-specific search (exhaust our configured sources)
        content = self._search_tavily_site_specific(query)
        if content:
            self.logger.info("Found content via Tavily site-specific search - returning")
            return content

        # STEP 7: Try DuckDuckGo with site-specific search (exhaust our configured sources)
        content = self._search_duckduckgo_site_specific(query)
        if content:
            self.logger.info("Found content via DuckDuckGo site-specific search - returning")
            return content

        # STEP 8: Try Tavily with general internet search (broader but still blockchain-focused)
        content = self._search_tavily(query)
        if content:
            self.logger.info("Found content via Tavily general search - returning")
            return content

        # STEP 9: Try DuckDuckGo with general internet search (last resort before OpenAI)
        content = self._search_duckduckgo(query)
        if content:
            self.logger.info("Found content via DuckDuckGo general search - returning")
            return content

        # STEP 10: If still no content, try to get any available network stats as fallback
        if self._is_walrus_query(query):
            fallback_stats = self._get_walrus_network_stats()
            if fallback_stats:
                self.logger.info("Using Walrus network stats as fallback")
                return fallback_stats

        # STEP 11: Final fallback - let AI service handle with its knowledge
        self.logger.info("All search methods exhausted - allowing AI service to handle with its knowledge")
        return None

