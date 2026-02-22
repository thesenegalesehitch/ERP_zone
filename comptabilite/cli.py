#!/usr/bin/env python3
"""
Script CLI pour le module Comptabilité

Interface en ligne de commande pour gérer les comptes,
écritures comptables et exercices.
"""
import argparse
import sys
import os
from datetime import date, datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.account import Account, JournalEntry, FiscalYear, AccountingPeriod


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./comptabilite.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialise la base de données"""
    from app.core.database import Base
    Base.metadata.create_all(bind=engine)
    print("✓ Base de données initialisée")


def list_accounts(db):
    """Liste tous les comptes"""
    accounts = db.query(Account).all()
    if not accounts:
        print("Aucun compte trouvé.")
        return
    
    print(f"\n{'='*70}")
    print(f"{'Code':<10} {'Nom':<35} {'Type':<10} {'Solde':<15}")
    print(f"{'='*70}")
    for a in accounts:
        print(f"{a.code:<10} {a.name[:35]:<35} {a.account_type:<10} {a.current_balance:>15,.2f}")


def create_account(db, code, name, account_type):
    """Crée un nouveau compte"""
    account = Account(
        code=code,
        name=name,
        account_type=account_type
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    print(f"✓ Compte {code} - {name} créé")
    return account


def show_account(db, account_id):
    """Affiche les détails d'un compte"""
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        print(f"Compte {account_id} non trouvé.")
        return
    
    print(f"\n{'='*60}")
    print(f"COMPTE: {account.code} - {account.name}")
    print(f"{'='*60}")
    print(f"Type:        {account.account_type}")
    print(f"Solde:       {account.current_balance:,.2f} {account.currency}")
    print(f"Actif:       {'Oui' if account.is_active else 'Non'}")
    print(f"Analytique:  {'Oui' if account.is_analytic else 'Non'}")


def list_journal_entries(db):
    """Liste les écritures comptables"""
    entries = db.query(JournalEntry).order_by(JournalEntry.date.desc()).all()
    if not entries:
        print("Aucune écriture trouvée.")
        return
    
    print(f"\n{'='*70}")
    print(f"{'N°':<10} {'Date':<12} {'Libellé':<30} {'Débit':<12} {'Crédit':<12}")
    print(f"{'='*70}")
    for e in entries:
        print(f"{e.entry_number:<10} {str(e.date):<12} {e.description[:30]:<30} {e.total_debit:>12,.2f} {e.total_credit:>12,.2f}")


def create_journal_entry(db, description, reference):
    """Crée une nouvelle écriture comptable"""
    # Générer le numéro d'écriture
    count = db.query(JournalEntry).count()
    entry_number = f"JE-{datetime.now().year}-{count+1:05d}"
    
    entry = JournalEntry(
        entry_number=entry_number,
        date=datetime.now().date(),
        description=description,
        reference=reference
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    print(f"✓ Écriture {entry_number} créée")
    return entry


def stats(db):
    """Affiche les statistiques comptables"""
    total_accounts = db.query(Account).count()
    active_accounts = db.query(Account).filter(Account.is_active == True).count()
    
    total_entries = db.query(JournalEntry).count()
    posted_entries = db.query(JournalEntry).filter(JournalEntry.is_posted == True).count()
    
    # Calcul des totaux par type
    actif_total = db.query(Account).filter(Account.account_type == "actif").all()
    passif_total = db.query(Account).filter(Account.account_type == "passif").all()
    charge_total = db.query(Account).filter(Account.account_type == "charge").all()
    produit_total = db.query(Account).filter(Account.account_type == "produit").all()
    
    actif_sum = sum(a.current_balance for a in actif_total)
    passif_sum = sum(a.current_balance for a in passif_total)
    
    print(f"\n{'='*50}")
    print(f"STATISTIQUES COMPTABLES")
    print(f"{'='*50}")
    print(f"Comptes total:       {total_accounts}")
    print(f"Comptes actifs:     {active_accounts}")
    print(f"Écritures:          {total_entries}")
    print(f"Écritures postées:  {posted_entries}")
    print(f"\nTotaux:")
    print(f"  Actif:   {actif_sum:,.2f}")
    print(f"  Passif:  {passif_sum:,.2f}")
    print(f"{'='*50}")


def main():
    parser = argparse.ArgumentParser(description="CLI Comptabilité")
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("init", help="Initialiser la base de données")
    
    acc_parser = subparsers.add_parser("accounts", help="Gestion des comptes")
    acc_parser.add_argument("--list", action="store_true")
    acc_parser.add_argument("--show", type=int)
    acc_parser.add_argument("--create", nargs=3, metavar=("CODE", "NOM", "TYPE"))
    
    je_parser = subparsers.add_parser("entries", help="Gestion des écritures")
    je_parser.add_argument("--list", action="store_true")
    je_parser.add_argument("--create", nargs=2, metavar=("DESCRIPTION", "REFERENCE"))
    
    subparsers.add_parser("stats", help="Statistiques")
    
    args = parser.parse_args()
    db = SessionLocal()
    
    try:
        if args.command == "init":
            init_db()
        elif args.command == "accounts":
            if args.list:
                list_accounts(db)
            elif args.show:
                show_account(db, args.show)
            elif args.create:
                create_account(db, args.create[0], args.create[1], args.create[2])
            else:
                list_accounts(db)
        elif args.command == "entries":
            if args.list:
                list_journal_entries(db)
            elif args.create:
                create_journal_entry(db, args.create[0], args.create[1])
            else:
                list_journal_entries(db)
        elif args.command == "stats":
            stats(db)
        else:
            parser.print_help()
    finally:
        db.close()


if __name__ == "__main__":
    main()
