"""
Modèle de données pour les produits

Ce module définit le modèle de données pour les produits
dans le module de gestion des stocks.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class ProductModel:
    """Modèle de produit"""
    
    def __init__(
        self,
        id: int,
        product_code: str,
        name: str,
        description: Optional[str] = None,
        category: Optional[str] = None,
        unit: str = "unite",
        price: float = 0,
        cost: float = 0,
        currency: str = "XOF",
        sku: Optional[str] = None,
        barcode: Optional[str] = None,
        weight: float = 0,
        dimensions: Optional[str] = None,
        image_url: Optional[str] = None,
        is_active: bool = True,
        min_stock_level: float = 0,
        max_stock_level: float = 0,
        reorder_point: float = 0,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.product_code = product_code
        self.name = name
        self.description = description
        self.category = category
        self.unit = unit
        self.price = price
        self.cost = cost
        self.currency = currency
        self.sku = sku
        self.barcode = barcode
        self.weight = weight
        self.dimensions = dimensions
        self.image_url = image_url
        self.is_active = is_active
        self.min_stock_level = min_stock_level
        self.max_stock_level = max_stock_level
        self.reorder_point = reorder_point
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "product_code": self.product_code,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "unit": self.unit,
            "price": self.price,
            "cost": self.cost,
            "currency": self.currency,
            "sku": self.sku,
            "barcode": self.barcode,
            "weight": self.weight,
            "dimensions": self.dimensions,
            "image_url": self.image_url,
            "is_active": self.is_active,
            "min_stock_level": self.min_stock_level,
            "max_stock_level": self.max_stock_level,
            "reorder_point": self.reorder_point,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ProductModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            product_code=data.get("product_code"),
            name=data.get("name"),
            description=data.get("description"),
            category=data.get("category"),
            unit=data.get("unit", "unite"),
            price=data.get("price", 0),
            cost=data.get("cost", 0),
            currency=data.get("currency", "XOF"),
            sku=data.get("sku"),
            barcode=data.get("barcode"),
            weight=data.get("weight", 0),
            dimensions=data.get("dimensions"),
            image_url=data.get("image_url"),
            is_active=data.get("is_active", True),
            min_stock_level=data.get("min_stock_level", 0),
            max_stock_level=data.get("max_stock_level", 0),
            reorder_point=data.get("reorder_point", 0),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def profit_margin(self) -> float:
        """Marge bénéficiaire"""
        if self.price == 0:
            return 0
        return ((self.price - self.cost) / self.price) * 100
    
    def is_active_product(self) -> bool:
        """Vérifie si actif"""
        return self.is_active


class ProductCategoryModel:
    """Modèle de catégorie de produit"""
    
    def __init__(
        self,
        id: int,
        name: str,
        code: str,
        parent_id: Optional[int] = None,
        description: Optional[str] = None,
        is_active: bool = True,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.code = code
        self.parent_id = parent_id
        self.description = description
        self.is_active = is_active
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "parent_id": self.parent_id,
            "description": self.description,
            "is_active": self.is_active,
            "notes": self.notes,
            "created_at": self.created_at
        }


class StockLevelModel:
    """Modèle de niveau de stock"""
    
    def __init__(
        self,
        id: int,
        product_id: int,
        warehouse_id: int,
        quantity: float = 0,
        reserved_quantity: float = 0,
        available_quantity: float = 0,
        last_updated: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.product_id = product_id
        self.warehouse_id = warehouse_id
        self.quantity = quantity
        self.reserved_quantity = reserved_quantity
        self.available_quantity = available_quantity
        self.last_updated = last_updated
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "warehouse_id": self.warehouse_id,
            "quantity": self.quantity,
            "reserved_quantity": self.reserved_quantity,
            "available_quantity": self.available_quantity,
            "last_updated": self.last_updated,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def calculate_available(self):
        """Calcule la quantité disponible"""
        self.available_quantity = self.quantity - self.reserved_quantity
