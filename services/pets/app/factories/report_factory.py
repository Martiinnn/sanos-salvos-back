"""
Sanos y Salvos — Report Factory Method Pattern
Creates specialized report instances based on report type.
"""

from datetime import date
from typing import Optional

from app.models.pet import Pet
from app.models.report import Report


class ReportFactory:
    """
    Factory Method Pattern — creates report instances based on type.
    Encapsulates the creation logic and applies type-specific defaults.
    """

    @staticmethod
    def create_report(
        report_type: str,
        pet: Pet,
        user_id: int,
        latitude: float,
        longitude: float,
        address: Optional[str] = None,
        date_event: Optional[date] = None,
        contact_name: Optional[str] = None,
        contact_phone: Optional[str] = None,
        contact_email: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Report:
        """
        Factory method — creates the appropriate report type.
        """
        if report_type not in ("perdido", "encontrado"):
            raise ValueError(f"Tipo de reporte inválido: {report_type}. Use 'perdido' o 'encontrado'.")

        report = Report(
            pet_id=pet.id,
            user_id=user_id,
            report_type=report_type,
            status="activo",
            latitude=latitude,
            longitude=longitude,
            address=address,
            date_event=date_event or date.today(),
            contact_name=contact_name,
            contact_phone=contact_phone,
            contact_email=contact_email,
            notes=notes,
        )

        # Type-specific defaults
        if report_type == "perdido":
            report.notes = report.notes or "Mascota perdida — se busca activamente"
        elif report_type == "encontrado":
            report.notes = report.notes or "Mascota encontrada — esperando identificación de dueño"

        return report
