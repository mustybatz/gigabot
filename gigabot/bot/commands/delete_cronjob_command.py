import discord
from gigabot.bot.commands.base_command import BaseCommand
from gigabot.adapters.kubernetes_adapter import KubernetesAdapter

from gigabot.adapters.errors import QuoteNotFound, SymbolAddressMismatch



class DeleteCronJobs(BaseCommand):
    """
    Command to fetch and display the current price of a specified cryptocurrency.

    This command allows users to query real-time price information for any supported
    cryptocurrency by interfacing with an external API, such as CoinMarketCap.
    """

    def __init__(self, context, namespace: str, name: str):
        """
        Initialize the PriceCommand with necessary parameters.

        Args:
            context: The context in which the command is executed.
            symbol (str): The cryptocurrency symbol to fetch the price for.
        """
        super().__init__(context)
        self.namespace = namespace
        self.name = name
        self.k8s_adapter = KubernetesAdapter()

    async def execute(self):
        """
        Execute the process of fetching and responding with the cryptocurrency price.

        This method will communicate with an external API to retrieve current price data
        and then send this information back to the user through the Discord context.
        """
        print(f"Deleting cronjob {self.name} in namespace {self.namespace}")

        cronjobs = self.k8s_adapter.list_cron_jobs(self.namespace)

        if self.name not in [cronjob.metadata.name for cronjob in cronjobs]:
            await self.context.respond(content=f"Cronjob {self.name} not found in namespace {self.namespace}")
            return

        self.k8s_adapter.delete_cron_job(self.namespace, self.name)

        await self.context.respond(content=f"Deleted cronjob {self.name} in namespace {self.namespace}")
