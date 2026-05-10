import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi.testclient import TestClient

from ecnhapi.api import create_app
from ecnhapi.config import Settings


def _client() -> TestClient:
    return TestClient(create_app(Settings(app_name="Test eCNH API", environment="test")))


def test_health_endpoint_returns_configured_service_metadata() -> None:
    response = _client().get("/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "Test eCNH API",
        "environment": "test",
    }


def test_token_endpoint_returns_canonical_metadata() -> None:
    response = _client().get("/v1/token")

    assert response.status_code == 200
    payload = response.json()
    assert payload["symbol"] == "eCNH"
    assert payload["decimals"] == 6
    assert payload["issuer"] == "UCOIN Group"


def test_networks_endpoint_returns_sorted_networks_with_solana_ca() -> None:
    response = _client().get("/v1/networks")

    assert response.status_code == 200
    payload = response.json()
    assert [network["code"] for network in payload] == ["bsc", "ethereum", "solana", "tron"]
    solana = next(network for network in payload if network["code"] == "solana")
    assert solana["contract_address"] == "7GQnqthWKa5v2GqXYWhmgWZY5mCRrniwK3Xuinm9GKw5"
    assert solana["status"] == "active"


def test_quote_endpoint_returns_decimal_strings() -> None:
    response = _client().get("/v1/quote", params={"amount": "10.005", "rate": "1.2345", "scale": 4})

    assert response.status_code == 200
    assert response.json()["converted_amount"] == "12.3512"


def test_quote_endpoint_returns_validation_details() -> None:
    response = _client().get("/v1/quote", params={"amount": "0"})

    assert response.status_code == 422
    assert response.json() == {"detail": "amount must be greater than zero"}
