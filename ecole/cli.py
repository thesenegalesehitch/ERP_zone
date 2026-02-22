#!/usr/bin/env python3
"""
Script CLI pour le module École

Interface en ligne de commande pour gérer les étudiants,
cours et inscriptions.
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.etudiant import Etudiant
from app.models.cours import Cours


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ecole.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialise la base de données"""
    from app.core.database import Base
    Base.metadata.create_all(bind=engine)
    print("✓ Base de données initialisée")


def list_etudiants(db):
    """Liste tous les étudiants"""
    etudiants = db.query(Etudiant).all()
    if not etudiants:
        print("Aucun étudiant trouvé.")
        return
    
    print(f"\n{'='*80}")
    print(f"{'ID':<4} {'Nom':<20} {'Prénom':<20} {'Email':<30}")
    print(f"{'='*80}")
    for e in etudiants:
        print(f"{e.id:<4} {e.nom:<20} {e.prenom:<20} {e.email:<30}")


def list_cours(db):
    """Liste tous les cours"""
    cours = db.query(Cours).all()
    if not cours:
        print("Aucun cours trouvé.")
        return
    
    print(f"\n{'='*70}")
    print(f"{'ID':<4} {'Nom':<30} {'Crédits':<10} {'Volume':<10}")
    print(f"{'='*70}")
    for c in cours:
        print(f"{c.id:<4} {c.nom:<30} {c.credits:<10} {c.volume_horaire:<10}")


def stats(db):
    """Affiche les statistiques"""
    total_etudiants = db.query(Etudiant).count()
    total_cours = db.query(Cours).count()
    
    print(f"\n{'='*50}")
    print(f"STATISTIQUES ÉCOLE")
    print(f"{'='*50}")
    print(f"Étudiants:  {total_etudiants}")
    print(f"Cours:      {total_cours}")
    print(f"{'='*50}")


def main():
    parser = argparse.ArgumentParser(description="CLI École")
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("init", help="Initialiser la base de données")
    subparsers.add_parser("etudiants", help="Liste des étudiants")
    subparsers.add_parser("cours", help="Liste des cours")
    subparsers.add_parser("stats", help="Statistiques")
    
    args = parser.parse_args()
    db = SessionLocal()
    
    try:
        if args.command == "init":
            init_db()
        elif args.command == "etudiants":
            list_etudiants(db)
        elif args.command == "cours":
            list_cours(db)
        elif args.command == "stats":
            stats(db)
        else:
            parser.print_help()
    finally:
        db.close()


if __name__ == "__main__":
    main()
