"""
Sanos y Salvos — Report Pydantic Schemas
"""

from datetime import datetime, date
from typing import Optional
import re

from pydantic import BaseModel, Field, field_validator, model_validator

from app.schemas.pet_schema import PetCreate, PetResponse


NAME_RE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$")
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def _clean(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    text = value.strip()
    return text or None


def _letter_count(value: str) -> int:
    return len(re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]", value))


class ReportBase(BaseModel):
    report_type: str = Field(..., description="'perdido' o 'encontrado'")
    latitude: float
    longitude: float
    address: Optional[str] = None
    date_event: Optional[date] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("report_type")
    @classmethod
    def validate_report_type(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in {"perdido", "encontrado"}:
            raise ValueError("El tipo de reporte debe ser perdido o encontrado")
        return value

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, value: float) -> float:
        if value < -90 or value > 90:
            raise ValueError("La latitud debe estar entre -90 y 90")
        return value

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, value: float) -> float:
        if value < -180 or value > 180:
            raise ValueError("La longitud debe estar entre -180 y 180")
        return value

    @field_validator("address")
    @classmethod
    def validate_address(cls, value: Optional[str]) -> Optional[str]:
        value = _clean(value)
        if value is None:
            return value
        if len(value) < 5 or len(value) > 160 or _letter_count(value) < 3:
            raise ValueError("Ingresa una direccion o referencia valida")
        return value

    @field_validator("date_event")
    @classmethod
    def validate_date_event(cls, value: Optional[date]) -> Optional[date]:
        if value and value > date.today():
            raise ValueError("La fecha del evento no puede ser futura")
        return value

    @field_validator("contact_name")
    @classmethod
    def validate_contact_name(cls, value: Optional[str]) -> Optional[str]:
        value = _clean(value)
        if value is None:
            return value
        if len(value) < 2 or len(value) > 80 or not NAME_RE.fullmatch(value) or _letter_count(value) < 2:
            raise ValueError("El nombre de contacto solo debe contener letras y espacios")
        return value

    @field_validator("contact_phone")
    @classmethod
    def validate_contact_phone(cls, value: Optional[str]) -> Optional[str]:
        value = _clean(value)
        if value is None:
            return value
        digits = re.sub(r"\D", "", value)
        if len(digits) < 8 or len(digits) > 12:
            raise ValueError("Ingresa un telefono valido")
        return value

    @field_validator("contact_email")
    @classmethod
    def validate_contact_email(cls, value: Optional[str]) -> Optional[str]:
        value = _clean(value)
        if value is None:
            return value
        if len(value) > 120 or not EMAIL_RE.fullmatch(value):
            raise ValueError("Ingresa un email valido")
        return value

    @field_validator("notes")
    @classmethod
    def validate_notes(cls, value: Optional[str]) -> Optional[str]:
        value = _clean(value)
        if value and len(value) > 500:
            raise ValueError("Las notas no pueden superar 500 caracteres")
        return value


class ReportCreate(ReportBase):
    """Create a report with pet data included."""
    pet: PetCreate

    @model_validator(mode="after")
    def require_create_fields(self):
        if not self.address:
            raise ValueError("Completa la direccion o referencia del lugar")
        if not self.date_event:
            raise ValueError("Debes ingresar la fecha del evento")
        if not self.contact_name:
            raise ValueError("Ingresa un nombre de contacto")
        if not self.contact_phone:
            raise ValueError("Ingresa un telefono de contacto")
        if not self.contact_email:
            raise ValueError("Ingresa un email de contacto")
        return self


class ReportUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None


class ReportResponse(ReportBase):
    id: int
    pet_id: int
    user_id: int
    status: str
    pet: PetResponse
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
