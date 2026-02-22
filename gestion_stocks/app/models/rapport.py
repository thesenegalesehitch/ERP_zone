"""
Modèle de données pour les rapports de stock

Ce module définit le modèle de données pour les rapports
dans le module de gestion des stocks.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class StockReportModel:
    """Modèle de rapport de stock"""
    
    def __init__(
        self,
        id: int,
        report_type: str,
        warehouse_id: Optional[int] = None,
        report_date: date = None,
        status: str = "genere",
        generated_by: int = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.report_type = report_type
        self.warehouse_id = warehouse_id
        self.report_date = report_date or date.today()
        self.status = status
        self.generated_by = generated_by
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "report_type": self.report_type,
            "warehouse_id": self.warehouse_id,
            "report_date": self.report_date,
            "status": self.status,
            "generated_by": self.generated_by,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "StockReportModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            report_type=data.get("report_type"),
            warehouse_id=data.get("warehouse_id"),
            report_date=data.get("report_date"),
            status=data.get("status", "genere"),
            generated_by=data.get("generated_by"),
            notes=data.get("notes"),
            created_at=data.get("created_at")
        )


class StockAlertModel:
    """Modèle d'alerte de stock"""
    
    def __init__(
        self,
        id: int,
        product_id: int,
        warehouse_id: int,
        alert_type: str,
        current_quantity: float,
        threshold: float,
        is_resolved: bool = False,
        resolved_date: Optional[date] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.product_id = product_id
        self.warehouse_id = warehouse_id
        self.alert_type = alert_type
        self.current_quantity = current_quantity
        self.threshold = threshold
        self.is_resolved = is_resolved
        self.resolved_date = resolved_date
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "warehouse_id": self.warehouse_id,
            "alert_type": self.alert_type,
            "current_quantity": self.current_quantity,
            "threshold": self.threshold,
            "is_resolved": self.is_resolved,
            "resolved_date": self.resolved_date,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def is_resolved_status(self) -> bool:
        """Vérifie si résolu"""
        return self.is_resolved


class StockForecastModel:
    """Modèle de prévision de stock"""
    
    def __init__(
        self,
        id: int,
        product_id: int,
        warehouse_id: int,
        forecast_date: date,
        predicted_demand: float,
        confidence_level: float = 0,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.product_id = product_id
        self.warehouse_id = warehouse_id
        self.forecast_date = forecast_date
        self.predicted_demand = predicted_demand
        self.confidence_level = confidence_level
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "warehouse_id": self.warehouse_id,
            "forecast_date": self.forecast_date,
            "predicted_demand": self.predicted_demand,
            "confidence_level": self.confidence_level,
            "notes": self.notes,
            "created_at": self.created_at
        }
