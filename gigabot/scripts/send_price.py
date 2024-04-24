import aiohttp
from discord import Webhook
import sys
import os
from gigabot.bot.config import Config
from gigabot.services.price_service import PriceService

conf = Config()
price_service = PriceService()

async def send_message_via_webhook(symbol):
    print(f"Querying price for {symbol} symbol")
                
    _, embed = await price_service.fetch_cryptocurrency_data(symbol)
    # Create an aiohttp session
    async with aiohttp.ClientSession() as session:
        # Create a webhook instance from the URL stored in your config
        webhook = Webhook.from_url(conf.DISCORD_WEBHOOK, session=session)
        # Send a message using the webhook
        await webhook.send(embed=embed, username="GIGABOT")

async def main():
    symbol = os.getenv('SYMBOL')
    await send_message_via_webhook(symbol)


import asyncio
# Run the main function in an asyncio event loop
asyncio.run(main())
