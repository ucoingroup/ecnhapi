from decimal import Decimal

import pytest

from ecnhapi.models import NetworkStatus
from ecnhapi.services import RateQuoteService, TokenMetadataService


def test_metadata_uses_expected_symbol_and_decimals() -> None:
    metadata = TokenMetadataService().get_metadata()

    assert metadata.symbol == "eCNH"
    assert metadata.decimals == 6


def test_networks_are_sorted_and_marked_planned_until_contracts_are_configured() -> None:
    networks = TokenMetadataService().list_networks()

    assert [network.code for network in networks] == sorted(network.code for network in networks)
    assert {network.status for network in networks} == {NetworkStatus.PLANNED}


def test_quote_rounds_half_up_with_string_decimals() -> None:
    quote = RateQuoteService().quote(amount="10.005", rate="1.2345", scale=4)

    assert quote.amount == Decimal("10.005")
    assert quote.rate == Decimal("1.2345")
    assert quote.converted_amount == Decimal("12.3512")


@pytest.mark.parametrize(
    ("amount", "rate", "scale", "message"),
    [
        ("0", "1", 6, "amount must be greater than zero"),
        ("1", "0", 6, "rate must be greater than zero"),
        ("NaN", "1", 6, "amount must be finite"),
        ("1", "1", 19, "scale must be between 0 and 18"),
    ],
)
def test_quote_validates_inputs(amount: str, rate: str, scale: int, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        RateQuoteService().quote(amount=amount, rate=rate, scale=scale)
