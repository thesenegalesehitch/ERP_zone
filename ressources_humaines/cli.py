#!/usr/bin/env python3
"""
Script CLI pour le module Ressources Humaines

Interface en ligne de commande pour gérer les employés,
congés, départements et autres fonctionnalités RH.
"""
import argparse
import sys
import os
from datetime import date, datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.employee import Employee, Attendance, Salary
from app.models.department import Department
from app.models.leave_request import LeaveRequest, LeaveBalance


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rh.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialise la base de données"""
    from app.core.database import Base
    Base.metadata.create_all(bind=engine)
    print("✓ Base de données initialisée")


def list_employees(db):
    """Liste tous les employés"""
    employees = db.query(Employee).all()
    if not employees:
        print("Aucun employé trouvé.")
        return
    
    print(f"\n{'='*70}")
    print(f"{'ID':<4} {'Nom':<20} {'Poste':<20} {'Département':<15}")
    print(f"{'='*70}")
    for e in employees:
        dept = db.query(Department).filter(Department.id == e.department_id).first()
        dept_name = dept.name if dept else "N/A"
        print(f"{e.id:<4} {e.first_name} {e.last_name:<15} {e.position or 'N/A':<20} {dept_name:<15}")


def list_departments(db):
    """Liste tous les départements"""
    departments = db.query(Department).all()
    if not departments:
        print("Aucun département trouvé.")
        return
    
    print(f"\n{'='*50}")
    print(f"{'ID':<4} {'Nom':<30} {'Description':<15}")
    print(f"{'='*50}")
    for d in departments:
        print(f"{d.id:<4} {d.name:<30} {d.description[:15] if d.description else 'N/A':<15}")


def show_employee(db, employee_id):
    """Affiche les détails d'un employé"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        print(f"Employé {employee_id} non trouvé.")
        return
    
    dept = db.query(Department).filter(Department.id == employee.department_id).first()
    
    print(f"\n{'='*60}")
    print(f"EMPLOYÉ: {employee.first_name} {employee.last_name}")
    print(f"{'='*60}")
    print(f"ID:            {employee.id}")
    print(f"Poste:         {employee.position or 'N/A'}")
    print(f"Département:    {dept.name if dept else 'N/A'}")
    print(f"Email:         {employee.email or 'N/A'}")
    print(f"Téléphone:     {employee.phone or 'N/A'}")
    print(f"Date embauche: {employee.hire_date}")
    print(f"Salaire:       {employee.salary or 'N/A'}")
    print(f"Statut:        {'Actif' if employee.is_active else 'Inactif'}")
    
    # Congés
    leaves = db.query(LeaveRequest).filter(
        LeaveRequest.employee_id == employee.id
    ).all()
    if leaves:
        print(f"\nDemandes decongé ({len(leaves)}):")
        for l in leaves:
            print(f"  - {l.start_date} au {l.end_date}: {l.status.value} ({l.leave_type.value})")


def list_leaves(db, employee_id=None):
    """Liste les demandes decongé"""
    if employee_id:
        leaves = db.query(LeaveRequest).filter(
            LeaveRequest.employee_id == employee_id
        ).all()
    else:
        leaves = db.query(LeaveRequest).all()
    
    if not leaves:
        print("Aucune demande decongé trouvée.")
        return
    
    print(f"\n{'='*70}")
    print(f"{'ID':<4} {'Employé':<20} {'Type':<12} {'Dates':<20} {'Statut':<10}")
    print(f"{'='*70}")
    for l in leaves:
        emp = db.query(Employee).filter(Employee.id == l.employee_id).first()
        emp_name = f"{emp.first_name} {emp.last_name}" if emp else "N/A"
        dates = f"{l.start_date} - {l.end_date}"
        print(f"{l.id:<4} {emp_name[:20]:<20} {l.leave_type.value:<12} {dates:<20} {l.status.value:<10}")


def create_employee(db, first_name, last_name, position, department_id):
    """Crée un nouvel employé"""
    employee = Employee(
        first_name=first_name,
        last_name=last_name,
        position=position,
        department_id=department_id,
        hire_date=datetime.now().date()
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    print(f"✓ Employé {first_name} {last_name} créé avec ID: {employee.id}")
    return employee


def stats(db):
    """Affiche les statistiques RH"""
    total_employees = db.query(Employee).count()
    active_employees = db.query(Employee).filter(Employee.is_active == True).count()
    
    departments = db.query(Department).count()
    
    pending_leaves = db.query(LeaveRequest).filter(
        LeaveRequest.status == "pending"
    ).count()
    
    approved_leaves = db.query(LeaveRequest).filter(
        LeaveRequest.status == "approved"
    ).count()
    
    print(f"\n{'='*50}")
    print(f"STATISTIQUES RH")
    print(f"{'='*50}")
    print(f"Employés total:     {total_employees}")
    print(f"Employés actifs:    {active_employees}")
    print(f"Départements:       {departments}")
    print(f"Congés en attente:  {pending_leaves}")
    print(f"Congés approuvés:   {approved_leaves}")
    print(f"{'='*50}")


def main():
    parser = argparse.ArgumentParser(description="CLI Ressources Humaines")
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("init", help="Initialiser la base de données")
    
    emp_parser = subparsers.add_parser("employees", help="Gestion des employés")
    emp_parser.add_argument("--list", action="store_true")
    emp_parser.add_argument("--show", type=int)
    emp_parser.add_argument("--create", nargs=4, metavar=("PRENOM", "NOM", "POSTE", "DEPT_ID"))
    
    dept_parser = subparsers.add_parser("departments", help="Gestion des départements")
    dept_parser.add_argument("--list", action="store_true")
    
    leave_parser = subparsers.add_parser("leaves", help="Gestion descongés")
    leave_parser.add_argument("--list", action="store_true")
    leave_parser.add_argument("--employee", type=int)
    
    subparsers.add_parser("stats", help="Statistiques")
    
    args = parser.parse_args()
    db = SessionLocal()
    
    try:
        if args.command == "init":
            init_db()
        elif args.command == "employees":
            if args.list:
                list_employees(db)
            elif args.show:
                show_employee(db, args.show)
            elif args.create:
                create_employee(
                    db, args.create[0], args.create[1],
                    args.create[2], int(args.create[3])
                )
            else:
                list_employees(db)
        elif args.command == "departments":
            list_departments(db)
        elif args.command == "leaves":
            list_leaves(db, args.employee)
        elif args.command == "stats":
            stats(db)
        else:
            parser.print_help()
    finally:
        db.close()


if __name__ == "__main__":
    main()
