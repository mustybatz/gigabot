import asyncio
import aiohttp
import discord
import logging
from discord import Webhook, Embed
from gigabot.adapters.models.dex_screener_models import Pair
from gigabot.bot.config import Config
from gigabot.services.price_service import PriceService

config = Config()
price_service = PriceService()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def send_alert(session, pair: Pair, gt: bool, value: float, change: float):
    """Sends an alert message via Discord webhook."""
    webhook = Webhook.from_url(config.DISCORD_WEBHOOK, session=session)

    # Create the embed message
    embed = Embed(
        title="Price Alert", color=discord.Color.blue() if gt else discord.Color.red()
    )
    embed.add_field(name="Pair", value=pair.baseToken.symbol)
    embed.add_field(
        name="Threshold", value=f"{'Greater than' if gt else 'Less than'} {value:.4f}%"
    )
    embed.add_field(
        name="Change",
        value=":chart_with_upwards_trend:" if gt else ":chart_with_downwards_trend:",
    )

    # Add the current change field to the embed message
    embed.add_field(
        name="Current Change",
        value=(
            f":chart_with_upwards_trend: {change:.2f}%"
            if change >= 0
            else f":chart_with_downwards_trend: {change:.2f}%"
        ),
        inline=False,
    )

    # Add the DexScreener dashboard URL to the embed message
    embed.add_field(name="DexScreener Dashboard", value=pair.url, inline=False)

    # Send the embed message
    await webhook.send(embed=embed)


def calculate_percentage_change(old, new):
    """Calculates the percentage change between two prices."""
    if old == 0:  # Prevent division by zero
        return float("inf")  # Infinite change if the old price was zero
    return ((new - old) / old) * 100


def transform_values(input_values):
    """Transforms comma-separated string values into a list of floats."""
    return [float(value.strip()) for value in input_values.split(",")]


async def alert_handler():
    """Monitors cryptocurrency prices and triggers alerts based on configured percentage thresholds."""
    gt_values = transform_values(config.ALERT_GREATER_THAN)
    lt_values = transform_values(config.ALERT_LESS_THAN)

    gt_values.sort()
    lt_values.sort()

    logging.info("Greater than values: %s", gt_values.sort())
    previous_price = None  # This will store the last price to compare changes
    baseline = None

    async with aiohttp.ClientSession() as session:
        while True:
            _, current_price = await price_service.fetch_dex_screener_data(
                config.SYMBOL
            )
            if current_price is None:
                logger.error("Failed to fetch price data. Retrying in 60 seconds.")
                await asyncio.sleep(60)
                continue

            if baseline is not None and previous_price is not None:
                change = calculate_percentage_change(
                    baseline, float(current_price.priceUsd)
                )
                a_change = calculate_percentage_change(
                    previous_price, float(current_price.priceUsd)
                )
                max_gt_value = max(
                    [gt_value for gt_value in gt_values if change >= gt_value],
                    default=None,
                )
                max_lt_value = min(
                    [lt_value for lt_value in lt_values if change <= lt_value],
                    default=None,
                )

                if a_change != 0:
                    # Send the most significant change alert
                    if max_gt_value is not None:
                        await send_alert(
                            session,
                            current_price,
                            gt=True,
                            value=max_gt_value,
                            change=change,
                        )
                    elif max_lt_value is not None:
                        await send_alert(
                            session,
                            current_price,
                            gt=False,
                            value=max_lt_value,
                            change=change,
                        )
            else:
                baseline = float(current_price.priceUsd)

            previous_price = float(current_price.priceUsd)
            logger.info("Current change: %s", calculate_percentage_change(
                    baseline, float(current_price.priceUsd)
                ))
            await asyncio.sleep(1)  # Check every second


if __name__ == "__main__":
    asyncio.run(alert_handler())
