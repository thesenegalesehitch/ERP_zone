"""
Modèle de données pour les indicateurs analytiques

Ce module définit le modèle de données pour les indicateurs
dans le module analytique.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class KPIIndicatorModel:
    """Modèle d'indicateur KPI"""
    
    def __init__(
        self,
        id: int,
        name: str,
        code: str,
        description: Optional[str] = None,
        target_value: float = 0,
        warning_threshold: float = 0,
        critical_threshold: float = 0,
        unit: Optional[str] = None,
        category: str = "general",
        is_active: bool = True,
        calculation_method: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.code = code
        self.description = description
        self.target_value = target_value
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        self.unit = unit
        self.category = category
        self.is_active = is_active
        self.calculation_method = calculation_method
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "target_value": self.target_value,
            "warning_threshold": self.warning_threshold,
            "critical_threshold": self.critical_threshold,
            "unit": self.unit,
            "category": self.category,
            "is_active": self.is_active,
            "calculation_method": self.calculation_method,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "KPIIndicatorModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            name=data.get("name"),
            code=data.get("code"),
            description=data.get("description"),
            target_value=data.get("target_value", 0),
            warning_threshold=data.get("warning_threshold", 0),
            critical_threshold=data.get("critical_threshold", 0),
            unit=data.get("unit"),
            category=data.get("category", "general"),
            is_active=data.get("is_active", True),
            calculation_method=data.get("calculation_method"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def get_status(self, value: float) -> str:
        """Obtient le statut"""
        if self.critical_threshold > 0 and value >= self.critical_threshold:
            return "critique"
        elif self.warning_threshold > 0 and value >= self.warning_threshold:
            return "avertissement"
        return "normal"
    
    def target_achieved(self, value: float) -> bool:
        """Vérifie si l'objectif est atteint"""
        return value >= self.target_value


class DataPointModel:
    """Modèle de point de données"""
    
    def __init__(
        self,
        id: int,
        indicator_id: int,
        value: float,
        record_date: date = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.indicator_id = indicator_id
        self.value = value
        self.record_date = record_date
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "indicator_id": self.indicator_id,
            "value": self.value,
            "record_date": self.record_date,
            "notes": self.notes,
            "created_at": self.created_at
        }


class DashboardWidgetModel:
    """Modèle de widget de tableau de bord"""
    
    def __init__(
        self,
        id: int,
        dashboard_id: int,
        widget_type: str,
        title: str,
        position_x: int = 0,
        position_y: int = 0,
        width: int = 1,
        height: int = 1,
        config: Optional[str] = None,
        is_visible: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.dashboard_id = dashboard_id
        self.widget_type = widget_type
        self.title = title
        self.position_x = position_x
        self.position_y = position_y
        self.width = width
        self.height = height
        self.config = config
        self.is_visible = is_visible
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "dashboard_id": self.dashboard_id,
            "widget_type": self.widget_type,
            "title": self.title,
            "position_x": self.position_x,
            "position_y": self.position_y,
            "width": self.width,
            "height": self.height,
            "config": self.config,
            "is_visible": self.is_visible,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
