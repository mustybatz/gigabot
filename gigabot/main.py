import logging.config
from bot.bot_setup import run_bot


logging.config.fileConfig('logging.ini')

if __name__ == "__main__":
    run_bot()
