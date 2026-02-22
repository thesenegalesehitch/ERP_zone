"""
Script de seeds (données initiales) pour le module de gestion de projets

Ce script插入 des données de test dans la base de données pour le développement
et les tests.
"""
import sys
import os
from datetime import date, timedelta
import random

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.project import Project, ProjectTeamMember, ProjectMilestone
from app.models.task import Task


# Configuration de la base de données
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./projects.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def generate_sample_data():
    """Génère des données d'exemple pour les projets et tâches"""
    
    db = SessionLocal()
    
    try:
        # Vérifier si des données existent déjà
        existing_projects = db.query(Project).count()
        if existing_projects > 0:
            print(f"⚠️  {existing_projects} projets existent déjà dans la base de données.")
            response = input("Voulez-vous continuer ? (o/n): ")
            if response.lower() != 'o':
                print("Opération annulée.")
                return
        
        print("🔄 Génération des données d'exemple...")
        
        # =====================================================================
        # Création des Projets
        # =====================================================================
        
        projects_data = [
            {
                "name": "Site Web Corporate ERP Zone",
                "description": "Refonte complète du site web corporate avec nouvelles fonctionnalités",
                "status": "active",
                "priority": "high",
                "budget": 75000.0,
                "progress": 65,
                "start_date": date.today() - timedelta(days=60),
                "end_date": date.today() + timedelta(days=30)
            },
            {
                "name": "Application Mobile iOS/Android",
                "description": "Développement d'une application mobile pour la gestion des projets",
                "status": "planning",
                "priority": "critical",
                "budget": 120000.0,
                "progress": 15,
                "start_date": date.today() - timedelta(days=15),
                "end_date": date.today() + timedelta(days=180)
            },
            {
                "name": "Module de Comptabilité Avancé",
                "description": "Nouveau module de comptabilité avec анализ financier",
                "status": "active",
                "priority": "medium",
                "budget": 45000.0,
                "progress": 40,
                "start_date": date.today() - timedelta(days=45),
                "end_date": date.today() + timedelta(days=60)
            },
            {
                "name": "Système de Reporting BI",
                "description": "Tableau de bord analytics pour les directeurs",
                "status": "on_hold",
                "priority": "medium",
                "budget": 35000.0,
                "progress": 25,
                "start_date": date.today() - timedelta(days=30),
                "end_date": date.today() + timedelta(days=90)
            },
            {
                "name": "Intégration API Partenaires",
                "description": "Connexion avec les APIs des partenaires commerciaux",
                "status": "completed",
                "priority": "low",
                "budget": 20000.0,
                "progress": 100,
                "start_date": date.today() - timedelta(days=120),
                "end_date": date.today() - timedelta(days=10)
            },
            {
                "name": "Migration vers Cloud AWS",
                "description": "Migration de l'infrastructure vers Amazon Web Services",
                "status": "planning",
                "priority": "high",
                "budget": 150000.0,
                "progress": 5,
                "start_date": date.today(),
                "end_date": date.today() + timedelta(days=365)
            },
            {
                "name": "Module RH - Gestion des Congés",
                "description": "Système de gestion des demandes de congés et absences",
                "status": "active",
                "priority": "medium",
                "budget": 25000.0,
                "progress": 80,
                "start_date": date.today() - timedelta(days=40),
                "end_date": date.today() + timedelta(days=15)
            },
            {
                "name": "Chatbot Support Client",
                "description": "Assistant virtuel pour le support client 24/7",
                "status": "active",
                "priority": "low",
                "budget": 18000.0,
                "progress": 55,
                "start_date": date.today() - timedelta(days=25),
                "end_date": date.today() + timedelta(days=45)
            }
        ]
        
        projects = []
        for p_data in projects_data:
            project = Project(**p_data)
            db.add(project)
            projects.append(project)
        
        db.commit()
        print(f"✓ {len(projects)} projets créés")
        
        # =====================================================================
        # Création des Tâches pour chaque projet
        # =====================================================================
        
        task_templates = [
            {"name": "Analyse des besoins", "hours": 16, "priority": "high"},
            {"name": "Conception technique", "hours": 24, "priority": "high"},
            {"name": "Développement backend", "hours": 80, "priority": "medium"},
            {"name": "Développement frontend", "hours": 60, "priority": "medium"},
            {"name": "Intégration API", "hours": 32, "priority": "medium"},
            {"name": "Tests unitaires", "hours": 20, "priority": "medium"},
            {"name": "Tests d'intégration", "hours": 16, "priority": "low"},
            {"name": "Tests utilisateurs (UAT)", "hours": 12, "priority": "low"},
            {"name": "Documentation technique", "hours": 15, "priority": "low"},
            {"name": "Formation utilisateurs", "hours": 8, "priority": "low"},
            {"name": "Déploiement production", "hours": 8, "priority": "critical"},
            {"name": "Support post-lancement", "hours": 24, "priority": "medium"}
        ]
        
        total_tasks = 0
        for project in projects:
            # Créer entre 5 et 10 tâches par projet
            num_tasks = random.randint(5, 10)
            selected_tasks = random.sample(task_templates, num_tasks)
            
            for i, task_template in enumerate(selected_tasks):
                # Déterminer le statut aléatoirement
                status_choices = ["todo", "in_progress", "done"]
                if project.status == "completed":
                    status = "done"
                elif project.status == "planning":
                    status = random.choice(["todo", "in_progress"])
                else:
                    status = random.choice(status_choices)
                
                # Calculer la progression
                if status == "done":
                    progress = 100
                    is_completed = True
                elif status == "in_progress":
                    progress = random.randint(20, 80)
                    is_completed = False
                else:
                    progress = 0
                    is_completed = False
                
                task = Task(
                    name=task_template["name"],
                    description=f"Tâche pour le projet {project.name}",
                    project_id=project.id,
                    status=status,
                    priority=task_template["priority"],
                    estimated_hours=task_template["hours"],
                    actual_hours=task_template["hours"] * (progress / 100) if progress > 0 else 0,
                    progress=progress,
                    is_completed=is_completed,
                    start_date=project.start_date,
                    due_date=project.end_date,
                    order=i
                )
                db.add(task)
                total_tasks += 1
        
        db.commit()
        print(f"✓ {total_tasks} tâches créées")
        
        # =====================================================================
        # Création des Jalons
        # =====================================================================
        
        milestones_data = [
            {"name": "Phase 1: Kick-off", "days_offset": 0, "status": "completed"},
            {"name": "Phase 2: Conception", "days_offset": 15, "status": "completed"},
            {"name": "Phase 3: Développement", "days_offset": 45, "status": "in_progress"},
            {"name": "Phase 4: Tests", "days_offset": 75, "status": "pending"},
            {"name": "Phase 5: Déploiement", "days_offset": 90, "status": "pending"}
        ]
        
        # Ajouter des jalons aux 3 premiers projets
        total_milestones = 0
        for project in projects[:3]:
            for i, m_data in enumerate(milestones_data):
                if project.status == "completed" and i < 2:
                    m_status = "completed"
                    is_completed = True
                elif project.status == "active" and i < 3:
                    m_status = "completed" if i < 2 else "in_progress"
                    is_completed = i < 2
                else:
                    m_status = "pending"
                    is_completed = False
                
                milestone = ProjectMilestone(
                    name=m_data["name"],
                    description=f"Jalon {i+1} du projet",
                    project_id=project.id,
                    due_date=project.start_date + timedelta(days=m_data["days_offset"]),
                    status=m_status,
                    is_completed=is_completed,
                    order=i
                )
                db.add(milestone)
                total_milestones += 1
        
        db.commit()
        print(f"✓ {total_milestones} jalons créés")
        
        # =====================================================================
        # Résumé
        # =====================================================================
        
        print("\n" + "="*60)
        print("RÉSUMÉ DES DONNÉES GÉNÉRÉES")
        print("="*60)
        print(f"Projets:     {len(projects)}")
        print(f"Tâches:      {total_tasks}")
        print(f"Jalons:      {total_milestones}")
        print(f"Membres:     0 (à ajouter manuellement)")
        print("="*60)
        print("\n✅ Données d'exemple générées avec succès!")
        print("\nVous pouvez maintenant:")
        print("  - Démarrer l'API: uvicorn main:app --reload")
        print("  - Accéder à la doc: http://localhost:8000/docs")
        print("  - Tester le CLI: python cli.py stats")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération des données: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def clear_data():
    """Supprime toutes les données de la base"""
    
    db = SessionLocal()
    
    try:
        db.query(Task).delete()
        db.query(ProjectMilestone).delete()
        db.query(ProjectTeamMember).delete()
        db.query(Project).delete()
        db.commit()
        print("✓ Toutes les données ont été supprimées.")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Script de seeds pour les projets")
    parser.add_argument("--clear", action="store_true", help="Supprimer toutes les données")
    parser.add_argument("--seed", action="store_true", help="Générer les données d'exemple")
    
    args = parser.parse_args()
    
    if args.clear:
        clear_data()
    elif args.seed:
        generate_sample_data()
    else:
        # Par défaut, demander confirmation pour générer
        generate_sample_data()
