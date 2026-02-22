"""
Modèle de données pour les transactions de vente

Ce module définit le modèle de données pour les transactions
dans le module de point de vente.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class SaleTransactionModel:
    """Modèle de transaction de vente"""
    
    def __init__(
        self,
        id: int,
        transaction_number: str,
        customer_id: Optional[int] = None,
        cashier_id: int = None,
        pos terminal_id: Optional[int] = None,
        subtotal: float = 0,
        tax_amount: float = 0,
        discount_amount: float = 0,
        total_amount: float = 0,
        amount_paid: float = 0,
        change_given: float = 0,
        payment_method: str = "especes",
        currency: str = "XOF",
        status: str = "en_cours",
        transaction_date: Optional[datetime] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.transaction_number = transaction_number
        self.customer_id = customer_id
        self.cashier_id = cashier_id
        self.terminal_id = terminal_id
        self.subtotal = subtotal
        self.tax_amount = tax_amount
        self.discount_amount = discount_amount
        self.total_amount = total_amount
        self.amount_paid = amount_paid
        self.change_given = change_given
        self.payment_method = payment_method
        self.currency = currency
        self.status = status
        self.transaction_date = transaction_date
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "transaction_number": self.transaction_number,
            "customer_id": self.customer_id,
            "cashier_id": self.cashier_id,
            "terminal_id": self.terminal_id,
            "subtotal": self.subtotal,
            "tax_amount": self.tax_amount,
            "discount_amount": self.discount_amount,
            "total_amount": self.total_amount,
            "amount_paid": self.amount_paid,
            "change_given": self.change_given,
            "payment_method": self.payment_method,
            "currency": self.currency,
            "status": self.status,
            "transaction_date": self.transaction_date,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "SaleTransactionModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            transaction_number=data.get("transaction_number"),
            customer_id=data.get("customer_id"),
            cashier_id=data.get("cashier_id"),
            terminal_id=data.get("terminal_id"),
            subtotal=data.get("subtotal", 0),
            tax_amount=data.get("tax_amount", 0),
            discount_amount=data.get("discount_amount", 0),
            total_amount=data.get("total_amount", 0),
            amount_paid=data.get("amount_paid", 0),
            change_given=data.get("change_given", 0),
            payment_method=data.get("payment_method", "especes"),
            currency=data.get("currency", "XOF"),
            status=data.get("status", "en_cours"),
            transaction_date=data.get("transaction_date"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def calculate_total(self):
        """Calcule le montant total"""
        self.total_amount = self.subtotal + self.tax_amount - self.discount_amount
    
    def calculate_change(self):
        """Calcule la monnaie"""
        if self.amount_paid >= self.total_amount:
            self.change_given = self.amount_paid - self.total_amount
    
    def is_paid(self) -> bool:
        """Vérifie si payé"""
        return self.amount_paid >= self.total_amount
    
    def is_completed(self) -> bool:
        """Vérifie si terminé"""
        return self.status == "termine"


class SaleLineModel:
    """Modèle de ligne de vente"""
    
    def __init__(
        self,
        id: int,
        transaction_id: int,
        product_id: int,
        quantity: float = 1,
        unit_price: float = 0,
        tax_rate: float = 0,
        discount_rate: float = 0,
        line_total: float = 0,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.transaction_id = transaction_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.tax_rate = tax_rate
        self.discount_rate = discount_rate
        self.line_total = line_total
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "transaction_id": self.transaction_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "tax_rate": self.tax_rate,
            "discount_rate": self.discount_rate,
            "line_total": self.line_total,
            "created_at": self.created_at
        }
    
    def calculate_line_total(self):
        """Calcule le total de la ligne"""
        subtotal = self.quantity * self.unit_price
        discount = subtotal * (self.discount_rate / 100)
        self.line_total = subtotal - discount


class ShiftModel:
    """Modèle de shift de vente"""
    
    def __init__(
        self,
        id: int,
        user_id: int,
        terminal_id: int,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        opening_cash: float = 0,
        closing_cash: float = 0,
        total_sales: float = 0,
        total_transactions: int = 0,
        expected_cash: float = 0,
        cash_difference: float = 0,
        status: str = "en_cours",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
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
        self.expected_cash = expected_cash
        self.cash_difference = cash_difference
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
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
            "expected_cash": self.expected_cash,
            "cash_difference": self.cash_difference,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def calculate_cash_difference(self):
        """Calcule la différence de caisse"""
        self.cash_difference = self.closing_cash - self.expected_cash
    
    def is_balanced(self) -> bool:
        """Vérifie si la caisse est équilibrée"""
        return self.cash_difference == 0
    
    def is_closed(self) -> bool:
        """Vérifie si le shift est fermé"""
        return self.status == "ferme"
