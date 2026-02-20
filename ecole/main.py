"""
ERP Zone - Module Ecole
=====================
Application pour la gestion scolaire.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Module Gestion Scolaire - ERP Zone"
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
        "message": "API ERP Zone - Module Ecole",
        "version": settings.PROJECT_VERSION
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "module": "ecole"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8005, reload=True)
