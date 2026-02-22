"""
Modèle de données pour les évaluations d'employés

Ce module définit le modèle de données pour les évaluations
dans le module des ressources humaines.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class EvaluationModel:
    """Modèle d'évaluation"""
    
    def __init__(
        self,
        id: int,
        employee_id: int,
        evaluation_period: str,
        evaluation_date: date = None,
        evaluator_id: int = None,
        overall_rating: float = 0,
        status: str = "en_cours",
        strengths: Optional[str] = None,
        weaknesses: Optional[str] = None,
        comments: Optional[str] = None,
        goals_achieved: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.employee_id = employee_id
        self.evaluation_period = evaluation_period
        self.evaluation_date = evaluation_date
        self.evaluator_id = evaluator_id
        self.overall_rating = overall_rating
        self.status = status
        self.strengths = strengths
        self.weaknesses = weaknesses
        self.comments = comments
        self.goals_achieved = goals_achieved
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "evaluation_period": self.evaluation_period,
            "evaluation_date": self.evaluation_date,
            "evaluator_id": self.evaluator_id,
            "overall_rating": self.overall_rating,
            "status": self.status,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "comments": self.comments,
            "goals_achieved": self.goals_achieved,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "EvaluationModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            employee_id=data.get("employee_id"),
            evaluation_period=data.get("evaluation_period"),
            evaluation_date=data.get("evaluation_date"),
            evaluator_id=data.get("evaluator_id"),
            overall_rating=data.get("overall_rating", 0),
            status=data.get("status", "en_cours"),
            strengths=data.get("strengths"),
            weaknesses=data.get("weaknesses"),
            comments=data.get("comments"),
            goals_achieved=data.get("goals_achieved"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_completed(self) -> bool:
        """Vérifie si terminée"""
        return self.status == "terminee"
    
    def rating_label(self) -> str:
        """Étiquette de notation"""
        if self.overall_rating >= 4.5:
            return "Excellent"
        elif self.overall_rating >= 3.5:
            return "Bon"
        elif self.overall_rating >= 2.5:
            return "Satisfaisant"
        elif self.overall_rating >= 1.5:
            return "Insatisfaisant"
        else:
            return "Médiocre"


class EvaluationCriteriaModel:
    """Modèle de critère d'évaluation"""
    
    def __init__(
        self,
        id: int,
        name: str,
        description: Optional[str] = None,
        category: str = "competence",
        weight: float = 1,
        max_score: float = 5,
        is_active: bool = True,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.weight = weight
        self.max_score = max_score
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "weight": self.weight,
            "max_score": self.max_score,
            "is_active": self.is_active,
            "created_at": self.created_at
        }


class EvaluationScoreModel:
    """Modèle de score d'évaluation"""
    
    def __init__(
        self,
        id: int,
        evaluation_id: int,
        criteria_id: int,
        score: float = 0,
        comments: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.evaluation_id = evaluation_id
        self.criteria_id = criteria_id
        self.score = score
        self.comments = comments
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "evaluation_id": self.evaluation_id,
            "criteria_id": self.criteria_id,
            "score": self.score,
            "comments": self.comments,
            "created_at": self.created_at
        }
