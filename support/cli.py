#!/usr/bin/env python3
"""CLI Support"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy import create_engine
engine = create_engine("sqlite:///./support.db")
def init_db():
    from app.core.database import Base
    Base.metadata.create_all(bind=engine)
    print("OK")
if __name__ == "__main__":
    init_db()
