import discord
import discord.ext.tasks
from gigabot.bot.config import Config
from gigabot.bot.commands.price_command import PriceCommand
from gigabot.bot.commands.price_cron_command import PriceCronCommand
import logging

import discord.ext

logger = logging.getLogger(__name__)

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is online and ready!")
    
@bot.slash_command(name='price', help='Fetch the current price of a cryptocurrency')
async def price(ctx, symbol: str, token_address: str):
    command = PriceCommand(ctx, symbol, token_address)
    await command.run()

@bot.slash_command(name='price-cron', help='Fetch the current price of a cryptocurrency periodically')
async def price_cron(ctx, symbol: str, token_address: str, minute: int, hour: int):
    command = PriceCronCommand(ctx, symbol, token_address, minute, hour)
    await command.run()


def run_bot():
    conf = Config()
    bot.run(conf.DISCORD_TOKEN)