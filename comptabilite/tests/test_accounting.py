"""
Tests unitaires pour le module Comptabilité
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import date

from main import app
from app.core.database import Base, get_db
from app.models.account import Account, JournalEntry


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


class TestAccount:
    """Tests pour le modèle Account"""
    
    def test_create_account(self, db_session):
        account = Account(
            code="101",
            name="Capital",
            account_type="passif"
        )
        db_session.add(account)
        db_session.commit()
        
        assert account.id is not None
        assert account.code == "101"
        assert account.name == "Capital"
        assert account.current_balance == 0.0
    
    def test_account_default_values(self, db_session):
        account = Account(code="101", name="Test", account_type="actif")
        db_session.add(account)
        db_session.commit()
        
        assert account.is_active is True
        assert account.is_analytic is False
        assert account.opening_balance == 0.0


class TestJournalEntry:
    """Tests pour le modèle JournalEntry"""
    
    def test_create_journal_entry(self, db_session):
        entry = JournalEntry(
            entry_number="JE-2024-00001",
            date=date.today(),
            description="Test entry"
        )
        db_session.add(entry)
        db_session.commit()
        
        assert entry.id is not None
        assert entry.is_balanced is False
        assert entry.is_posted is False


class TestAccounting:
    """Tests pour les opérations comptables"""
    
    def test_account_balance_calculation(self, db_session):
        # Créer deux comptes
        debit_account = Account(code="401", name="Fournisseurs", account_type="passif")
        credit_account = Account(code="101", name="Capital", account_type="passif")
        
        db_session.add(debit_account)
        db_session.add(credit_account)
        db_session.commit()
        
        # Créer une écriture
        entry = JournalEntry(
            entry_number="JE-2024-00001",
            date=date.today(),
            description="Test",
            total_debit=1000.0,
            total_credit=1000.0,
            is_balanced=True
        )
        db_session.add(entry)
        db_session.commit()
        
        assert entry.total_debit == entry.total_credit


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
