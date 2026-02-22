"""
API Routes pour les transactions

Ce module définit les routes API pour la gestion des transactions.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime


router = APIRouter(prefix="/transactions", tags=["transactions"])


# Mock data pour les tests
MOCK_ACCOUNTS = [
    {"id": 1, "code": "401", "name": "Fournisseurs", "account_type": "passif_courant", "balance": 0},
    {"id": 2, "code": "411", "name": "Clients", "account_type": "actif_courant", "balance": 0},
    {"id": 3, "code": "501", "name": "Caisse", "account_type": "tresorerie", "balance": 0},
    {"id": 4, "code": "521", "name": "Banque", "account_type": "tresorerie", "balance": 0},
    {"id": 5, "code": "601", "name": "Achats", "account_type": "charge", "balance": 0},
    {"id": 6, "code": "701", "name": "Ventes", "account_type": "produit", "balance": 0}
]


@router.get("/accounts")
async def get_accounts(
    account_type: str = None,
    search: str = None
):
    """Récupère la liste des comptes"""
    accounts = MOCK_ACCOUNTS
    
    if account_type:
        accounts = [a for a in accounts if a["account_type"] == account_type]
    if search:
        accounts = [a for a in accounts if search.lower() in a["name"].lower()]
    
    return {"accounts": accounts, "total": len(accounts)}


@router.get("/accounts/{account_id}")
async def get_account(account_id: int):
    """Récupère un compte par son ID"""
    for account in MOCK_ACCOUNTS:
        if account["id"] == account_id:
            return account
    
    raise HTTPException(status_code=404, detail="Compte non trouvé")


@router.post("/accounts")
async def create_account(account_data: dict):
    """Crée un nouveau compte"""
    new_account = {
        "id": len(MOCK_ACCOUNTS) + 1,
        **account_data,
        "balance": 0
    }
    MOCK_ACCOUNTS.append(new_account)
    return new_account


@router.get("/")
async def get_transactions(
    journal_type: str = None,
    account_id: int = None,
    start_date: datetime = None,
    end_date: datetime = None
):
    """Récupère la liste des transactions"""
    return {"transactions": [], "total": 0}


@router.post("/")
async def create_transaction(transaction_data: dict):
    """Crée une nouvelle transaction"""
    return {
        "id": 1,
        **transaction_data,
        "status": "validee",
        "created_at": datetime.now()
    }


@router.get("/{transaction_id}")
async def get_transaction(transaction_id: int):
    """Récupère une transaction par son ID"""
    raise HTTPException(status_code=404, detail="Transaction non trouvée")


@router.get("/balance/sheet")
async def get_balance_sheet():
    """Récupère le bilan"""
    return {
        "assets": [],
        "liabilities": [],
        "equity": []
    }


@router.get("/income/statement")
async def get_income_statement():
    """Récupère le compte de résultat"""
    return {
        "revenues": [],
        "expenses": [],
        "net_result": 0
    }
