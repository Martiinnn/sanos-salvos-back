"""
Sanos y Salvos — Geolocation Microservice
Handles geospatial data processing and map interfaces.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("geo-service")

app = FastAPI(
    title="Sanos y Salvos — Geolocalización",
    description="Microservicio de geolocalización con PostGIS para mapeo interactivo",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "healthy", "service": "geolocation-service"}
