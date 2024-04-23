import discord
from gigabot.bot.commands.base_command import BaseCommand
from gigabot.adapters.kubernetes_adapter import KubernetesAdapter

from gigabot.adapters.errors import QuoteNotFound, SymbolAddressMismatch



class ListCronJobs(BaseCommand):
    """
    Command to fetch and display the current price of a specified cryptocurrency.

    This command allows users to query real-time price information for any supported
    cryptocurrency by interfacing with an external API, such as CoinMarketCap.
    """

    def __init__(self, context, namespace: str):
        """
        Initialize the PriceCommand with necessary parameters.

        Args:
            context: The context in which the command is executed.
            symbol (str): The cryptocurrency symbol to fetch the price for.
        """
        super().__init__(context)
        self.namespace = namespace
        self.k8s_adapter = KubernetesAdapter()

    async def execute(self):
        """
        Execute the process of fetching and responding with the cryptocurrency price.

        This method will communicate with an external API to retrieve current price data
        and then send this information back to the user through the Discord context.
        """
        print(f"Gathering cronjobs for {self.namespace} ns")
                
        cronjobs = self.k8s_adapter.get_cron_jobs(self.namespace)

        embed = discord.Embed(title=f"CronJobs in Namespace: {self.namespace}", color=discord.Color.green())

        for cronjob in cronjobs:
            embed.add_field(name=cronjob.metadata.name, value=f"Schedule: {cronjob.spec.schedule}", inline=False)

        await self.context.respond(embed=embed)
