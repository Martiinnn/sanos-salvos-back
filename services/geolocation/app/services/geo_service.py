"""
Sanos y Salvos — Geolocation Service
Processes geospatial data for the mapping interface.
"""

from sqlalchemy.orm import Session
from app.repositories.location_repository import LocationRepository


class GeoService:
    """Business logic for geospatial operations."""

    def __init__(self, db: Session):
        self.repo = LocationRepository(db)

    def register_location(self, report_id: int, lat: float, lng: float, address: str = None, zone: str = None):
        return self.repo.create(report_id, lat, lng, address, zone)

    def get_all_reports(self):
        return self.repo.get_all()

    def find_nearby(self, lat: float, lng: float, radius_km: float = 5.0):
        return self.repo.find_nearby(lat, lng, radius_km)

    def get_heatmap(self):
        return self.repo.get_heatmap_data()

    def get_zone_stats(self):
        return self.repo.get_zone_stats()
