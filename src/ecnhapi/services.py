"""Business services backing the HTTP API endpoints."""

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from .models import NetworkInfo, NetworkStatus, RateQuote, TokenMetadata

DEFAULT_TOKEN_METADATA = TokenMetadata(
    symbol="eCNH",
    name="Electronic Chinese Yuan Offshore",
    decimals=6,
    issuer="UCOIN Group",
    description="API-ready metadata for eCNH ecosystem integrations.",
)

DEFAULT_NETWORKS: tuple[NetworkInfo, ...] = (
    NetworkInfo(
        code="ethereum",
        name="Ethereum",
        chain_id=1,
        contract_address=None,
        decimals=6,
        status=NetworkStatus.PLANNED,
    ),
    NetworkInfo(
        code="bsc",
        name="BNB Smart Chain",
        chain_id=56,
        contract_address=None,
        decimals=6,
        status=NetworkStatus.PLANNED,
    ),
    NetworkInfo(
        code="tron",
        name="TRON",
        chain_id=None,
        contract_address=None,
        decimals=6,
        status=NetworkStatus.PLANNED,
    ),
)


class TokenMetadataService:
    """Read-only token metadata service."""

    def __init__(self, metadata: TokenMetadata = DEFAULT_TOKEN_METADATA) -> None:
        self._metadata = metadata

    def get_metadata(self) -> TokenMetadata:
        """Return canonical eCNH token metadata."""

        return self._metadata

    def list_networks(self) -> tuple[NetworkInfo, ...]:
        """Return default network metadata sorted by network code."""

        return tuple(sorted(DEFAULT_NETWORKS, key=lambda item: item.code))


class RateQuoteService:
    """Create deterministic currency conversion quotes from caller-supplied rates."""

    def __init__(self, source_currency: str = "CNH", target_currency: str = "eCNH") -> None:
        self.source_currency = source_currency.upper()
        self.target_currency = target_currency

    def quote(
        self, amount: str | int | Decimal, rate: str | int | Decimal = "1", scale: int = 6
    ) -> RateQuote:
        """Convert a CNH amount into eCNH units using a positive supplied rate.

        The service is intentionally deterministic and does not fetch market data. Integrators can
        pass their own audited treasury or oracle rate while receiving consistent validation,
        rounding, and response shapes from the API.
        """

        if scale < 0 or scale > 18:
            raise ValueError("scale must be between 0 and 18")

        amount_decimal = _to_decimal(amount, "amount")
        rate_decimal = _to_decimal(rate, "rate")
        if amount_decimal <= 0:
            raise ValueError("amount must be greater than zero")
        if rate_decimal <= 0:
            raise ValueError("rate must be greater than zero")

        quantizer = Decimal("1").scaleb(-scale)
        converted = (amount_decimal * rate_decimal).quantize(quantizer, rounding=ROUND_HALF_UP)
        return RateQuote(
            source_currency=self.source_currency,
            target_currency=self.target_currency,
            amount=amount_decimal,
            rate=rate_decimal,
            converted_amount=converted,
            scale=scale,
        )


def _to_decimal(value: str | int | Decimal, field_name: str) -> Decimal:
    """Parse a numeric value as Decimal and reject booleans/non-finite values."""

    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be a decimal number")
    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{field_name} must be a decimal number") from exc
    if not parsed.is_finite():
        raise ValueError(f"{field_name} must be finite")
    return parsed
