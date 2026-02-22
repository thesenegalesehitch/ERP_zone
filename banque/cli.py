#!/usr/bin/env python3
"""
Script CLI pour le module Banque

Interface en ligne de commande pour gérer les clients,
comptes bancaires et transactions.
"""
import argparse
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.client import ClientBancaire
from app.models.compte import Compte, TypeCompte
from app.models.transaction import Transaction, TypeTransaction


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./banque.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialise la base de données"""
    from app.core.database import Base
    Base.metadata.create_all(bind=engine)
    print("✓ Base de données initialisée")


def list_clients(db):
    """Liste tous les clients"""
    clients = db.query(ClientBancaire).all()
    if not clients:
        print("Aucun client trouvé.")
        return
    
    print(f"\n{'='*70}")
    print(f"{'ID':<4} {'Nom':<25} {'Email':<30} {'Téléphone':<15}")
    print(f"{'='*70}")
    for c in clients:
        print(f"{c.id:<4} {c.nom:<25} {c.email:<30} {c.telephone or 'N/A':<15}")


def list_comptes(db, client_id=None):
    """Liste les comptes bancaires"""
    if client_id:
        comptes = db.query(Compte).filter(Compte.client_id == client_id).all()
    else:
        comptes = db.query(Compte).all()
    
    if not comptes:
        print("Aucun compte trouvé.")
        return
    
    print(f"\n{'='*80}")
    print(f"{'ID':<4} {'Numéro':<15} {'Type':<12} {'Solde':<15} {'Client':<20}")
    print(f"{'='*80}")
    for c in compas:
        client = db.query(ClientBancaire).filter(ClientBancaire.id == c.client_id).first()
        client_nom = client.nom[:20] if client else "N/A"
        print(f"{c.id:<4} {c.numero_compte:<15} {c.type_compte.value:<12} {c.solde:>15,.2f} {client_nom:<20}")


def list_transactions(db, compte_id=None):
    """Liste les transactions"""
    if compte_id:
        transactions = db.query(Transaction).filter(
            Transaction.compte_id == compte_id
        ).order_by(Transaction.date_transaction.desc()).all()
    else:
        transactions = db.query(Transaction).order_by(Transaction.date_transaction.desc()).all()
    
    if not transactions:
        print("Aucune transaction trouvée.")
        return
    
    print(f"\n{'='*80}")
    print(f"{'ID':<4} {'Date':<20} {'Type':<12} {'Montant':<15} {'Description':<30}")
    print(f"{'='*80}")
    for t in transactions:
        print(f"{t.id:<4} {str(t.date_transaction):<20} {t.type_transaction.value:<12} {t.montant:>15,.2f} {t.description[:30] if t.description else 'N/A':<30}")


def create_client(db, nom, email, telephone, adresse):
    """Crée un nouveau client"""
    client = ClientBancaire(
        nom=nom,
        email=email,
        telephone=telephone,
        adresse=adresse
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    print(f"✓ Client {nom} créé avec ID: {client.id}")
    return client


def create_compte(db, numero, type_compte, client_id, solde_initial=0):
    """Crée un nouveau compte"""
    compte = Compte(
        numero_compte=numero,
        type_compte=TypeCompte(type_compte),
        client_id=client_id,
        solde=solde_initial
    )
    db.add(compte)
    db.commit()
    db.refresh(compte)
    print(f"✓ Compte {numero} créé")
    return compte


def create_transaction(db, compte_id, type_transaction, montant, description=""):
    """Crée une nouvelle transaction"""
    transaction = Transaction(
        compte_id=compte_id,
        type_transaction=TypeTransaction(type_transaction),
        montant=montant,
        description=description
    )
    db.add(transaction)
    
    # Mettre à jour le solde du compte
    compte = db.query(Compte).filter(Compte.id == compte_id).first()
    if compte:
        if type_transaction == "credit":
            compte.solde += montant
        elif type_transaction == "debit":
            compte.solde -= montant
    
    db.commit()
    db.refresh(transaction)
    print(f"✓ Transaction créée: {type_transaction} de {montant}")
    return transaction


def stats(db):
    """Affiche les statistiques bancaires"""
    total_clients = db.query(ClientBancaire).count()
    total_comptes = db.query(Compte).count()
    comptes_actifs = db.query(Compte).filter(Compte.est_actif == 1).count()
    total_transactions = db.query(Transaction).count()
    
    total_solde = db.query(Compte).filter(Compte.est_actif == 1).all()
    somme_solde = sum(c.solde for c in total_solde)
    
    print(f"\n{'='*50}")
    print(f"STATISTIQUES BANCAIRES")
    print(f"{'='*50}")
    print(f"Clients:            {total_clients}")
    print(f"Comptes total:     {total_comptes}")
    print(f"Comptes actifs:    {comptes_actifs}")
    print(f"Transactions:       {total_transactions}")
    print(f"Somme des soldes:  {somme_solde:,.2f}")
    print(f"{'='*50}")


def main():
    parser = argparse.ArgumentParser(description="CLI Banque")
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("init", help="Initialiser la base de données")
    
    client_parser = subparsers.add_parser("clients", help="Gestion des clients")
    client_parser.add_argument("--list", action="store_true")
    client_parser.add_argument("--create", nargs=4, metavar=("NOM", "EMAIL", "TEL", "ADRESSE"))
    
    compte_parser = subparsers.add_parser("comptes", help="Gestion des comptes")
    compte_parser.add_argument("--list", action="store_true")
    compte_parser.add_argument("--client", type=int, help="Filtrer par client")
    compte_parser.add_argument("--create", nargs=4, metavar=("NUMERO", "TYPE", "CLIENT_ID", "SOLDE"))
    
    trans_parser = subparsers.add_parser("transactions", help="Gestion des transactions")
    trans_parser.add_argument("--list", action="store_true")
    trans_parser.add_argument("--compte", type=int, help="Filtrer par compte")
    trans_parser.add_argument("--create", nargs=4, metavar=("COMPTE_ID", "TYPE", "MONTANT", "DESCRIPTION"))
    
    subparsers.add_parser("stats", help="Statistiques")
    
    args = parser.parse_args()
    db = SessionLocal()
    
    try:
        if args.command == "init":
            init_db()
        elif args.command == "clients":
            if args.list:
                list_clients(db)
            elif args.create:
                create_client(db, args.create[0], args.create[1], args.create[2], args.create[3])
            else:
                list_clients(db)
        elif args.command == "comptes":
            if args.list:
                list_comptes(db, args.client if hasattr(args, 'client') else None)
            elif args.create:
                create_compte(db, args.create[0], args.create[1], int(args.create[2]), float(args.create[3]))
            else:
                list_comptes(db)
        elif args.command == "transactions":
            if args.list:
                list_transactions(db, args.compte if hasattr(args, 'compte') else None)
            elif args.create:
                create_transaction(db, int(args.create[0]), args.create[1], float(args.create[2]), args.create[3])
            else:
                list_transactions(db)
        elif args.command == "stats":
            stats(db)
        else:
            parser.print_help()
    finally:
        db.close()


if __name__ == "__main__":
    main()
