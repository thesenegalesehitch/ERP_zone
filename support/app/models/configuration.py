"""
Modèle de données pour la configuration du support

Ce module définit le modèle de données pour la configuration
dans le module de support.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class SupportSettingsModel:
    """Modèle de paramètres de support"""
    
    def __init__(
        self,
        id: int,
        setting_key: str,
        setting_value: Optional[str] = None,
        setting_type: str = "texte",
        description: Optional[str] = None,
        is_active: bool = True,
        category: str = "general",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.setting_key = setting_key
        self.setting_value = setting_value
        self.setting_type = setting_type
        self.description = description
        self.is_active = is_active
        self.category = category
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "setting_key": self.setting_key,
            "setting_value": self.setting_value,
            "setting_type": self.setting_type,
            "description": self.description,
            "is_active": self.is_active,
            "category": self.category,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "SupportSettingsModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            setting_key=data.get("setting_key"),
            setting_value=data.get("setting_value"),
            setting_type=data.get("setting_type", "texte"),
            description=data.get("description"),
            is_active=data.get("is_active", True),
            category=data.get("category", "general"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def get_typed_value(self):
        """Retourne la valeur typée"""
        if self.setting_type == "entier":
            return int(self.setting_value) if self.setting_value else 0
        elif self.setting_type == "decimal":
            return float(self.setting_value) if self.setting_value else 0.0
        elif self.setting_type == "booleen":
            return self.setting_value.lower() == "true" if self.setting_value else False
        return self.setting_value


class EmailTemplateModel:
    """Modèle de modèle d'email"""
    
    def __init__(
        self,
        id: int,
        template_name: str,
        subject: str,
        body: str,
        template_type: str = "notification",
        is_active: bool = True,
        variables: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.template_name = template_name
        self.subject = subject
        self.body = body
        self.template_type = template_type
        self.is_active = is_active
        self.variables = variables
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "template_name": self.template_name,
            "subject": self.subject,
            "body": self.body,
            "template_type": self.template_type,
            "is_active": self.is_active,
            "variables": self.variables,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def get_variables(self) -> list:
        """Retourne les variables"""
        if not self.variables:
            return []
        return [v.strip() for v in self.variables.split(",")]
    
    def render(self, context: dict) -> dict:
        """Rend le template avec le contexte"""
        subject = self.subject
        body = self.body
        
        for key, value in context.items():
            placeholder = f"{{{key}}}"
            subject = subject.replace(placeholder, str(value))
            body = body.replace(placeholder, str(value))
        
        return {"subject": subject, "body": body}


class SLAModel:
    """Modèle de SLA"""
    
    def __init__(
        self,
        id: int,
        name: str,
        priority: str,
        first_response_time: int = 0,
        resolution_time: int = 0,
        is_active: bool = True,
        description: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.priority = priority
        self.first_response_time = first_response_time
        self.resolution_time = resolution_time
        self.is_active = is_active
        self.description = description
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "priority": self.priority,
            "first_response_time": self.first_response_time,
            "resolution_time": self.resolution_time,
            "is_active": self.is_active,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def first_response_hours(self) -> float:
        """Retourne le temps de première réponse en heures"""
        return self.first_response_time / 60
    
    def resolution_hours(self) -> float:
        """Retourne le temps de résolution en heures"""
        return self.resolution_time / 60
