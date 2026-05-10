"""FastAPI application factory for eCNH API."""

from dataclasses import asdict
from decimal import Decimal
from typing import Annotated

import uvicorn
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse

from .config import Settings, get_settings
from .services import RateQuoteService, TokenMetadataService


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application."""

    settings = settings or get_settings()
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        docs_url="/docs" if settings.docs_enabled else None,
        redoc_url="/redoc" if settings.docs_enabled else None,
    )
    app.include_router(_build_router(), prefix=settings.api_prefix)

    @app.get("/", include_in_schema=False)
    def index() -> RedirectResponse:
        return RedirectResponse(url=f"{settings.api_prefix}/health")

    return app


def _build_router() -> APIRouter:
    router = APIRouter()

    @router.get("/health", tags=["system"])
    def health(settings: Annotated[Settings, Depends(get_settings)]) -> dict[str, str]:
        return {"status": "ok", "service": settings.app_name, "environment": settings.environment}

    @router.get("/token", tags=["token"])
    def token_metadata() -> dict[str, object]:
        return asdict(TokenMetadataService().get_metadata())

    @router.get("/networks", tags=["token"])
    def networks() -> list[dict[str, object]]:
        return [asdict(network) for network in TokenMetadataService().list_networks()]

    @router.get("/quote", tags=["quote"])
    def quote(
        amount: Annotated[str, Query(description="CNH amount to convert into eCNH")],
        rate: Annotated[
            str, Query(description="Caller-supplied CNH to eCNH conversion rate")
        ] = "1",
        scale: Annotated[int, Query(ge=0, le=18, description="Decimal places in the result")] = 6,
    ) -> dict[str, object]:
        try:
            response = RateQuoteService().quote(amount=amount, rate=rate, scale=scale)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        return _decimal_safe(asdict(response))

    return router


def _decimal_safe(payload: dict[str, object]) -> dict[str, object]:
    """Render Decimal values as strings to avoid binary floating point drift in JSON."""

    return {
        key: str(value) if isinstance(value, Decimal) else value
        for key, value in payload.items()
    }


app = create_app()


def run() -> None:
    """Run the API using uvicorn for local development."""

    uvicorn.run("ecnhapi.api:app", host="0.0.0.0", port=8000, reload=True)
