import requests
from bot.config import Config
from adapters.errors import SymbolAddressMismatch, QuoteNotFound
from adapters.models import CryptocurrencyQuote
from adapters.utils import create_cryptocurrency_quote
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
                    if token['platform']['token_address'] == token_address:
                        return token['id']
                
                raise SymbolAddressMismatch('Token Address does not match with any symbol.')
            except KeyError:
                logger.error("Error: Cryptocurrency symbol not found or API structure changed.")
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
        url = f"{self.BASE_URL}/quotes/latest"
        parameters = {
            'id': id,
            'convert': 'USD'
        }
        response = requests.get(url, headers=self.headers, params=parameters)
        data = response.json()
        if response.status_code == 200:
            try:
                tokens = data['data'][symbol]
                
                for token in tokens:
                    if token['id'] == id:
                        return create_cryptocurrency_quote(token)
                            
                raise QuoteNotFound('Quote was not found for specified ID.')
            except KeyError:
                logger.error("Error: Cryptocurrency symbol not found or API structure changed.")
                return None
        else:
            logger.error(f"Error fetching data: {data.get('status', {}).get('error_message', 'Unknown error')}")
            return None
