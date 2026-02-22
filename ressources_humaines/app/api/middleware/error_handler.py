"""
Middleware pour la gestion des erreurs

Ce middleware intercepte les erreurs et retourne des réponses
standardisées au format JSON.
"""
import logging
import traceback
from datetime import datetime
from typing import Union

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError


logger = logging.getLogger("ressources_humaines.middleware")


class ErrorHandlerMiddleware:
    """
    Middleware de gestion des erreurs pour FastAPI.
    
    Intercepte les exceptions et les convertit en réponses JSON cohérentes.
    """
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        # Passer la requête au prochain middleware
        response = await self.app(scope, receive, send)
        return response


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Gestionnaire pour les erreurs de validation des requêtes.
    
    Retourne une erreur 422 avec les détails de validation.
    """
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(f"Validation error: {errors}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "Erreur de validation",
            "details": errors,
            "timestamp": datetime.now().isoformat()
        }
    )


async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    Gestionnaire pour les erreurs de base de données.
    
    Retourne une erreur 500 avec un message générique.
    """
    logger.error(f"Database error: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Erreur de base de données",
            "message": "Une erreur est survenue lors de l'accès aux données",
            "timestamp": datetime.now().isoformat()
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Gestionnaire générique pour toutes les autres exceptions.
    
    Retourne une erreur 500 avec les détails (en mode debug).
    """
    logger.error(
        f"Unhandled exception: {str(exc)}",
        exc_info=True
    )
    
    # En production, ne pas exposer les détails de l'erreur
    content = {
        "success": False,
        "error": "Erreur interne du serveur",
        "timestamp": datetime.now().isoformat()
    }
    
    # En mode debug, inclure les détails
    if logger.isEnabledFor(logging.DEBUG):
        content["details"] = str(exc)
        content["traceback"] = traceback.format_exc()
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=content
    )


class APIException(Exception):
    """
    Exception personnalisée pour les erreurs API.
    
    Permet de définir des erreurs spécifiques avec codes et messages personnalisés.
    """
    
    def __init__(
        self,
        status_code: int,
        message: str,
        error_code: str = None,
        details: dict = None
    ):
        self.status_code = status_code
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_json(self):
        """Convertit l'exception en réponse JSON"""
        return {
            "success": False,
            "error": self.message,
            "error_code": self.error_code,
            "details": self.details,
            "timestamp": datetime.now().isoformat()
        }


class NotFoundException(APIException):
    """Exception pour les ressources non trouvées"""
    
    def __init__(self, resource: str, resource_id: Union[int, str]):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=f"{resource} avec l'ID {resource_id} non trouvé",
            error_code="RESOURCE_NOT_FOUND",
            details={"resource": resource, "id": resource_id}
        )


class ConflictException(APIException):
    """Exception pour les conflits de données"""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=message,
            error_code="CONFLICT",
            details=details
        )


class UnauthorizedException(APIException):
    """Exception pour les erreurs d'authentification"""
    
    def __init__(self, message: str = "Non autorisé"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            error_code="UNAUTHORIZED"
        )


class ForbiddenException(APIException):
    """Exception pour les erreurs d'autorisation"""
    
    def __init__(self, message: str = "Accès refusé"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            error_code="FORBIDDEN"
        )


class ValidationException(APIException):
    """Exception pour les erreurs de validation métier"""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            error_code="VALIDATION_ERROR",
            details=details
        )


async def api_exception_handler(request: Request, exc: APIException):
    """Gestionnaire pour les exceptions API personnalisées"""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_json()
    )
