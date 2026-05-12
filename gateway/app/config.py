"""
Sanos y Salvos — API Gateway Configuration
"""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "dev-secret-key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # Database (for auth)
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "sanosysalvos")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "sanosysalvos2026")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "sanosysalvos_db")

    # Service URLs
    PETS_SERVICE_URL: str | None = os.getenv("PETS_SERVICE_URL")
    GEO_SERVICE_URL: str | None = os.getenv("GEO_SERVICE_URL")
    MATCH_SERVICE_URL: str | None = os.getenv("MATCH_SERVICE_URL")
    NOTIFICATIONS_SERVICE_URL: str | None = os.getenv("NOTIFICATIONS_SERVICE_URL")

    PETS_SERVICE_HOST: str = os.getenv("PETS_SERVICE_HOST", "localhost")
    PETS_SERVICE_PORT: str = os.getenv("PETS_SERVICE_PORT", "8001")
    GEO_SERVICE_HOST: str = os.getenv("GEO_SERVICE_HOST", "localhost")
    GEO_SERVICE_PORT: str = os.getenv("GEO_SERVICE_PORT", "8002")
    MATCH_SERVICE_HOST: str = os.getenv("MATCH_SERVICE_HOST", "localhost")
    MATCH_SERVICE_PORT: str = os.getenv("MATCH_SERVICE_PORT", "8003")
    NOTIFICATIONS_SERVICE_HOST: str = os.getenv("NOTIFICATIONS_SERVICE_HOST", "localhost")
    NOTIFICATIONS_SERVICE_PORT: str = os.getenv("NOTIFICATIONS_SERVICE_PORT", "8004")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @staticmethod
    def _build_service_url(explicit_url: str | None, host: str, port: str) -> str:
        if explicit_url:
            return explicit_url.rstrip("/")

        normalized_host = host.strip()
        if normalized_host.startswith("http://") or normalized_host.startswith("https://"):
            return normalized_host.rstrip("/")

        # Render public domains must use HTTPS.
        use_https = normalized_host.endswith(".onrender.com") or port == "443"
        scheme = "https" if use_https else "http"

        # Avoid malformed URLs like http://service.onrender.com:443
        if (scheme == "https" and port == "443") or (scheme == "http" and port == "80"):
            return f"{scheme}://{normalized_host}"

        return f"{scheme}://{normalized_host}:{port}"

    @property
    def pets_url(self) -> str:
        return self._build_service_url(
            self.PETS_SERVICE_URL,
            self.PETS_SERVICE_HOST,
            self.PETS_SERVICE_PORT,
        )

    @property
    def geo_url(self) -> str:
        return self._build_service_url(
            self.GEO_SERVICE_URL,
            self.GEO_SERVICE_HOST,
            self.GEO_SERVICE_PORT,
        )

    @property
    def match_url(self) -> str:
        return self._build_service_url(
            self.MATCH_SERVICE_URL,
            self.MATCH_SERVICE_HOST,
            self.MATCH_SERVICE_PORT,
        )

    @property
    def notifications_url(self) -> str:
        return self._build_service_url(
            self.NOTIFICATIONS_SERVICE_URL,
            self.NOTIFICATIONS_SERVICE_HOST,
            self.NOTIFICATIONS_SERVICE_PORT,
        )

    class Config:
        env_file = ".env"


settings = Settings()
