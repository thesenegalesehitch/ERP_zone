# Module Comptabilité

## Description
Module de gestion comptable pour ERP Zone.

## Fonctionnalités
- Plan comptable
- Transactions financières
- Gestion des factures
- Paiements et encaissements

## Modèles de données
- **Account**: Comptes comptable
- **Transaction**: Transactions
- **Invoice**: Factures
- **Payment**: Paiements

## Démarrage

```bash
cd comptabilite
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
```
