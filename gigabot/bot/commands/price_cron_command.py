from discord.ext import commands
from gigabot.bot.commands.base_command import BaseCommand
from gigabot.adapters.coinmarketcap_adapter import CoinMarketCapAdapter
from gigabot.services.price_service import PriceService
from crontab import CronTab
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PriceCronCommand(BaseCommand):
    """
    Command to fetch and display the current price of a specified cryptocurrency periodically.

    This command allows users to query real-time price information for any supported
    cryptocurrency by interfacing with an external API, such as CoinMarketCap.
    """

    def __init__(self, context, symbol: str, token_address: str, minute: int, hour: int):
        """
        Initialize the PriceCronCommand with necessary parameters.

        Args:
            context: The context in which the command is executed.
            symbol (str): The cryptocurrency symbol to fetch the price for.
            token_address (str): The token address to fetch the price for.
            minute (int): Minute scheduling for cron.
            hour (int): Hour scheduling for cron.
        """
        super().__init__(context)
        self.symbol = symbol
        self.token_address = token_address
        self.minute = minute
        self.hour = hour
        self.cmc_adapter = CoinMarketCapAdapter()
        self.price_service = PriceService()

    async def execute(self):
        """
        Set up a cron job to run a script that fetches and displays cryptocurrency prices.
        """
        # Determine the absolute path to the script
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'send_price.py'))

        # Create a new cron job using the user 'root'
        with CronTab(user='root') as cron:
            # Construct the command to run the Python script using Poetry
            command = f'cd /Users/mustybatz/gigabot && poetry run python {script_path} {self.token_address} {self.symbol} > /tmp/log.txt'
            # Create a new job with the command
            job = cron.new(command=command)
            # Schedule the job
            job.minute.on(self.minute)
            job.hour.on(self.hour)

            # Write the job to the crontab
            cron.write()
            await self.context.send(f'Cron job for {self.symbol} scheduled to run every {self.hour} hour(s) at minute {self.minute}.')

# Note: You must have the appropriate permissions to modify the crontab for 'root' or any user.
# Also, ensure that your Poetry environment is correctly set up to run the Python script.
