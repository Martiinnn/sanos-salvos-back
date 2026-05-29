import base64
import hashlib
import json
from typing import Any

from fastapi import HTTPException, Request

from app.config import settings


def _extract_bearer_token(request: Request) -> str:
    auth_header = request.headers.get("authorization", "")
    scheme, _, token = auth_header.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        raise HTTPException(
            status_code=401,
            detail="Debes iniciar sesion o registrarte para realizar esta accion.",
        )
    return token.strip()


def _decode_unverified_payload(token: str) -> dict[str, Any]:
    try:
        payload_part = token.split(".")[1]
        padded = payload_part + "=" * (-len(payload_part) % 4)
        return json.loads(base64.urlsafe_b64decode(padded.encode("utf-8")))
    except (IndexError, ValueError, json.JSONDecodeError):
        raise HTTPException(status_code=401, detail="Token de autenticacion invalido.")


def _stable_numeric_user_id(firebase_uid: str) -> int:
    digest = hashlib.sha256(firebase_uid.encode("utf-8")).hexdigest()
    return int(digest[:12], 16) % 2_147_483_647 or 1


def _verify_with_google_auth(token: str) -> dict[str, Any] | None:
    if not settings.FIREBASE_PROJECT_ID:
        return None

    try:
        from google.auth.transport import requests as google_requests
        from google.oauth2 import id_token
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail="El gateway no tiene instalada la dependencia google-auth para validar Firebase.",
        )

    try:
        claims = id_token.verify_firebase_token(
            token,
            google_requests.Request(),
            audience=settings.FIREBASE_PROJECT_ID,
        )
    except ValueError:
        raise HTTPException(status_code=401, detail="Sesion invalida o expirada.")

    return claims


def require_authenticated_user(request: Request) -> dict[str, str]:
    token = _extract_bearer_token(request)

    if settings.REQUIRE_FIREBASE_AUTH:
        claims = _verify_with_google_auth(token) or _decode_unverified_payload(token)
    else:
        claims = _decode_unverified_payload(token)

    firebase_uid = claims.get("user_id") or claims.get("sub")
    if not firebase_uid:
        raise HTTPException(status_code=401, detail="Token de autenticacion invalido.")

    return {
        "X-User-Id": str(_stable_numeric_user_id(firebase_uid)),
        "X-User-Firebase-Uid": str(firebase_uid),
        "X-User-Email": str(claims.get("email") or ""),
    }
