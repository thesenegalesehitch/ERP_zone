#!/usr/bin/env python3
"""
Script CLI pour le module de gestion de projets

Ce script fournit une interface en ligne de commande pour gérer
les projets, tâches et membres d'équipe.
"""
import argparse
import sys
import os
from datetime import date, datetime

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.project import Project, ProjectTeamMember, ProjectMilestone
from app.models.task import Task


# Configuration de la base de données
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./projects.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Obtient une session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Crée toutes les tables dans la base de données"""
    from app.core.database import Base
    Base.metadata.create_all(bind=engine)
    print("✓ Tables créées avec succès")


def list_projects(db):
    """Liste tous les projets"""
    projects = db.query(Project).all()
    if not projects:
        print("Aucun projet trouvé.")
        return
    
    print(f"\n{'='*60}")
    print(f"{'ID':<5} {'Nom':<30} {'Statut':<15} {'Progression':<10}")
    print(f"{'='*60}")
    for p in projects:
        print(f"{p.id:<5} {p.name:<30} {p.status:<15} {p.progress}%")


def create_project(db, name, description, budget, priority):
    """Crée un nouveau projet"""
    project = Project(
        name=name,
        description=description,
        budget=budget or 0.0,
        priority=priority or "medium",
        status="planning"
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    print(f"✓ Projet '{name}' créé avec ID: {project.id}")
    return project


def show_project(db, project_id):
    """Affiche les détails d'un projet"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        print(f"Projet {project_id} non trouvé.")
        return
    
    print(f"\n{'='*60}")
    print(f"PROJET: {project.name}")
    print(f"{'='*60}")
    print(f"ID:          {project.id}")
    print(f"Description: {project.description or 'N/A'}")
    print(f"Statut:      {project.status}")
    print(f"Priorité:    {project.priority}")
    print(f"Budget:      {project.budget:,.2f}")
    print(f"Progression: {project.progress}%")
    print(f"Date début:  {project.start_date or 'N/A'}")
    print(f"Date fin:    {project.end_date or 'N/A'}")
    
    # Afficher les tâches
    tasks = db.query(Task).filter(Task.project_id == project.id).all()
    if tasks:
        print(f"\nTâches ({len(tasks)}):")
        print(f"{'='*60}")
        for task in tasks:
            print(f"  - [{task.status}] {task.name} (Priorité: {task.priority})")
    
    # Afficher les membres
    members = db.query(ProjectTeamMember).filter(ProjectTeamMember.project_id == project.id).all()
    if members:
        print(f"\nMembres de l'équipe ({len(members)}):")
        print(f"{'='*60}")
        for m in members:
            print(f"  - User #{m.user_id} - Rôle: {m.role}")
    
    # Afficher les jalons
    milestones = db.query(ProjectMilestone).filter(ProjectMilestone.project_id == project.id).all()
    if milestones:
        print(f"\nJalons ({len(milestones)}):")
        print(f"{'='*60}")
        for m in milestones:
            status_icon = "✓" if m.is_completed else "○"
            print(f"  {status_icon} {m.name} - Échéance: {m.due_date or 'N/A'}")


def update_project_status(db, project_id, status):
    """Met à jour le statut d'un projet"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        print(f"Projet {project_id} non trouvé.")
        return
    
    project.status = status
    project.updated_at = datetime.now().date()
    db.commit()
    print(f"✓ Statut du projet mis à jour: {status}")


def create_task(db, project_id, name, description, priority):
    """Crée une nouvelle tâche"""
    task = Task(
        name=name,
        description=description,
        project_id=project_id,
        priority=priority or "medium",
        status="todo"
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    print(f"✓ Tâche '{name}' créée avec ID: {task.id}")
    return task


def list_tasks(db, project_id=None):
    """Liste les tâches"""
    if project_id:
        tasks = db.query(Task).filter(Task.project_id == project_id).all()
    else:
        tasks = db.query(Task).all()
    
    if not tasks:
        print("Aucune tâche trouvée.")
        return
    
    print(f"\n{'='*60}")
    print(f"{'ID':<5} {'Nom':<35} {'Statut':<15} {'Projet':<10}")
    print(f"{'='*60}")
    for t in tasks:
        proj = db.query(Project).filter(Project.id == t.project_id).first()
        proj_name = proj.name[:10] if proj else "N/A"
        print(f"{t.id:<5} {t.name[:35]:<35} {t.status:<15} {proj_name:<10}")


def update_task_status(db, task_id, status):
    """Met à jour le statut d'une tâche"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        print(f"Tâche {task_id} non trouvée.")
        return
    
    task.status = status
    if status == "done":
        task.is_completed = True
        task.completed_date = datetime.now().date()
        task.progress = 100
    task.updated_at = datetime.now().date()
    db.commit()
    print(f"✓ Tâche mise à jour: {status}")


