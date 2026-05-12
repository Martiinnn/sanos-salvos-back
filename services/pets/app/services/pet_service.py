"""
Sanos y Salvos — Pet Service Layer
Business logic for pet management and reporting.
"""

import logging
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.pet import Pet
from app.models.report import Report
from app.repositories.pet_repository import PetRepository, ReportRepository
from app.factories.report_factory import ReportFactory
from app.schemas.report_schema import ReportCreate

logger = logging.getLogger("pet_service")


class PetService:
    """Orchestrates pet and report business logic."""

    def __init__(self, db: Session):
        self.pet_repo = PetRepository(db)
        self.report_repo = ReportRepository(db)
        self.db = db

    async def create_report(self, data: ReportCreate, user_id: int) -> Report:
        """
        Create a new pet report (lost or found).
        1. Create the Pet entity
        2. Use ReportFactory to create the Report
        """
        # 1. Create pet
        pet = Pet(
            name=data.pet.name,
            species=data.pet.species,
            breed=data.pet.breed,
            color=data.pet.color,
            size=data.pet.size,
            age_estimate=data.pet.age_estimate,
            description=data.pet.description,
            photo_url=data.pet.photo_url,
            distinctive_features=data.pet.distinctive_features,
        )
        pet = self.pet_repo.create(pet)

        # 2. Use Factory Method to create report
        report = ReportFactory.create_report(
            report_type=data.report_type,
            pet=pet,
            user_id=user_id,
            latitude=data.latitude,
            longitude=data.longitude,
            address=data.address,
            date_event=data.date_event,
            contact_name=data.contact_name,
            contact_phone=data.contact_phone,
            contact_email=data.contact_email,
            notes=data.notes,
        )
        report = self.report_repo.create(report)

        return report

    def get_report(self, report_id: int) -> Optional[Report]:
        return self.report_repo.get_by_id(report_id)

    def get_reports(
        self,
        skip: int = 0,
        limit: int = 50,
        report_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Report]:
        return self.report_repo.get_all(skip, limit, report_type, status)

    def get_user_reports(self, user_id: int) -> List[Report]:
        return self.report_repo.get_by_user(user_id)

    def update_report_status(self, report_id: int, status: str) -> Optional[Report]:
        return self.report_repo.update_status(report_id, status)

    def get_stats(self) -> dict:
        counts = self.report_repo.count_by_type()
        return {
            "total_perdidos": counts.get("perdido", 0),
            "total_encontrados": counts.get("encontrado", 0),
            "total_activos": sum(counts.values()),
        }
