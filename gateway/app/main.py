"""
Sanos y Salvos - API Gateway
Main entry point. Centralizes routing and resilience.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routing.proxy import router as proxy_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gateway")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("API Gateway starting...")
    logger.info(f"  -> Pets Service:          {settings.pets_url}")
    logger.info(f"  -> Geolocation Service:   {settings.geo_url}")
    logger.info(f"  -> Match Service:         {settings.match_url}")
    logger.info(f"  -> Notifications Service: {settings.notifications_url}")
    yield
    logger.info("API Gateway shutting down...")


app = FastAPI(
    title="Sanos y Salvos - API Gateway",
    description="Gateway centralizado con routing y Circuit Breaker",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "api-gateway",
        "version": "1.0.0",
    }


app.include_router(proxy_router)
