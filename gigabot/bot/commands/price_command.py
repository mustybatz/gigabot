from gigabot.bot.commands.base_command import BaseCommand
from gigabot.adapters.coinmarketcap_adapter import CoinMarketCapAdapter
from gigabot.services.price_service import PriceService

class PriceCommand(BaseCommand):
    """
    Command to fetch and display the current price of a specified cryptocurrency.

    This command allows users to query real-time price information for any supported
    cryptocurrency by interfacing with an external API, such as CoinMarketCap.
    """

    def __init__(self, context, symbol: str):
        """
        Initialize the PriceCommand with necessary parameters.

        Args:
            context: The context in which the command is executed.
            symbol (str): The cryptocurrency symbol to fetch the price for.
        """
        super().__init__(context)
        self.symbol = symbol
        self.cmc_adapter = CoinMarketCapAdapter()
        self.price_service = PriceService()

    async def execute(self):
        """
        Execute the process of fetching and responding with the cryptocurrency price.

        This method will communicate with an external API to retrieve current price data
        and then send this information back to the user through the Discord context.
        """
        print(f"Querying price for {self.symbol} symbol")
                
        _, embed = await self.price_service.fetch_cryptocurrency_data(self.symbol)
        
        await self.context.respond(embed=embed)
