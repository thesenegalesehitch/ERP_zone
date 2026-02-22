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
        name: str,
        sku: str,
        description: Optional[str] = None,
        barcode: Optional[str] = None,
        category: Optional[str] = None,
        unit_price: float = 0,
        cost_price: float = 0,
        quantity: int = 0,
        reorder_point: int = 10,
        warehouse_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.sku = sku
        self.description = description
        self.barcode = barcode
        self.category = category
        self.unit_price = unit_price
        self.cost_price = cost_price
        self.quantity = quantity
        self.reorder_point = reorder_point
        self.warehouse_id = warehouse_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "sku": self.sku,
            "description": self.description,
            "barcode": self.barcode,
            "category": self.category,
            "unit_price": self.unit_price,
            "cost_price": self.cost_price,
            "quantity": self.quantity,
            "reorder_point": self.reorder_point,
            "warehouse_id": self.warehouse_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ProductModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            name=data.get("name"),
            sku=data.get("sku"),
            description=data.get("description"),
            barcode=data.get("barcode"),
            category=data.get("category"),
            unit_price=data.get("unit_price", 0),
            cost_price=data.get("cost_price", 0),
            quantity=data.get("quantity", 0),
            reorder_point=data.get("reorder_point", 10),
            warehouse_id=data.get("warehouse_id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_low_stock(self) -> bool:
        """Vérifie si le stock est bas"""
        return self.quantity <= self.reorder_point
    
    def is_out_of_stock(self) -> bool:
        """Vérifie si le produit est en rupture de stock"""
        return self.quantity == 0
    
    def stock_value(self) -> float:
        """Calcule la valeur du stock"""
        return self.quantity * self.cost_price


class StockMovementModel:
    """Modèle de mouvement de stock"""
    
    def __init__(
        self,
        id: int,
        product_id: int,
        movement_type: str,
        quantity: int,
        previous_quantity: int,
        new_quantity: int,
        reason: Optional[str] = None,
        reference: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.product_id = product_id
        self.movement_type = movement_type
        self.quantity = quantity
        self.previous_quantity = previous_quantity
        self.new_quantity = new_quantity
        self.reason = reason
        self.reference = reference
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "movement_type": self.movement_type,
            "quantity": self.quantity,
            "previous_quantity": self.previous_quantity,
            "new_quantity": self.new_quantity,
            "reason": self.reason,
            "reference": self.reference,
            "created_at": self.created_at
        }


class WarehouseModel:
    """Modèle d'entrepôt"""
    
    def __init__(
        self,
        id: int,
        name: str,
        address: Optional[str] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.address = address
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "is_active": self.is_active,
            "created_at": self.created_at
        }
