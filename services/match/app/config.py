"""
Sanos y Salvos — Match Service Configuration
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

POSTGRES_USER = os.getenv("POSTGRES_USER", "sanosysalvos")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "sanosysalvos2026")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "sanosysalvos_db")

# Use asyncpg for asynchronous PostgreSQL access
DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# SQLAlchemy Async Engine
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()
