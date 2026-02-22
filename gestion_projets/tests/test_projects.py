"""
Tests unitaires pour le module de gestion des projets

Ce fichier contient les tests unitaires pour les modèles et routes de projets.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from app.core.database import Base, get_db
from app.models.project import Project
from app.models.task import Task


# Configuration de la base de données de test
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override de la dépendance get_db pour les tests"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db_session():
    """Fixture pour créer une session de base de données de test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    """Fixture pour créer un client de test"""
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_project(db_session):
    """Fixture pour créer un projet de test"""
    project = Project(
        name="Projet Test",
        description="Description du projet test",
        status="planning",
        priority="medium",
        budget=10000.0,
        progress=0
    )
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)
    return project


@pytest.fixture
def sample_task(db_session, sample_project):
    """Fixture pour créer une tâche de test"""
    task = Task(
        name="Tâche Test",
        description="Description de la tâche test",
        project_id=sample_project.id,
        status="todo",
        priority="medium"
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task


# ==================== TESTS DES MODÈLES ====================

class TestProjectModel:
    """Tests pour le modèle Project"""
    
    def test_create_project(self, db_session):
        """Test de création d'un projet"""
        project = Project(
            name="Nouveau Projet",
            description="Description",
            status="active",
            priority="high",
            budget=50000.0
        )
        db_session.add(project)
        db_session.commit()
        
        assert project.id is not None
        assert project.name == "Nouveau Projet"
        assert project.status == "active"
        assert project.budget == 50000.0
    
    def test_project_default_values(self, db_session):
        """Test des valeurs par défaut d'un projet"""
        project = Project(name="Projet par défaut")
        db_session.add(project)
        db_session.commit()
        
        assert project.status == "planning"
        assert project.priority == "medium"
        assert project.progress == 0
        assert project.budget == 0.0
        assert project.is_active is True
    
    def test_project_relationships(self, db_session, sample_project):
        """Test des relations du projet"""
        task = Task(
            name="Tâche liée",
            project_id=sample_project.id,
            status="todo"
        )
        db_session.add(task)
        db_session.commit()
        
        assert len(sample_project.tasks) == 1
        assert sample_project.tasks[0].name == "Tâche liée"


class TestTaskModel:
    """Tests pour le modèle Task"""
    
    def test_create_task(self, db_session, sample_project):
        """Test de création d'une tâche"""
        task = Task(
            name="Nouvelle Tâche",
            description="Description de la tâche",
            project_id=sample_project.id,
            status="in_progress",
            priority="high"
        )
        db_session.add(task)
        db_session.commit()
        
        assert task.id is not None
        assert task.name == "Nouvelle Tâche"
        assert task.status == "in_progress"
        assert task.is_completed is False
    
    def test_task_default_values(self, db_session, sample_project):
        """Test des valeurs par défaut d'une tâche"""
        task = Task(
            name="Tâche par défaut",
            project_id=sample_project.id
        )
        db_session.add(task)
        db_session.commit()
        
        assert task.status == "todo"
        assert task.priority == "medium"
        assert task.progress == 0
        assert task.is_blocked is False
    
    def test_task_parent_child(self, db_session, sample_project):
        """Test des relations parent-enfant des tâches"""
        parent_task = Task(
            name="Tâche parente",
            project_id=sample_project.id
        )
        db_session.add(parent_task)
        db_session.commit()
        db_session.refresh(parent_task)
        
        child_task = Task(
            name="Sous-tâche",
            project_id=sample_project.id,
            parent_id=parent_task.id
        )
        db_session.add(child_task)
        db_session.commit()
        
        assert child_task.parent_id == parent_task.id
        assert len(parent_task.subtasks) == 1


# ==================== TESTS DES ROUTES ====================

class TestProjectRoutes:
    """Tests pour les routes API des projets"""
    
    def test_create_project_endpoint(self, client):
        """Test de création d'un projet via l'API"""
        response = client.post(
            "/api/v1/projects/",
            json={
                "name": "Projet API",
                "description": "Projet créé via API",
                "status": "planning",
                "budget": 25000.0
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Projet API"
        assert data["budget"] == 25000.0
    
    def test_get_projects(self, client, sample_project):
        """Test de récupération de la liste des projets"""
        response = client.get("/api/v1/projects/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
    
    def test_get_project_by_id(self, client, sample_project):
        """Test de récupération d'un projet par ID"""
        response = client.get(f"/api/v1/projects/{sample_project.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_project.id
        assert data["name"] == sample_project.name
    
    def test_get_project_not_found(self, client):
        """Test de récupération d'un projet inexistant"""
        response = client.get("/api/v1/projects/99999")
        assert response.status_code == 404
    
    def test_update_project(self, client, sample_project):
        """Test de mise à jour d'un projet"""
        response = client.put(
            f"/api/v1/projects/{sample_project.id}",
            json={
                "name": "Projet modifié",
                "status": "active",
                "progress": 50
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Projet modifié"
        assert data["status"] == "active"
        assert data["progress"] == 50
    
    def test_delete_project(self, client, sample_project):
        """Test de suppression d'un projet"""
        response = client.delete(f"/api/v1/projects/{sample_project.id}")
        assert response.status_code == 204
        
        # Vérifier que le projet est bien supprimé
        response = client.get(f"/api/v1/projects/{sample_project.id}")
        assert response.status_code == 404
    
    def test_search_projects(self, client, sample_project):
        """Test de recherche de projets"""
        response = client.get("/api/v1/projects/search?q=Test")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
    
    def test_get_project_stats(self, client, sample_project):
        """Test de récupération des statistiques"""
        response = client.get("/api/v1/projects/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "by_status" in data
        assert "by_priority" in data


class TestTaskRoutes:
    """Tests pour les routes API des tâches"""
    
    def test_create_task_endpoint(self, client, sample_project):
        """Test de création d'une tâche via l'API"""
        response = client.post(
            f"/api/v1/projects/{sample_project.id}/tasks/",
            json={
                "name": "Tâche API",
                "description": "Tâche créée via API",
                "project_id": sample_project.id,
                "priority": "high"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Tâche API"
    
    def test_get_tasks_by_project(self, client, sample_project, sample_task):
        """Test de récupération des tâches d'un projet"""
        response = client.get(f"/api/v1/projects/{sample_project.id}/tasks/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
    
    def test_update_task_status(self, client, sample_task):
        """Test de mise à jour du statut d'une tâche"""
        response = client.patch(
            f"/api/v1/tasks/{sample_task.id}",
            json={"status": "done", "progress": 100, "is_completed": True}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "done"
        assert data["progress"] == 100


# ==================== TESTS DE VALIDATION ====================

class TestValidation:
    """Tests pour la validation des données"""
    
    def test_project_name_required(self, client):
        """Test que le nom du projet est requis"""
        response = client.post(
            "/api/v1/projects/",
            json={"description": "Sans nom"}
        )
        assert response.status_code == 422  # Validation Error
    
    def test_project_name_min_length(self, client):
        """Test de la longueur minimale du nom"""
        response = client.post(
            "/api/v1/projects/",
            json={"name": ""}
        )
        assert response.status_code == 422
    
    def test_task_progress_bounds(self, client, sample_project):
        """Test des limites du progress (0-100)"""
        response = client.post(
            f"/api/v1/projects/{sample_project.id}/tasks/",
            json={
                "name": "Tâche test",
                "project_id": sample_project.id,
                "progress": 150  # Invalid
            }
        )
        assert response.status_code == 422
    
    def test_budget_positive(self, client):
        """Test que le budget doit être positif"""
        response = client.post(
            "/api/v1/projects/",
            json={
                "name": "Projet budget négatif",
                "budget": -1000
            }
        )
        assert response.status_code == 422


# ==================== TESTS D'INTÉGRATION ====================

class TestIntegration:
    """Tests d'intégration pour les workflows complets"""
    
    def test_full_project_lifecycle(self, client):
        """Test du cycle de vie complet d'un projet"""
        # 1. Créer un projet
        response = client.post(
            "/api/v1/projects/",
            json={
                "name": "Projet Lifecycle",
                "status": "planning",
                "budget": 100000
            }
        )
        assert response.status_code == 201
        project_id = response.json()["id"]
        
        # 2. Mettre à jour vers actif
        response = client.put(
            f"/api/v1/projects/{project_id}",
            json={"status": "active"}
        )
        assert response.json()["status"] == "active"
        
        # 3. Créer des tâches
        for i in range(3):
            response = client.post(
                f"/api/v1/projects/{project_id}/tasks/",
                json={
                    "name": f"Tâche {i+1}",
                    "project_id": project_id
                }
            )
            assert response.status_code == 201
        
        # 4. Vérifier les statistiques
        response = client.get("/api/v1/projects/stats")
        assert response.status_code == 200
        stats = response.json()
        assert stats["total"] >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
