# eCNH API Reference

The API is versioned under `/v1` and is intentionally deterministic: it exposes metadata and validates caller-supplied quote inputs, but it does not fetch external market data.

## `GET /v1/health`

Returns deployment health and basic service metadata.

```json
{
  "status": "ok",
  "service": "eCNH API",
  "environment": "development"
}
```

## `GET /v1/token`

Returns canonical token metadata used by wallets, exchanges, payment integrations, and internal services.

```json
{
  "symbol": "eCNH",
  "name": "Electronic Chinese Yuan Offshore",
  "decimals": 6,
  "issuer": "UCOIN Group",
  "description": "API-ready metadata for eCNH ecosystem integrations."
}
```

## `GET /v1/networks`

Returns network metadata sorted by network code. Contract addresses are `null` until official deployments are configured; the current eCNH CA is exposed on the Solana network entry.

```json
[
  {
    "code": "solana",
    "name": "Solana",
    "chain_id": null,
    "contract_address": "7GQnqthWKa5v2GqXYWhmgWZY5mCRrniwK3Xuinm9GKw5",
    "decimals": 6,
    "status": "active"
  }
]
```

Network status values:

- `planned`: integration metadata is tracked, but production settlement is not live.
- `active`: production integration is available.
- `paused`: integration is temporarily unavailable.

## `GET /v1/quote`

Creates a deterministic conversion quote from caller-supplied parameters.

| Query parameter | Required | Default | Description |
| --- | --- | --- | --- |
| `amount` | Yes | - | Positive CNH amount to convert. |
| `rate` | No | `1` | Positive caller-supplied CNH-to-eCNH rate. |
| `scale` | No | `6` | Decimal places in `converted_amount`; allowed range is `0` through `18`. |

Example:

```http
GET /v1/quote?amount=10.005&rate=1.2345&scale=4
```

```json
{
  "source_currency": "CNH",
  "target_currency": "eCNH",
  "amount": "10.005",
  "rate": "1.2345",
  "converted_amount": "12.3512",
  "scale": 4
}
```

Validation failures return HTTP `422` with a short `detail` message.

## eCNH CA

`7GQnqthWKa5v2GqXYWhmgWZY5mCRrniwK3Xuinm9GKw5`
