"""
Modèle de données pour les cartes bancaires

Ce module définit le modèle de données pour les cartes
dans le module banque.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class CardModel:
    """Modèle de carte bancaire"""
    
    def __init__(
        self,
        id: int,
        card_number: str,
        account_id: int,
        card_type: str = "debit",
        card_brand: str = "visa",
        status: str = "active",
        expiry_date: Optional[date] = None,
        cvv: Optional[str] = None,
        pin: Optional[str] = None,
        daily_limit: float = 0,
        monthly_limit: float = 0,
        used_today: float = 0,
        used_month: float = 0,
        issued_at: Optional[datetime] = None,
        activated_at: Optional[datetime] = None,
        blocked_at: Optional[datetime] = None,
        expires_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.card_number = card_number
        self.account_id = account_id
        self.card_type = card_type
        self.card_brand = card_brand
        self.status = status
        self.expiry_date = expiry_date
        self.cvv = cvv
        self.pin = pin
        self.daily_limit = daily_limit
        self.monthly_limit = monthly_limit
        self.used_today = used_today
        self.used_month = used_month
        self.issued_at = issued_at or datetime.now()
        self.activated_at = activated_at
        self.blocked_at = blocked_at
        self.expires_at = expires_at
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "card_number": self.card_number,
            "account_id": self.account_id,
            "card_type": self.card_type,
            "card_brand": self.card_brand,
            "status": self.status,
            "expiry_date": self.expiry_date,
            "daily_limit": self.daily_limit,
            "monthly_limit": self.monthly_limit,
            "used_today": self.used_today,
            "used_month": self.used_month,
            "issued_at": self.issued_at,
            "activated_at": self.activated_at,
            "blocked_at": self.blocked_at,
            "expires_at": self.expires_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "CardModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            card_number=data.get("card_number"),
            account_id=data.get("account_id"),
            card_type=data.get("card_type", "debit"),
            card_brand=data.get("card_brand", "visa"),
            status=data.get("status", "active"),
            expiry_date=data.get("expiry_date"),
            cvv=data.get("cvv"),
            pin=data.get("pin"),
            daily_limit=data.get("daily_limit", 0),
            monthly_limit=data.get("monthly_limit", 0),
            used_today=data.get("used_today", 0),
            used_month=data.get("used_month", 0),
            issued_at=data.get("issued_at"),
            activated_at=data.get("activated_at"),
            blocked_at=data.get("blocked_at"),
            expires_at=data.get("expires_at"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_active(self) -> bool:
        """Vérifie si la carte est active"""
        return self.status == "active"
    
    def is_blocked(self) -> bool:
        """Vérifie si la carte est bloquée"""
        return self.status == "blocked"
    
    def can_use(self, amount: float) -> bool:
        """Vérifie si la carte peut être utilisée"""
        if not self.is_active():
            return False
        if self.used_today + amount > self.daily_limit:
            return False
        if self.used_month + amount > self.monthly_limit:
            return False
        return True
    
    def is_expired(self) -> bool:
        """Vérifie si la carte est expirée"""
        if not self.expiry_date:
            return False
        return date.today() > self.expiry_date


class CardTransactionModel:
    """Modèle de transaction par carte"""
    
    def __init__(
        self,
        id: int,
        card_id: int,
        transaction_type: str,
        amount: float,
        merchant_name: Optional[str] = None,
        merchant_category: Optional[str] = None,
        location: Optional[str] = None,
        reference: Optional[str] = None,
        status: str = "completed",
        response_code: Optional[str] = None,
        transaction_date: Optional[datetime] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.card_id = card_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.merchant_name = merchant_name
        self.merchant_category = merchant_category
        self.location = location
        self.reference = reference
        self.status = status
        self.response_code = response_code
        self.transaction_date = transaction_date or datetime.now()
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "card_id": self.card_id,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "merchant_name": self.merchant_name,
            "merchant_category": self.merchant_category,
            "location": self.location,
            "reference": self.reference,
            "status": self.status,
            "response_code": self.response_code,
            "transaction_date": self.transaction_date,
            "created_at": self.created_at
        }
    
    def is_successful(self) -> bool:
        """Vérifie si la transaction est réussie"""
        return self.status == "completed"


class CardLimitModel:
    """Modèle de limite de carte"""
    
    def __init__(
        self,
        id: int,
        card_id: int,
        limit_type: str,
        limit_amount: float,
        is_active: bool = True,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.card_id = card_id
        self.limit_type = limit_type
        self.limit_amount = limit_amount
        self.is_active = is_active
        self.start_date = start_date
        self.end_date = end_date
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "card_id": self.card_id,
            "limit_type": self.limit_type,
            "limit_amount": self.limit_amount,
            "is_active": self.is_active,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