def add_milestone(db, project_id, name, due_date):
    """Ajoute un jalon au projet"""
    milestone = ProjectMilestone(
        name=name,
        project_id=project_id,
        due_date=datetime.strptime(due_date, "%Y-%m-%d").date() if due_date else None,
        status="pending"
    )
    db.add(milestone)
    db.commit()
    db.refresh(milestone)
    print(f"✓ Jalon '{name}' créé")
    return milestone


def get_stats(db):
    """Affiche les statistiques des projets"""
    total = db.query(Project).count()
    active = db.query(Project).filter(Project.is_active == True).count()
    
    by_status = {}
    for status in ['planning', 'active', 'completed', 'cancelled', 'on_hold']:
        by_status[status] = db.query(Project).filter(Project.status == status).count()
    
    by_priority = {}
    for priority in ['low', 'medium', 'high', 'critical']:
        by_priority[priority] = db.query(Project).filter(Project.priority == priority).count()
    
    total_tasks = db.query(Task).count()
    done_tasks = db.query(Task).filter(Task.status == "done").count()
    
    print(f"\n{'='*60}")
    print(f"STATISTIQUES")
    print(f"{'='*60}")
    print(f"Projets total:      {total}")
    print(f"Projets actifs:     {active}")
    print(f"\nPar statut:")
    for status, count in by_status.items():
        print(f"  - {status}: {count}")
    print(f"\nPar priorité:")
    for priority, count in by_priority.items():
        print(f"  - {priority}: {count}")
    print(f"\nTâches: {done_tasks}/{total_tasks} terminées")


def main():
    """Point d'entrée principal du CLI"""
    parser = argparse.ArgumentParser(
        description="CLI pour la gestion de projets ERP",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")
    
    # Commande init
    init_parser = subparsers.add_parser("init", help="Initialiser la base de données")
    
    # Commande projects list
    projects_parser = subparsers.add_parser("projects", help="Gestion des projets")
    projects_parser.add_argument("--list", action="store_true", help="Lister les projets")
    projects_parser.add_argument("--create", nargs="+", help="Créer un projet")
    projects_parser.add_argument("--show", type=int, help="Afficher un projet")
    projects_parser.add_argument("--update-status", nargs=2, metavar=("ID", "STATUS"), help="Mettre à jour le statut")
    
    # Commande tasks
    tasks_parser = subparsers.add_parser("tasks", help="Gestion des tâches")
    tasks_parser.add_argument("--list", action="store_true", help="Lister les tâches")
    tasks_parser.add_argument("--project", type=int, help="Filtrer par projet")
    tasks_parser.add_argument("--create", nargs="+", help="Créer une tâche")
    tasks_parser.add_argument("--status", nargs=2, metavar=("ID", "STATUS"), help="Mettre à jour le statut")
    
    # Commande stats
    stats_parser = subparsers.add_parser("stats", help="Afficher les statistiques")
    
    args = parser.parse_args()
    
    db = SessionLocal()
    
    try:
        if args.command == "init":
            create_tables()
        
        elif args.command == "projects":
            if args.list:
                list_projects(db)
            elif args.create:
                name = " ".join(args.create[:-1]) if len(args.create) > 1 else args.create[0]
                create_project(db, name, "", 0.0, "medium")
            elif args.show:
                show_project(db, args.show)
            elif args.update_status:
                update_project_status(db, int(args.update_status[0]), args.update_status[1])
            else:
                list_projects(db)
        
        elif args.command == "tasks":
            if args.list:
                list_tasks(db, args.project)
            elif args.create:
                name = " ".join(args.create[:-1]) if len(args.create) > 1 else args.create[0]
                project_id = args.project or 1
                create_task(db, project_id, name, "", "medium")
            elif args.status:
                update_task_status(db, int(args.status[0]), args.status[1])
            else:
                list_tasks(db)
        
        elif args.command == "stats":
            get_stats(db)
        
        else:
            parser.print_help()
    
    finally:
        db.close()


if __name__ == "__main__":
    main()
