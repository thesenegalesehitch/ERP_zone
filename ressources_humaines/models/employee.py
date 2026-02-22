"""
Module des modèles d'employés

Ce module définit les modèles de données pour la gestion des employés.
"""
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Employee(Base):
    """
    Modèle Employee - Représente un employé dans le système
    
    Attributs:
        id: Identifiant unique
        first_name: Prénom
        last_name: Nom
        date_of_birth: Date de naissance
        hire_date: Date d'embauche
        position: Poste/Intitulé du poste
        salary: Salaire de base
        phone: Numéro de téléphone
        email: Adresse email professionnelle
        address: Adresse
        emergency_contact: Contact d'urgence
        emergency_phone: Téléphone d'urgence
        is_active: Statut actif
        manager_id: ID du manager
        employment_type: Type de contrat (cdi, cdd, interim)
        department_id: ID du département
        user_id: ID de l'utilisateur associé
    """
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), index=True, nullable=False)
    last_name = Column(String(100), index=True, nullable=False)
    date_of_birth = Column(Date)
    hire_date = Column(Date, nullable=False)
    end_date = Column(Date)  # Date de fin de contrat
    position = Column(String(200))
    salary = Column(Float)  # Salaire de base
    phone = Column(String(20))
    email = Column(String(200))
    address = Column(Text)
    emergency_contact = Column(String(200))
    emergency_phone = Column(String(20))
    is_active = Column(Boolean, default=True)
    manager_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    employment_type = Column(String(20), default="cdi")  # cdi, cdd, interim, freelance
    
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Relations
    user = relationship("User", back_populates="employee")
    department = relationship("Department", back_populates="employees")
    manager = relationship("Employee", remote_side=[id], backref="subordinates")
    leave_requests = relationship("LeaveRequest", back_populates="employee", cascade="all, delete-orphan")
    attendances = relationship("Attendance", back_populates="employee", cascade="all, delete-orphan")
    salaries = relationship("Salary", back_populates="employee", cascade="all, delete-orphan")


class Attendance(Base):
    """
    Modèle Attendance - Suivi des présences
    """
    __tablename__ = "attendances"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    check_in = Column(Date)  # Heure d'entrée
    check_out = Column(Date)  # Heure de sortie
    status = Column(String(20), default="present")  # present, absent, late, leave
    notes = Column(Text)
    
    employee = relationship("Employee", back_populates="attendances")


class Salary(Base):
    """
    Modèle Salary - Gestion de la paie
    """
    __tablename__ = "salaries"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    month = Column(Integer, nullable=False)  # Mois (1-12)
    year = Column(Integer, nullable=False)  # Année
    base_salary = Column(Float, nullable=False)
    bonuses = Column(Float, default=0)
    deductions = Column(Float, default=0)
    net_salary = Column(Float, nullable=False)
    payment_date = Column(Date)
    payment_status = Column(String(20), default="pending")  # pending, paid, cancelled
    notes = Column(Text)
    
    employee = relationship("Employee", back_populates="salaries")