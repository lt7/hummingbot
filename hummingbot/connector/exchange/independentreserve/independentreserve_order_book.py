import datetime
from typing import Dict, Optional

from hummingbot.core.data_type.common import TradeType
from hummingbot.core.data_type.order_book import OrderBook
from hummingbot.core.data_type.order_book_message import (
    OrderBookMessage,
    OrderBookMessageType
)


class IndependentreserveOrderBook(OrderBook):

    @classmethod
    def snapshot_message_from_exchange(cls,
                                       msg: Dict[str, any],
                                       timestamp: float,
                                       metadata: Optional[Dict] = None) -> OrderBookMessage:
        """
        Creates a snapshot message with the order book snapshot message
        :param msg: the response from the exchange when requesting the order book snapshot
        :param timestamp: the snapshot timestamp
        :param metadata: a dictionary with extra information to add to the snapshot data
        :return: a snapshot message with the snapshot information received from the exchange
        """
        # Clean up timestamp provided in snapshot
        t = datetime.datetime.strptime(msg["CreatedTimestampUtc"].split(".")[0], '%Y-%m-%dT%H:%M:%S')
        # Nanoseconds provided but dateformat can't handle those
        t = t + datetime.timedelta(microseconds=int(msg["CreatedTimestampUtc"].split(".")[1][:-1]) / 1000)
        # t_float = float(t.strftime("%Y%m%d%H%M%S.%f"))
        bids = []
        asks = []
        for buy in msg["BuyOrders"]:
            value = [buy["Price"], buy["Volume"]]
            bids.append(value)

        for ask in msg["SellOrders"]:
            value = [ask["Price"], ask["Volume"]]
            asks.append(value)

        if metadata:
            msg.update(metadata)
        return OrderBookMessage(OrderBookMessageType.SNAPSHOT, {
            "trading_pair": metadata["trading_pair"],
            # "update_id": t_float,
            "update_id": 0,  # first update set nonce to 0
            "bids": bids,
            "asks": asks
        }, timestamp=timestamp)

    @classmethod
    def diff_message_from_exchange(cls,
                                   msg: Dict[str, any],
                                   timestamp: Optional[float] = None,
                                   metadata: Optional[Dict] = None) -> OrderBookMessage:
        """
        Creates a diff message with the changes in the order book received from the exchange
        :param msg: the changes in the order book
        :param timestamp: the timestamp of the difference
        :param metadata: a dictionary with extra information to add to the difference data
        :return: a diff message with the changes in the order book notified by the exchange
        """

        if metadata:
            msg.update(metadata)

        # Not a WebSocket diff update
        if "Channel" not in msg:
            # Clean up timestamp provided in snapshot
            t = datetime.datetime.strptime(msg["CreatedTimestampUtc"].split(".")[0], '%Y-%m-%dT%H:%M:%S')
            # Nanoseconds provided but dateformat can't handle those
            t = t + datetime.timedelta(microseconds=int(msg["CreatedTimestampUtc"].split(".")[1][:-1]) / 1000)
            # t_float = float(t.strftime("%Y%m%d%H%M%S.%f"))

            return OrderBookMessage(OrderBookMessageType.DIFF, {
                "trading_pair": str(metadata["trading_pair"]),
                # "first_update_id": msg["Nonce"],
                "update_id": msg["Nonce"],
                "bids": msg["BuyOrders"],
                "asks": msg["SellOrders"]
            }, timestamp=timestamp)
        else:
            # WebSocket diff messages
            # Secondary currency is always the fiat, check pair to determine which one
            fiat = (metadata["trading_pair"].split('-'))[1].lower()

            if msg["Event"] == "NewOrder" and "LimitBid" in msg["Data"]["OrderType"]:
                bid_price = msg["Data"]["Price"][fiat]

                update = {
                    "trading_pair": str(metadata["trading_pair"]),
                    "order_type": msg["Data"]["OrderType"],
                    "order_guid": msg["Data"]["OrderGuid"],
                    "update_id": msg["Nonce"],
                    "bids": [[str(bid_price), str(msg["Data"]["Volume"])]],
                    "asks": [[float(0), float(0)]],
                    "event": msg["Event"]
                }

            if msg["Event"] == "NewOrder" and "LimitOffer" in msg["Data"]["OrderType"]:
                ask_price = msg["Data"]["Price"][fiat]
                update = {
                    "trading_pair": str(metadata["trading_pair"]),
                    "order_type": msg["Data"]["OrderType"],
                    "order_guid": msg["Data"]["OrderGuid"],
                    "update_id": msg["Nonce"],
                    "bids": [[float(0), float(0)]],
                    "asks": [[str(ask_price), str(msg["Data"]["Volume"])]],
                    "event": msg["Event"]
                }

            if msg["Event"] == "OrderCanceled":
                update = {
                    "trading_pair": str(metadata["trading_pair"]),
                    "order_type": msg["Data"]["OrderType"],
                    "order_guid": msg["Data"]["OrderGuid"],
                    "update_id": msg["Nonce"],
                    "event": msg["Event"]
                }
            if msg["Event"] == "OrderChanged":

                if msg["Data"]["OrderType"] in ("MarketBid", "LimitBid"):
                    update = {
                        "trading_pair": str(metadata["trading_pair"]),
                        "order_type": msg["Data"]["OrderType"],
                        "order_guid": msg["Data"]["OrderGuid"],
                        "update_id": msg["Nonce"],
                        "price": msg["Data"]["Volume"],
                        "event": msg["Event"]
                    }

                if msg["Data"]["OrderType"] in ("MarketOffer", "LimitOffer"):
                    update = {
                        "trading_pair": str(metadata["trading_pair"]),
                        "order_type": msg["Data"]["OrderType"],
                        "order_guid": msg["Data"]["OrderGuid"],
                        "update_id": msg["Nonce"],
                        "price": msg["Data"]["Volume"],
                        "event": msg["Event"]
                    }

            return OrderBookMessage(OrderBookMessageType.DIFF, update, timestamp=timestamp)

    @classmethod
    def trade_message_from_exchange(cls, msg: Dict[str, any], metadata: Optional[Dict] = None):
        """
        Creates a trade message with the information from the trade event sent by the exchange. As primary pair (Xbt)
        can retrieve an update for any secondary (fiat) pair depending on which region (AU/NZ/SG/US) was executed in,
        need to extract primary pair from channel, and from update determine secondary pair.
        :param msg: the trade event details sent by the exchange
        :param metadata: a dictionary with extra information to add to trade message
        :return: a trade message with the details of the trade as provided by the exchange
        """
        if metadata:
            msg.update(metadata)
        ts = msg["Time"]
        currencies = msg["trading_pair"].split('-')
        for key, value in msg["Data"]["Price"].items():
            if currencies[1] == key:
                price = value
        # trading_pair = primaryCurrency[1].capitalize() + "-" + message_secondarypair
        # prices = msg["Data"]["Price"].item()
        return OrderBookMessage(OrderBookMessageType.TRADE, {
            "trading_pair": msg["trading_pair"],
            "trade_type": float(TradeType.SELL.value) if msg["Data"]["Side"] == "Sell" else float(TradeType.BUY.value),
            "trade_id": msg["Data"]["TradeGuid"],
            "update_id": msg["Nonce"],
            "price": price,
            "amount": msg["Data"]["Volume"]
        }, timestamp=ts * 1e-3)
