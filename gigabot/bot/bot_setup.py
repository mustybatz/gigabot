import discord
from bot.config import Config
from bot.commands.price_command import PriceCommand
import logging

logger = logging.getLogger(__name__)

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is online and ready!")
    
@bot.slash_command(name='price', help='Fetch the current price of a cryptocurrency')
async def price(ctx, symbol: str, token_address: str):
    command = PriceCommand(ctx, symbol, token_address)
    await command.run()

def run_bot():
    
    conf = Config()
    
    bot.run(conf.DISCORD_TOKEN)