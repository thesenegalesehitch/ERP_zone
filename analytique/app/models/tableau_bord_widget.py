"""
Modèle de données pour les widgets de tableau de bord

Ce module définit le modèle de données pour les widgets
dans le module analytique.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class DashboardWidgetModel:
    """Modèle de widget de tableau de bord"""
    
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
        self.data_source = data_source
        self.refresh_interval = refresh_interval
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
            "data_source": self.data_source,
            "refresh_interval": self.refresh_interval,
            "is_visible": self.is_visible,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "DashboardWidgetModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            dashboard_id=data.get("dashboard_id"),
            widget_type=data.get("widget_type"),
            title=data.get("title"),
            position_x=data.get("position_x", 0),
            position_y=data.get("position_y", 0),
            width=data.get("width", 4),
            height=data.get("height", 3),
            config=data.get("config"),
            data_source=data.get("data_source"),
            refresh_interval=data.get("refresh_interval", 300),
            is_visible=data.get("is_visible", True),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_visible(self) -> bool:
        """Vérifie si le widget est visible"""
        return self.is_visible


class ChartModel:
    """Modèle de graphique"""
    
    def __init__(
        self,
        id: int,
        name: str,
        chart_type: str,
        x_axis: str,
        y_axis: str,
        group_by: Optional[str] = None,
        aggregation: str = "sum",
        color_scheme: Optional[str] = None,
        show_legend: bool = True,
        show_grid: bool = True,
        is_stacked: bool = False,
        data_config: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.chart_type = chart_type
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.group_by = group_by
        self.aggregation = aggregation
        self.color_scheme = color_scheme
        self.show_legend = show_legend
        self.show_grid = show_grid
        self.is_stacked = is_stacked
        self.data_config = data_config
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "chart_type": self.chart_type,
            "x_axis": self.x_axis,
            "y_axis": self.y_axis,
            "group_by": self.group_by,
            "aggregation": self.aggregation,
            "color_scheme": self.color_scheme,
            "show_legend": self.show_legend,
            "show_grid": self.show_grid,
            "is_stacked": self.is_stacked,
            "data_config": self.data_config,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class DashboardShareModel:
    """Modèle de partage de tableau de bord"""
    
    def __init__(
        self,
        id: int,
        dashboard_id: int,
        shared_with: int,
        permission: str = "view",
        shared_by: int = None,
        shared_at: Optional[datetime] = None,
        expires_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.dashboard_id = dashboard_id
        self.shared_with = shared_with
        self.permission = permission
        self.shared_by = shared_by
        self.shared_at = shared_at or datetime.now()
        self.expires_at = expires_at
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "dashboard_id": self.dashboard_id,
            "shared_with": self.shared_with,
            "permission": self.permission,
            "shared_by": self.shared_by,
            "shared_at": self.shared_at,
            "expires_at": self.expires_at,
            "created_at": self.created_at
        }
    
    def is_expired(self) -> bool:
        """Vérifie si le partage est expiré"""
        if not self.expires_at:
            return False
        return datetime.now() > self.expires_at


class DataExportModel:
    """Modèle d'export de données"""
    
    def __init__(
        self,
        id: int,
        name: str,
        export_type: str,
        format: str = "csv",
        filters: Optional[str] = None,
        columns: Optional[str] = None,
        file_path: Optional[str] = None,
        file_size: int = 0,
        record_count: int = 0,
        status: str = "en_attente",
        requested_by: int = None,
        generated_at: Optional[datetime] = None,
        expires_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.export_type = export_type
        self.format = format
        self.filters = filters
        self.columns = columns
        self.file_path = file_path
        self.file_size = file_size
        self.record_count = record_count
        self.status = status
        self.requested_by = requested_by
        self.generated_at = generated_at
        self.expires_at = expires_at
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "export_type": self.export_type,
            "format": self.format,
            "filters": self.filters,
            "columns": self.columns,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "record_count": self.record_count,
            "status": self.status,
            "requested_by": self.requested_by,
            "generated_at": self.generated_at,
            "expires_at": self.expires_at,
            "created_at": self.created_at
        }
    
    def is_ready(self) -> bool:
        """Vérifie si l'export est prêt"""
        return self.status == "pret"
