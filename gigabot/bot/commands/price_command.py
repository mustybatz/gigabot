from discord.ext import commands
from bot.commands.base_command import BaseCommand
from gigabot.adapters.coinmarketcap_adapter import CoinMarketCapAdapter
import logging

from gigabot.adapters.errors import QuoteNotFound, SymbolAddressMismatch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PriceCommand(BaseCommand):
    """
    Command to fetch and display the current price of a specified cryptocurrency.

    This command allows users to query real-time price information for any supported
    cryptocurrency by interfacing with an external API, such as CoinMarketCap.
    """

    def __init__(self, context, symbol: str, token_address: str):
        """
        Initialize the PriceCommand with necessary parameters.

        Args:
            context: The context in which the command is executed.
            symbol (str): The cryptocurrency symbol to fetch the price for.
        """
        super().__init__(context)
        self.symbol = symbol
        self.token_address = token_address
        self.cmc_adapter = CoinMarketCapAdapter()

    async def execute(self):
        """
        Execute the process of fetching and responding with the cryptocurrency price.

        This method will communicate with an external API to retrieve current price data
        and then send this information back to the user through the Discord context.
        """
        print(f"Querying price for {self.symbol} symbol")
        token_id = None
        quote = None
        
        try:
            token_id = self.cmc_adapter.map_to_id(self.token_address, self.symbol)
        except SymbolAddressMismatch as e:
            response_message = f"{e.message}"
            await self.context.respond(response_message)
            return
        
        print(f"Found ID for [{self.symbol}]: {token_id}")
        
        try:
            quote = self.cmc_adapter.get_quote(token_id, self.symbol)
        except QuoteNotFound as e:
            response_message = f"{e.message}"
            await self.context.respond(response_message)
            return

        response_message = f"The current price of {self.symbol} is {quote.quote.USD.price} USD"
        
        
        await self.context.respond(response_message)
