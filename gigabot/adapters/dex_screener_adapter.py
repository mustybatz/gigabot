import requests
from logging import getLogger
from gigabot.adapters.models.dex_screener_models import (
    Pair,
    PairsResponse,
    Social,
    Token,
    Info,
    Website,
)

logger = getLogger(__name__)


class DexScreenerAdapter:
    """
    Adapter class to handle interactions with the DexScreener API.
    This class abstracts the API endpoints of DexScreener and provides methods
    to fetch cryptocurrency pairs and token data in a simplified manner.
    """

    def __init__(self):
        """
        Initializes the adapter by setting up the base URL for the DexScreener API.
        """
        self.BASE_URL = "https://api.dexscreener.com/latest/dex"

    def get_pairs(self, chain_id: str, pair_addresses: str):
        """
        Fetches one or multiple pairs by chain ID and pair addresses.
        """
        url = f"{self.BASE_URL}/pairs/{chain_id}/{pair_addresses}"
        try:
            response = requests.get(url, timeout=10, headers={'Cache-Control': 'no-cache'})
            response.raise_for_status()
            data = response.json()
            pairs = []
            for pair_data in data.get("pairs", []):
                try:
                    pairs.append(self.parse_pair(pair_data))
                except Exception as e:
                    logger.error(f"Failed to parse pair: {pair_data} due to {e}")
            return PairsResponse(
                schemaVersion=data.get("schemaVersion", "unknown"), pairs=pairs
            )
        except requests.RequestException as e:
            logger.error(f"Failed to fetch pairs: {e}")
            return None

    def get_tokens(self, token_addresses: str):
        """
        Fetches one or multiple pairs by token addresses.
        """
        url = f"{self.BASE_URL}/tokens/{token_addresses}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            pairs = []
            for pair_data in data.get("pairs", []):
                try:
                    pairs.append(self.parse_pair(pair_data))
                except Exception as e:
                    logger.error(f"Failed to parse pair: {pair_data} due to {e}")
            return PairsResponse(
                schemaVersion=data.get("schemaVersion", "unknown"), pairs=pairs
            )
        except requests.RequestException as e:
            logger.error(f"Failed to fetch tokens: {e}")
            return None

    def search_pairs(self, query: str):
        """
        Searches for pairs matching a query.
        """
        url = f"{self.BASE_URL}/search?q={query}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            pairs = []
            for pair_data in data.get("pairs", []):
                try:
                    pairs.append(self.parse_pair(pair_data))
                except Exception as e:
                    logger.error(f"Failed to parse pair: {pair_data} due to {e}")
            return PairsResponse(
                schemaVersion=data.get("schemaVersion", "unknown"), pairs=pairs
            )
        except requests.RequestException as e:
            logger.error(f"Failed to search for pairs: {e}")
            return None

    def parse_pair(self, pair_data):
        """
        Parses pair data into a Pair object.
        """
        return Pair(
            chainId=pair_data["chainId"],
            dexId=pair_data["dexId"],
            url=pair_data["url"],
            pairAddress=pair_data["pairAddress"],
            baseToken=Token(**pair_data["baseToken"]),
            quoteToken=Token(**pair_data["quoteToken"]),
            priceNative=pair_data["priceNative"],
            priceUsd=pair_data.get("priceUsd"),
            txns=pair_data["txns"],
            volume=pair_data["volume"],
            priceChange=pair_data["priceChange"],
            liquidity=pair_data.get("liquidity"),
            fdv=pair_data.get("fdv"),
            pairCreatedAt=pair_data.get("pairCreatedAt"),
            info=self.parse_info(pair_data.get("info")),
        )

    def parse_info(self, info_data):
        """
        Parses additional info data into an Info object.
        """
        if not info_data:
            return None
        return Info(
            imageUrl=info_data["imageUrl"],
            websites=[Website(**website) for website in info_data.get("websites", [])],
            socials=[Social(**social) for social in info_data.get("socials", [])],
        )
