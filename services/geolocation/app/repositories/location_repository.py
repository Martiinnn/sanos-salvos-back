"""
Sanos y Salvos — Location Repository
Handles geospatial queries using PostGIS.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from geoalchemy2.functions import ST_DWithin, ST_MakePoint, ST_SetSRID

from app.models.location import Location


class LocationRepository:
    """Repository for geospatial location operations."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, report_id: int, lat: float, lng: float, address: str = None, zone: str = None) -> Location:
        """Create a new location entry with PostGIS coordinates."""
        location = Location(
            report_id=report_id,
            coordinates=f"SRID=4326;POINT({lng} {lat})",
            address=address,
            zone=zone,
        )
        self.db.add(location)
        self.db.commit()
        self.db.refresh(location)
        return location

    def get_all(self) -> list:
        """Get all locations with coordinates as lat/lng."""
        results = self.db.execute(
            text("""
                SELECT l.id, l.report_id, ST_Y(l.coordinates::geometry) as lat,
                       ST_X(l.coordinates::geometry) as lng, l.address, l.zone, l.created_at,
                       r.report_type, r.status, p.name as pet_name, p.species, p.breed,
                       p.color, p.size, p.photo_url
                FROM geo_service.locations l
                LEFT JOIN pets_service.reports r ON l.report_id = r.id
                LEFT JOIN pets_service.pets p ON r.pet_id = p.id
                WHERE r.status = 'activo'
                ORDER BY l.created_at DESC
            """)
        )
        return [dict(row._mapping) for row in results]

    def find_nearby(self, lat: float, lng: float, radius_km: float = 5.0) -> list:
        """Find locations within a given radius (km) using PostGIS ST_DWithin."""
        radius_meters = radius_km * 1000
        results = self.db.execute(
            text("""
                SELECT l.id, l.report_id, ST_Y(l.coordinates::geometry) as lat,
                       ST_X(l.coordinates::geometry) as lng, l.address, l.zone,
                       ST_Distance(l.coordinates::geography,
                                   ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography) as distance_m,
                       r.report_type, r.status, p.name as pet_name, p.species, p.breed,
                       p.color, p.size, p.photo_url
                FROM geo_service.locations l
                LEFT JOIN pets_service.reports r ON l.report_id = r.id
                LEFT JOIN pets_service.pets p ON r.pet_id = p.id
                WHERE r.status = 'activo'
                AND ST_DWithin(
                    l.coordinates::geography,
                    ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography,
                    :radius
                )
                ORDER BY distance_m ASC
            """),
            {"lat": lat, "lng": lng, "radius": radius_meters},
        )
        return [dict(row._mapping) for row in results]

    def get_heatmap_data(self) -> list:
        """Get coordinates for heatmap visualization."""
        results = self.db.execute(
            text("""
                SELECT ST_Y(l.coordinates::geometry) as lat,
                       ST_X(l.coordinates::geometry) as lng,
                       r.report_type
                FROM geo_service.locations l
                LEFT JOIN pets_service.reports r ON l.report_id = r.id
                WHERE r.status = 'activo'
            """)
        )
        return [dict(row._mapping) for row in results]

    def get_zone_stats(self) -> list:
        """Get zone statistics — areas with most reports."""
        results = self.db.execute(
            text("""
                SELECT l.zone, COUNT(*) as total_reports,
                       SUM(CASE WHEN r.report_type = 'perdido' THEN 1 ELSE 0 END) as perdidos,
                       SUM(CASE WHEN r.report_type = 'encontrado' THEN 1 ELSE 0 END) as encontrados
                FROM geo_service.locations l
                LEFT JOIN pets_service.reports r ON l.report_id = r.id
                WHERE l.zone IS NOT NULL
                GROUP BY l.zone
                ORDER BY total_reports DESC
            """)
        )
        return [dict(row._mapping) for row in results]
