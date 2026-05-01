"""
Sanos y Salvos — Match Model (MongoDB document schema)
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class MatchResult(BaseModel):
    """Represents a match between a lost and found pet report."""
    report_lost_id: int
    report_found_id: int
    score: float = Field(..., ge=0, le=100, description="Match confidence score (0-100)")
    score_breakdown: dict = Field(default_factory=dict, description="Detailed scoring by criteria")
    status: str = Field(default="pendiente", description="pendiente, confirmado, descartado")
    pet_lost_name: Optional[str] = None
    pet_found_name: Optional[str] = None
    user_lost_id: int = 0
    user_found_id: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    notified: bool = False
