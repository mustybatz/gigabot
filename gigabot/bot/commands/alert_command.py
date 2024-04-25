import logging
from typing import List
from gigabot.adapters.kubernetes_adapter import KubernetesAdapter
from gigabot.bot.commands.base_command import BaseCommand
from gigabot.adapters.coinmarketcap_adapter import CoinMarketCapAdapter
from gigabot.bot.config import Config
from gigabot.services.price_service import PriceService


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlertCommand(BaseCommand):
    """
    A command to set up price alerts for a specific cryptocurrency.
    """

    def __init__(self, context, symbol: str, above_than: List[float], below_than: List[float]):
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

        # Create instances of the adapters and services
        kubernetes_adapter = KubernetesAdapter()
        
        kubernetes_adapter.create_deployment(
            namespace=self.config.KUBERNETES_NAMESPACE,
            name="price-alert",
            image=self.config.KUBERNETES_IMAGE,
            env_vars={
                "SYMBOL": self.symbol,
                "ABOVE_THAN": ",".join(map(str, self.above_than)),
                "BELOW_THAN": ",".join(map(str, self.below_than)),
            },
            secret_name=self.config.KUBERNETES_SECRET_NAME,
            replicas=1,
        )

        