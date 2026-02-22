# Module Ressources Humaines - ERP Zone

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![FastAPI](https://img.shields.io/badge/fastapi-0.104.1-red)

## 📋 Description

Module complet de gestion des ressources humaines pour ERP Zone. Ce module fournit une API REST pour gérer les employés, départements, rôles, congés, présences et paie.

### Fonctionnalités principales

- ✅ **Gestion des employés** - CRUD complet avec informations personnelles et professionnelles
- ✅ **Gestion des départements** - Structure organisationnelle
- ✅ **Gestion des rôles** - Système RBAC
- ✅ **Gestion des congés** - Demandes, approbations, soldes
- ✅ **Suivi des présences** - Pointage, présences/absences
- ✅ **Gestion de la paie** - Salaires, primes, deductions
- ✅ **Authentification JWT** - Sécurité avancée
- ✅ **Système RBAC** - Contrôle d'accès basé sur les rôles

---

## 🏗 Architecture

```
ressources_humaines/
├── app/
│   ├── api/
│   │   ├── routes/          # Endpoints API
│   │   └── middleware/      # Middleware (erreur, logging)
│   ├── core/
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # Connexion BD
│   │   ├── security.py      # Sécurité
│   │   └── logging_config.py # Logging
│   ├── models/              # Modèles SQLAlchemy
│   └── schemas/            # Schémas Pydantic
├── tests/                   # Tests unitaires
├── cli.py                   # Interface CLI
├── main.py                  # Point d'entrée
├── Dockerfile              # Conteneurisation
├── docker-compose.yml      # Orchestration
└── requirements.txt        # Dépendances
```

---

## 🚀 Installation

```bash
# Installation des dépendances
pip install -r requirements.txt

# Configuration
cp .env.example .env

# Initialisation de la base de données
python cli.py init

# Démarrage du serveur
uvicorn main:app --reload --port 8002
```

---

## 📖 Utilisation

### API REST

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/employees/` | Liste des employés |
| POST | `/employees/` | Créer un employé |
| GET | `/employees/{id}` | Détails employé |
| PUT | `/employees/{id}` | Modifier employé |
| DELETE | `/employees/{id}` | Supprimer employé |

### CLI

```bash
# Liste des employés
python cli.py employees --list

# Statistiques RH
python cli.py stats
```

---

## 📝 Modèles de données

### Employee

| Champ | Type | Description |
|-------|------|-------------|
| first_name | String | Prénom |
| last_name | String | Nom |
| position | String | Poste |
| hire_date | Date | Date d'embauche |
| salary | Float | Salaire |
| department_id | Integer | Département |

### LeaveRequest

| Champ | Type | Description |
|-------|------|-------------|
| employee_id | Integer | Employé |
| leave_type | Enum | Type de congé |
| start_date | Date | Date de début |
| end_date | Date | Date de fin |
| status | Enum | Statut |

---

## 🧪 Tests

```bash
pytest tests/ -v
```

---

## 📄 License

MIT
