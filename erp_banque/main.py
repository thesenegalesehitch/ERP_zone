"""
ERP Zone - Module Banque
=======================
Application principale pour la gestion bancaire.

Fonctionnalités:
- Gestion des clients bancaires
- Gestion des comptes (courant, épargne)
- Transactions (débit, crédit, virement)
- Authentification JWT
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Module Gestion Bancaire - ERP Zone"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "API ERP Zone - Module Banque",
        "version": settings.PROJECT_VERSION
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "module": "banque"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8004, reload=True)
