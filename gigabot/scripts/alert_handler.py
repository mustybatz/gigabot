import time
from discord import Webhook
from gigabot.bot.config import Config
from gigabot.services.price_service import PriceService

config = Config()
price_service = PriceService()

def transform_values(input_values):
    values = input_values.split(",")
    transformed_values = []
    for value in values:
        transformed_values.append(float(value))
    return transformed_values

def alert_handler():
    gt_values = transform_values(config.ALERT_GREATER_THAN)
    lt_values = transform_values(config.ALERT_LESS_THAN)

    result, pair = price_service.fetch_dex_screener_data(config.SYMBOL)
    
    if result is not None:
        print(result)
        return
    
    for gt_value in gt_values:


    

def main():
    while True:
        alert_handler()
        time.sleep(1)

if __name__ == "__main__":
    main()
