import discord
import discord.ext.tasks
from gigabot.bot.config import Config
from gigabot.bot.commands.price_command import PriceCommand
from gigabot.bot.commands.price_cron_command import PriceCronCommand
from gigabot.bot.commands.list_cronjobs import ListCronJobs
from gigabot.bot.commands.delete_cronjob_command import DeleteCronJobs
import logging

import discord.ext

logger = logging.getLogger(__name__)

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is online and ready!")
    
@bot.slash_command(name='price', help='Fetch the current price of a cryptocurrency')
async def price(ctx, symbol: str):
    command = PriceCommand(ctx, symbol)
    await command.run()

@bot.slash_command(name='price-cron', help='Fetch the current price of a cryptocurrency periodically')
async def price_cron(ctx, symbol: str, minute: int, hour: int):
    command = PriceCronCommand(ctx, symbol, minute, hour)
    await command.run()

@bot.slash_command(name='list-cron', help='Fetch the current cronjobs')
async def list_cron(ctx):
    command = ListCronJobs(ctx, 'gigabot')
    await command.run()

@bot.slash_command(name='del-cron', help='Delete the given cronjob')
async def delete_cron(ctx, name: str):
    command = DeleteCronJobs(ctx, 'gigabot', name)
    await command.run()


def run_bot():
    conf = Config()
    bot.run(conf.DISCORD_TOKEN)