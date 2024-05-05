import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import discord
import logging
from gigabot.bot.commands.alert_command import AlertCommand
from gigabot.bot.commands.delete_alert_command import DeleteAlertCommand
from gigabot.bot.commands.delete_cronjob_command import DeleteCronJobs
from gigabot.bot.commands.list_alerts_command import ListAlertsCommand
from gigabot.bot.commands.list_cronjobs import ListCronJobs
from gigabot.bot.commands.price_command import PriceCommand
from gigabot.bot.commands.price_cron_command import PriceCronCommand
from gigabot.bot.config import Config

logger = logging.getLogger(__name__)

bot = discord.Bot()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"OK")


def start_server(port=3000):
    server_address = ('', port)
    httpd = ThreadedHTTPServer(server_address, RequestHandler)
    logger.info(f"Serving HTTP on 0.0.0.0 port {port} (http://0.0.0.0:{port}/)")
    httpd.serve_forever()


@bot.event
async def on_ready():
    logger.info(f"{bot.user} is online and ready!")


@bot.slash_command(name='price', help='Fetch the current price of a cryptocurrency')
async def price(ctx, symbol: str):
    command = PriceCommand(ctx, symbol)
    await command.run()


@bot.slash_command(name='price-cron', help='Fetch the current price of a cryptocurrency periodically')
async def price_cron(ctx, symbol: str, minute: int, hour: int):
    command = PriceCronCommand(ctx, symbol, minute, hour)
    await command.run()


@bot.slash_command(name='list-cron', help='List the current cronjobs')
async def list_cron(ctx):
    command = ListCronJobs(ctx, 'gigabot')
    await command.run()


@bot.slash_command(name='del-cron', help='Delete a specified cronjob')
async def delete_cron(ctx, name: str):
    command = DeleteCronJobs(ctx, 'gigabot', name)
    await command.run()


@bot.slash_command(name='alert', help='Set up price alerts for a specific cryptocurrency')
async def alert(ctx, symbol: str, above_than: str, below_than: str):
    command = AlertCommand(ctx, symbol, above_than, below_than)
    await command.run()


@bot.slash_command(name='list-alerts', help='List the current alerts')
async def list_alerts(ctx):
    command = ListAlertsCommand(ctx)
    await command.run()


@bot.slash_command(name='del-alert', help='Delete a specified alert')
async def delete_alert(ctx, name: str):
    command = DeleteAlertCommand(ctx, name)
    await command.run()


class Bot:
    @staticmethod
    def run_bot():
        conf = Config()

        # Start the HTTP server on a separate thread
        server_thread = threading.Thread(target=start_server, args=(3000,), daemon=True)
        server_thread.start()

        # Now run the Discord bot
        bot.run(conf.DISCORD_TOKEN)
