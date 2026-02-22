"""
Modèle de données pour les journaux

Ce module définit le modèle de données pour les journaux
dans le module comptabilité.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class JournalModel:
    """Modèle de journal comptable"""
    
    def __init__(
        self,
        id: int,
        name: str,
        code: str,
        journal_type: str = "general",
        is_default: bool = False,
        is_active: bool = True,
        default_debit_account_id: Optional[int] = None,
        default_credit_account_id: Optional[int] = None,
        description: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.code = code
        self.journal_type = journal_type
        self.is_default = is_default
        self.is_active = is_active
        self.default_debit_account_id = default_debit_account_id
        self.default_credit_account_id = default_credit_account_id
        self.description = description
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "journal_type": self.journal_type,
            "is_default": self.is_default,
            "is_active": self.is_active,
            "default_debit_account_id": self.default_debit_account_id,
            "default_credit_account_id": self.default_credit_account_id,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "JournalModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            name=data.get("name"),
            code=data.get("code"),
            journal_type=data.get("journal_type", "general"),
            is_default=data.get("is_default", False),
            is_active=data.get("is_active", True),
            default_debit_account_id=data.get("default_debit_account_id"),
            default_credit_account_id=data.get("default_credit_account_id"),
            description=data.get("description"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_active(self) -> bool:
        """Vérifie si le journal est actif"""
        return self.is_active


class JournalEntryModel:
    """Modèle d'écriture comptable"""
    
    def __init__(
        self,
        id: int,
        journal_id: int,
        entry_number: str,
        entry_date: date,
        description: str,
        reference: Optional[str] = None,
        status: str = "brouillon",
        total_debit: float = 0,
        total_credit: float = 0,
        created_by: int = None,
        validated_by: Optional[int] = None,
        validated_at: Optional[datetime] = None,
        posted_by: Optional[int] = None,
        posted_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.journal_id = journal_id
        self.entry_number = entry_number
        self.entry_date = entry_date
        self.description = description
        self.reference = reference
        self.status = status
        self.total_debit = total_debit
        self.total_credit = total_credit
        self.created_by = created_by
        self.validated_by = validated_by
        self.validated_at = validated_at
        self.posted_by = posted_by
        self.posted_at = posted_at
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "journal_id": self.journal_id,
            "entry_number": self.entry_number,
            "entry_date": self.entry_date,
            "description": self.description,
            "reference": self.reference,
            "status": self.status,
            "total_debit": self.total_debit,
            "total_credit": self.total_credit,
            "created_by": self.created_by,
            "validated_by": self.validated_by,
            "validated_at": self.validated_at,
            "posted_by": self.posted_by,
            "posted_at": self.posted_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_balanced(self) -> bool:
        """Vérifie si l'écriture est équilibrée"""
        return abs(self.total_debit - self.total_credit) < 0.01
    
    def is_posted(self) -> bool:
        """Vérifie si l'écriture est passée"""
        return self.status == "passe"
    
    def is_validated(self) -> bool:
        """Vérifie si l'écriture est validée"""
        return self.status in ["valide", "passe"]


class JournalEntryLineModel:
    """Modèle de ligne d'écriture"""
    
    def __init__(
        self,
        id: int,
        entry_id: int,
        account_id: int,
        debit: float = 0,
        credit: float = 0,
        description: Optional[str] = None,
        partner_id: Optional[int] = None,
        analytic_account_id: Optional[int] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.entry_id = entry_id
        self.account_id = account_id
        self.debit = debit
        self.credit = credit
        self.description = description
        self.partner_id = partner_id
        self.analytic_account_id = analytic_account_id
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "entry_id": self.entry_id,
            "account_id": self.account_id,
            "debit": self.debit,
            "credit": self.credit,
            "description": self.description,
            "partner_id": self.partner_id,
            "analytic_account_id": self.analytic_account_id,
            "created_at": self.created_at
        }
    
    def is_debit(self) -> bool:
        """Vérifie si c'est un débit"""
        return self.debit > 0
    
    def is_credit(self) -> bool:
        """Vérifie si c'est un crédit"""
        return self.credit > 0


class ReconciliationModel:
    """Modèle de reconciliation"""
    
    def __init__(
        self,
        id: int,
        account_id: int,
        reconciliation_date: date,
        status: str = "en_cours",
        total_debit: float = 0,
        total_credit: float = 0,
        difference: float = 0,
        notes: Optional[str] = None,
        performed_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.account_id = account_id
        self.reconciliation_date = reconciliation_date
        self.status = status
        self.total_debit = total_debit
        self.total_credit = total_credit
        self.difference = difference
        self.notes = notes
        self.performed_by = performed_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "account_id": self.account_id,
            "reconciliation_date": self.reconciliation_date,
            "status": self.status,
            "total_debit": self.total_debit,
            "total_credit": self.total_credit,
            "difference": self.difference,
            "notes": self.notes,
            "performed_by": self.performed_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_balanced(self) -> bool:
        """Vérifie si la reconciliation est équilibrée"""
        return abs(self.difference) < 0.01
