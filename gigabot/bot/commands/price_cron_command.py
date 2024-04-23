from discord.ext import commands
from gigabot.adapters.kubernetes_adapter import KubernetesAdapter
from gigabot.bot.commands.base_command import BaseCommand
from gigabot.adapters.coinmarketcap_adapter import CoinMarketCapAdapter
from gigabot.bot.config import Config
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
        self.k8s_adapter = KubernetesAdapter()
        self.price_service = PriceService()
        self.config = Config()

    async def execute(self):
        """
        Set up a cron job to run a script that fetches and displays cryptocurrency prices.
        """
        # Get the CoinMarketCap URL from the environment variables
        cmc_url = self.config.COINMARKETCAP_URL

        # Get the Discord webhook URL from the environment variables
        discord_webhook = self.config.DISCORD_WEBHOOK

        # Create a Kubernetes CronJob to run the price fetching script
        self.k8s_adapter.create_cron_job(
            namespace="gigabot",
            name=f"price-cron-{self.symbol}",
            hours=self.hour,
            minutes=self.minute,
            image="registry.digitalocean.com/gigabot/gigabot-task:latest",
            env_vars={
                "COINMARKETCAP_URL": cmc_url,
                "DISCORD_WEBHOOK": discord_webhook,
                "SYMBOL": self.symbol,
                "TOKEN_ADDRESS": self.token_address,
            },
            secret_name="gigabot-secrets",
            image_pull_secret="gigabot"
        )
        
        await self.context.send(f'Cron job for {self.symbol} scheduled to run every {self.hour} hour(s) at minute {self.minute}.')
