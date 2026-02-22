"""
Modèle de données pour les catégories

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
        code: str,
        description: Optional[str] = None,
        parent_id: Optional[int] = None,
        image_url: Optional[str] = None,
        display_order: int = 0,
        is_active: bool = True,
        product_count: int = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.code = code
        self.description = description
        self.parent_id = parent_id
        self.image_url = image_url
        self.display_order = display_order
        self.is_active = is_active
        self.product_count = product_count
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "parent_id": self.parent_id,
            "image_url": self.image_url,
            "display_order": self.display_order,
            "is_active": self.is_active,
            "product_count": self.product_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "CategoryModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            name=data.get("name"),
            code=data.get("code"),
            description=data.get("description"),
            parent_id=data.get("parent_id"),
            image_url=data.get("image_url"),
            display_order=data.get("display_order", 0),
            is_active=data.get("is_active", True),
            product_count=data.get("product_count", 0),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_active(self) -> bool:
        """Vérifie si la catégorie est active"""
        return self.is_active
    
    def has_parent(self) -> bool:
        """Vérifie si la catégorie a un parent"""
        return self.parent_id is not None


class BrandModel:
    """Modèle de marque"""
    
    def __init__(
        self,
        id: int,
        name: str,
        code: str,
        description: Optional[str] = None,
        logo_url: Optional[str] = None,
        website: Optional[str] = None,
        is_active: bool = True,
        product_count: int = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.code = code
        self.description = description
        self.logo_url = logo_url
        self.website = website
        self.is_active = is_active
        self.product_count = product_count
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "logo_url": self.logo_url,
            "website": self.website,
            "is_active": self.is_active,
            "product_count": self.product_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class UnitOfMeasureModel:
    """Modèle d'unité de mesure"""
    
    def __init__(
        self,
        id: int,
        name: str,
        code: str,
        abbreviation: str,
        type: str = "quantity",
        conversion_factor: float = 1,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.code = code
        self.abbreviation = abbreviation
        self.type = type
        self.conversion_factor = conversion_factor
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "abbreviation": self.abbreviation,
            "type": self.type,
            "conversion_factor": self.conversion_factor,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class ProductVariantModel:
    """Modèle de variante de produit"""
    
    def __init__(
        self,
        id: int,
        product_id: int,
        sku: str,
        name: str,
        price: float = 0,
        cost_price: float = 0,
        barcode: Optional[str] = None,
        attributes: Optional[str] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.product_id = product_id
        self.sku = sku
        self.name = name
        self.price = price
        self.cost_price = cost_price
        self.barcode = barcode
        self.attributes = attributes
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "sku": self.sku,
            "name": self.name,
            "price": self.price,
            "cost_price": self.cost_price,
            "barcode": self.barcode,
            "attributes": self.attributes,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_active(self) -> bool:
        """Vérifie si la variante est active"""
        return self.is_active
