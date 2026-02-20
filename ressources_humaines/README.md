# Module Ressources Humaines

## Description
Module de gestion des ressources humaines pour ERP Zone.

## Fonctionnalités
- Gestion des employés
- Gestion des départements
- Gestion des rôles
- Gestion des demandes de congés
- Authentification JWT
- Système RBAC (Role-Based Access Control)

## Modèles de données
- **User**: Utilisateurs du système
- **Employee**: Informations employees
- **Department**: Départements
- **Role**: Rôles utilisateurs
- **LeaveRequest**: Demandes de congès

## Routes API

### Authentification
- `POST /auth/register` - Inscription
- `POST /auth/token` - Connexion
- `GET /auth/me` - Profil utilisateur

### Employés
- `GET /employees` - Liste des employés
- `POST /employees` - Créer un employé
- `GET /employees/{id}` - Détail employé
- `PUT /employees/{id}` - Modifier employé
- `DELETE /employees/{id}` - Supprimer employé

### Départements
- `GET /departments` - Liste des départements
- `POST /departments` - Créer un département
- `GET /departments/{id}` - Détail département
- `PUT /departments/{id}` - Modifier département
- `DELETE /departments/{id}` - Supprimer département

### Rôles
- `GET /roles` - Liste des rôles
- `POST /roles` - Créer un rôle

## Démarrage

```bash
cd ressources_humaines
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Technologies
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication
