"""
Modèle de données - Livre
=========================
Représentation de la table 'livres' en base de données.
Un livre possède un titre, un ISBN, un prix, un stock,
une catégorie et peut être écrit par plusieurs auteurs.

Attributs:
- id: Identifiant unique (clé primaire)
- titre: Titre du livre
- isbn: Numéro ISBN unique
- prix: Prix de vente en euros
- stock_quantite: Quantité en stock
- categorie_id: Lien vers la catégorie
- date_publication: Date de publication
- description: Résumé du livre
- est_actif: Livre disponible à la vente
- created_at: Date de création
- updated_at: Date de modification
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Livre(Base):
    """
    Modèle Livre
    ============
    Représente un livre dans le catalogue de la librairie.
    """
    
    __tablename__ = "livres"

    # Clé primaire auto-incrémentée
    id = Column(Integer, primary_key=True, index=True)
    
    # Titre du livre (obligatoire, max 255 caractères)
    titre = Column(String(255), nullable=False, index=True)
    
    # ISBN unique (obligatoire)
    isbn = Column(String(13), unique=True, nullable=False, index=True)
    
    # Prix de vente en euros
    prix = Column(Float, nullable=False, default=0.0)
    
    # Quantité disponible en stock
    stock_quantite = Column(Integer, nullable=False, default=0)
    
    # ID de la catégorie (clé étrangère)
    categorie_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    # Date de publication du livre
    date_publication = Column(DateTime, nullable=True)
    
    # Résumé/description du livre
    description = Column(Text, nullable=True)
    
    # Indique si le livre est disponible à la vente
    est_actif = Column(Boolean, default=True, nullable=False)
    
    # Date de création automatique
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Date de modification automatique
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relations
    categorie = relationship("Categorie", back_populates="livres")
    auteurs = relationship("Auteur", secondary="livre_auteurs", back_populates="livres")
    ventes = relationship("Vente", back_populates="livre")
