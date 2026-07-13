from unittest.mock import MagicMock, patch

import pytest
import requests

from src.apps.imbalance_settlement.utils.exceptions import APIError

MODULE_PATH = "src.apps.imbalance_settlement.utils.api.requests.request"
RETRY_PATH = "src.apps.imbalance_settlement.utils.api.time.sleep"
settlement_date = "2026-01-01"


def make_response(status_code=200, json_data=None, content=b"{}", reason="OK"):
    """Creating a response with MagicMock.
    :param status_code: expected response status code
    :param json_data: json payload
    :param content: HTTP response
    :param reason: Status code reason
    :return:
    """
    resp = MagicMock(spec=requests.Response)
    resp.status_code = status_code
    resp.ok = 200 <= status_code < 400
    resp.reason = reason
    resp.content = content
    resp.json.return_value = {} if json_data is None else json_data  # Mocked fake data
    resp.raise_for_status.side_effect = requests.HTTPError(f"{status_code} error")
    return resp


class TestGetSuccess:

    @patch(f"{MODULE_PATH}")
    def test_api_client_get_success(
        self, mock_request, mock_api_client, mock_valid_data
    ):
        """"""
        mock_request.return_value = make_response(
            status_code=200, json_data=mock_valid_data
        )

        result = mock_api_client.get(endpoint=f"settlement/{settlement_date}")

        assert result == mock_valid_data

    @patch(f"{MODULE_PATH}")
    def test_api_client_get_correct_url_and_method_success(
        self, mock_request, mock_api_client
    ):
        mock_request.return_value = make_response(status_code=200, json_data={})

        mock_api_client.get(endpoint=f"settlement/{settlement_date}")

        _, kwargs = mock_request.call_args
        assert (
            kwargs["url"] == f"{mock_api_client.base_url}/settlement/{settlement_date}/"
        )
        assert kwargs["method"] == "GET"
        assert kwargs["timeout"] == mock_api_client.timeout

    @patch(f"{MODULE_PATH}")
    def test_api_client_get_when_body_empty_success(
        self, mock_request, mock_api_client
    ):
        mock_request.return_value = make_response(status_code=200, content=b"")

        result = mock_api_client.get(endpoint=f"settlement/{settlement_date}")

        assert result is None

    @patch(f"{MODULE_PATH}")
    def test_api_client_get_with_query_params_success(
        self, mock_request, mock_api_client
    ):
        mock_request.return_value = make_response(status_code=200, json_data={})

        mock_api_client.get(
            endpoint=f"settlement/{settlement_date}", params={"format": "json"}
        )

        _, kwargs = mock_request.call_args
        assert kwargs["params"] == {"format": "json"}


class TestRetryBehaviour:

    @patch(f"{RETRY_PATH}", return_value=None)
    @patch(f"{MODULE_PATH}")
    def test_api_client_request_retry_success(
        self, mock_request, mock_sleep, mock_api_client, mock_valid_data
    ):
        failed = make_response(status_code=500, content=b"")  # service error
        failed.ok = False  # Unsuccessful
        succeeded = make_response(status_code=200, json_data=mock_valid_data)
        mock_request.side_effect = [
            failed,
            succeeded,
        ]  # First calls failed, then succeeded

        result = mock_api_client.get(endpoint=f"settlement/{settlement_date}")

        assert result == mock_valid_data
        assert mock_request.call_count == 2
        mock_sleep.assert_called_once_with(mock_api_client.retry_delay)

    @patch(f"{RETRY_PATH}", return_value=None)
    @patch(f"{MODULE_PATH}")
    def test_api_client_request_connection_error_retry_then_runtime_error(
        self,
        mock_request,
        mock_sleep,
        mock_api_client,
    ):
        mock_request.side_effect = requests.exceptions.ConnectionError(
            "Connection Error"
        )

        with pytest.raises(RuntimeError, match="Request failed after 3 attempts"):
            mock_api_client.get(endpoint=f"settlement/{settlement_date}")

        assert mock_request.call_count == mock_api_client.retries

    @patch(f"{RETRY_PATH}", return_value=None)
    @patch(f"{MODULE_PATH}")
    def test_api_client_request_connection_error_then_success(
        self, mock_request, mock_sleep, mock_api_client, mock_valid_data
    ):
        mock_request.side_effect = [
            requests.exceptions.ConnectionError("Connection Error"),
            make_response(status_code=200, json_data=mock_valid_data),
        ]

        result = mock_api_client.get(endpoint=f"settlement/{settlement_date}")

        assert result == mock_valid_data
        assert mock_request.call_count == 2

    @patch(f"{RETRY_PATH}", return_value=None)
    @patch(f"{MODULE_PATH}")
    def test_api_client_request_timeout_error_retry_then_runtime_error(
        self, mock_request, mock_sleep, mock_api_client
    ):
        mock_request.side_effect = requests.exceptions.Timeout("Timeout Error")

        with pytest.raises(RuntimeError, match="Request failed after 3 attempts"):
            mock_api_client.get(endpoint=f"settlement/{settlement_date}")

        assert mock_request.call_count == mock_api_client.retries


class TestErrorHandling:
    @patch(f"{MODULE_PATH}")
    def test_api_client_request_raises_api_error_bad_request(
        self, mock_request, mock_api_client
    ):
        resp = make_response(status_code=400, content=b"")
        resp.ok = False
        resp.reason = "Bad Request"
        mock_request.return_value = resp

        settlement_date = "2026-07-98"
        with pytest.raises(APIError, match="Bad Request 400"):
            mock_api_client.get(endpoint=f"settlement/{settlement_date}")

    @patch(f"{MODULE_PATH}")
    def test_api_client_incorrect_base_url_not_found(
        self, mock_request, mock_api_client
    ):
        resp = make_response(status_code=404, content=b"")
        resp.ok = False
        resp.reason = "Not Found"
        mock_request.return_value = resp

        mock_api_client.base_url = "https://api.example.comm"  # Incorrect base_url
        with pytest.raises(APIError, match="Not Found 404"):
            mock_api_client.get(endpoint=f"settlement/{settlement_date}")
