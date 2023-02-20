from hummingbot.core.api_throttler.data_types import LinkedLimitWeightPair, RateLimit
from hummingbot.core.data_type.in_flight_order import OrderState

HBOT_ORDER_ID_PREFIX = "x-XEKWYICX"
MAX_ORDER_ID_LEN = 36

# Base URL
REST_URL = "https://api.independentreserve.{}"
WSS_URL = "wss://websockets.independentreserve.{}"

# API not versioned
PUBLIC_API_VERSION = "/Public"
PRIVATE_API_VERSION = "/Private"

# Public API endpoints or IndependentreserveClient function
PRIMARY_CURRENCY_CODES_PATH_URL = "/GetValidPrimaryCurrencyCodes"
SECONDARY_CURRENCY_CODES_PATH_URL = "/GetValidSecondaryCurrencyCodes"
TICKER_PRICE_CHANGE_PATH_URL = "/GetRecentTrades?primaryCurrencyCode={}&secondaryCurrencyCode={}&numberOfRecentTradesToRetrieve=50"
ORDER_BOOK_PATH_URL = "/GetOrderBook?primaryCurrencyCode={}&secondaryCurrencyCode={}"
MINIMUM_VOLUMES_PATH_URL = "/GetOrderMinimumVolumes"
PING_PATH_URL = "/GetValidMarketOrderTypes"

# Private API endpoints or IndependentreserveClient function
ACCOUNTS_PATH_URL = "/GetAccounts"
MY_TRADES_PATH_URL = "/GetTrades"
ORDER_PATH_URL = "/order"


WS_HEARTBEAT_TIME_INTERVAL = 30

# Independentreserve params

# Not all trading rules are available via API, so decimal places supported for each cryptocurrency from
# https://www.independentreserve.com/au/products/api#overview
# Currency, Code, Volume Decimal Places, Offer/Bid Decimal Places
SYMBOL_DECIMAL_PLACES = [
    {
        "Currency": "Bitcoin", "Code": "Xbt", "VolumeDecimalPlaces": 8, "QuoteDecimalPlaces": 2
    }, {
        "Currency": "Ethereum", "Code": "Eth", "VolumeDecimalPlaces": 8, "QuoteDecimalPlaces": 2
    }, {
        "Currency": "Ripple", "Code": "Xrp", "VolumeDecimalPlaces": 5, "QuoteDecimalPlaces": 5
    }, {
        "Currency": "Tether", "Code": "Usdt", "VolumeDecimalPlaces": 5, "QuoteDecimalPlaces": 5
    }, {
        "Currency": "Cardano", "Code": "Ada", "VolumeDecimalPlaces": 5, "QuoteDecimalPlaces": 5
    }, {
        "Currency": "Aave", "Code": "Aave", "VolumeDecimalPlaces": 5, "QuoteDecimalPlaces": 4
    }, {
        "Currency": "Basic Attention Token", "Code": "Bat", "VolumeDecimalPlaces": 5, "QuoteDecimalPlaces": 5
    }, {
        "Currency": "Bitcoin Cash", "Code": "Bch", "VolumeDecimalPlaces": 8, "QuoteDecimalPlaces": 2
    }, {
        "Currency": "Compound", "Code": "Comp", "VolumeDecimalPlaces": 8, "QuoteDecimalPlaces": 2
    }, {
        "Currency": "Dai", "Code": "Dai", "VolumeDecimalPlaces": 5, "QuoteDecimalPlaces": 5
    }, {
        "Currency": "Dogecoin", "Code": "Doge", "VolumeDecimalPlaces": 5, "QuoteDecimalPlaces": 5
    }, {
        "Currency": "Polkadot", "Code": "Dot", "VolumeDecimalPlaces": 5, "QuoteDecimalPlaces": 4
    }, {
        "Currency": "EOS", "Code": "Eos", "VolumeDecimalPlaces": 4, "QuoteDecimalPlaces": 4
    }, {
        "Currency": "Ethereum Classic", "Code": "Etc", "VolumeDecimalPlaces": 8, "QuoteDecimalPlaces": 2
    }, {
        "Currency": "The Graph", "Code": "Grt", "VolumeDecimalPlaces": 5, "QuoteDecimalPlaces": 5
    }, {
        "Currency": "Chainlink", "Code": "Link", "VolumeDecimalPlaces": 4, "QuoteDecimalPlaces": 4
    }, {
        "Currency": "Litecoin", "Code": "Ltc", "VolumeDecimalPlaces": 8, "QuoteDecimalPlaces": 2
    }, {
        "Currency": "OMG Network", "Code": "Omg", "VolumeDecimalPlaces": 5, "QuoteDecimalPlaces": 4
    }, {
        "Currency": "Perth Mint Gold Token", "Code": "Pmgt", "VolumeDecimalPlaces": 5, "QuoteDecimalPlaces": 2
    }, {
        "Currency": "Synthetix Network Token", "Code": "Snx", "VolumeDecimalPlaces": 5, "QuoteDecimalPlaces": 4
    }, {
        "Currency": "Uniswap", "Code": "Uniswap", "VolumeDecimalPlaces": 5, "QuoteDecimalPlaces": 4
    }, {
        "Currency": "USD Coin", "Code": "Usdc", "VolumeDecimalPlaces": 5, "QuoteDecimalPlaces": 5
    }, {
        "Currency": "Stellar Lumens", "Code": "Xlm", "VolumeDecimalPlaces": 5, "QuoteDecimalPlaces": 5
    }, {
        "Currency": "yearn.finance", "Code": "Yfi", "VolumeDecimalPlaces": 8, "QuoteDecimalPlaces": 2
    }, {
        "Currency": "0x0x", "Code": "Zrx", "VolumeDecimalPlaces": 5, "QuoteDecimalPlaces": 5
    }
]


