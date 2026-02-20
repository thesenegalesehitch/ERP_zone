"""
Schémas - Journal Comptable
===========================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class JournalEntryBase(BaseModel):
    """Écriture comptable"""
    account_id: int
    debit: float = 0.0
    credit: float = 0.0
    description: Optional[str] = None


class JournalEntryCreate(JournalEntryBase):
    pass


class JournalEntryResponse(JournalEntryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
