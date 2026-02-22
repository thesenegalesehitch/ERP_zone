"""
Tests unitaires pour le module École
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models.etudiant import Etudiant
from app.models.cours import Cours


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


class TestEtudiant:
    """Tests pour le modèle Étudiant"""
    
    def test_create_etudiant(self, db_session):
        etudiant = Etudiant(
            nom="Diop",
            prenom="Moussa",
            email="moussa.diop@example.com"
        )
        db_session.add(etudiant)
        db_session.commit()
        
        assert etudiant.id is not None
        assert etudiant.nom == "Diop"
        assert etudiant.prenom == "Moussa"


class TestCours:
    """Tests pour le modèle Cours"""
    
    def test_create_cours(self, db_session):
        cours = Cours(
            nom="Mathématiques",
            credits=4,
            volume_horaire=48
        )
        db_session.add(cours)
        db_session.commit()
        
        assert cours.id is not None
        assert cours.nom == "Mathématiques"
        assert cours.credits == 4


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
