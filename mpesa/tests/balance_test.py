import pytest
import respx
from httpx import Response, HTTPStatusError
from mpesa.api.balance import Balance


@pytest.fixture
def balance_instance():
    return Balance(env="sandbox", app_key="test_key", app_secret="test_secret")


@respx.mock
def test_get_balance_success(balance_instance):
    respx.post("https://sandbox.safaricom.co.ke/mpesa/accountbalance/v1/query").mock(
        return_value=Response(
            200,
            json={
                "ResponseCode": "0",
                "ResponseDescription": "Balance retrieved successfully",
            },
        )
    )

    response = balance_instance.get_balance(
        initiator="test_initiator",
        security_credential="test_security_credential",
        party_a="600000",
        identifier_type=4,
        remarks="Test balance query",
        queue_timeout_url="https://example.com/timeout",
        result_url="https://example.com/result",
    )

    assert response["ResponseCode"] == "0"
    assert response["ResponseDescription"] == "Balance retrieved successfully"


@respx.mock
def test_get_balance_http_error(balance_instance):
    respx.post("https://sandbox.safaricom.co.ke/mpesa/accountbalance/v1/query").mock(
        return_value=Response(500, json={"error": "Internal Server Error"})
    )

    with pytest.raises(HTTPStatusError):
        balance_instance.get_balance(
            initiator="test_initiator",
            security_credential="test_security_credential",
            party_a="600000",
            identifier_type=4,
            remarks="Test balance query",
            queue_timeout_url="https://example.com/timeout",
            result_url="https://example.com/result",
        )


@respx.mock
def test_get_balance_value_error(balance_instance):
    incomplete_instance = Balance(env="sandbox")

    with pytest.raises(
        ValueError, match="App key and app secret must be provided for authentication."
    ):
        incomplete_instance.get_balance(
            initiator="test_initiator",
            security_credential="test_security_credential",
            party_a="600000",
            identifier_type=4,
            remarks="Test balance query",
            queue_timeout_url="https://example.com/timeout",
            result_url="https://example.com/result",
        )
