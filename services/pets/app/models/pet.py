"""
Sanos y Salvos — Pet Model (SQLAlchemy)
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.config import Base


class Pet(Base):
    """Represents a pet in the system."""
    __tablename__ = "pets"
    __table_args__ = {"schema": "pets_service"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    species = Column(String(50), nullable=False, default="perro")
    breed = Column(String(100), nullable=True)
    color = Column(String(100), nullable=False)
    size = Column(String(20), nullable=False)  # pequeño, mediano, grande
    age_estimate = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    photo_url = Column(Text, nullable=True)
    distinctive_features = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
