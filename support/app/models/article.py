"""
Modèle de données pour les articles

Ce module définit le modèle de données pour les articles
dans le module de support.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class ArticleModel:
    """Modèle d'article"""
    
    def __init__(
        self,
        id: int,
        title: str,
        slug: str,
        content: str,
        category: str,
        tags: Optional[str] = None,
        author_id: int = None,
        status: str = "brouillon",
        view_count: int = 0,
        helpful_count: int = 0,
        not_helpful_count: int = 0,
        is_featured: bool = False,
        published_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.title = title
        self.slug = slug
        self.content = content
        self.category = category
        self.tags = tags
        self.author_id = author_id
        self.status = status
        self.view_count = view_count
        self.helpful_count = helpful_count
        self.not_helpful_count = not_helpful_count
        self.is_featured = is_featured
        self.published_at = published_at
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "content": self.content,
            "category": self.category,
            "tags": self.tags,
            "author_id": self.author_id,
            "status": self.status,
            "view_count": self.view_count,
            "helpful_count": self.helpful_count,
            "not_helpful_count": self.not_helpful_count,
            "is_featured": self.is_featured,
            "published_at": self.published_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ArticleModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            title=data.get("title"),
            slug=data.get("slug"),
            content=data.get("content"),
            category=data.get("category"),
            tags=data.get("tags"),
            author_id=data.get("author_id"),
            status=data.get("status", "brouillon"),
            view_count=data.get("view_count", 0),
            helpful_count=data.get("helpful_count", 0),
            not_helpful_count=data.get("not_helpful_count", 0),
            is_featured=data.get("is_featured", False),
            published_at=data.get("published_at"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_published(self) -> bool:
        """Vérifie si l'article est publié"""
        return self.status == "publie"
    
    def helpfulness_ratio(self) -> float:
        """Calcule le ratio d'utilité"""
        total = self.helpful_count + self.not_helpful_count
        if total == 0:
            return 0
        return (self.helpful_count / total) * 100
    
    def increment_views(self):
        """Incrémenter les vues"""
        self.view_count += 1
    
    def mark_helpful(self):
        """Marquer comme utile"""
        self.helpful_count += 1
    
    def mark_not_helpful(self):
        """Marquer comme non utile"""
        self.not_helpful_count += 1


class CategoryModel:
    """Modèle de catégorie"""
    
    def __init__(
        self,
        id: int,
        name: str,
        slug: str,
        description: Optional[str] = None,
        parent_id: Optional[int] = None,
        article_count: int = 0,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.slug = slug
        self.description = description
        self.parent_id = parent_id
        self.article_count = article_count
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
            "parent_id": self.parent_id,
            "article_count": self.article_count,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class CommentModel:
    """Modèle de commentaire"""
    
    def __init__(
        self,
        id: int,
        article_id: int,
        user_id: int,
        content: str,
        parent_id: Optional[int] = None,
        status: str = "approuve",
        helpful_count: int = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.article_id = article_id
        self.user_id = user_id
        self.content = content
        self.parent_id = parent_id
        self.status = status
        self.helpful_count = helpful_count
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "article_id": self.article_id,
            "user_id": self.user_id,
            "content": self.content,
            "parent_id": self.parent_id,
            "status": self.status,
            "helpful_count": self.helpful_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_approved(self) -> bool:
        """Vérifie si le commentaire est approuvé"""
        return self.status == "approuve"
