"""
ERP Zone - Module Restaurant
===========================
Application pour la gestion de restaurant.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Module Gestion Restaurant - ERP Zone"
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
        "message": "API ERP Zone - Module Restaurant",
        "version": settings.PROJECT_VERSION
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "module": "restaurant"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8006, reload=True)
