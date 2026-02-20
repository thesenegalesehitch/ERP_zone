"""
ERP Zone - Module Librairie
===========================
Application principale FastAPI pour la gestion d'une librairie.

Fonctionnalités:
- Gestion du catalogue de livres
- Gestion des clients et fidélisation
- Gestion des ventes
- Système d'authentification JWT
- Gestion des rôles et permissions (RBAC)

Démarrage:
    uvicorn main:app --reload --port 8003
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import auth, livres

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="""
    ## Module Librairie
    
    API de gestion pour une librairie avec les fonctionnalités suivantes:
    
    * **Livres**: Gestion du catalogue (CRUD complet)
    * **Catégories**: Organisation des livres par genre
    * **Auteurs**: Gestion des auteurs
    * **Clients**: Gestion de la clientèle et fidélité
    * **Ventes**: Suivi des ventes
    
    ## Authentification
    
    L'API utilise JWT (JSON Web Tokens) pour l'authentification.
    Utilisez le endpoint `/auth/token` pour obtenir un token.
    """,
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(auth.router)
app.include_router(livres.router)


@app.get("/")
def root():
    """
    Page d'accueil
    ==============
    Retourne les informations de base de l'API.
    """
    return {
        "message": "API ERP Zone - Module Librairie",
        "version": settings.PROJECT_VERSION,
        "documentation": "/docs"
    }


@app.get("/health")
def health_check():
    """
    Vérification de santé
    =====================
    Endpoint pour vérifier que l'API est opérationnelle.
    """
    return {"status": "healthy", "module": "librairie"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True)
