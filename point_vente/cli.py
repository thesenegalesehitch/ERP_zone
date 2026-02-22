#!/usr/bin/env python3
"""
Script CLI pour le module Point de Vente
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pos.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    from app.core.database import Base
    Base.metadata.create_all(bind=engine)
    print("✓ Base de données initialisée")


def main():
    parser = argparse.ArgumentParser(description="CLI Point de Vente")
    parser.add_argument("init", help="Initialiser la base de données")
    args = parser.parse_args()
    
    if args.init:
        init_db()


if __name__ == "__main__":
    main()
