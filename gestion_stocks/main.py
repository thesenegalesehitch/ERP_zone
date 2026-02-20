from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.products import router as products_router
from app.api.routes.categories import router as categories_router
from app.api.routes.suppliers import router as suppliers_router
from app.api.routes.stock import router as stock_router
from app.api.routes.auth import router as auth_router
from app.core.config import settings
from app.core.database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="""## Module Gestion des Stocks

API de gestion des stocks et inventaires pour ERP Zone.

### Fonctionnalités

* **Produits**: Gestion du catalogue produits
* **Catégories**: Organisation par catégorie
* **Fournisseurs**: Gestion des fournisseurs
* **Stocks**: Suivi des niveaux de stock
* **Mouvements**: Historique des mouvements de stock

### Authentification

L'API utilise JWT pour l'authentification.
Utilisez le endpoint `/auth/token` pour obtenir un token.
"""
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(products_router, prefix="/api/v1")
app.include_router(categories_router, prefix="/api/v1")
app.include_router(suppliers_router, prefix="/api/v1")
app.include_router(stock_router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "Welcome to ERP Zone Inventory Module API",
        "version": settings.PROJECT_VERSION,
        "documentation": "/docs"
    }
