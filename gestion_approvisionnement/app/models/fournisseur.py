"""
Modèle de données pour les fournisseurs

Ce module définit le modèle de données pour les fournisseurs
dans le module d'approvisionnement.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class SupplierModel:
    """Modèle de fournisseur"""
    
    def __init__(
        self,
        id: int,
        supplier_code: str,
        company_name: str,
        contact_person: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        country: str = "Sénégal",
        tax_id: Optional[str] = None,
        status: str = "actif",
        rating: float = 0,
        payment_terms: Optional[str] = None,
        delivery_terms: Optional[str] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.supplier_code = supplier_code
        self.company_name = company_name
        self.contact_person = contact_person
        self.email = email
        self.phone = phone
        self.address = address
        self.city = city
        self.country = country
        self.tax_id = tax_id
        self.status = status
        self.rating = rating
        self.payment_terms = payment_terms
        self.delivery_terms = delivery_terms
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "supplier_code": self.supplier_code,
            "company_name": self.company_name,
            "contact_person": self.contact_person,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "tax_id": self.tax_id,
            "status": self.status,
            "rating": self.rating,
            "payment_terms": self.payment_terms,
            "delivery_terms": self.delivery_terms,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "SupplierModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            supplier_code=data.get("supplier_code"),
            company_name=data.get("company_name"),
            contact_person=data.get("contact_person"),
            email=data.get("email"),
            phone=data.get("phone"),
            address=data.get("address"),
            city=data.get("city"),
            country=data.get("country", "Sénégal"),
            tax_id=data.get("tax_id"),
            status=data.get("status", "actif"),
            rating=data.get("rating", 0),
            payment_terms=data.get("payment_terms"),
            delivery_terms=data.get("delivery_terms"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_active(self) -> bool:
        """Vérifie si actif"""
        return self.status == "actif"
    
    def full_address(self) -> str:
        """Adresse complète"""
        parts = [self.address, self.city, self.country]
        return ", ".join([p for p in parts if p])


class SupplierContactModel:
    """Modèle de contact de fournisseur"""
    
    def __init__(
        self,
        id: int,
        supplier_id: int,
        first_name: str,
        last_name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        role: Optional[str] = None,
        is_primary: bool = False,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.supplier_id = supplier_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.role = role
        self.is_primary = is_primary
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "supplier_id": self.supplier_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "is_primary": self.is_primary,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def full_name(self) -> str:
        """Nom complet"""
        return f"{self.first_name} {self.last_name}"


class SupplierEvaluationModel:
    """Modèle d'évaluation de fournisseur"""
    
    def __init__(
        self,
        id: int,
        supplier_id: int,
        evaluation_date: datetime = None,
        quality_score: float = 0,
        delivery_score: float = 0,
        price_score: float = 0,
        service_score: float = 0,
        overall_score: float = 0,
        evaluator_id: int = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.supplier_id = supplier_id
        self.evaluation_date = evaluation_date
        self.quality_score = quality_score
        self.delivery_score = delivery_score
        self.price_score = price_score
        self.service_score = service_score
        self.overall_score = overall_score
        self.evaluator_id = evaluator_id
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "supplier_id": self.supplier_id,
            "evaluation_date": self.evaluation_date,
            "quality_score": self.quality_score,
            "delivery_score": self.delivery_score,
            "price_score": self.price_score,
            "service_score": self.service_score,
            "overall_score": self.overall_score,
            "evaluator_id": self.evaluator_id,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def calculate_overall(self):
        """Calcule le score global"""
        self.overall_score = ((self.quality_score + self.delivery_score + 
                              self.price_score + self.service_score) / 4)
