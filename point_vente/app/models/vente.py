"""
Modèle de données pour les ventes

Ce module définit le modèle de données pour les ventes
dans le module point de vente.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class SaleModel:
    """Modèle de vente"""
    
    def __init__(
        self,
        id: int,
        sale_number: str,
        total_amount: float,
        tax_amount: float = 0,
        discount_amount: float = 0,
        payment_method: str = "especes",
        payment_status: str = "non_paye",
        customer_id: Optional[int] = None,
        cashier_id: int = None,
        status: str = "en_cours",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.sale_number = sale_number
        self.total_amount = total_amount
        self.tax_amount = tax_amount
        self.discount_amount = discount_amount
        self.payment_method = payment_method
        self.payment_status = payment_status
        self.customer_id = customer_id
        self.cashier_id = cashier_id
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "sale_number": self.sale_number,
            "total_amount": self.total_amount,
            "tax_amount": self.tax_amount,
            "discount_amount": self.discount_amount,
            "payment_method": self.payment_method,
            "payment_status": self.payment_status,
            "customer_id": self.customer_id,
            "cashier_id": self.cashier_id,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "SaleModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            sale_number=data.get("sale_number"),
            total_amount=data.get("total_amount"),
            tax_amount=data.get("tax_amount", 0),
            discount_amount=data.get("discount_amount", 0),
            payment_method=data.get("payment_method", "especes"),
            payment_status=data.get("payment_status", "non_paye"),
            customer_id=data.get("customer_id"),
            cashier_id=data.get("cashier_id"),
            status=data.get("status", "en_cours"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def calculate_total(self) -> float:
        """Calcule le montant total avec taxes et remises"""
        return self.total_amount + self.tax_amount - self.discount_amount
    
    def is_paid(self) -> bool:
        """Vérifie si la vente est payée"""
        return self.payment_status == "paye"


class SaleItemModel:
    """Modèle d'article de vente"""
    
    def __init__(
        self,
        id: int,
        sale_id: int,
        product_id: int,
        quantity: int,
        unit_price: float,
        tax_rate: float = 0,
        discount_rate: float = 0,
        total_price: float = 0,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.sale_id = sale_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.tax_rate = tax_rate
        self.discount_rate = discount_rate
        self.total_price = total_price or (quantity * unit_price)
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "sale_id": self.sale_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "tax_rate": self.tax_rate,
            "discount_rate": self.discount_rate,
            "total_price": self.total_price,
            "created_at": self.created_at
        }
    
    def calculate_total(self) -> float:
        """Calcule le prix total avec remise"""
        subtotal = self.quantity * self.unit_price
        discount = subtotal * (self.discount_rate / 100)
        return subtotal - discount


class CashRegisterModel:
    """Modèle de caisse"""
    
    def __init__(
        self,
        id: int,
        name: str,
        initial_amount: float = 0,
        current_amount: float = 0,
        status: str = "ferme",
        opened_at: Optional[datetime] = None,
        closed_at: Optional[datetime] = None,
        opened_by: int = None,
        closed_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.initial_amount = initial_amount
        self.current_amount = current_amount
        self.status = status
        self.opened_at = opened_at
        self.closed_at = closed_at
        self.opened_by = opened_by
        self.closed_by = closed_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "initial_amount": self.initial_amount,
            "current_amount": self.current_amount,
            "status": self.status,
            "opened_at": self.opened_at,
            "closed_at": self.closed_at,
            "opened_by": self.opened_by,
            "closed_by": self.closed_by,
            "created_at": self.created_at
        }
    
    def is_open(self) -> bool:
        """Vérifie si la caisse est ouverte"""
        return self.status == "ouvert"
    
    def add_amount(self, amount: float):
        """Ajoute un montant à la caisse"""
        if self.is_open():
            self.current_amount += amount
    
    def remove_amount(self, amount: float):
        """Retire un montant de la caisse"""
        if self.is_open():
            self.current_amount -= amount


class ReceiptModel:
    """Modèle de reçu"""
    
    def __init__(
        self,
        id: int,
        sale_id: int,
        receipt_number: str,
        total_amount: float,
        amount_paid: float,
        change_amount: float = 0,
        payment_method: str = "especes",
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.sale_id = sale_id
        self.receipt_number = receipt_number
        self.total_amount = total_amount
        self.amount_paid = amount_paid
        self.change_amount = change_amount or (amount_paid - total_amount)
        self.payment_method = payment_method
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "sale_id": self.sale_id,
            "receipt_number": self.receipt_number,
            "total_amount": self.total_amount,
            "amount_paid": self.amount_paid,
            "change_amount": self.change_amount,
            "payment_method": self.payment_method,
            "created_at": self.created_at
        }
