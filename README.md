# ecnhapi

A lightweight FastAPI foundation for eCNH ecosystem integrations. The service exposes deterministic token metadata, supported-network metadata, health checks, and caller-supplied quote calculations without depending on unaudited market-data side effects.

## Features

- Versioned HTTP API under `/v1`.
- Health endpoint for deployment probes.
- Canonical eCNH token metadata endpoint.
- Network metadata endpoint with explicit lifecycle states.
- Decimal-safe quote endpoint using caller-supplied conversion rates.
- Environment-driven configuration with the `ECNHAPI_` prefix.
- Unit-tested business services with deterministic rounding and validation.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn ecnhapi.api:app --reload
```

Open <http://127.0.0.1:8000/docs> for interactive API documentation.

## API overview

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/v1/health` | Deployment and monitoring health check. |
| `GET` | `/v1/token` | eCNH token metadata. |
| `GET` | `/v1/networks` | Supported network metadata and integration status. |
| `GET` | `/v1/quote?amount=100&rate=1` | Decimal-safe quote generated from caller-supplied rate. |

## Configuration

Configuration is loaded from environment variables and an optional `.env` file.

| Variable | Default | Description |
| --- | --- | --- |
| `ECNHAPI_APP_NAME` | `eCNH API` | Display name returned by health checks and docs. |
| `ECNHAPI_ENVIRONMENT` | `development` | Deployment environment label. |
| `ECNHAPI_API_PREFIX` | `/v1` | Prefix for versioned API routes. |
| `ECNHAPI_DOCS_ENABLED` | `true` | Enables or disables Swagger/ReDoc routes. |

## Development

```bash
pytest
python -m compileall src tests
```

The quote service is deterministic by design. It does not fetch live exchange rates; integrations should pass the audited treasury, oracle, or partner rate they intend to use.
