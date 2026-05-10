"""Pydantic schemas used by the HTTP API layer."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class NetworkStatusSchema(StrEnum):
    """Public lifecycle states for network integrations."""

    ACTIVE = "active"
    PAUSED = "paused"
    PLANNED = "planned"


class HealthResponse(BaseModel):
    """Service health response."""

    status: str = Field(examples=["ok"])
    service: str = Field(examples=["eCNH API"])
    environment: str = Field(examples=["development"])


class TokenMetadataResponse(BaseModel):
    """Canonical eCNH token metadata response."""

    symbol: str = Field(examples=["eCNH"])
    name: str = Field(examples=["Electronic Chinese Yuan Offshore"])
    decimals: int = Field(ge=0, le=18, examples=[6])
    issuer: str = Field(examples=["UCOIN Group"])
    description: str


class NetworkResponse(BaseModel):
    """Network metadata exposed to API consumers."""

    code: str = Field(examples=["ethereum"])
    name: str = Field(examples=["Ethereum"])
    chain_id: int | None = Field(default=None, examples=[1])
    contract_address: str | None = Field(default=None)
    decimals: int = Field(ge=0, le=18, examples=[6])
    status: NetworkStatusSchema


class QuoteResponse(BaseModel):
    """Decimal-safe quote response rendered as strings for numeric fields."""

    source_currency: str = Field(examples=["CNH"])
    target_currency: str = Field(examples=["eCNH"])
    amount: str = Field(examples=["100"])
    rate: str = Field(examples=["1"])
    converted_amount: str = Field(examples=["100.000000"])
    scale: int = Field(ge=0, le=18, examples=[6])


class ErrorResponse(BaseModel):
    """Simple validation error response."""

    detail: str = Field(examples=["amount must be greater than zero"])

    model_config = ConfigDict(json_schema_extra={"description": "Validation failure details."})
