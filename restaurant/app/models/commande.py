"""
Modèle de données pour les commandes restaurant

Ce module définit le modèle de données pour les commandes
dans le module restaurant.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class RestaurantOrderModel:
    """Modèle de commande restaurant"""
    
    def __init__(
        self,
        id: int,
        order_number: str,
        table_number: Optional[int] = None,
        order_type: str = "sur_place",
        status: str = "nouvelle",
        customer_name: Optional[str] = None,
        customer_count: int = 1,
        subtotal: float = 0,
        tax_amount: float = 0,
        discount_amount: float = 0,
        total_amount: float = 0,
        payment_method: Optional[str] = None,
        payment_status: str = "non_paye",
        notes: Optional[str] = None,
        waiter_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.order_number = order_number
        self.table_number = table_number
        self.order_type = order_type
        self.status = status
        self.customer_name = customer_name
        self.customer_count = customer_count
        self.subtotal = subtotal
        self.tax_amount = tax_amount
        self.discount_amount = discount_amount
        self.total_amount = total_amount
        self.payment_method = payment_method
        self.payment_status = payment_status
        self.notes = notes
        self.waiter_id = waiter_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "order_number": self.order_number,
            "table_number": self.table_number,
            "order_type": self.order_type,
            "status": self.status,
            "customer_name": self.customer_name,
            "customer_count": self.customer_count,
            "subtotal": self.subtotal,
            "tax_amount": self.tax_amount,
            "discount_amount": self.discount_amount,
            "total_amount": self.total_amount,
            "payment_method": self.payment_method,
            "payment_status": self.payment_status,
            "notes": self.notes,
            "waiter_id": self.waiter_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "RestaurantOrderModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            order_number=data.get("order_number"),
            table_number=data.get("table_number"),
            order_type=data.get("order_type", "sur_place"),
            status=data.get("status", "nouvelle"),
            customer_name=data.get("customer_name"),
            customer_count=data.get("customer_count", 1),
            subtotal=data.get("subtotal", 0),
            tax_amount=data.get("tax_amount", 0),
            discount_amount=data.get("discount_amount", 0),
            total_amount=data.get("total_amount", 0),
            payment_method=data.get("payment_method"),
            payment_status=data.get("payment_status", "non_paye"),
            notes=data.get("notes"),
            waiter_id=data.get("waiter_id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def calculate_total(self) -> float:
        """Calcule le montant total"""
        return self.subtotal + self.tax_amount - self.discount_amount
    
    def is_paid(self) -> bool:
        """Vérifie si la commande est payée"""
        return self.payment_status == "paye"
    
    def is_completed(self) -> bool:
        """Vérifie si la commande est terminée"""
        return self.status == "terminee"


class MenuItemModel:
    """Modèle d'article du menu"""
    
    def __init__(
        self,
        id: int,
        name: str,
        description: Optional[str] = None,
        category: str = "plat",
        price: float,
        cost_price: float = 0,
        preparation_time: int = 15,
        is_available: bool = True,
        is_vegetarian: bool = False,
        allergens: Optional[str] = None,
        image_url: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.price = price
        self.cost_price = cost_price
        self.preparation_time = preparation_time
        self.is_available = is_available
        self.is_vegetarian = is_vegetarian
        self.allergens = allergens
        self.image_url = image_url
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "cost_price": self.cost_price,
            "preparation_time": self.preparation_time,
            "is_available": self.is_available,
            "is_vegetarian": self.is_vegetarian,
            "allergens": self.allergens,
            "image_url": self.image_url,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def profit_margin(self) -> float:
        """Calcule la marge bénéficiaire"""
        if self.price == 0:
            return 0
        return ((self.price - self.cost_price) / self.price) * 100


class OrderItemModel:
    """Modèle d'article de commande"""
    
    def __init__(
        self,
        id: int,
        order_id: int,
        menu_item_id: int,
        quantity: int,
        unit_price: float,
        status: str = "en_attente",
        notes: Optional[str] = None,
        served_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.order_id = order_id
        self.menu_item_id = menu_item_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.status = status
        self.notes = notes
        self.served_at = served_at
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "order_id": self.order_id,
            "menu_item_id": self.menu_item_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "status": self.status,
            "notes": self.notes,
            "served_at": self.served_at,
            "created_at": self.created_at
        }
    
    def calculate_total(self) -> float:
        """Calcule le total de l'article"""
        return self.quantity * self.unit_price
    
    def is_served(self) -> bool:
        """Vérifie si l'article est servi"""
        return self.status == "servi"


class TableModel:
    """Modèle de table"""
    
    def __init__(
        self,
        id: int,
        table_number: int,
        capacity: int = 4,
        status: str = "libre",
        section: Optional[str] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.table_number = table_number
        self.capacity = capacity
        self.status = status
        self.section = section
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "table_number": self.table_number,
            "capacity": self.capacity,
            "status": self.status,
            "section": self.section,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def is_available(self) -> bool:
        """Vérifie si la table est disponible"""
        return self.status == "libre"
