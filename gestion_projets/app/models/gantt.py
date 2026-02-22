"""
Modèle de données pour le diagramme de Gantt

Ce module définit le modèle de données pour le diagramme de Gantt
dans le module de gestion de projets.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class GanttTaskModel:
    """Modèle de tâche Gantt"""
    
    def __init__(
        self,
        id: int,
        task_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        progress: int = 0,
        dependencies: Optional[str] = None,
        color: Optional[str] = None,
        is_milestone: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.task_id = task_id
        self.start_date = start_date
        self.end_date = end_date
        self.progress = progress
        self.dependencies = dependencies
        self.color = color
        self.is_milestone = is_milestone
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "task_id": self.task_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "progress": self.progress,
            "dependencies": self.dependencies,
            "color": self.color,
            "is_milestone": self.is_milestone,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "GanttTaskModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            task_id=data.get("task_id"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            progress=data.get("progress", 0),
            dependencies=data.get("dependencies"),
            color=data.get("color"),
            is_milestone=data.get("is_milestone", False),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def duration_days(self) -> Optional[int]:
        """Calcule la durée en jours"""
        if not self.start_date or not self.end_date:
            return None
        return (self.end_date - self.start_date).days
    
    def is_completed(self) -> bool:
        """Vérifie si la tâche est terminée"""
        return self.progress >= 100


class ProjectPhaseModel:
    """Modèle de phase de projet"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        name: str,
        description: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        status: str = "planifie",
        order: int = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.order = order
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status,
            "order": self.order,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_completed(self) -> bool:
        """Vérifie si la phase est terminée"""
        return self.status == "termine"
    
    def is_in_progress(self) -> bool:
        """Vérifie si la phase est en cours"""
        return self.status == "en_cours"


class ProjectBudgetModel:
    """Modèle de budget de projet"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        planned_budget: float = 0,
        actual_cost: float = 0,
        approved_budget: float = 0,
        currency: str = "XOF",
        status: str = "planifie",
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.planned_budget = planned_budget
        self.actual_cost = actual_cost
        self.approved_budget = approved_budget
        self.currency = currency
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "planned_budget": self.planned_budget,
            "actual_cost": self.actual_cost,
            "approved_budget": self.approved_budget,
            "currency": self.currency,
            "status": self.status,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def budget_variance(self) -> float:
        """Calcule l'écart de budget"""
        return self.planned_budget - self.actual_cost
    
    def budget_usage_percent(self) -> float:
        """Calcule le pourcentage d'utilisation"""
        if self.planned_budget == 0:
            return 0
        return (self.actual_cost / self.planned_budget) * 100


class ProjectRiskModel:
    """Modèle de risque de projet"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        title: str,
        description: Optional[str] = None,
        probability: str = "moyenne",
        impact: str = "moyenne",
        risk_level: str = "moyen",
        mitigation_plan: Optional[str] = None,
        status: str = "identifie",
        identified_by: int = None,
        identified_at: Optional[datetime] = None,
        resolved_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.title = title
        self.description = description
        self.probability = probability
        self.impact = impact
        self.risk_level = risk_level
        self.mitigation_plan = mitigation_plan
        self.status = status
        self.identified_by = identified_by
        self.identified_at = identified_at or datetime.now()
        self.resolved_at = resolved_at
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "probability": self.probability,
            "impact": self.impact,
            "risk_level": self.risk_level,
            "mitigation_plan": self.mitigation_plan,
            "status": self.status,
            "identified_by": self.identified_by,
            "identified_at": self.identified_at,
            "resolved_at": self.resolved_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_resolved(self) -> bool:
        """Vérifie si le risque est résolu"""
        return self.status == "resolu"
    
    def calculate_risk_level(self):
        """Calcule le niveau de risque"""
        prob_values = {"faible": 1, "moyenne": 2, "haute": 3}
        impact_values = {"faible": 1, "moyenne": 2, "haute": 3, "critique": 4}
        
        prob = prob_values.get(self.probability, 2)
        imp = impact_values.get(self.impact, 2)
        level = prob * imp
        
        if level >= 9:
            self.risk_level = "critique"
        elif level >= 6:
            self.risk_level = "eleve"
        elif level >= 3:
            self.risk_level = "moyen"
        else:
            self.risk_level = "faible"
