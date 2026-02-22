"""
Modèle de données pour les tableaux de bord

Ce module définit le modèle de données pour les tableaux de bord
dans le module analytique.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class DashboardModel:
    """Modèle de tableau de bord"""
    
    def __init__(
        self,
        id: int,
        name: str,
        dashboard_type: str = "standard",
        description: Optional[str] = None,
        layout_config: Optional[str] = None,
        is_public: bool = False,
        is_default: bool = False,
        created_by: int = None,
        owner_id: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.dashboard_type = dashboard_type
        self.description = description
        self.layout_config = layout_config
        self.is_public = is_public
        self.is_default = is_default
        self.created_by = created_by
        self.owner_id = owner_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "dashboard_type": self.dashboard_type,
            "description": self.description,
            "layout_config": self.layout_config,
            "is_public": self.is_public,
            "is_default": self.is_default,
            "created_by": self.created_by,
            "owner_id": self.owner_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "DashboardModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            name=data.get("name"),
            dashboard_type=data.get("dashboard_type", "standard"),
            description=data.get("description"),
            layout_config=data.get("layout_config"),
            is_public=data.get("is_public", False),
            is_default=data.get("is_default", False),
            created_by=data.get("created_by"),
            owner_id=data.get("owner_id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )


class WidgetModel:
    """Modèle de widget"""
    
    def __init__(
        self,
        id: int,
        dashboard_id: int,
        widget_type: str,
        title: Optional[str] = None,
        position_x: int = 0,
        position_y: int = 0,
        width: int = 4,
        height: int = 3,
        config: Optional[str] = None,
        data_source: Optional[str] = None,
        refresh_interval: int = 300,
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
        self.data_source = data_source
        self.refresh_interval = refresh_interval
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
            "data_source": self.data_source,
            "refresh_interval": self.refresh_interval,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class ChartConfigModel:
    """Modèle de configuration de graphique"""
    
    def __init__(
        self,
        id: int,
        name: str,
        chart_type: str,
        x_axis_field: Optional[str] = None,
        y_axis_fields: Optional[str] = None,
        group_by: Optional[str] = None,
        aggregation: str = "sum",
        color_scheme: Optional[str] = None,
        show_legend: bool = True,
        show_grid: bool = True,
        is_stacked: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.chart_type = chart_type
        self.x_axis_field = x_axis_field
        self.y_axis_fields = y_axis_fields
        self.group_by = group_by
        self.aggregation = aggregation
        self.color_scheme = color_scheme
        self.show_legend = show_legend
        self.show_grid = show_grid
        self.is_stacked = is_stacked
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "chart_type": self.chart_type,
            "x_axis_field": self.x_axis_field,
            "y_axis_fields": self.y_axis_fields,
            "group_by": self.group_by,
            "aggregation": self.aggregation,
            "color_scheme": self.color_scheme,
            "show_legend": self.show_legend,
            "show_grid": self.show_grid,
            "is_stacked": self.is_stacked,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class KPIModel:
    """Modèle d'indicateur clé de performance"""
    
    def __init__(
        self,
        id: int,
        name: str,
        kpi_type: str,
        value: float = 0,
        previous_value: float = 0,
        target: Optional[float] = None,
        unit: Optional[str] = None,
        currency: Optional[str] = None,
        format: str = "number",
        threshold_warning: Optional[float] = None,
        threshold_critical: Optional[float] = None,
        period_type: str = "monthly",
        category: Optional[str] = None,
        last_updated: Optional[datetime] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.kpi_type = kpi_type
        self.value = value
        self.previous_value = previous_value
        self.target = target
        self.unit = unit
        self.currency = currency
        self.format = format
        self.threshold_warning = threshold_warning
        self.threshold_critical = threshold_critical
        self.period_type = period_type
        self.category = category
        self.last_updated = last_updated or datetime.now()
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "kpi_type": self.kpi_type,
            "value": self.value,
            "previous_value": self.previous_value,
            "target": self.target,
            "unit": self.unit,
            "currency": self.currency,
            "format": self.format,
            "threshold_warning": self.threshold_warning,
            "threshold_critical": self.threshold_critical,
            "period_type": self.period_type,
            "category": self.category,
            "last_updated": self.last_updated,
            "created_at": self.created_at
        }
    
    def change_percent(self) -> float:
        """Calcule le pourcentage de changement"""
        if self.previous_value == 0:
            return 0
        return ((self.value - self.previous_value) / abs(self.previous_value)) * 100
    
    def status(self) -> str:
        """Retourne le statut"""
        if self.target is None:
            return "normal"
        if self.threshold_critical and abs(self.value - self.target) >= self.threshold_critical:
            return "critical"
        if self.threshold_warning and abs(self.value - self.target) >= self.threshold_warning:
            return "warning"
        return "normal"
