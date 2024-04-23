import aiohttp
from discord import Webhook
import sys
from gigabot.bot.config import Config
from gigabot.services.price_service import PriceService

conf = Config()
price_service = PriceService()

async def send_message_via_webhook(token_address, symbol):
    print(f"Querying price for {symbol} symbol")
                
    _, embed = await price_service.fetch_cryptocurrency_data(token_address, symbol)
    # Create an aiohttp session
    async with aiohttp.ClientSession() as session:
        # Create a webhook instance from the URL stored in your config
        webhook = Webhook.from_url(conf.DISCORD_WEBHOOK, session=session)
        # Send a message using the webhook
        await webhook.send(embed=embed, username="GIGABOT")

async def main():
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <token_address> <symbol>")
        return
    
    token_address = sys.argv[1]
    symbol = sys.argv[2]
    await send_message_via_webhook(token_address, symbol)


import asyncio
# Run the main function in an asyncio event loop
asyncio.run(main())
