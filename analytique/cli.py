#!/usr/bin/env python3
"""
Script CLI pour le module Analytique
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./analytique.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    from app.core.database import Base
    Base.metadata.create_all(bind=engine)
    print("✓ Base de données initialisée")


def stats(db):
    print("Statistiques analytiques")
    print("À implémenter")


def main():
    parser = argparse.ArgumentParser(description="CLI Analytique")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("init", help="Initialiser")
    subparsers.add_parser("stats", help="Statistiques")
    args = parser.parse_args()
    db = SessionLocal()
    try:
        if args.command == "init":
            init_db()
        elif args.command == "stats":
            stats(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
