"""
Sanos y Salvos — Location Model (PostGIS)
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, func
from geoalchemy2 import Geometry
from app.config import Base


class Location(Base):
    """Geospatial location for a pet report — uses PostGIS POINT geometry."""
    __tablename__ = "locations"
    __table_args__ = {"schema": "geo_service"}

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, nullable=False, index=True)
    coordinates = Column(Geometry("POINT", srid=4326), nullable=False)
    address = Column(Text, nullable=True)
    zone = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
