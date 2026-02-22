"""
Modèle de données pour les équipes de projet

Ce module définit le modèle de données pour les équipes
dans le module de gestion de projets.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class TeamModel:
    """Modèle d'équipe"""
    
    def __init__(
        self,
        id: int,
        name: str,
        project_id: Optional[int] = None,
        description: Optional[str] = None,
        team_lead_id: Optional[int] = None,
        status: str = "actif",
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.project_id = project_id
        self.description = description
        self.team_lead_id = team_lead_id
        self.status = status
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "project_id": self.project_id,
            "description": self.description,
            "team_lead_id": self.team_lead_id,
            "status": self.status,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TeamModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            name=data.get("name"),
            project_id=data.get("project_id"),
            description=data.get("description"),
            team_lead_id=data.get("team_lead_id"),
            status=data.get("status", "actif"),
            created_by=data.get("created_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_active(self) -> bool:
        """Vérifie si active"""
        return self.status == "actif"


class TeamMemberModel:
    """Modèle de membre d'équipe"""
    
    def __init__(
        self,
        id: int,
        team_id: int,
        user_id: int,
        role: str = "membre",
        joined_date: date = None,
        is_active: bool = True,
        notes: Optional[str] = None,
        added_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.team_id = team_id
        self.user_id = user_id
        self.role = role
        self.joined_date = joined_date or date.today()
        self.is_active = is_active
        self.notes = notes
        self.added_by = added_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "team_id": self.team_id,
            "user_id": self.user_id,
            "role": self.role,
            "joined_date": self.joined_date,
            "is_active": self.is_active,
            "notes": self.notes,
            "added_by": self.added_by,
            "created_at": self.created_at
        }
    
    def is_active_member(self) -> bool:
        """Vérifie si actif"""
        return self.is_active


class TeamSkillModel:
    """Modèle de compétence d'équipe"""
    
    def __init__(
        self,
        id: int,
        team_id: int,
        skill_name: str,
        skill_level: str = "intermediaire",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.team_id = team_id
        self.skill_name = skill_name
        self.skill_level = skill_level
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "team_id": self.team_id,
            "skill_name": self.skill_name,
            "skill_level": self.skill_level,
            "notes": self.notes,
            "created_at": self.created_at
        }
