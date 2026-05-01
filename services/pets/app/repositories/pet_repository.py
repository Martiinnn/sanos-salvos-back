"""
Sanos y Salvos — Pet Repository Pattern
Abstracts database access for Pet and Report entities.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.pet import Pet
from app.models.report import Report


class PetRepository:
    """Repository for Pet CRUD operations — abstracts persistence layer."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, pet: Pet) -> Pet:
        self.db.add(pet)
        self.db.commit()
        self.db.refresh(pet)
        return pet

    def get_by_id(self, pet_id: int) -> Optional[Pet]:
        return self.db.query(Pet).filter(Pet.id == pet_id).first()

    def get_all(self, skip: int = 0, limit: int = 50) -> List[Pet]:
        return self.db.query(Pet).offset(skip).limit(limit).all()

    def update(self, pet_id: int, data: dict) -> Optional[Pet]:
        pet = self.get_by_id(pet_id)
        if not pet:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(pet, key, value)
        self.db.commit()
        self.db.refresh(pet)
        return pet

    def delete(self, pet_id: int) -> bool:
        pet = self.get_by_id(pet_id)
        if not pet:
            return False
        self.db.delete(pet)
        self.db.commit()
        return True


class ReportRepository:
    """Repository for Report CRUD operations."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, report: Report) -> Report:
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def get_by_id(self, report_id: int) -> Optional[Report]:
        return self.db.query(Report).filter(Report.id == report_id).first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 50,
        report_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Report]:
        query = self.db.query(Report)
        if report_type:
            query = query.filter(Report.report_type == report_type)
        if status:
            query = query.filter(Report.status == status)
        return query.order_by(Report.created_at.desc()).offset(skip).limit(limit).all()

    def get_by_user(self, user_id: int) -> List[Report]:
        return (
            self.db.query(Report)
            .filter(Report.user_id == user_id)
            .order_by(Report.created_at.desc())
            .all()
        )

    def update_status(self, report_id: int, status: str) -> Optional[Report]:
        report = self.get_by_id(report_id)
        if not report:
            return None
        report.status = status
        self.db.commit()
        self.db.refresh(report)
        return report

    def count_by_type(self) -> dict:
        """Get report counts by type."""
        from sqlalchemy import func
        results = (
            self.db.query(Report.report_type, func.count(Report.id))
            .filter(Report.status == "activo")
            .group_by(Report.report_type)
            .all()
        )
        return {r[0]: r[1] for r in results}
