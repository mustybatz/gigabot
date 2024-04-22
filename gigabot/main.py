from bot.bot_setup import run_bot
import logging.config

logging.config.fileConfig('logging.ini')

if __name__ == "__main__":
    run_bot()
