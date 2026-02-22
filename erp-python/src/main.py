"""
ERP Library - Python FastAPI Application
Main application entry point.

Author: Alexandre Albert Ndour
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .api.controllers import auth_controller, user_controller
from .api.middleware.logging import LoggingMiddleware
from .api.middleware.error_handler import ErrorHandlerMiddleware
from .infrastructure.database.connection import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    app = FastAPI(
        title="ERP Library API",
        description="Multi-language ERP Library - Python Implementation",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Custom middleware
    app.add_middleware(ErrorHandlerMiddleware)
    app.add_middleware(LoggingMiddleware)
    
    # Include routers
    app.include_router(auth_controller.router, prefix="/api/v1")
    app.include_router(user_controller.router, prefix="/api/v1")
    
    # Health check
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "service": "erp-library",
            "language": "python"
        }
    
    @app.get("/")
    async def root():
        return {
            "message": "ERP Library API",
            "version": "1.0.0",
            "documentation": "/docs"
        }
    
    return app


# Application instance
app = create_app()


# Run with: uvicorn erp_python.src.main:app --reload
