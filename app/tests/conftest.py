import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from app.core.database import Base, get_db
from app.core.security import get_password_hash
from app.models.role import Role
from app.models.user import User


# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db_session():
    # Create tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Create default role for testing
    default_role = Role(name="user", description="Default user role")
    db.add(default_role)
    db.commit()
    
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def authenticated_client(client: TestClient, db_session):
    """Create an authenticated test client with a valid token"""
    # Create a test user
    from app.core.security import create_access_token
    from datetime import timedelta
    
    # Create default role
    role = Role(name="admin", description="Admin role")
    db_session.add(role)
    db_session.commit()
    db_session.refresh(role)
    
    # Create test user
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword123"),
        role_id=role.id,
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    # Generate token
    access_token = create_access_token(
        data={"sub": user.email, "role": role.name},
        expires_delta=timedelta(minutes=30)
    )
    
    # Add Authorization header to client
    client.headers["Authorization"] = f"Bearer {access_token}"
    return client