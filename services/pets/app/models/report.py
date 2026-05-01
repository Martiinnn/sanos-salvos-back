"""
Sanos y Salvos — Report Model (SQLAlchemy)
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Float, ForeignKey, func
from sqlalchemy.orm import relationship
from app.config import Base


class Report(Base):
    """Represents a lost/found pet report."""
    __tablename__ = "reports"
    __table_args__ = {"schema": "pets_service"}

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets_service.pets.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, nullable=False)
    report_type = Column(String(20), nullable=False)  # 'perdido' or 'encontrado'
    status = Column(String(20), nullable=False, default="activo")  # activo, resuelto, expirado
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(Text, nullable=True)
    date_event = Column(Date, nullable=True)
    contact_name = Column(String(200), nullable=True)
    contact_phone = Column(String(20), nullable=True)
    contact_email = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    pet = relationship("Pet", backref="reports", lazy="joined")
