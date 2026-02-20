"""
Schémas de validation - Authentification
========================================
Schémas Pydantic pour l'authentification JWT.
"""

from pydantic import BaseModel


class Token(BaseModel):
    """Schéma du token d'accès"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schéma des données du token"""
    username: str | None = None
