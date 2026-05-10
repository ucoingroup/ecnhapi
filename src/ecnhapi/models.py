"""Domain models for token metadata, networks, and quote responses."""

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


class NetworkStatus(StrEnum):
    """Supported lifecycle states for an eCNH network integration."""

    ACTIVE = "active"
    PAUSED = "paused"
    PLANNED = "planned"


@dataclass(frozen=True, slots=True)
class NetworkInfo:
    """Metadata describing an available eCNH settlement network."""

    code: str
    name: str
    chain_id: int | None
    contract_address: str | None
    decimals: int
    status: NetworkStatus


@dataclass(frozen=True, slots=True)
class TokenMetadata:
    """Canonical eCNH token metadata exposed by the API."""

    symbol: str
    name: str
    decimals: int
    issuer: str
    description: str


@dataclass(frozen=True, slots=True)
class RateQuote:
    """A deterministic quote generated from a supplied CNH amount and rate."""

    source_currency: str
    target_currency: str
    amount: Decimal
    rate: Decimal
    converted_amount: Decimal
    scale: int
