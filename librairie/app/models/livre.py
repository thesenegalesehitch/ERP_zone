"""
Modèle de données pour les livres

Ce module définit le modèle de données pour les livres
dans le module de gestion de librairie.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class BookModel:
    """Modèle de livre"""
    
    def __init__(
        self,
        id: int,
        isbn: str,
        title: str,
        author: str,
        publisher: Optional[str] = None,
        publish_year: Optional[int] = None,
        category: Optional[str] = None,
        description: Optional[str] = None,
        language: str = "français",
        pages: int = 0,
        price: float = 0,
        currency: str = "XOF",
        total_copies: int = 1,
        available_copies: int = 1,
        location: Optional[str] = None,
        cover_image: Optional[str] = None,
        status: str = "disponible",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher = publisher
        self.publish_year = publish_year
        self.category = category
        self.description = description
        self.language = language
        self.pages = pages
        self.price = price
        self.currency = currency
        self.total_copies = total_copies
        self.available_copies = available_copies
        self.location = location
        self.cover_image = cover_image
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "publish_year": self.publish_year,
            "category": self.category,
            "description": self.description,
            "language": self.language,
            "pages": self.pages,
            "price": self.price,
            "currency": self.currency,
            "total_copies": self.total_copies,
            "available_copies": self.available_copies,
            "location": self.location,
            "cover_image": self.cover_image,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "BookModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            isbn=data.get("isbn"),
            title=data.get("title"),
            author=data.get("author"),
            publisher=data.get("publisher"),
            publish_year=data.get("publish_year"),
            category=data.get("category"),
            description=data.get("description"),
            language=data.get("language", "français"),
            pages=data.get("pages", 0),
            price=data.get("price", 0),
            currency=data.get("currency", "XOF"),
            total_copies=data.get("total_copies", 1),
            available_copies=data.get("available_copies", 1),
            location=data.get("location"),
            cover_image=data.get("cover_image"),
            status=data.get("status", "disponible"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_available(self) -> bool:
        """Vérifie si disponible"""
        return self.available_copies > 0
    
    def borrowed_copies(self) -> int:
        """Nombre d'exemplaires empruntés"""
        return self.total_copies - self.available_copies


class BookCopyModel:
    """Modèle d'exemplaire de livre"""
    
    def __init__(
        self,
        id: int,
        book_id: int,
        copy_number: str,
        status: str = "disponible",
        condition: str = "neuf",
        acquisition_date: Optional[datetime] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.book_id = book_id
        self.copy_number = copy_number
        self.status = status
        self.condition = condition
        self.acquisition_date = acquisition_date
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "book_id": self.book_id,
            "copy_number": self.copy_number,
            "status": self.status,
            "condition": self.condition,
            "acquisition_date": self.acquisition_date,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def is_available(self) -> bool:
        """Vérifie si disponible"""
        return self.status == "disponible"


class AuthorModel:
    """Modèle d'auteur"""
    
    def __init__(
        self,
        id: int,
        first_name: str,
        last_name: str,
        biography: Optional[str] = None,
        country: Optional[str] = None,
        birth_year: Optional[int] = None,
        photo_url: Optional[str] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.biography = biography
        self.country = country
        self.birth_year = birth_year
        self.photo_url = photo_url
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "biography": self.biography,
            "country": self.country,
            "birth_year": self.birth_year,
            "photo_url": self.photo_url,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def full_name(self) -> str:
        """Nom complet"""
        return f"{self.first_name} {self.last_name}"