SIDE_BUY = 'BUY'
SIDE_SELL = 'SELL'

TIME_IN_FORCE_GTC = 'GTC'  # Good till cancelled
TIME_IN_FORCE_IOC = 'IOC'  # Immediate or cancel
TIME_IN_FORCE_FOK = 'FOK'  # Fill or kill

# Rate Limit Type
REQUEST_WEIGHT = "REQUEST_WEIGHT"
ORDERS = "ORDERS"
ORDERS_24HR = "ORDERS_24HR"

# Rate Limit time intervals
ONE_MINUTE = 60
ONE_SECOND = 1
ONE_DAY = 86400

MAX_REQUEST = 5000

# Order States
ORDER_STATE = {
    "PENDING": OrderState.PENDING_CREATE,
    "NEW": OrderState.OPEN,
    "FILLED": OrderState.FILLED,
    "PARTIALLY_FILLED": OrderState.PARTIALLY_FILLED,
    "PENDING_CANCEL": OrderState.OPEN,
    "CANCELED": OrderState.CANCELLED,
    "REJECTED": OrderState.FAILED,
    "EXPIRED": OrderState.FAILED,
}

# Websocket event types
# Use Channel identifier of orderbook-SYM to cover all DIFF states
DIFF_EVENT_TYPE = "OrderBook"
TRADE_EVENT_TYPE = "Trade"
HEARTBEAT_EVENT_TYPE = "Heartbeat"

RATE_LIMITS = [
    # Pools
    RateLimit(limit_id=REQUEST_WEIGHT, limit=1200, time_interval=ONE_MINUTE),
    RateLimit(limit_id=ORDERS, limit=10, time_interval=ONE_SECOND),
    RateLimit(limit_id=ORDERS_24HR, limit=100000, time_interval=ONE_DAY),
    # Weighted Limits
    RateLimit(limit_id=TICKER_PRICE_CHANGE_PATH_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, 40)]),
    RateLimit(limit_id=PRIMARY_CURRENCY_CODES_PATH_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[(LinkedLimitWeightPair(REQUEST_WEIGHT, 10))]),
    RateLimit(limit_id=SECONDARY_CURRENCY_CODES_PATH_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[(LinkedLimitWeightPair(REQUEST_WEIGHT, 10))]),
    RateLimit(limit_id=MINIMUM_VOLUMES_PATH_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[(LinkedLimitWeightPair(REQUEST_WEIGHT, 10))]),
    RateLimit(limit_id=PING_PATH_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[(LinkedLimitWeightPair(REQUEST_WEIGHT, 10))]),
    RateLimit(limit_id=ORDER_BOOK_PATH_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, 50)]),
    RateLimit(limit_id=ACCOUNTS_PATH_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, 10)]),
    RateLimit(limit_id=MY_TRADES_PATH_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, 10)]),
    RateLimit(limit_id=ORDER_PATH_URL, limit=MAX_REQUEST, time_interval=ONE_MINUTE,
              linked_limits=[LinkedLimitWeightPair(REQUEST_WEIGHT, 1),
                             LinkedLimitWeightPair(ORDERS, 1),
                             LinkedLimitWeightPair(ORDERS_24HR, 1)]),
]
