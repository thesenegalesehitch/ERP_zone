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
        name: str,
        description: Optional[str] = None,
        category: str = "technique",
        probability: str = "moyenne",
        impact: str = "moyen",
        risk_score: int = 0,
        status: str = "identifie",
        identified_date: date = None,
        mitigation_plan: Optional[str] = None,
        contingency_plan: Optional[str] = None,
        owner_id: Optional[int] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.name = name
        self.description = description
        self.category = category
        self.probability = probability
        self.impact = impact
        self.risk_score = risk_score
        self.status = status
        self.identified_date = identified_date
        self.mitigation_plan = mitigation_plan
        self.contingency_plan = contingency_plan
        self.owner_id = owner_id
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "probability": self.probability,
            "impact": self.impact,
            "risk_score": self.risk_score,
            "status": self.status,
            "identified_date": self.identified_date,
            "mitigation_plan": self.mitigation_plan,
            "contingency_plan": self.contingency_plan,
            "owner_id": self.owner_id,
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
            name=data.get("name"),
            description=data.get("description"),
            category=data.get("category", "technique"),
            probability=data.get("probability", "moyenne"),
            impact=data.get("impact", "moyen"),
            risk_score=data.get("risk_score", 0),
            status=data.get("status", "identifie"),
            identified_date=data.get("identified_date"),
            mitigation_plan=data.get("mitigation_plan"),
            contingency_plan=data.get("contingency_plan"),
            owner_id=data.get("owner_id"),
            created_by=data.get("created_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def calculate_risk_score(self):
        """Calcule le score de risque"""
        probability_map = {"tres_faible": 1, "faible": 2, "moyenne": 3, "haute": 4, "tres_haute": 5}
        impact_map = {"tres_faible": 1, "faible": 2, "moyen": 3, "eleve": 4, "critique": 5}
        
        prob = probability_map.get(self.probability, 3)
        imp = impact_map.get(self.impact, 3)
        self.risk_score = prob * imp
    
    def risk_level(self) -> str:
        """Niveau de risque"""
        if self.risk_score >= 16:
            return "critique"
        elif self.risk_score >= 12:
            return "eleve"
        elif self.risk_score >= 6:
            return "moyen"
        else:
            return "faible"


class RiskUpdateModel:
    """Modèle de mise à jour de risque"""
    
    def __init__(
        self,
        id: int,
        risk_id: int,
        update_date: date = None,
        status: str = "en_suivi",
        probability: Optional[str] = None,
        impact: Optional[str] = None,
        notes: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.risk_id = risk_id
        self.update_date = update_date
        self.status = status
        self.probability = probability
        self.impact = impact
        self.notes = notes
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "risk_id": self.risk_id,
            "update_date": self.update_date,
            "status": self.status,
            "probability": self.probability,
            "impact": self.impact,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at
        }


class IssueModel:
    """Modèle de problème"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        title: str,
        description: Optional[str] = None,
        issue_type: str = "technique",
        priority: str = "moyenne",
        status: str = "ouverte",
        assignee_id: Optional[int] = None,
        due_date: Optional[date] = None,
        resolved_date: Optional[date] = None,
        notes: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.title = title
        self.description = description
        self.issue_type = issue_type
        self.priority = priority
        self.status = status
        self.assignee_id = assignee_id
        self.due_date = due_date
        self.resolved_date = resolved_date
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
            "issue_type": self.issue_type,
            "priority": self.priority,
            "status": self.status,
            "assignee_id": self.assignee_id,
            "due_date": self.due_date,
            "resolved_date": self.resolved_date,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_resolved(self) -> bool:
        """Vérifie si résolu"""
        return self.status == "resolue"
    
    def is_overdue(self) -> bool:
        """Vérifie si en retard"""
        if not self.due_date or self.is_resolved():
            return False
        return date.today() > self.due_date
