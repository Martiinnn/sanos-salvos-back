"""
Sanos y Salvos - Match Microservice
Motor de coincidencias con algoritmo de scoring ponderado.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import engine, Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("match-service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Match Microservice starting...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    logger.info("Match Microservice shutting down...")


app = FastAPI(
    title="Sanos y Salvos - Motor de Coincidencias",
    description="Microservicio que analiza reportes y detecta coincidencias entre mascotas perdidas y encontradas",
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
    return {"status": "healthy", "service": "match-service"}
