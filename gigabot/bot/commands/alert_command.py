import logging
from typing import List
from gigabot.adapters.kubernetes_adapter import ExistingDeployment, KubernetesAdapter
from gigabot.bot.commands.base_command import BaseCommand
from gigabot.bot.config import Config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlertCommand(BaseCommand):
    """
    A command to set up price alerts for a specific cryptocurrency.
    """

    def __init__(self, context, symbol: str, above_than: str, below_than: str):
        """
        Initializes the command with the symbol of the cryptocurrency and the price thresholds for the alert.
        symbol: The symbol of the cryptocurrency to set up the alert for.
        above_than: A list of price thresholds above which to trigger the alert.
        below_than: A list of price thresholds below which to trigger the alert.
        """
        super().__init__(context)
        self.symbol = symbol
        self.above_than = above_than
        self.below_than = below_than
        
        self.config = Config()

    async def execute(self):
        """
        Execute the command to fetch the price of the specified cryptocurrency.
        """

        await self.context.defer()

        # Proceed with your long-running task
        cmc_url = self.config.COINMARKETCAP_URL
        discord_webhook = self.config.DISCORD_WEBHOOK


        # Create instances of the adapters and services
        kubernetes_adapter = KubernetesAdapter()

        name = f"price-alert-{self.symbol}".lower()
        
        try:
            kubernetes_adapter.create_deployment(
                namespace="gigabot-dev",
                name=name,
                image="registry.digitalocean.com/gigabot/gigabot-alert:latest",
                env_vars={
                    "SYMBOL": self.symbol,
                    "ALERT_GREATER_THAN": self.above_than,
                    "ALERT_LESS_THAN": self.below_than,
                    "COINMARKETCAP_URL": cmc_url,
                    "DISCORD_WEBHOOK": discord_webhook  
                },
                secret_name="gigabot-secret-dev",
                replicas=1,
                image_pull_secret="gigabot"
            )
        except ExistingDeployment as e:
            logger.error(f"Deployment already exists: {e}")

            await self.context.followup.send("Deployment already exists")
            return

        await self.context.followup.send(
            "Deployment created"
        )
        

        