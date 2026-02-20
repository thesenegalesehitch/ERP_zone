from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.auth import router as auth_router
from app.api.routes.roles import router as roles_router
from app.api.routes.employees import router as employees_router
from app.api.routes.departments import router as departments_router
from app.api.routes.leave_requests import router as leave_requests_router
from app.core.config import settings
from app.core.database import Base, engine, SessionLocal
from app.models.role import Role


# Create default roles
def create_default_roles():
    """Create default roles if they don't exist"""
    db = SessionLocal()
    try:
        default_roles = [
            {"name": "admin", "description": "Administrator with full access"},
            {"name": "hr_manager", "description": "HR Manager with HR access"},
            {"name": "employee", "description": "Regular employee"},
            {"name": "manager", "description": "Department manager"},
        ]
        for role_data in default_roles:
            existing_role = db.query(Role).filter(Role.name == role_data["name"]).first()
            if not existing_role:
                role = Role(**role_data)
                db.add(role)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error creating default roles: {e}")
    finally:
        db.close()


# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize default roles
create_default_roles()

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.DESCRIPTION,
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(roles_router, prefix="/api/v1")
app.include_router(employees_router, prefix="/api/v1")
app.include_router(departments_router, prefix="/api/v1")
app.include_router(leave_requests_router, prefix="/api/v1")


@app.get("/", summary="Root endpoint")
def root():
    """
    Root endpoint that returns a welcome message and API information
    """
    return {
        "message": "Welcome to ERP Zone RH Module API",
        "version": settings.PROJECT_VERSION,
        "documentation": "/docs",
        "redoc": "/redoc"
    }