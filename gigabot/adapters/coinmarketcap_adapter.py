import requests
from gigabot.bot.config import Config
from gigabot.adapters.errors import SymbolAddressMismatch
from gigabot.adapters.models.crypto_quote import CryptocurrencyQuote
from gigabot.adapters.utils import create_cryptocurrency_quote, create_coin_info
from logging import getLogger

logger = getLogger(__name__)

class CoinMarketCapAdapter:
    """
    Adapter class to handle interactions with the CoinMarketCap API.

    This class abstracts the API endpoints of CoinMarketCap and provides methods
    to fetch cryptocurrency prices and other data in a simplified manner.
    """


    def __init__(self):
        """
        Initializes the adapter with the API key loaded from the environment.
        """
        config = Config()
        self.api_key = config.COINMARKETCAP_TOKEN
        self.BASE_URL = config.COINMARKETCAP_URL
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key,
        }

    # Create a function for fetching the CoinMarketCap ID for a given token address    
    def map_to_id(self, token_address: str, symbol: str) -> int:
        """
        Fetches the CoinMarketCap ID for the specified token address.
        
        Args:
            token_address (str): The token address to fetch the ID for.
        
        Returns:
            int: The CoinMarketCap ID for the specified token address.
        
        Raises:
            SymbolAddressMismatch: Token Address does not match with any symbol.
        
        """
        
        url = f"{self.BASE_URL}/v1/cryptocurrency/map"
        parameters = {
            'start': 1,
            'limit': 100,
            'sort': 'id',
            'symbol': symbol
        }
        
        response = requests.get(url, headers=self.headers, params=parameters)
        data = response.json()
        
        print(f"Executing map_to_id for token_address: {token_address} and Symbol: {symbol}")
        
        if response.status_code == 200:
            try:
                for token in data['data']:
                    tkn:str = token['platform']['token_address']
                    if tkn.lower() == token_address.lower():
                        return token['id']
                
                raise SymbolAddressMismatch('Token Address does not match with any symbol.')
            except KeyError:
                logger.error("Error: Cryptocurrency symbol not found or API structure changed.")
                return None
            except SymbolAddressMismatch as e:
                logger.error(e)
                return None
        else:
            logger.error(f"Error fetching data: {data.get('status', {}).get('error_message', 'Unknown error')}")
            return None

    def get_quote(self, id: int, symbol: str) -> CryptocurrencyQuote:
        """
        Fetches the current quote of the specified cryptocurrency ID.

        Args:
            id (int): The cryptocurrency ID to fetch the price for.
            symbol (str): The cryptocurrency symbol to fetch the price for

        Returns:
            float: The current price of the cryptocurrency or None if not found.
        
        Raises:
            QuoteNotFound: If the symbol was not found for the specified ID.

        """
        url = f"{self.BASE_URL}/v2/cryptocurrency/quotes/latest"
        parameters = {
            'id': id
        }
        response = requests.get(url, headers=self.headers, params=parameters, timeout=60)
        data = response.json()
        if response.status_code == 200:
            try:
                tokens = data['data'][f'{id}']

                return create_cryptocurrency_quote(tokens)
            except KeyError:
                logger.error("Error: Cryptocurrency symbol not found or API structure changed.")
                return None
        else:
            logger.error(f"Error fetching data: {data.get('status', {}).get('error_message', 'Unknown error')}")
            return None

    def get_coin_info(self, coin_id: int):
        """
            Class docstring
        """
        url = f"{self.BASE_URL}/v2/cryptocurrency/info"
        parameters = {
            'id': coin_id
        }

        response = requests.get(url, headers=self.headers, params=parameters, timeout=60)
        data = response.json()

        if response.status_code == 200:
            try:
                coin = data['data'][f'{coin_id}']

                return create_coin_info(coin)
            except KeyError as e:
                logger.error(e)
                return None
        else:
            logger.error("Error fetching data: %s", data.get('status', {}).get('error_message', 'Unknown error'))
            return None