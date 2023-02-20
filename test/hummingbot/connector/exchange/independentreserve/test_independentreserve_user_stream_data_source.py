import asyncio
import json
# import re
import unittest

# from aioresponses import aioresponses
from typing import (
    Any,
    Awaitable,
    Dict,
    Optional,
)
from unittest.mock import MagicMock
# from unittest.mock import AsyncMock MagicMock, patch


import hummingbot.connector.exchange.independentreserve.independentreserve_constants as CONSTANTS
# import hummingbot.connector.exchange.independentreserve.independentreserve_utils as utils
from hummingbot.connector.exchange.independentreserve.independentreserve_api_user_stream_data_source import IndependentreserveAPIUserStreamDataSource
from hummingbot.connector.exchange.independentreserve.independentreserve_auth import IndependentreserveAuth
from hummingbot.core.api_throttler.async_throttler import AsyncThrottler
from test.hummingbot.connector.network_mocking_assistant import NetworkMockingAssistant


class IndependentreserveUserStreamDataSourceUnitTests(unittest.TestCase):
    # the level is required to receive logs from the data source logger
    level = 0

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.ev_loop = asyncio.get_event_loop()
        cls.base_asset = "COINALPHA"
        cls.quote_asset = "HBOT"
        cls.trading_pair = f"{cls.base_asset}-{cls.quote_asset}"
        cls.ex_trading_pair = cls.base_asset + cls.quote_asset
        cls.domain = "com"

        cls.listen_key = "TEST_LISTEN_KEY"

    def setUp(self) -> None:
        super().setUp()
        self.log_records = []
        self.listening_task: Optional[asyncio.Task] = None
        self.mocking_assistant = NetworkMockingAssistant()

        self.throttler = AsyncThrottler(rate_limits=CONSTANTS.RATE_LIMITS)
        self.mock_time_provider = MagicMock()
        self.mock_time_provider.time.return_value = 1000
        self.data_source = IndependentreserveAPIUserStreamDataSource(
            auth=IndependentreserveAuth(api_key="TEST_API_KEY", secret_key="TEST_SECRET", time_provider=self.mock_time_provider),
            domain=self.domain,
            throttler=self.throttler
        )

        self.data_source.logger().setLevel(1)
        self.data_source.logger().addHandler(self)

        self.resume_test_event = asyncio.Event()

    def tearDown(self) -> None:
        self.listening_task and self.listening_task.cancel()
        super().tearDown()

    def handle(self, record):
        self.log_records.append(record)

    def _is_logged(self, log_level: str, message: str) -> bool:
        return any(record.levelname == log_level and record.getMessage() == message
                   for record in self.log_records)

    def _raise_exception(self, exception_class):
        raise exception_class

    def _create_exception_and_unlock_test_with_event(self, exception):
        self.resume_test_event.set()
        raise exception

    def _create_return_value_and_unlock_test_with_event(self, value):
        self.resume_test_event.set()
        return value

    def async_run_with_timeout(self, coroutine: Awaitable, timeout: float = 1):
        ret = self.ev_loop.run_until_complete(asyncio.wait_for(coroutine, timeout))
        return ret

    def _error_response(self) -> Dict[str, Any]:
        resp = {
            "code": "ERROR CODE",
            "msg": "ERROR MESSAGE"
        }

        return resp

    def _user_update_event(self):
        # Balance Update
        resp = {
            "e": "balanceUpdate",
            "E": 1573200697110,
            "a": "BTC",
            "d": "100.00000000",
            "T": 1573200697068
        }
        return json.dumps(resp)

    def _successfully_subscribed_event(self):
        resp = {
            "result": None,
            "id": 1
        }
        return resp

    def test_last_recv_time(self):
        # Initial last_recv_time
        self.assertEqual(0, self.data_source.last_recv_time)

        ws_assistant = self.async_run_with_timeout(self.data_source._get_ws_assistant())
        ws_assistant._connection._last_recv_time = 1000
        self.assertEqual(1000, self.data_source.last_recv_time)

    def test_get_throttler_instance(self):
        self.assertIsInstance(self.data_source._get_throttler_instance(), AsyncThrottler)
