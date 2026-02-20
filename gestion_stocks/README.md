# Module Gestion des Stocks

## Description
Module de gestion des stocks et inventaires pour ERP Zone.

## Fonctionnalités
- Gestion des produits
- Gestion des catégories
- Gestion des fournisseurs
- Suivi des stocks
- Mouvements de stock

## Modèles de données
- **Product**: Produits
- **Category**: Catégories de produits
- **Supplier**: Fournisseurs
- **Stock**: Niveaux de stock
- **StockMovement**: Mouvements de stock

## Démarrage

```bash
cd gestion_stocks
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

## Technologies
- FastAPI
- SQLAlchemy
- PostgreSQL
