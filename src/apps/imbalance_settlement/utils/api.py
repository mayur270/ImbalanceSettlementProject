import time
from typing import Any, Dict, Optional

import requests
from requests.exceptions import ConnectionError, RequestException, Timeout

from src.apps.imbalance_settlement.configs.settlement_system_prices.configuration import (
    config,
)
from src.apps.imbalance_settlement.utils.constants import ERRORS, RETRY_STATUS_CODE
from src.apps.imbalance_settlement.utils.exceptions import APIError


class APIClient:
    """Generic API Class"""

    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30,
        retries: int = 3,
        retry_delay: int = 2,
    ) -> None:
        """Initialises the API class.
        :param base_url: Base url of website.
        :param headers: HTTP Headers required for request including metadata.
        :param timeout: Length of time in seconds before timeout error.
        :param retries: Number of retries if it fails.
        :param retry_delay: Length of time delay between retries.
        """
        self.base_url = base_url
        self.headers = headers or {}
        self.timeout = timeout
        self.retries = retries
        self.retry_delay = retry_delay

    def _request(
        self, method: str, endpoint: str, **kwargs
    ) -> Optional[requests.Response]:
        """Handles API request.
        :param method: HTTP method e.g. "GET", "POST"
        :param endpoint: URL path for the api request required in addition to base_url.
        :param kwargs: Additional keyword arguments. Used in request header.
        :return: requests.Response or Raises an error (
                Connection, Timeout, Runtime
            )
        """

        url = f"{self.base_url}/{endpoint}/"

        request_headers = {
            **self.headers,
            **kwargs.pop("headers" or {}),
        }

        for attempt in range(1, self.retries + 1):

            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=request_headers,
                    timeout=self.timeout,
                    **kwargs,
                )

                result = self._handle_response(response, attempt)
                if result == "retry":
                    continue
                return result

            except (ConnectionError, Timeout) as e:
                if attempt == self.retries:
                    msg = f"Request failed after {self.retries} attempts."
                    raise RuntimeError(msg) from e

                time.sleep(self.retry_delay)

            except RequestException as e:
                raise APIError(f"Request failed: {e}") from e

    def _handle_response(self, response: requests.Response, attempt: int) -> Any:
        """Processes and handles responses.
        :param response: Gets response object
        :param attempt: If it is 1st, 2nd or 3rd attempt etc.
        :return: Response, None or 'retry'
        """
        if response.ok:
            return response.json() if response.content else None

        if response.status_code in RETRY_STATUS_CODE and attempt < self.retries:
            time.sleep(self.retry_delay)
            return "retry"

        if response.status_code in ERRORS:
            raise ERRORS[response.status_code](
                f"{response.reason} {response.status_code}"
            )

        response.raise_for_status()

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Optional[requests.Response]:
        """HTTP Get request.
        :param endpoint: URL path for the api request required in addition to base_url.
        :param params: Query parameters for the API request.
        :param headers: HTTP Headers required for request including metadata.
        :return: requests.Response
        """
        return self._request(
            method="GET",
            endpoint=endpoint,
            params=params,
            headers=headers or {},
        )


api_client = APIClient(base_url=config.BASE_URL, headers=config.HEADERS)
