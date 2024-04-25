import logging
from typing import List

import discord
from gigabot.adapters.kubernetes_adapter import ExistingDeployment, KubernetesAdapter
from gigabot.bot.commands.base_command import BaseCommand
from gigabot.bot.config import Config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ListAlertsCommand(BaseCommand):
    """
    A command to set up price alerts for a specific cryptocurrency.
    """

    def __init__(self, context):
        """
        Initializes the command with the symbol of the cryptocurrency and the price thresholds for the alert.
        symbol: The symbol of the cryptocurrency to set up the alert for.
        above_than: A list of price thresholds above which to trigger the alert.
        below_than: A list of price thresholds below which to trigger the alert.
        """
        super().__init__(context)
        
        self.config = Config()
        self.k8s_adapter = KubernetesAdapter()

    async def execute(self):
        """
        Execute the command to fetch the price of the specified cryptocurrency.
        """

        await self.context.defer()

        depls = self.k8s_adapter.list_deployments("gigabot-dev")

        embed = discord.Embed(title="List of Alerts", color=discord.Color.blue())

        for depl in depls:
            if depl.metadata.name.startswith("price-alert-"):
                embed.add_field(name="name", value=depl.metadata.name, inline=False)

        await self.context.followup.send(embed=embed)
        
        

        