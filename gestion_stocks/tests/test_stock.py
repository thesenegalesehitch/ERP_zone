"""
Tests unitaires pour le module Gestion de Stocks
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import date

from main import app
from app.core.database import Base, get_db
from app.models.product import Product
from app.models.category import Category
from app.models.stock import Stock


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


class TestCategory:
    """Tests pour le modèle Category"""
    
    def test_create_category(self, db_session):
        category = Category(
            name="Electronique",
            description="Produits électroniques"
        )
        db_session.add(category)
        db_session.commit()
        
        assert category.id is not None
        assert category.name == "Electronique"
    
    def test_category_default_values(self, db_session):
        category = Category(name="Test")
        db_session.add(category)
        db_session.commit()
        
        assert category.is_active is True


class TestProduct:
    """Tests pour le modèle Product"""
    
    def test_create_product(self, db_session):
        category = Category(name="Test")
        db_session.add(category)
        db_session.commit()
        
        product = Product(
            name="Ordinateur",
            price=500.0,
            category_id=category.id
        )
        db_session.add(product)
        db_session.commit()
        
        assert product.id is not None
        assert product.name == "Ordinateur"
        assert product.price == 500.0
    
    def test_product_with_stock(self, db_session):
        category = Category(name="Test")
        db_session.add(category)
        db_session.commit()
        
        product = Product(
            name="Souris",
            price=25.0,
            category_id=category.id
        )
        db_session.add(product)
        db_session.commit()
        
        stock = Stock(
            product_id=product.id,
            quantity=100,
            min_stock_level=10
        )
        db_session.add(stock)
        db_session.commit()
        
        assert stock.quantity == 100
        assert stock.product.name == "Souris"


class TestStock:
    """Tests pour la gestion du stock"""
    
    def test_low_stock_alert(self, db_session):
        category = Category(name="Test")
        db_session.add(category)
        db_session.commit()
        
        product = Product(
            name="Produit",
            price=10.0,
            category_id=category.id
        )
        db_session.add(product)
        db_session.commit()
        
        stock = Stock(
            product_id=product.id,
            quantity=5,
            min_stock_level=10
        )
        db_session.add(stock)
        db_session.commit()
        
        # Le stock est en dessous du minimum
        assert stock.quantity < stock.min_stock_level


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
