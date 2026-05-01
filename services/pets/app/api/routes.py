"""
Sanos y Salvos — Pets API Routes
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session

from app.config import get_db
from app.schemas.pet_schema import PetResponse
from app.schemas.report_schema import ReportCreate, ReportResponse, ReportUpdate
from app.services.pet_service import PetService

router = APIRouter(prefix="/api/pets", tags=["Mascotas"])


def _get_user_id(request: Request) -> int:
    """Extract user_id from JWT payload passed by the gateway."""
    auth = request.headers.get("Authorization", "")
    # In a real scenario the gateway validates the token; here we trust internal network
    # For demo purposes, accept a user_id header or default to 1
    user_id = request.headers.get("X-User-Id", "1")
    return int(user_id)


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Get report statistics."""
    service = PetService(db)
    return service.get_stats()


@router.post("/reports", response_model=ReportResponse, status_code=201)
async def create_report(
    data: ReportCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    """Create a new pet report (lost or found)."""
    user_id = _get_user_id(request)
    service = PetService(db)
    try:
        report = await service.create_report(data, user_id)
        return report
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/reports", response_model=list[ReportResponse])
def list_reports(
    report_type: Optional[str] = Query(None, description="Filtrar por tipo: perdido/encontrado"),
    status: Optional[str] = Query(None, description="Filtrar por estado: activo/resuelto"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all pet reports with optional filters."""
    service = PetService(db)
    return service.get_reports(skip, limit, report_type, status)


@router.get("/reports/{report_id}", response_model=ReportResponse)
def get_report(report_id: int, db: Session = Depends(get_db)):
    """Get a specific report by ID."""
    service = PetService(db)
    report = service.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return report


@router.get("/my-reports", response_model=list[ReportResponse])
def get_my_reports(request: Request, db: Session = Depends(get_db)):
    """Get all reports by the current user."""
    user_id = _get_user_id(request)
    service = PetService(db)
    return service.get_user_reports(user_id)


@router.patch("/reports/{report_id}/status")
def update_report_status(
    report_id: int,
    data: ReportUpdate,
    db: Session = Depends(get_db),
):
    """Update report status (e.g. mark as resolved)."""
    service = PetService(db)
    report = service.update_report_status(report_id, data.status)
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return {"message": "Estado actualizado", "status": report.status}
