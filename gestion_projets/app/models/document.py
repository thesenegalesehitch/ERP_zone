"""
Modèle de données pour les documents

Ce module définit le modèle de données pour les documents
dans le module de gestion de projets.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class DocumentModel:
    """Modèle de document"""
    
    def __init__(
        self,
        id: int,
        name: str,
        project_id: Optional[int] = None,
        document_type: str = "general",
        file_path: Optional[str] = None,
        file_size: int = 0,
        mime_type: Optional[str] = None,
        description: Optional[str] = None,
        version: str = "1.0",
        status: str = "actif",
        uploaded_by: int = None,
        approved_by: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.project_id = project_id
        self.document_type = document_type
        self.file_path = file_path
        self.file_size = file_size
        self.mime_type = mime_type
        self.description = description
        self.version = version
        self.status = status
        self.uploaded_by = uploaded_by
        self.approved_by = approved_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "project_id": self.project_id,
            "document_type": self.document_type,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "mime_type": self.mime_type,
            "description": self.description,
            "version": self.version,
            "status": self.status,
            "uploaded_by": self.uploaded_by,
            "approved_by": self.approved_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "DocumentModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            name=data.get("name"),
            project_id=data.get("project_id"),
            document_type=data.get("document_type", "general"),
            file_path=data.get("file_path"),
            file_size=data.get("file_size", 0),
            mime_type=data.get("mime_type"),
            description=data.get("description"),
            version=data.get("version", "1.0"),
            status=data.get("status", "actif"),
            uploaded_by=data.get("uploaded_by"),
            approved_by=data.get("approved_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def file_size_mb(self) -> float:
        """Taille du fichier en MB"""
        return self.file_size / (1024 * 1024)
    
    def is_approved(self) -> bool:
        """Vérifie si approuvé"""
        return self.approved_by is not None


class DocumentVersionModel:
    """Modèle de version de document"""
    
    def __init__(
        self,
        id: int,
        document_id: int,
        version: str,
        file_path: Optional[str] = None,
        file_size: int = 0,
        changes: Optional[str] = None,
        uploaded_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.document_id = document_id
        self.version = version
        self.file_path = file_path
        self.file_size = file_size
        self.changes = changes
        self.uploaded_by = uploaded_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "document_id": self.document_id,
            "version": self.version,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "changes": self.changes,
            "uploaded_by": self.uploaded_by,
            "created_at": self.created_at
        }


class CommentModel:
    """Modèle de commentaire"""
    
    def __init__(
        self,
        id: int,
        document_id: int,
        user_id: int,
        content: str,
        parent_id: Optional[int] = None,
        is_internal: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.document_id = document_id
        self.user_id = user_id
        self.content = content
        self.parent_id = parent_id
        self.is_internal = is_internal
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "document_id": self.document_id,
            "user_id": self.user_id,
            "content": self.content,
            "parent_id": self.parent_id,
            "is_internal": self.is_internal,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
