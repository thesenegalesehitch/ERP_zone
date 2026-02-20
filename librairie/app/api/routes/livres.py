"""
Routes API - Gestion des Livres
================================
Endpoints pour la gestion des livres dans la librairie.

Opérations CRUD:
- GET /livres: Liste tous les livres
- GET /livres/{id}: Récupère un livre par ID
- POST /livres: Crée un nouveau livre
- PUT /livres/{id}: Met à jour un livre
- DELETE /livres/{id}: Supprime un livre
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.livre import Livre
from app.schemas.livre import LivreCreate, LivreResponse, LivreUpdate
from app.api.routes.auth import get_current_user

router = APIRouter(prefix="/livres", tag=["Livres"])


@router.get("/", response_model=list[LivreResponse])
def liste_livres(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
):
    """
    Liste tous les livres
    =====================
    Retourne la liste paginée des livres.
    """
    livres = db.query(Livre).offset(skip).limit(limit).all()
    return livres


@router.get("/{livre_id}", response_model=LivreResponse)
def detail_livre(
    livre_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    """
    Détail d'un livre
    =================
    Retourne les détails d'un livre par son ID.
    """
    livre = db.query(Livre).filter(Livre.id == livre_id).first()
    if not livre:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    return livre


@router.post("/", response_model=LivreResponse, status_code=status.HTTP_201_CREATED)
def creer_livre(
    livre: LivreCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Créer un livre
    =============
    Crée un nouveau livre dans le catalogue.
    """
    # Vérifier si l'ISBN existe déjà
    livre_existant = db.query(Livre).filter(Livre.isbn == livre.isbn).first()
    if livre_existant:
        raise HTTPException(status_code=400, detail="ISBN déjà existant")
    
    nouveau_livre = Livre(**livre.model_dump())
    db.add(nouveau_livre)
    db.commit()
    db.refresh(nouveau_livre)
    return nouveau_livre


@router.put("/{livre_id}", response_model=LivreResponse)
def modifier_livre(
    livre_id: int,
    livre_update: LivreUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Modifier un livre
    =================
    Met à jour les informations d'un livre.
    """
    livre = db.query(Livre).filter(Livre.id == livre_id).first()
    if not livre:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    
    update_data = livre_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(livre, key, value)
    
    db.commit()
    db.refresh(livre)
    return livre


@router.delete("/{livre_id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_livre(
    livre_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Supprimer un livre
    ==================
    Supprime un livre du catalogue.
    """
    livre = db.query(Livre).filter(Livre.id == livre_id).first()
    if not livre:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    
    db.delete(livre)
    db.commit()
    return None
