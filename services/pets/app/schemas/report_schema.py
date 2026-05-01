"""
Sanos y Salvos — Report Pydantic Schemas
"""

from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field

from app.schemas.pet_schema import PetCreate, PetResponse


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


class ReportCreate(ReportBase):
    """Create a report with pet data included."""
    pet: PetCreate


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
