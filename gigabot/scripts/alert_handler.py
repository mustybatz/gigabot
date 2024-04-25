import asyncio
import aiohttp
import discord
import logging
from discord import Webhook, Embed
from gigabot.bot.config import Config
from gigabot.services.price_service import PriceService

config = Config()
price_service = PriceService()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Observer:
    """Observer interface for receiving price updates."""
    async def update(self, pair, gt, value, change):
        pass


class PriceMonitor:
    """Monitors cryptocurrency prices and notifies observers of changes."""
    def __init__(self):
        self._observers = []
        self.previous_price = None
        self.baseline = None

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    async def notify(self, session, pair, gt, value, change):
        for observer in self._observers:
            await observer.update(session, pair, gt, value, change)

    async def run(self):
        gt_values = transform_values(config.ALERT_GREATER_THAN)
        lt_values = transform_values(config.ALERT_LESS_THAN)
        gt_values.sort()
        lt_values.sort()

        async with aiohttp.ClientSession() as session:
            while True:
                _, current_price = await price_service.fetch_dex_screener_data(config.SYMBOL)
                if current_price is None:
                    logger.error("Failed to fetch price data. Retrying in 60 seconds.")
                    await asyncio.sleep(60)
                    continue

                if self.baseline is not None and self.previous_price is not None:
                    change = calculate_percentage_change(self.baseline, float(current_price.priceUsd))
                    a_change = calculate_percentage_change(self.previous_price, float(current_price.priceUsd))
                    max_gt_value = max([gt_value for gt_value in gt_values if change >= gt_value], default=None)
                    max_lt_value = min([lt_value for lt_value in lt_values if change <= lt_value], default=None)

                    if a_change != 0:
                        if max_gt_value is not None:
                            await self.notify(session, current_price, gt=True, value=max_gt_value, change=change)
                        elif max_lt_value is not None:
                            await self.notify(session, current_price, gt=False, value=max_lt_value, change=change)
                else:
                    self.baseline = float(current_price.priceUsd)

                self.previous_price = float(current_price.priceUsd)
                logger.info("Current change: %s", calculate_percentage_change(self.baseline, float(current_price.priceUsd)))
                await asyncio.sleep(1)


class DiscordAlert(Observer):
    """An observer that sends alerts via Discord webhook."""
    async def update(self, session, pair, gt, value, change):
        webhook = Webhook.from_url(config.DISCORD_WEBHOOK, session=session)
        embed = Embed(
            title="Price Alert",
            color=discord.Color.blue() if gt else discord.Color.red()
        )
        embed.add_field(name="Pair", value=pair.baseToken.symbol)
        embed.add_field(name="Threshold", value=f"{'Greater than' if gt else 'Less than'} {value:.4f}%")
        embed.add_field(name="Change", value=":chart_with_upwards_trend:" if gt else ":chart_with_downwards_trend:")
        embed.add_field(name="Current Change", value=(f":chart_with_upwards_trend: {change:.2f}%" if change >= 0 else f":chart_with_downwards_trend: {change:.2f}%"), inline=False)
        embed.add_field(name="DexScreener Dashboard", value=pair.url, inline=False)
        await webhook.send(embed=embed)


def calculate_percentage_change(old, new):
    """Calculates the percentage change between two prices."""
    if old == 0:
        return float("inf")
    return ((new - old) / old) * 100


def transform_values(input_values):
    """Transforms comma-separated string values into a list of floats."""
    return [float(value.strip()) for value in input_values.split(",")]


if __name__ == "__main__":
    monitor = PriceMonitor()
    discord_alert = DiscordAlert()
    monitor.attach(discord_alert)
   
