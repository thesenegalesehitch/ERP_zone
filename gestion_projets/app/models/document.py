"""
Modèle de données pour les documents de projet

Ce module définit le modèle de données pour les documents
dans le module de gestion de projets.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class DocumentModel:
    """Modèle de document"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        name: str,
        document_type: str = "general",
        file_path: Optional[str] = None,
        file_url: Optional[str] = None,
        file_size: Optional[int] = None,
        mime_type: Optional[str] = None,
        description: Optional[str] = None,
        version: str = "1.0",
        status: str = "actif",
        is_latest: bool = True,
        uploaded_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.name = name
        self.document_type = document_type
        self.file_path = file_path
        self.file_url = file_url
        self.file_size = file_size
        self.mime_type = mime_type
        self.description = description
        self.version = version
        self.status = status
        self.is_latest = is_latest
        self.uploaded_by = uploaded_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "document_type": self.document_type,
            "file_path": self.file_path,
            "file_url": self.file_url,
            "file_size": self.file_size,
            "mime_type": self.mime_type,
            "description": self.description,
            "version": self.version,
            "status": self.status,
            "is_latest": self.is_latest,
            "uploaded_by": self.uploaded_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "DocumentModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            project_id=data.get("project_id"),
            name=data.get("name"),
            document_type=data.get("document_type", "general"),
            file_path=data.get("file_path"),
            file_url=data.get("file_url"),
            file_size=data.get("file_size"),
            mime_type=data.get("mime_type"),
            description=data.get("description"),
            version=data.get("version", "1.0"),
            status=data.get("status", "actif"),
            is_latest=data.get("is_latest", True),
            uploaded_by=data.get("uploaded_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_active(self) -> bool:
        """Vérifie si actif"""
        return self.status == "actif"
    
    def file_size_mb(self) -> float:
        """Taille du fichier en MB"""
        if not self.file_size:
            return 0
        return self.file_size / (1024 * 1024)


class DocumentVersionModel:
    """Modèle de version de document"""
    
    def __init__(
        self,
        id: int,
        document_id: int,
        version: str,
        file_path: Optional[str] = None,
        file_url: Optional[str] = None,
        file_size: Optional[int] = None,
        changes: Optional[str] = None,
        uploaded_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.document_id = document_id
        self.version = version
        self.file_path = file_path
        self.file_url = file_url
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
            "file_url": self.file_url,
            "file_size": self.file_size,
            "changes": self.changes,
            "uploaded_by": self.uploaded_by,
            "created_at": self.created_at
        }


class DocumentShareModel:
    """Modèle de partage de document"""
    
    def __init__(
        self,
        id: int,
        document_id: int,
        shared_with: int,
        permission: str = "lecture",
        shared_by: int = None,
        shared_at: Optional[datetime] = None,
        expires_at: Optional[date] = None,
        is_active: bool = True
    ):
        self.id = id
        self.document_id = document_id
        self.shared_with = shared_with
        self.permission = permission
        self.shared_by = shared_by
        self.shared_at = shared_at or datetime.now()
        self.expires_at = expires_at
        self.is_active = is_active
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "document_id": self.document_id,
            "shared_with": self.shared_with,
            "permission": self.permission,
            "shared_by": self.shared_by,
            "shared_at": self.shared_at,
            "expires_at": self.expires_at,
            "is_active": self.is_active
        }
    
    def is_expired(self) -> bool:
        """Vérifie si expiré"""
        if not self.expires_at:
            return False
        return date.today() > self.expires_at
