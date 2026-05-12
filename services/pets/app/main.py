"""
Sanos y Salvos - Pets Microservice
Manages structured pet reports (lost & found).
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pets-service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Pets Microservice starting...")
    yield
    logger.info("Pets Microservice shutting down...")


app = FastAPI(
    title="Sanos y Salvos - Gestion de Mascotas",
    description="Microservicio para registro y gestion de reportes de mascotas perdidas y encontradas",
    version="1.0.0",
    lifespan=lifespan,
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
    return {"status": "healthy", "service": "pets-service"}
