"""
Sanos y Salvos — Geolocation API Routes
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.config import get_db
from app.services.geo_service import GeoService

router = APIRouter(prefix="/api/geo", tags=["Geolocalización"])


class LocationCreate(BaseModel):
    report_id: int
    latitude: float
    longitude: float
    address: Optional[str] = None
    zone: Optional[str] = None


@router.post("/locations", status_code=201)
def create_location(data: LocationCreate, db: Session = Depends(get_db)):
    """Register a new geolocation for a report."""
    service = GeoService(db)
    loc = service.register_location(
        report_id=data.report_id,
        lat=data.latitude,
        lng=data.longitude,
        address=data.address,
        zone=data.zone,
    )
    return {"id": loc.id, "message": "Ubicación registrada"}


@router.get("/reports")
def get_all_reports(db: Session = Depends(get_db)):
    """Get all active reports with geolocation data for the map."""
    service = GeoService(db)
    return service.get_all_reports()


@router.get("/nearby")
def find_nearby(
    lat: float = Query(..., description="Latitud"),
    lng: float = Query(..., description="Longitud"),
    radius: float = Query(5.0, description="Radio en km"),
    db: Session = Depends(get_db),
):
    """Find reports near a given location."""
    service = GeoService(db)
    return service.find_nearby(lat, lng, radius)


@router.get("/heatmap")
def get_heatmap(db: Session = Depends(get_db)):
    """Get coordinate data for heatmap visualization."""
    service = GeoService(db)
    return service.get_heatmap()


@router.get("/zones")
def get_zones(db: Session = Depends(get_db)):
    """Get zone statistics — areas with highest incident rates."""
    service = GeoService(db)
    return service.get_zone_stats()
