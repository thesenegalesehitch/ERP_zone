from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.products import router as products_router
from app.api.routes.categories import router as categories_router
from app.api.routes.suppliers import router as suppliers_router
from app.api.routes.stock import router as stock_router
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
