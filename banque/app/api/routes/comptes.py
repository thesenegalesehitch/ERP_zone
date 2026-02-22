"""
API Routes pour les comptes bancaires

Ce module définit les routes API pour la gestion des comptes bancaires.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime


router = APIRouter(prefix="/comptes", tags=["comptes"])


# Mock data pour les tests
MOCK_ACCOUNTS = [
    {
        "id": 1,
        "account_number": "SN012345678901234567890",
        "account_name": "Compte Courant Principal",
        "account_type": "compte_courant",
        "balance": 5000000,
        "currency": "XOF",
        "overdraft_limit": 500000,
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]


@router.get("/")
async def get_accounts(
    account_type: str = None,
    is_active: bool = None
):
    """Récupère la liste des comptes"""
    accounts = MOCK_ACCOUNTS
    
    if account_type:
        accounts = [a for a in accounts if a["account_type"] == account_type]
    if is_active is not None:
        accounts = [a for a in accounts if a["is_active"] == is_active]
    
    return {"accounts": accounts, "total": len(accounts)}


@router.get("/{account_id}")
async def get_account(account_id: int):
    """Récupère un compte par son ID"""
    for account in MOCK_ACCOUNTS:
        if account["id"] == account_id:
            return account
    
    raise HTTPException(status_code=404, detail="Compte non trouvé")


@router.post("/")
async def create_account(account_data: dict):
    """Crée un nouveau compte"""
    new_account = {
        "id": len(MOCK_ACCOUNTS) + 1,
        **account_data,
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    MOCK_ACCOUNTS.append(new_account)
    return new_account


@router.put("/{account_id}")
async def update_account(account_id: int, account_data: dict):
    """Met à jour un compte"""
    for i, account in enumerate(MOCK_ACCOUNTS):
        if account["id"] == account_id:
            MOCK_ACCOUNTS[i] = {
                **account,
                **account_data,
                "updated_at": datetime.now()
            }
            return MOCK_ACCOUNTS[i]
    
    raise HTTPException(status_code=404, detail="Compte non trouvé")


@router.post("/{account_id}/transactions")
async def create_transaction(account_id: int, transaction_data: dict):
    """Crée une transaction"""
    return {
        "id": 1,
        "account_id": account_id,
        **transaction_data,
        "balance_after": 0,
        "status": "validee",
        "created_at": datetime.now()
    }


@router.get("/{account_id}/transactions")
async def get_transactions(account_id: int):
    """Récupère les transactions d'un compte"""
    return {"transactions": [], "total": 0}


@router.post("/transferts")
async def create_transfer(transfer_data: dict):
    """Crée un virement"""
    return {
        "id": 1,
        **transfer_data,
        "status": "valide",
        "created_at": datetime.now()
    }


@router.get("/{account_id}/solde")
async def get_balance(account_id: int):
    """Récupère le solde d'un compte"""
    for account in MOCK_ACCOUNTS:
        if account["id"] == account_id:
            return {
                "account_id": account_id,
                "balance": account["balance"],
                "overdraft_limit": account["overdraft_limit"],
                "available": account["balance"] + account["overdraft_limit"]
            }
    
    raise HTTPException(status_code=404, detail="Compte non trouvé")


# Routes pour les prêts
MOCK_LOANS = []


@router.get("/prets/")
async def get_loans():
    """Récupère la liste des prêts"""
    return {"loans": [], "total": 0}


@router.post("/prets/")
async def create_loan(loan_data: dict):
    """Crée un nouveau prêt"""
    new_loan = {
        "id": len(MOCK_LOANS) + 1,
        **loan_data,
        "status": "en_cours",
        "paid_amount": 0,
        "created_at": datetime.now()
    }
    MOCK_LOANS.append(new_loan)
    return new_loan
