"""
Modèle de données pour les risques de projet

Ce module définit le modèle de données pour les risques
dans le module de gestion de projets.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class RiskModel:
    """Modèle de risque"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        title: str,
        description: Optional[str] = None,
        risk_type: str = "technique",
        impact: str = "moyen",
        probability: str = "moyenne",
        severity: float = 0,
        status: str = "identifie",
        mitigation_plan: Optional[str] = None,
        identified_date: date = None,
        due_date: Optional[date] = None,
        resolved_date: Optional[date] = None,
        assigned_to: Optional[int] = None,
        notes: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.title = title
        self.description = description
        self.risk_type = risk_type
        self.impact = impact
        self.probability = probability
        self.severity = severity
        self.status = status
        self.mitigation_plan = mitigation_plan
        self.identified_date = identified_date or date.today()
        self.due_date = due_date
        self.resolved_date = resolved_date
        self.assigned_to = assigned_to
        self.notes = notes
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "risk_type": self.risk_type,
            "impact": self.impact,
            "probability": self.probability,
            "severity": self.severity,
            "status": self.status,
            "mitigation_plan": self.mitigation_plan,
            "identified_date": self.identified_date,
            "due_date": self.due_date,
            "resolved_date": self.resolved_date,
            "assigned_to": self.assigned_to,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "RiskModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            project_id=data.get("project_id"),
            title=data.get("title"),
            description=data.get("description"),
            risk_type=data.get("risk_type", "technique"),
            impact=data.get("impact", "moyen"),
            probability=data.get("probability", "moyenne"),
            severity=data.get("severity", 0),
            status=data.get("status", "identifie"),
            mitigation_plan=data.get("mitigation_plan"),
            identified_date=data.get("identified_date"),
            due_date=data.get("due_date"),
            resolved_date=data.get("resolved_date"),
            assigned_to=data.get("assigned_to"),
            notes=data.get("notes"),
            created_by=data.get("created_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def calculate_severity(self) -> float:
        """Calcule la sévérité"""
        impact_values = {"faible": 1, "moyen": 2, "eleve": 3, "critique": 4}
        probability_values = {"faible": 1, "moyenne": 2, "haute": 3, "tres_haute": 4}
        impact = impact_values.get(self.impact, 2)
        probability = probability_values.get(self.probability, 2)
        return impact * probability
    
    def is_resolved(self) -> bool:
        """Vérifie si résolu"""
        return self.status == "resolu"


class RiskUpdateModel:
    """Modèle de mise à jour de risque"""
    
    def __init__(
        self,
        id: int,
        risk_id: int,
        previous_status: str,
        new_status: str,
        notes: Optional[str] = None,
        updated_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.risk_id = risk_id
        self.previous_status = previous_status
        self.new_status = new_status
        self.notes = notes
        self.updated_by = updated_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "risk_id": self.risk_id,
            "previous_status": self.previous_status,
            "new_status": self.new_status,
            "notes": self.notes,
            "updated_by": self.updated_by,
            "created_at": self.created_at
        }


class RiskCategoryModel:
    """Modèle de catégorie de risque"""
    
    def __init__(
        self,
        id: int,
        name: str,
        description: Optional[str] = None,
        color: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.color = color
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "color": self.color,
            "created_at": self.created_at
        }
