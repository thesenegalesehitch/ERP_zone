"""
API Routes pour les livres

Ce module définit les routes API pour la gestion de la librairie.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime


router = APIRouter(prefix="/livres", tags=["librairie"])


# Mock data pour les tests
MOCK_BOOKS = [
    {
        "id": 1,
        "title": "Les Misérables",
        "author": "Victor Hugo",
        "isbn": "978-2-07-040078-3",
        "publisher": "Gallimard",
        "publication_year": 1862,
        "genre": "roman",
        "quantity": 5,
        "available": 3,
        "price": 2500,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]


@router.get("/")
async def get_books(
    genre: str = None,
    available_only: bool = None,
    search: str = None
):
    """Récupère la liste des livres"""
    books = MOCK_BOOKS
    
    if genre:
        books = [b for b in books if b["genre"] == genre]
    if available_only:
        books = [b for b in books if b["available"] > 0]
    if search:
        books = [b for b in books if search.lower() in b["title"].lower() or search.lower() in b["author"].lower()]
    
    return {"books": books, "total": len(books)}


@router.get("/{book_id}")
async def get_book(book_id: int):
    """Récupère un livre par son ID"""
    for book in MOCK_BOOKS:
        if book["id"] == book_id:
            return book
    
    raise HTTPException(status_code=404, detail="Livre non trouvé")


@router.post("/")
async def create_book(book_data: dict):
    """Crée un nouveau livre"""
    new_book = {
        "id": len(MOCK_BOOKS) + 1,
        **book_data,
        "available": book_data.get("quantity", 1),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    MOCK_BOOKS.append(new_book)
    return new_book


@router.put("/{book_id}")
async def update_book(book_id: int, book_data: dict):
    """Met à jour un livre"""
    for i, book in enumerate(MOCK_BOOKS):
        if book["id"] == book_id:
            MOCK_BOOKS[i] = {
                **book,
                **book_data,
                "updated_at": datetime.now()
            }
            return MOCK_BOOKS[i]
    
    raise HTTPException(status_code=404, detail="Livre non trouvé")


# Routes pour les prêts
MOCK_LOANS = []


@router.get("/prets/")
async def get_loans(member_id: int = None, status: str = None):
    """Récupère la liste des prêts"""
    loans = MOCK_LOANS
    
    if member_id:
        loans = [l for l in loans if l["member_id"] == member_id]
    if status:
        loans = [l for l in loans if l["status"] == status]
    
    return {"loans": loans, "total": len(loans)}


@router.post("/prets/")
async def create_loan(loan_data: dict):
    """Crée un nouveau prêt"""
    new_loan = {
        "id": len(MOCK_LOANS) + 1,
        **loan_data,
        "status": "actif",
        "loan_date": datetime.now(),
        "due_date": datetime.now(),
        "renewal_count": 0,
        "created_at": datetime.now()
    }
    MOCK_LOANS.append(new_loan)
    return new_loan


@router.post("/prets/{loan_id}/return")
async def return_book(loan_id: int):
    """Retourne un livre"""
    for i, loan in enumerate(MOCK_LOANS):
        if loan["id"] == loan_id:
            MOCK_LOANS[i]["status"] = "termine"
            MOCK_LOANS[i]["return_date"] = datetime.now()
            return MOCK_LOANS[i]
    
    raise HTTPException(status_code=404, detail="Prêt non trouvé")


# Routes pour les membres
MOCK_MEMBERS = []


@router.get("/membres/")
async def get_members(
    membership_type: str = None,
    status: str = None
):
    """Récupère la liste des membres"""
    members = MOCK_MEMBERS
    
    if membership_type:
        members = [m for m in members if m["membership_type"] == membership_type]
    if status:
        members = [m for m in members if m["status"] == status]
    
    return {"members": members, "total": len(members)}


@router.post("/membres/")
async def create_member(member_data: dict):
    """Crée un nouveau membre"""
    new_member = {
        "id": len(MOCK_MEMBERS) + 1,
        **member_data,
        "status": "actif",
        "membership_start": datetime.now(),
        "membership_end": datetime.now(),
        "created_at": datetime.now()
    }
    MOCK_MEMBERS.append(new_member)
    return new_member
