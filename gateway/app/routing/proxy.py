"""
Sanos y Salvos — API Gateway Reverse Proxy
Routes incoming requests to the appropriate microservice through Circuit Breakers.
"""

import httpx
import logging
import time
from collections import defaultdict, deque
from fastapi import APIRouter, Request, Response, HTTPException

from app.auth.firebase import require_authenticated_user
from app.config import settings
from app.resilience.circuit_breaker import (
    pets_breaker,
    geo_breaker,
    match_breaker,
    notifications_breaker,
    ServiceUnavailableError,
)

logger = logging.getLogger("proxy")

router = APIRouter()

REPORT_CREATE_LIMIT = 5
REPORT_CREATE_WINDOW_SECONDS = 10 * 60
report_create_attempts = defaultdict(deque)

# Service routing map
SERVICE_MAP = {
    "pets": {"url": settings.pets_url, "breaker": pets_breaker},
    "geo": {"url": settings.geo_url, "breaker": geo_breaker},
    "matches": {"url": settings.match_url, "breaker": match_breaker},
    "notifications": {"url": settings.notifications_url, "breaker": notifications_breaker},
}


def get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


def enforce_report_create_rate_limit(request: Request) -> None:
    client_ip = get_client_ip(request)
    now = time.monotonic()
    attempts = report_create_attempts[client_ip]

    while attempts and now - attempts[0] > REPORT_CREATE_WINDOW_SECONDS:
        attempts.popleft()

    if len(attempts) >= REPORT_CREATE_LIMIT:
        retry_after = int(REPORT_CREATE_WINDOW_SECONDS - (now - attempts[0]))
        raise HTTPException(
            status_code=429,
            detail="Demasiados reportes creados. Intenta nuevamente en unos minutos.",
            headers={"Retry-After": str(max(retry_after, 1))},
        )

    attempts.append(now)


async def proxy_request(
    service_name: str,
    path: str,
    request: Request,
    extra_headers: dict[str, str] | None = None,
) -> Response:
    """
    Forward a request to the target microservice through its circuit breaker.
    """
    service = SERVICE_MAP.get(service_name)
    if not service:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")

    target_url = f"{service['url']}/{path}"
    breaker = service["breaker"]

    # Forward headers (pass auth token downstream)
    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("content-length", None)
    if extra_headers:
        headers.update(extra_headers)

    # Read request body
    body = await request.body()

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                params=dict(request.query_params),
            )

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )
    except httpx.ConnectError:
        logger.error(f"Cannot connect to {service_name} at {target_url}")
        raise HTTPException(
            status_code=503,
            detail=f"El servicio '{service_name}' no está disponible en este momento",
        )
    except httpx.TimeoutException:
        logger.error(f"Timeout connecting to {service_name}")
        raise HTTPException(
            status_code=504,
            detail=f"Tiempo de espera agotado para '{service_name}'",
        )
    except ServiceUnavailableError:
        raise HTTPException(
            status_code=503,
            detail=f"Circuit Breaker activado: '{service_name}' está temporalmente fuera de servicio",
        )


# =============================================================
# Proxy Routes — Forward to microservices
# =============================================================

@router.api_route("/api/pets/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_pets(path: str, request: Request):
    """Proxy requests to the Pets microservice."""
    auth_headers = None
    if request.method == "POST" and path.strip("/") == "reports":
        auth_headers = require_authenticated_user(request)
        enforce_report_create_rate_limit(request)
    elif request.method == "GET" and path.strip("/").startswith("my-reports"):
        auth_headers = require_authenticated_user(request)
    elif request.method == "DELETE" and path.startswith("reports/"):
        auth_headers = require_authenticated_user(request)
    return await proxy_request("pets", f"api/pets/{path}", request, auth_headers)


@router.api_route("/api/geo/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_geo(path: str, request: Request):
    """Proxy requests to the Geolocation microservice."""
    auth_headers = None
    if request.method == "POST" and path.strip("/") == "locations":
        auth_headers = require_authenticated_user(request)
    return await proxy_request("geo", f"api/geo/{path}", request, auth_headers)


@router.api_route("/api/matches/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_matches(path: str, request: Request):
    """Proxy requests to the Match microservice."""
    return await proxy_request("matches", f"api/matches/{path}", request)


@router.api_route("/api/notifications/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_notifications(path: str, request: Request):
    """Proxy requests to the Notifications microservice."""
    return await proxy_request("notifications", f"api/notifications/{path}", request)
