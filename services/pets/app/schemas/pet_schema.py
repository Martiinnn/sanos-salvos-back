"""
Sanos y Salvos — Pet Pydantic Schemas
"""

from datetime import datetime
from typing import Optional
import re

from pydantic import BaseModel, Field, field_validator, model_validator


NAME_RE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$")
COLOR_RE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ, /-]+$")


def _clean(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    text = value.strip()
    return text or None


def _letter_count(value: str) -> int:
    return len(re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]", value))


def _word_count(value: str) -> int:
    return len([word for word in value.split() if word])


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
    @field_validator("name")
    @classmethod
    def validate_name(cls, value: Optional[str]) -> Optional[str]:
        value = _clean(value)
        if value is None:
            return value
        if len(value) < 2 or len(value) > 60 or not NAME_RE.fullmatch(value) or _letter_count(value) < 2:
            raise ValueError("El nombre solo debe contener letras y espacios")
        return value

    @field_validator("species")
    @classmethod
    def validate_species(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in {"perro", "gato", "otro"}:
            raise ValueError("La especie debe ser perro, gato u otro")
        return value

    @field_validator("breed")
    @classmethod
    def validate_breed(cls, value: Optional[str]) -> Optional[str]:
        value = _clean(value)
        if value is None:
            return value
        if len(value) > 80 or not NAME_RE.fullmatch(value) or _letter_count(value) < 2:
            raise ValueError("La raza solo debe contener letras y espacios")
        return value

    @field_validator("color")
    @classmethod
    def validate_color(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 3 or len(value) > 80 or not COLOR_RE.fullmatch(value) or _letter_count(value) < 3:
            raise ValueError("El color debe describirse con palabras")
        return value

    @field_validator("size")
    @classmethod
    def validate_size(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in {"pequeño", "mediano", "grande"}:
            raise ValueError("El tamano debe ser pequeño, mediano o grande")
        return value

    @field_validator("age_estimate")
    @classmethod
    def validate_age_estimate(cls, value: Optional[str]) -> Optional[str]:
        value = _clean(value)
        if value is None:
            return value
        if len(value) > 40 or _letter_count(value) < 3:
            raise ValueError("La edad aproximada debe incluir texto")
        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: Optional[str]) -> Optional[str]:
        value = _clean(value)
        if value is None:
            return value
        if len(value) < 20 or len(value) > 500 or _word_count(value) < 3 or _letter_count(value) < 10:
            raise ValueError("La descripcion debe tener al menos 20 caracteres y 3 palabras")
        return value

    @field_validator("photo_url")
    @classmethod
    def validate_photo_url(cls, value: Optional[str]) -> Optional[str]:
        value = _clean(value)
        if value is None:
            return value
        if len(value) > 300 or not re.match(r"^https?://", value):
            raise ValueError("La URL de foto debe comenzar con http:// o https://")
        return value

    @field_validator("distinctive_features")
    @classmethod
    def validate_distinctive_features(cls, value: Optional[str]) -> Optional[str]:
        value = _clean(value)
        if value and len(value) > 300:
            raise ValueError("Las caracteristicas distintivas no pueden superar 300 caracteres")
        return value

    @model_validator(mode="after")
    def require_create_fields(self):
        if not self.name:
            raise ValueError("Completa el nombre de la mascota")
        if not self.description:
            raise ValueError("La descripcion de la mascota es obligatoria")
        return self


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
