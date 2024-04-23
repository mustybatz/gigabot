# file: services/price_service.py

import discord
from gigabot.adapters.coinmarketcap_adapter import CoinMarketCapAdapter
from gigabot.adapters.errors import SymbolAddressMismatch

class PriceService:
    def __init__(self):
        self.cmc_adapter = CoinMarketCapAdapter()

    async def fetch_cryptocurrency_data(self, token_address, symbol):
        try:
            token_id = self.cmc_adapter.map_to_id(token_address, symbol)
        except SymbolAddressMismatch as e:
            return f"{e}", None

        try:
            quote = self.cmc_adapter.get_quote(token_id, symbol)
            c_info = self.cmc_adapter.get_coin_info(token_id)
        except Exception as e:
            return f"{e}", None

        return None, self.format_response(c_info, quote)

    def format_response(self, coin_info, quote):
        embed = discord.Embed(
            title=f"{coin_info.name} coin info and price",
            description="Here's your info!",
            color=discord.Colour.blurple()
        )
        embed.add_field(name="Coin price and info", value=f"`{quote.quote.USD.price} USD`")
        embed.add_field(name="Market Cap", value=f"`{quote.self_reported_market_cap:,} USD`", inline=True)
        embed.add_field(name="% Change in 1h", value=f"`{quote.quote.USD.percent_change_1h:.4f}%`", inline=True)
        embed.add_field(name="% Change in 24h", value=f"`{quote.quote.USD.percent_change_24h:.4f}%`", inline=True)
        
        embed.set_footer(text="Thanks for using our bot.")
        embed.set_author(name="GIGABOT", icon_url="https://w0.peakpx.com/wallpaper/927/822/HD-wallpaper-triplechad-gigachad.jpg", url=coin_info.urls.website[0])
        embed.set_image(url=coin_info.logo)

        return embed
