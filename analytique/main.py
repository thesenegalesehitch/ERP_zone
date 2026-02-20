from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.reports import router as reports_router
from app.api.routes.dashboards import router as dashboards_router
from app.core.config import settings
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
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

app.include_router(reports_router, prefix="/api/v1")
app.include_router(dashboards_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Welcome to ERP Zone Analytics Module API", "version": settings.PROJECT_VERSION}
