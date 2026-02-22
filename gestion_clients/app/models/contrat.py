"""
Modèle de données pour les contrats clients

Ce module définit le modèle de données pour les contrats
dans le module de gestion des clients.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class ContractModel:
    """Modèle de contrat"""
    
    def __init__(
        self,
        id: int,
        contract_number: str,
        client_id: int,
        title: str,
        description: Optional[str] = None,
        contract_type: str = "prestations",
        status: str = "brouillon",
        start_date: date,
        end_date: Optional[date] = None,
        value: float = 0,
        currency: str = "XOF",
        payment_terms: Optional[str] = None,
        renewal_date: Optional[date] = None,
        auto_renew: bool = False,
        notes: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.contract_number = contract_number
        self.client_id = client_id
        self.title = title
        self.description = description
        self.contract_type = contract_type
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
        self.value = value
        self.currency = currency
        self.payment_terms = payment_terms
        self.renewal_date = renewal_date
        self.auto_renew = auto_renew
        self.notes = notes
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "contract_number": self.contract_number,
            "client_id": self.client_id,
            "title": self.title,
            "description": self.description,
            "contract_type": self.contract_type,
            "status": self.status,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "value": self.value,
            "currency": self.currency,
            "payment_terms": self.payment_terms,
            "renewal_date": self.renewal_date,
            "auto_renew": self.auto_renew,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ContractModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            contract_number=data.get("contract_number"),
            client_id=data.get("client_id"),
            title=data.get("title"),
            description=data.get("description"),
            contract_type=data.get("contract_type", "prestations"),
            status=data.get("status", "brouillon"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            value=data.get("value", 0),
            currency=data.get("currency", "XOF"),
            payment_terms=data.get("payment_terms"),
            renewal_date=data.get("renewal_date"),
            auto_renew=data.get("auto_renew", False),
            notes=data.get("notes"),
            created_by=data.get("created_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_active(self) -> bool:
        """Vérifie si actif"""
        return self.status == "actif"
    
    def is_expired(self) -> bool:
        """Vérifie si expiré"""
        if not self.end_date:
            return False
        return date.today() > self.end_date
    
    def days_until_expiry(self) -> int:
        """Jours avant expiration"""
        if not self.end_date:
            return -1
        delta = self.end_date - date.today()
        return delta.days
    
    def is_expiring_soon(self, days: int = 30) -> bool:
        """Vérifie si expire bientôt"""
        days_left = self.days_until_expiry()
        return 0 <= days_left <= days


class ContractClauseModel:
    """Modèle de clause contractuelle"""
    
    def __init__(
        self,
        id: int,
        contract_id: int,
        title: str,
        content: str,
        clause_type: str = "generale",
        order: int = 0,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.contract_id = contract_id
        self.title = title
        self.content = content
        self.clause_type = clause_type
        self.order = order
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "contract_id": self.contract_id,
            "title": self.title,
            "content": self.content,
            "clause_type": self.clause_type,
            "order": self.order,
            "created_at": self.created_at
        }


class ContractAttachmentModel:
    """Modèle de pièce jointe de contrat"""
    
    def __init__(
        self,
        id: int,
        contract_id: int,
        file_name: str,
        file_path: str,
        file_type: Optional[str] = None,
        description: Optional[str] = None,
        uploaded_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.contract_id = contract_id
        self.file_name = file_name
        self.file_path = file_path
        self.file_type = file_type
        self.description = description
        self.uploaded_by = uploaded_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "contract_id": self.contract_id,
            "file_name": self.file_name,
            "file_path": self.file_path,
            "file_type": self.file_type,
            "description": self.description,
            "uploaded_by": self.uploaded_by,
            "created_at": self.created_at
        }
