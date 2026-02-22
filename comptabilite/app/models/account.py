"""
Module des modèles de comptes comptables

Ce module définit les modèles de données pour la gestion des comptes.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from app.core.database import Base


class Account(Base):
    """
    Modèle Account - Plan comptable
    
    Représente un compte dans le plan comptable de l'entreprise.
    
    Types de comptes:
    - ACTIF (1): Comptes d'actif
    - PASSIF (2): Comptes de passif
    - CHARGE (6): Comptes de charges
    - PRODUIT (7): Comptes de produits
    """
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)  # Numéro de compte
    name = Column(String(200), nullable=False)  # Nom du compte
    description = Column(Text)  # Description
    account_type = Column(String(20), nullable=False)  # Type: actif, passif, charge, produit
    parent_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)  # Compte parent
    is_active = Column(Boolean, default=True)  # Actif/inactif
    is_analytic = Column(Boolean, default=False)  # Compte analytique
    opening_balance = Column(Float, default=0.0)  # Solde d'ouverture
    current_balance = Column(Float, default=0.0)  # Solde actuel
    currency = Column(String(3), default="XOF")  # Devise
    allow_negative = Column(Boolean, default=False)  # Autoriser soldes négatifs
    
    # Relations
    parent = relationship("Account", remote_side=[id], backref="children")
    journal_entries = relationship("JournalEntryLine", back_populates="account")

    def __repr__(self):
        return f"<Account {self.code} - {self.name}>"


class JournalEntry(Base):
    """
    Modèle JournalEntry - Écriture comptable
    
    Représente une écriture comptable complète avec ses lignes.
    """
    __tablename__ = "journal_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    entry_number = Column(String(50), unique=True, nullable=False, index=True)  # Numéro d'écriture
    date = Column(Date, nullable=False, index=True)  # Date de l'écriture
    reference = Column(String(100))  # Pièce justificative
    description = Column(Text, nullable=False)  # Libellé
    total_debit = Column(Float, default=0.0)  # Total débit
    total_credit = Column(Float, default=0.0)  # Total crédit
    is_balanced = Column(Boolean, default=False)  # Équilibrée
    is_posted = Column(Boolean, default=False)  # Comptabilisée
    is_archived = Column(Boolean, default=False)  # Archivée
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(Date)
    posted_at = Column(Date)
    
    # Relations
    lines = relationship("JournalEntryLine", back_populates="entry", cascade="all, delete-orphan")


class JournalEntryLine(Base):
    """
    Modèle JournalEntryLine - Ligne d'écriture comptable
    
    Représente une ligne individuelle d'une écriture comptable.
    """
    __tablename__ = "journal_entry_lines"
    
    id = Column(Integer, primary_key=True, index=True)
    entry_id = Column(Integer, ForeignKey("journal_entries.id"), nullable=False, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    debit = Column(Float, default=0.0)  # Montant débit
    credit = Column(Float, default=0.0)  # Montant crédit
    description = Column(Text)  # Libellé ligne
    analytic_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)  # Compte analytique
    
    # Relations
    entry = relationship("JournalEntry", back_populates="lines")
    account = relationship("Account", back_populates="journal_entries")


class FiscalYear(Base):
    """
    Modèle FiscalYear - Exercice comptable
    
    Définit un exercice comptable avec ses périodes.
    """
    __tablename__ = "fiscal_years"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # Nom de l'exercice
    start_date = Column(Date, nullable=False)  # Date de début
    end_date = Column(Date, nullable=False)  # Date de fin
    is_closed = Column(Boolean, default=False)  # Clôturé
    is_active = Column(Boolean, default=True)  # Actif
    closing_date = Column(Date)  # Date de clôture


class AccountingPeriod(Base):
    """
    Modèle AccountingPeriod - Période comptable
    
    Représente une période (mois) dans un exercice.
    """
    __tablename__ = "accounting_periods"
    
    id = Column(Integer, primary_key=True, index=True)
    fiscal_year_id = Column(Integer, ForeignKey("fiscal_years.id"), nullable=False)
    period_number = Column(Integer, nullable=False)  # 1-12
    name = Column(String(50), nullable=False)  # Nom du mois
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_closed = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=False)  # Verrouillé pour écriture
