"""
Modèle de données pour les rapports analytiques

Ce module définit le modèle de données pour les rapports
dans le module analytique.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class AnalyticsReportModel:
    """Modèle de rapport analytique"""
    
    def __init__(
        self,
        id: int,
        report_type: str,
        name: str,
        period_start: date,
        period_end: date,
        data: Optional[str] = None,
        status: str = "planifie",
        generated_by: int = None,
        generated_at: Optional[datetime] = None,
        schedule: Optional[str] = None,
        recipients: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.report_type = report_type
        self.name = name
        self.period_start = period_start
        self.period_end = period_end
        self.data = data
        self.status = status
        self.generated_by = generated_by
        self.generated_at = generated_at
        self.schedule = schedule
        self.recipients = recipients
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "report_type": self.report_type,
            "name": self.name,
            "period_start": self.period_start,
            "period_end": self.period_end,
            "data": self.data,
            "status": self.status,
            "generated_by": self.generated_by,
            "generated_at": self.generated_at,
            "schedule": self.schedule,
            "recipients": self.recipients,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "AnalyticsReportModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            report_type=data.get("report_type"),
            name=data.get("name"),
            period_start=data.get("period_start"),
            period_end=data.get("period_end"),
            data=data.get("data"),
            status=data.get("status", "planifie"),
            generated_by=data.get("generated_by"),
            generated_at=data.get("generated_at"),
            schedule=data.get("schedule"),
            recipients=data.get("recipients"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_generated(self) -> bool:
        """Vérifie si le rapport est généré"""
        return self.status == "genere"
    
    def is_scheduled(self) -> bool:
        """Vérifie si le rapport est planifié"""
        return self.schedule is not None


class DashboardModel:
    """Modèle de tableau de bord"""
    
    def __init__(
        self,
        id: int,
        name: str,
        description: Optional[str] = None,
        layout: Optional[str] = None,
        widgets: Optional[str] = None,
        is_default: bool = False,
        is_public: bool = False,
        owner_id: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.layout = layout
        self.widgets = widgets
        self.is_default = is_default
        self.is_public = is_public
        self.owner_id = owner_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "layout": self.layout,
            "widgets": self.widgets,
            "is_default": self.is_default,
            "is_public": self.is_public,
            "owner_id": self.owner_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def widget_count(self) -> int:
        """Nombre de widgets"""
        if not self.widgets:
            return 0
        return len(self.widgets.split(",")) if "," in self.widgets else 1


class MetricModel:
    """Modèle de métrique"""
    
    def __init__(
        self,
        id: int,
        name: str,
        metric_type: str,
        value: float = 0,
        previous_value: float = 0,
        change_percentage: float = 0,
        unit: Optional[str] = None,
        target: Optional[float] = None,
        date: Optional[date] = None,
        category: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.metric_type = metric_type
        self.value = value
        self.previous_value = previous_value
        self.change_percentage = change_percentage
        self.unit = unit
        self.target = target
        self.date = date
        self.category = category
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "metric_type": self.metric_type,
            "value": self.value,
            "previous_value": self.previous_value,
            "change_percentage": self.change_percentage,
            "unit": self.unit,
            "target": self.target,
            "date": self.date,
            "category": self.category,
            "created_at": self.created_at
        }
    
    def calculate_change(self):
        """Calcule le pourcentage de changement"""
        if self.previous_value == 0:
            self.change_percentage = 0
        else:
            self.change_percentage = ((self.value - self.previous_value) / 
                                     self.previous_value) * 100
    
    def is_positive_change(self) -> bool:
        """Vérifie si le changement est positif"""
        return self.change_percentage > 0
    
    def target_achieved(self) -> bool:
        """Vérifie si l'objectif est atteint"""
        if self.target is None:
            return False
        return self.value >= self.target
