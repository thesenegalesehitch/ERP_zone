"""
Modèle de données pour les catégories

Ce module définit le modèle de données pour les catégories
dans le module librairie.

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
        slug: str,
        description: Optional[str] = None,
        parent_id: Optional[int] = None,
        display_order: int = 0,
        is_active: bool = True,
        book_count: int = 0,
        image_url: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.slug = slug
        self.description = description
        self.parent_id = parent_id
        self.display_order = display_order
        self.is_active = is_active
        self.book_count = book_count
        self.image_url = image_url
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "parent_id": self.parent_id,
            "display_order": self.display_order,
            "is_active": self.is_active,
            "book_count": self.book_count,
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
            slug=data.get("slug"),
            description=data.get("description"),
            parent_id=data.get("parent_id"),
            display_order=data.get("display_order", 0),
            is_active=data.get("is_active", True),
            book_count=data.get("book_count", 0),
            image_url=data.get("image_url"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_active(self) -> bool:
        """Vérifie si la catégorie est active"""
        return self.is_active
    
    def has_parent(self) -> bool:
        """Vérifie si la catégorie a un parent"""
        return self.parent_id is not None


class PublisherModel:
    """Modèle d'éditeur"""
    
    def __init__(
        self,
        id: int,
        name: str,
        slug: str,
        description: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        country: str = "Sénégal",
        phone: Optional[str] = None,
        email: Optional[str] = None,
        website: Optional[str] = None,
        logo_url: Optional[str] = None,
        book_count: int = 0,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.slug = slug
        self.description = description
        self.address = address
        self.city = city
        self.country = country
        self.phone = phone
        self.email = email
        self.website = website
        self.logo_url = logo_url
        self.book_count = book_count
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "phone": self.phone,
            "email": self.email,
            "website": self.website,
            "logo_url": self.logo_url,
            "book_count": self.book_count,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class AuthorModel:
    """Modèle d'auteur"""
    
    def __init__(
        self,
        id: int,
        first_name: str,
        last_name: str,
        slug: str,
        biography: Optional[str] = None,
        birth_date: Optional[datetime] = None,
        death_date: Optional[datetime] = None,
        country: Optional[str] = None,
        photo_url: Optional[str] = None,
        book_count: int = 0,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.slug = slug
        self.biography = biography
        self.birth_date = birth_date
        self.death_date = death_date
        self.country = country
        self.photo_url = photo_url
        self.book_count = book_count
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "slug": self.slug,
            "biography": self.biography,
            "birth_date": self.birth_date,
            "death_date": self.death_date,
            "country": self.country,
            "photo_url": self.photo_url,
            "book_count": self.book_count,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def get_full_name(self) -> str:
        """Retourne le nom complet"""
        return f"{self.first_name} {self.last_name}"


class ReviewModel:
    """Modèle d'avis"""
    
    def __init__(
        self,
        id: int,
        book_id: int,
        member_id: int,
        rating: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        is_approved: bool = False,
        helpful_count: int = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.book_id = book_id
        self.member_id = member_id
        self.rating = rating
        self.title = title
        self.content = content
        self.is_approved = is_approved
        self.helpful_count = helpful_count
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "book_id": self.book_id,
            "member_id": self.member_id,
            "rating": self.rating,
            "title": self.title,
            "content": self.content,
            "is_approved": self.is_approved,
            "helpful_count": self.helpful_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_valid_rating(self) -> bool:
        """Vérifie si la note est valide"""
        return 1 <= self.rating <= 5
