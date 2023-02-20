# from typing import Any, Dict

import hummingbot.connector.exchange.independentreserve.independentreserve_constants as CONSTANTS
from hummingbot.client.config.config_methods import using_exchange
from hummingbot.client.config.config_var import ConfigVar


CENTRALIZED = True
EXAMPLE_PAIR = "ZRX-ETH"
DEFAULT_FEES = [0.1, 0.1]

""" - unused in IR
def is_exchange_information_valid(exchange_info: Dict[str, Any]) -> bool:

    Verifies if a trading pair is enabled to operate with based on its exchange information
    :param exchange_info: the exchange information for a trading pair
    :return: True if the trading pair is enabled, False otherwise

    return exchange_info.get("status", None) == "TRADING" and "SPOT" in exchange_info.get("permissions", list())
"""


def public_rest_url(path_url: str, symbols: str = None, domain: str = "com") -> str:
    """
    Creates a full URL for provided public REST endpoint
    :param path_url: a public REST endpoint
    :param domain: the Independentreserve domain to connect to ("com" or "us"). The default value is "com"
    :param symbols: Primary and Secondary currency pairs
    :return: the full URL to the endpoint
    """
    if not symbols:
        return CONSTANTS.REST_URL.format(domain) + CONSTANTS.PUBLIC_API_VERSION + path_url
    else:
        return CONSTANTS.REST_URL.format(domain) + CONSTANTS.PUBLIC_API_VERSION + path_url.format(symbols[0], symbols[1])


def private_rest_url(path_url: str, domain: str = "com") -> str:
    """
    Creates a full URL for provided private REST endpoint
    :param path_url: a private REST endpoint
    :param domain: the Independentreserve domain to connect to ("com" or "us"). The default value is "com"
    :return: the full URL to the endpoint
    """
    return CONSTANTS.REST_URL.format(domain) + CONSTANTS.PRIVATE_API_VERSION + path_url


KEYS = {
    "independentreserve_api_key":
        ConfigVar(key="independentreserve_api_key",
                  prompt="Enter your Independentreserve API key >>> ",
                  required_if=using_exchange("independentreserve"),
                  is_secure=True,
                  is_connect_key=True),
    "independentreserve_api_secret":
        ConfigVar(key="independentreserve_api_secret",
                  prompt="Enter your Independentreserve API secret >>> ",
                  required_if=using_exchange("independentreserve"),
                  is_secure=True,
                  is_connect_key=True),
}
"""
OTHER_DOMAINS = ["independentreserve_us"]
OTHER_DOMAINS_PARAMETER = {"independentreserve_us": "us"}
OTHER_DOMAINS_EXAMPLE_PAIR = {"independentreserve_us": "BTC-USDT"}
OTHER_DOMAINS_DEFAULT_FEES = {"independentreserve_us": [0.1, 0.1]}
OTHER_DOMAINS_KEYS = {"independentreserve_us": {
    "independentreserve_us_api_key":
        ConfigVar(key="independentreserve_us_api_key",
                  prompt="Enter your Independentreserve US API key >>> ",
                  required_if=using_exchange("independentreserve_us"),
                  is_secure=True,
                  is_connect_key=True),
    "independentreserve_us_api_secret":
        ConfigVar(key="independentreserve_us_api_secret",
                  prompt="Enter your Independentreserve US API secret >>> ",
                  required_if=using_exchange("independentreserve_us"),
                  is_secure=True,
                  is_connect_key=True),
}}
"""
