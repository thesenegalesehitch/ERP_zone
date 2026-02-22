"""
Modèle de données pour les produits

Ce module définit le modèle de données pour les produits
dans le module de point de vente.

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
        image_url: Optional[str] = None,
        is_active: bool = True,
        is_available: bool = True,
        tax_included: bool = False,
        tax_rate: float = 0,
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
        self.image_url = image_url
        self.is_active = is_active
        self.is_available = is_available
        self.tax_included = tax_included
        self.tax_rate = tax_rate
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
            "image_url": self.image_url,
            "is_active": self.is_active,
            "is_available": self.is_available,
            "tax_included": self.tax_included,
            "tax_rate": self.tax_rate,
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
            image_url=data.get("image_url"),
            is_active=data.get("is_active", True),
            is_available=data.get("is_available", True),
            tax_included=data.get("tax_included", False),
            tax_rate=data.get("tax_rate", 0),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def calculate_tax(self) -> float:
        """Calcule la taxe"""
        return self.price * (self.tax_rate / 100)
    
    def price_with_tax(self) -> float:
        """Prix avec taxe"""
        return self.price + self.calculate_tax()
    
    def profit_margin(self) -> float:
        """Marge bénéficiaire"""
        if self.price == 0:
            return 0
        return ((self.price - self.cost) / self.price) * 100
    
    def is_active_product(self) -> bool:
        """Vérifie si actif"""
        return self.is_active and self.is_available


class CategoryModel:
    """Modèle de catégorie"""
    
    def __init__(
        self,
        id: int,
        name: str,
        code: str,
        parent_id: Optional[int] = None,
        description: Optional[str] = None,
        is_active: bool = True,
        image_url: Optional[str] = None,
        sort_order: int = 0,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.code = code
        self.parent_id = parent_id
        self.description = description
        self.is_active = is_active
        self.image_url = image_url
        self.sort_order = sort_order
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
            "image_url": self.image_url,
            "sort_order": self.sort_order,
            "created_at": self.created_at
        }


class POSSessionModel:
    """Modèle de session POS"""
    
    def __init__(
        self,
        id: int,
        user_id: int,
        terminal_id: int,
        start_time: datetime = None,
        end_time: Optional[datetime] = None,
        opening_cash: float = 0,
        closing_cash: float = 0,
        total_sales: float = 0,
        total_transactions: int = 0,
        status: str = "en_cours",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.terminal_id = terminal_id
        self.start_time = start_time
        self.end_time = end_time
        self.opening_cash = opening_cash
        self.closing_cash = closing_cash
        self.total_sales = total_sales
        self.total_transactions = total_transactions
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "terminal_id": self.terminal_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "opening_cash": self.opening_cash,
            "closing_cash": self.closing_cash,
            "total_sales": self.total_sales,
            "total_transactions": self.total_transactions,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def is_closed(self) -> bool:
        """Vérifie si fermée"""
        return self.status == "ferme"
