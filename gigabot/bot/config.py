import os
from dotenv import load_dotenv

class Config:
    """
    A singleton class that manages the configuration settings for the application.
    This class loads environment variables from a .env file and provides access
    to them via properties. This ensures that there is only one instance of the
    configuration settings throughout the application.

    Attributes:
        _instance (Config): A private class-level instance representing the singleton instance of the Config.
        _DISCORD_TOKEN (str): Private variable to hold the Discord token.
        _COINMARKETCAP_TOKEN (str): Private variable to hold the CoinMarketCap API token.
    """
    _instance = None

    def __new__(cls):
        """
        Ensure that only one instance of Config is created. If an instance already exists,
        it returns the existing instance instead of creating a new one.

        Returns:
            Config: The singleton instance of the Config class.
        """
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._load_environment_variables()
        return cls._instance

    @classmethod
    def _load_environment_variables(cls):
        """
        Load environment variables from the .env file into the class variables.
        This method is automatically called the first time Config is instantiated.
        """
        load_dotenv()
        cls._DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
        cls._COINMARKETCAP_TOKEN = os.getenv('COINMARKETCAP_TOKEN')
        cls._COINMARKETCAP_URL = os.getenv('COINMARKETCAP_URL')
        cls._DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK')
        cls._SYMBOL = os.getenv('SYMBOL')
        cls._ALERT_GREATER_THAN = os.getenv('ALERT_GREATER_THAN')
        cls._ALERT_LESS_THAN = os.getenv('ALERT_LESS_THAN')

    @property
    def DISCORD_TOKEN(self):
        """
        Get the Discord token from the environment variables.

        Returns:
            str: The Discord token.
        """
        return self._DISCORD_TOKEN

    @property
    def DISCORD_WEBHOOK(self):
        """
        Get the Discord webhook from the environment variables.

        Returns:
            str: The Discord token.
        """
        return self._DISCORD_WEBHOOK

    @property
    def COINMARKETCAP_TOKEN(self):
        """
        Get the CoinMarketCap API token from the environment variables.

        Returns:
            str: The CoinMarketCap API token.
        """
        return self._COINMARKETCAP_TOKEN
    
    @property
    def COINMARKETCAP_URL(self):
        """
        Get the CoinMarketCap API URL from the environment variables.

        Returns:
            str: The CoinMarketCap API URL.
        """
        return self._COINMARKETCAP_URL

    @property
    def SYMBOL(self):
        """
        Get the cryptocurrency symbol from the environment variables.

        Returns:
            str: The cryptocurrency symbol.
        """
        return self._SYMBOL
    
    @property
    def ALERT_GREATER_THAN(self):
        """
        Get the alert threshold for price greater than from the environment variables.

        Returns:
            str: The alert threshold for price greater than.
        """
        return self._ALERT_GREATER_THAN
    
    @property
    def ALERT_LESS_THAN(self):
        """
        Get the alert threshold for price less than from the environment variables.

        Returns:
            str: The alert threshold for price less than.
        """
        return self._ALERT_LESS_THAN