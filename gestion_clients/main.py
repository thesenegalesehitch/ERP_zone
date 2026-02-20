from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.customers import router as customers_router
from app.api.routes.leads import router as leads_router
from app.api.routes.opportunities import router as opportunities_router
from app.core.config import settings
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.DESCRIPTION,
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

app.include_router(customers_router, prefix="/api/v1")
app.include_router(leads_router, prefix="/api/v1")
app.include_router(opportunities_router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "Welcome to ERP Zone CRM Module API",
        "version": settings.PROJECT_VERSION,
        "documentation": "/docs"
    }
