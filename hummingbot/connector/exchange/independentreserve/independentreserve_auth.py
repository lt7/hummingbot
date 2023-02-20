import hashlib
import hmac
import json
from collections import OrderedDict

from typing import (
    Any,
    Dict
)
# from urllib.parse import urlencode

from hummingbot.connector.time_synchronizer import TimeSynchronizer
from hummingbot.core.web_assistant.auth import AuthBase
from hummingbot.core.web_assistant.connections.data_types import RESTRequest, RESTMethod, WSRequest


class IndependentreserveAuth(AuthBase):

    def __init__(self, api_key: str, secret_key: str, time_provider: TimeSynchronizer):
        self.api_key = api_key
        self.secret_key = secret_key
        self.time_provider = time_provider

    async def rest_authenticate(self, request: RESTRequest) -> RESTRequest:
        """
        Adds the server time and the signature to the request, required for authenticated interactions. It also adds
        the required parameter in the request header.
        :param request: the request to be configured for authenticated interaction
        """
        if request.method == RESTMethod.POST:
            # request.data = self.add_auth_to_data(url=request.url, params=request.data)
            request.data = self.add_auth_to_data(url=request.url, params=request.params)
        else:
            request.data = self.add_auth_to_data(url=request.url, params=request.params)

        headers = {}
        if request.headers is not None:
            headers.update(request.headers)
        headers.update(self.header_for_authentication())
        request.headers = headers

        return request

    async def ws_authenticate(self, request: WSRequest) -> WSRequest:
        """
        This method is intended to configure a websocket request to be authenticated. Independentreserve does not use this
        functionality
        """
        return request  # pass-through

    def add_auth_to_data(self, url: str, params: Dict[str, Any]):
        """
        Add authentication as per https://www.independentreserve.com/au/products/api#authentication
        :param url: private URL we are attempting to authenticate with
        :param params:
        :return:
        """
        timestamp = int(self.time_provider.time() * 1e3)
        request_params = [url, "apiKey=" + self.api_key, "nonce=" + str(timestamp)]
        if params:
            for key in params:
                request_params.append(f"{key}={params[key]}")

        message = ','.join(request_params)
        signature = self._generate_signature(message)

        data = OrderedDict([
            ('apiKey', self.api_key),
            ('nonce', str(timestamp)),
            ('signature', str(signature)),
        ])
        # Append params to data OrderDict
        if params:
            for key in params:
                data[key] = params[key]

        return json.dumps(data, sort_keys=False)

    def header_for_authentication(self) -> Dict[str, str]:
        return {'Content-Type': 'application/json'}

    def _generate_signature(self, params: list) -> str:

        # encoded_params_str = urlencode(params)
        digest = hmac.new(self.secret_key.encode("utf8"),
                          msg=params.encode("utf8"),
                          digestmod=hashlib.sha256).hexdigest().upper()
        return digest
