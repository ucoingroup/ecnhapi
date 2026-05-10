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
- Typed OpenAPI response schemas for easier partner integration.
- CI workflow for linting, compilation, and tests on supported Python versions.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn ecnhapi.api:app --reload
```

For local configuration, copy `.env.example` to `.env` and override only the values you need.

Open <http://127.0.0.1:8000/docs> for interactive API documentation. See [`docs/API.md`](docs/API.md) for the consolidated endpoint reference, [`docs/ROADMAP.md`](docs/ROADMAP.md) for next milestones, and [`CHANGELOG.md`](CHANGELOG.md) for the work completed in this release.

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
python -m ruff check .
```

The quote service is deterministic by design. It does not fetch live exchange rates; integrations should pass the audited treasury, oracle, or partner rate they intend to use.

## eCNH CA

`7GQnqthWKa5v2GqXYWhmgWZY5mCRrniwK3Xuinm9GKw5`
