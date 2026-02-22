"""
Modèle de données pour les équipes de projet

Ce module définit le modèle de données pour les équipes
dans le module de gestion de projets.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class ProjectTeamModel:
    """Modèle d'équipe de projet"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        name: str,
        description: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.name = name
        self.description = description
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ProjectTeamModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            project_id=data.get("project_id"),
            name=data.get("name"),
            description=data.get("description"),
            created_at=data.get("created_at")
        )


class TeamMemberModel:
    """Modèle de membre d'équipe"""
    
    def __init__(
        self,
        id: int,
        team_id: int,
        user_id: int,
        role: str = "membre",
        allocation_percentage: float = 100,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.team_id = team_id
        self.user_id = user_id
        self.role = role
        self.allocation_percentage = allocation_percentage
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "team_id": self.team_id,
            "user_id": self.user_id,
            "role": self.role,
            "allocation_percentage": self.allocation_percentage,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "is_active": self.is_active,
            "created_at": self.created_at
        }
    
    def is_manager(self) -> bool:
        """Vérifie si le membre est gestionnaire"""
        return self.role == "gestionnaire"
    
    def is_fully_allocated(self) -> bool:
        """Vérifie si le membre est entièrement alloué"""
        return self.allocation_percentage >= 100


class TeamSkillModel:
    """Modèle de compétence d'équipe"""
    
    def __init__(
        self,
        id: int,
        team_id: int,
        skill_name: str,
        level: str = "intermediaire",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.team_id = team_id
        self.skill_name = skill_name
        self.level = level
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "team_id": self.team_id,
            "skill_name": self.skill_name,
            "level": self.level,
            "notes": self.notes,
            "created_at": self.created_at
        }


class MemberAvailabilityModel:
    """Modèle de disponibilité de membre"""
    
    def __init__(
        self,
        id: int,
        member_id: int,
        date: str,
        available_hours: float = 8,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.member_id = member_id
        self.date = date
        self.available_hours = available_hours
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "member_id": self.member_id,
            "date": self.date,
            "available_hours": self.available_hours,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def is_available(self) -> bool:
        """Vérifie si le membre est disponible"""
        return self.available_hours > 0
