"""
Modèle de données pour les clients du support

Ce module définit le modèle de données pour les clients
dans le module de support.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class SupportClientModel:
    """Modèle de client support"""
    
    def __init__(
        self,
        id: int,
        client_id: int,
        account_manager_id: Optional[int] = None,
        tier: str = "standard",
        status: str = "actif",
        priority_support: bool = False,
        sla_level: Optional[str] = None,
        contract_start: Optional[datetime] = None,
        contract_end: Optional[datetime] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.client_id = client_id
        self.account_manager_id = account_manager_id
        self.tier = tier
        self.status = status
        self.priority_support = priority_support
        self.sla_level = sla_level
        self.contract_start = contract_start
        self.contract_end = contract_end
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "client_id": self.client_id,
            "account_manager_id": self.account_manager_id,
            "tier": self.tier,
            "status": self.status,
            "priority_support": self.priority_support,
            "sla_level": self.sla_level,
            "contract_start": self.contract_start,
            "contract_end": self.contract_end,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "SupportClientModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            client_id=data.get("client_id"),
            account_manager_id=data.get("account_manager_id"),
            tier=data.get("tier", "standard"),
            status=data.get("status", "actif"),
            priority_support=data.get("priority_support", False),
            sla_level=data.get("sla_level"),
            contract_start=data.get("contract_start"),
            contract_end=data.get("contract_end"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_active(self) -> bool:
        """Vérifie si actif"""
        return self.status == "actif"
    
    def is_premium(self) -> bool:
        """Vérifie si premium"""
        return self.tier == "premium"


class ServiceContractModel:
    """Modèle de contrat de service"""
    
    def __init__(
        self,
        id: int,
        client_id: int,
        contract_number: str,
        service_type: str = "support",
        start_date: datetime = None,
        end_date: datetime = None,
        total_value: float = 0,
        currency: str = "XOF",
        status: str = "actif",
        terms: Optional[str] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.client_id = client_id
        self.contract_number = contract_number
        self.service_type = service_type
        self.start_date = start_date
        self.end_date = end_date
        self.total_value = total_value
        self.currency = currency
        self.status = status
        self.terms = terms
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "client_id": self.client_id,
            "contract_number": self.contract_number,
            "service_type": self.service_type,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "total_value": self.total_value,
            "currency": self.currency,
            "status": self.status,
            "terms": self.terms,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_active(self) -> bool:
        """Vérifie si actif"""
        return self.status == "actif"
    
    def is_expired(self) -> bool:
        """Vérifie si expiré"""
        if not self.end_date:
            return False
        return datetime.now() > self.end_date


class SupportMetricModel:
    """Modèle de métrique de support"""
    
    def __init__(
        self,
        id: int,
        client_id: int,
        period: str,
        total_tickets: int = 0,
        resolved_tickets: int = 0,
        avg_response_time: float = 0,
        avg_resolution_time: float = 0,
        satisfaction_score: float = 0,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.client_id = client_id
        self.period = period
        self.total_tickets = total_tickets
        self.resolved_tickets = resolved_tickets
        self.avg_response_time = avg_response_time
        self.avg_resolution_time = avg_resolution_time
        self.satisfaction_score = satisfaction_score
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "client_id": self.client_id,
            "period": self.period,
            "total_tickets": self.total_tickets,
            "resolved_tickets": self.resolved_tickets,
            "avg_response_time": self.avg_response_time,
            "avg_resolution_time": self.avg_resolution_time,
            "satisfaction_score": self.satisfaction_score,
            "created_at": self.created_at
        }
    
    def resolution_rate(self) -> float:
        """Taux de résolution"""
        if self.total_tickets == 0:
            return 0
        return (self.resolved_tickets / self.total_tickets) * 100
