"""
Tests unitaires pour le module Banque
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime

from main import app
from app.core.database import Base, get_db
from app.models.client import ClientBancaire
from app.models.compte import Compte, TypeCompte
from app.models.transaction import Transaction, TypeTransaction


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


class TestClientBancaire:
    """Tests pour le modèle ClientBancaire"""
    
    def test_create_client(self, db_session):
        client = ClientBancaire(
            nom="Dupont",
            email="dupont@example.com",
            telephone="0123456789"
        )
        db_session.add(client)
        db_session.commit()
        
        assert client.id is not None
        assert client.nom == "Dupont"
        assert client.email == "dupont@example.com"


class TestCompte:
    """Tests pour le modèle Compte"""
    
    def test_create_compte(self, db_session):
        client = ClientBancaire(nom="Test", email="test@test.com")
        db_session.add(client)
        db_session.commit()
        
        compte = Compte(
            numero_compte="FR0012345678",
            type_compte=TypeCompte.COURANT,
            client_id=client.id,
            solde=1000.0
        )
        db_session.add(compte)
        db_session.commit()
        
        assert compte.id is not None
        assert compte.numero_compte == "FR0012345678"
        assert compte.solde == 1000.0
    
    def test_compte_default_values(self, db_session):
        client = ClientBancaire(nom="Test", email="test@test.com")
        db_session.add(client)
        db_session.commit()
        
        compte = Compte(
            numero_compte="FR0012345679",
            client_id=client.id
        )
        db_session.add(compte)
        db_session.commit()
        
        assert compte.est_actif == 1
        assert compte.solde == 0.0


class TestTransaction:
    """Tests pour les transactions"""
    
    def test_credit_transaction(self, db_session):
        client = ClientBancaire(nom="Test", email="test@test.com")
        db_session.add(client)
        db_session.commit()
        
        compte = Compte(
            numero_compte="FR0012345678",
            client_id=client.id,
            solitaire=500.0
        )
        db_session.add(compte)
        db_session.commit()
        
        transaction = Transaction(
            compte_id=compte.id,
            type_transaction=TypeTransaction.CREDIT,
            montant=100.0,
            description="Dépôt"
        )
        db_session.add(transaction)
        db_session.commit()
        
        assert transaction.id is not None
        assert transaction.montant == 100.0
    
    def test_debit_transaction(self, db_session):
        client = ClientBancaire(nom="Test", email="test@test.com")
        db_session.add(client)
        db_session.commit()
        
        compte = Compte(
            numero_compte="FR0012345678",
            client_id=client.id,
            solde=500.0
        )
        db_session.add(compte)
        db_session.commit()
        
        transaction = Transaction(
            compte_id=compte.id,
            type_transaction=TypeTransaction.DEBIT,
            montant=50.0,
            description="Retrait"
        )
        db_session.add(transaction)
        db_session.commit()
        
        assert transaction.montant == 50.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
