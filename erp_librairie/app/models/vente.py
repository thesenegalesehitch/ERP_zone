"""
Modèle de données - Vente
=========================
Représente les ventes de livres aux clients.

Attributs:
- id: Identifiant unique
- client_id: Lien vers le client
- livre_id: Lien vers le livre vendu
- quantite: Quantité de livres vendus
- prix_unitaire: Prix au moment de la vente
- montant_total: Montant total de la vente
- date_vente: Date de la vente
- created_at: Date de création
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Vente(Base):
    """Modèle Vente - Ventes de livres"""
    
    __tablename__ = "ventes"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    livre_id = Column(Integer, ForeignKey("livres.id"), nullable=False)
    quantite = Column(Integer, nullable=False, default=1)
    prix_unitaire = Column(Float, nullable=False)
    montant_total = Column(Float, nullable=False)
    date_vente = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relations
    client = relationship("Client", back_populates="ventes")
    livre = relationship("Livre", back_populates="ventes")
