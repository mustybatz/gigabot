import logging
from typing import List

import discord
from gigabot.adapters.kubernetes_adapter import ExistingDeployment, KubernetesAdapter
from gigabot.bot.commands.base_command import BaseCommand
from gigabot.bot.config import Config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DeleteAlertCommand(BaseCommand):
    """
    A command to set up price alerts for a specific cryptocurrency.
    """

    def __init__(self, context, name: str):
        """
        Initializes the command with the alert name to delete.
        name: The name of the alert to delete.
        """
        super().__init__(context)
        
        self.config = Config()
        self.name = name
        self.k8s_adapter = KubernetesAdapter()

    async def execute(self):
        """
        Execute the command to fetch the price of the specified cryptocurrency.
        """

        await self.context.defer()

        depls = self.k8s_adapter.list_deployments("gigabot-dev")

        embed = discord.Embed(title="List of Alerts", color=discord.Color.blue())

        for depl in depls:
            if depl.metadata.name == self.name:
                self.k8s_adapter.delete_deployment("gigabot-dev", depl.metadata.name)

        await self.context.followup.send(f"Deleted alert {self.name}")
        
        

        