"""
Sanos y Salvos — Pet Pydantic Schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PetBase(BaseModel):
    name: Optional[str] = None
    species: str = Field(default="perro", description="Especie: perro, gato, etc.")
    breed: Optional[str] = None
    color: str = Field(..., description="Color principal del animal")
    size: str = Field(..., description="Tamaño: pequeño, mediano, grande")
    age_estimate: Optional[str] = None
    description: Optional[str] = None
    photo_url: Optional[str] = None
    distinctive_features: Optional[str] = None


class PetCreate(PetBase):
    pass


class PetUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    color: Optional[str] = None
    size: Optional[str] = None
    age_estimate: Optional[str] = None
    description: Optional[str] = None
    photo_url: Optional[str] = None
    distinctive_features: Optional[str] = None


class PetResponse(PetBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
