"""
Modèle de données pour les catégories de produits

Ce module définit le modèle de données pour les catégories
dans le module de gestion des stocks.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class CategoryModel:
    """Modèle de catégorie"""
    
    def __init__(
        self,
        id: int,
        name: str,
        description: Optional[str] = None,
        parent_id: Optional[int] = None,
        code: Optional[str] = None,
        is_active: bool = True,
        image_url: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.parent_id = parent_id
        self.code = code
        self.is_active = is_active
        self.image_url = image_url
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "parent_id": self.parent_id,
            "code": self.code,
            "is_active": self.is_active,
            "image_url": self.image_url,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "CategoryModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            name=data.get("name"),
            description=data.get("description"),
            parent_id=data.get("parent_id"),
            code=data.get("code"),
            is_active=data.get("is_active", True),
            image_url=data.get("image_url"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_active_status(self) -> bool:
        """Vérifie si active"""
        return self.is_active


class SubCategoryModel:
    """Modèle de sous-catégorie"""
    
    def __init__(
        self,
        id: int,
        category_id: int,
        name: str,
        description: Optional[str] = None,
        code: Optional[str] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.category_id = category_id
        self.name = name
        self.description = description
        self.code = code
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description,
            "code": self.code,
            "is_active": self.is_active,
            "created_at": self.created_at
        }


class CategoryAttributeModel:
    """Modèle d'attribut de catégorie"""
    
    def __init__(
        self,
        id: int,
        category_id: int,
        name: str,
        attribute_type: str = "text",
        is_required: bool = False,
        options: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.category_id = category_id
        self.name = name
        self.attribute_type = attribute_type
        self.is_required = is_required
        self.options = options
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "category_id": self.category_id,
            "name": self.name,
            "attribute_type": self.attribute_type,
            "is_required": self.is_required,
            "options": self.options,
            "created_at": self.created_at
        }
