"""
Modèle de données pour les métriques

Ce module définit le modèle de données pour les métriques
dans le module analytique.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class MetricModel:
    """Modèle de métrique"""
    
    def __init__(
        self,
        id: int,
        name: str,
        metric_type: str,
        value: float = 0,
        previous_value: float = 0,
        unit: Optional[str] = None,
        target: Optional[float] = None,
        threshold_warning: Optional[float] = None,
        threshold_critical: Optional[float] = None,
        period_start: Optional[date] = None,
        period_end: Optional[date] = None,
        category: Optional[str] = None,
        module: Optional[str] = None,
        is_active: bool = True,
        calculated_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.metric_type = metric_type
        self.value = value
        self.previous_value = previous_value
        self.unit = unit
        self.target = target
        self.threshold_warning = threshold_warning
        self.threshold_critical = threshold_critical
        self.period_start = period_start
        self.period_end = period_end
        self.category = category
        self.module = module
        self.is_active = is_active
        self.calculated_at = calculated_at or datetime.now()
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "metric_type": self.metric_type,
            "value": self.value,
            "previous_value": self.previous_value,
            "unit": self.unit,
            "target": self.target,
            "threshold_warning": self.threshold_warning,
            "threshold_critical": self.threshold_critical,
            "period_start": self.period_start,
            "period_end": self.period_end,
            "category": self.category,
            "module": self.module,
            "is_active": self.is_active,
            "calculated_at": self.calculated_at,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "MetricModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            name=data.get("name"),
            metric_type=data.get("metric_type"),
            value=data.get("value", 0),
            previous_value=data.get("previous_value", 0),
            unit=data.get("unit"),
            target=data.get("target"),
            threshold_warning=data.get("threshold_warning"),
            threshold_critical=data.get("threshold_critical"),
            period_start=data.get("period_start"),
            period_end=data.get("period_end"),
            category=data.get("category"),
            module=data.get("module"),
            is_active=data.get("is_active", True),
            calculated_at=data.get("calculated_at"),
            created_at=data.get("created_at")
        )
    
    def change_percent(self) -> float:
        """Calcule le pourcentage de changement"""
        if self.previous_value == 0:
            return 0
        return ((self.value - self.previous_value) / abs(self.previous_value)) * 100
    
    def status(self) -> str:
        """Retourne le statut"""
        if self.target is None:
            return "normal"
        
        diff = abs(self.value - self.target)
        
        if self.threshold_critical and diff >= self.threshold_critical:
            return "critical"
        if self.threshold_warning and diff >= self.threshold_warning:
            return "warning"
        return "normal"
    
    def progress_percent(self) -> float:
        """Calcule le pourcentage de progression vers l'objectif"""
        if self.target is None or self.target == 0:
            return 0
        return min(100, (self.value / self.target) * 100)


class DataPointModel:
    """Modèle de point de données"""
    
    def __init__(
        self,
        id: int,
        metric_id: int,
        value: float,
        recorded_at: Optional[datetime] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.metric_id = metric_id
        self.value = value
        self.recorded_at = recorded_at or datetime.now()
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "metric_id": self.metric_id,
            "value": self.value,
            "recorded_at": self.recorded_at,
            "notes": self.notes,
            "created_at": self.created_at
        }


class AlertModel:
    """Modèle d'alerte"""
    
    def __init__(
        self,
        id: int,
        title: str,
        description: Optional[str] = None,
        alert_type: str = "info",
        severity: str = "moyenne",
        metric_id: Optional[int] = None,
        is_read: bool = False,
        is_resolved: bool = False,
        resolved_by: Optional[int] = None,
        resolved_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.title = title
        self.description = description
        self.alert_type = alert_type
        self.severity = severity
        self.metric_id = metric_id
        self.is_read = is_read
        self.is_resolved = is_resolved
        self.resolved_by = resolved_by
        self.resolved_at = resolved_at
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "alert_type": self.alert_type,
            "severity": self.severity,
            "metric_id": self.metric_id,
            "is_read": self.is_read,
            "is_resolved": self.is_resolved,
            "resolved_by": self.resolved_by,
            "resolved_at": self.resolved_at,
            "created_at": self.created_at
        }
    
    def resolve(self, user_id: int):
        """Résout l'alerte"""
        self.is_resolved = True
        self.resolved_by = user_id
        self.resolved_at = datetime.now()
    
    def mark_read(self):
        """Marque l'alerte comme lue"""
        self.is_read = True


class ExportModel:
    """Modèle d'export de données"""
    
    def __init__(
        self,
        id: int,
        name: str,
        export_type: str,
        format: str = "csv",
        parameters: Optional[str] = None,
        file_path: Optional[str] = None,
        file_size: int = 0,
        record_count: int = 0,
        status: str = "en_attente",
        requested_by: int = None,
        generated_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.export_type = export_type
        self.format = format
        self.parameters = parameters
        self.file_path = file_path
        self.file_size = file_size
        self.record_count = record_count
        self.status = status
        self.requested_by = requested_by
        self.generated_at = generated_at
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "export_type": self.export_type,
            "format": self.format,
            "parameters": self.parameters,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "record_count": self.record_count,
            "status": self.status,
            "requested_by": self.requested_by,
            "generated_at": self.generated_at,
            "created_at": self.created_at
        }
    
    def is_completed(self) -> bool:
        """Vérifie si l'export est terminé"""
        return self.status == "termine"
