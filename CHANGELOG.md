# Changelog

## 0.1.0 - 2026-05-10

### Added

- FastAPI application factory and versioned `/v1` routes.
- Health, token metadata, network metadata, and deterministic quote endpoints.
- Domain models, service-layer validation, decimal-safe quote rounding, and typed OpenAPI response schemas.
- Environment-driven configuration through `ECNHAPI_` variables and `.env.example`.
- Unit tests for service behavior and API endpoint behavior.
- Developer documentation, API reference, roadmap, `.gitignore`, and GitHub Actions CI workflow.

### Changed

- Added the eCNH CA to the README, API reference, and Solana network metadata.

### Notes

- Network contract addresses are placeholders until audited deployments are configured.
- Quote generation intentionally uses caller-supplied rates and does not fetch external market data.
