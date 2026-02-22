# Module de Gestion de Projets - ERP Zone

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![FastAPI](https://img.shields.io/badge/fastapi-0.104.1-red)
![License](https://img.shields.io/badge/license-MIT-yellow)

## 📋 Description

Ce module fait partie du système ERP Zone et fournit une API REST complète pour la **gestion de projets**, de **tâches** et d'**équipes**. Il permet de gérer le cycle de vie complet d'un projet, de la planification à la livraison.

### Fonctionnalités principales

- ✅ **Gestion des projets** - CRUD complet avec statuts, priorités, budgets
- ✅ **Gestion des tâches** - Sous-tâches, assignations, suivi du temps
- ✅ **Équipe projet** - Membres, rôles et responsabilités
- ✅ **Jalons (Milestones)** - Suivi des étapes clés
- ✅ **Documents** - Gestion des fichiers associés aux projets
- ✅ **Tableaux Kanban** - Vue tâches par statut
- ✅ **Statistiques** - Tableaux de bord et métriques
- ✅ **Recherche** - Recherche avancee par nom et description

---

## 🏗 Architecture

```
gestion_projets/
├── app/
│   ├── api/
│   │   └── routes/          # Endpoints API
│   ├── core/
│   │   ├── config.py        # Configuration
│   │   └── database.py      # Connexion BD
│   ├── models/              # Modèles SQLAlchemy
│   ├── schemas/            # Schémas Pydantic
│   └── database/
│       └── seeds.py         # Données initiales
├── tests/                   # Tests unitaires
├── cli.py                   # Interface CLI
├── main.py                  # Point d'entrée
├── Dockerfile              # Conteneurisation
├── docker-compose.yml      # Orchestration
└── requirements.txt        # Dépendances
```

---

## 🚀 Installation

### Prérequis

- Python 3.11+
- PostgreSQL 15+ (optionnel, SQLite pour le développement)
- Docker & Docker Compose (optionnel)

### Installation locale

```bash
# Cloner le projet
cd gestion_projets

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configuration des variables d'environnement
cp .env.example .env
# Éditer .env avec vos paramètres

# Initialiser la base de données
python cli.py init

# Générer des données de test (optionnel)
python -m app.database.seeds --seed

# Démarrer le serveur
uvicorn main:app --reload
```

### Avec Docker

```bash
# Construction de l'image
docker build -t erp-zone-projects .

# Avec Docker Compose
docker-compose up -d
```

---

## 📖 Utilisation

### API REST

Le serveur est accessible à l'adresse: **http://localhost:8000**

#### Documentation interactive

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### Endpoints principaux

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/v1/projects/` | Liste des projets |
| POST | `/api/v1/projects/` | Créer un projet |
| GET | `/api/v1/projects/{id}` | Détails d'un projet |
| PUT | `/api/v1/projects/{id}` | Mettre à jour un projet |
| PATCH | `/api/v1/projects/{id}` | Mise à jour partielle |
| DELETE | `/api/v1/projects/{id}` | Supprimer un projet |
| GET | `/api/v1/projects/stats` | Statistiques |
| GET | `/api/v1/projects/search` | Recherche |
| GET | `/api/v1/projects/{id}/details` | Projet avec détails |

### Interface CLI

```bash
# Initialiser la base de données
python cli.py init

# Liste des projets
python cli.py projects --list

# Créer un projet
python cli.py projects --create "Mon Projet"

# Détails d'un projet
python cli.py projects --show 1

# Mettre à jour le statut
python cli.py projects --update-status 1 active

# Liste des tâches
python cli.py tasks --list

# Tâches d'un projet
python cli.py tasks --list --project 1

# Statistiques
python cli.py stats
```

---

## 🧪 Tests

```bash
# Installer les dépendances de test
pip install pytest pytest-cov

# Exécuter tous les tests
pytest tests/ -v

# Avec coverage
pytest tests/ --cov=app --cov-report=html
```

---

## 📝 Modèles de données

### Projet (Project)

| Champ | Type | Description |
|-------|------|-------------|
| id | Integer | Identifiant unique |
| name | String(255) | Nom du projet |
| description | Text | Description détaillée |
| status | String | Statut (planning/active/completed/cancelled/on_hold) |
| priority | String | Priorité (low/medium/high/critical) |
| budget | Float | Budget alloué |
| progress | Integer | Pourcentage d'avancement (0-100) |
| start_date | Date | Date de début |
| end_date | Date | Date de fin prévue |
| actual_end_date | Date | Date de fin réelle |
| is_active | Boolean | Projet actif |

### Tâche (Task)

| Champ | Type | Description |
|-------|------|-------------|
| id | Integer | Identifiant unique |
| name | String(255) | Nom de la tâche |
| project_id | Integer | Projet parent |
| parent_id | Integer | Tâche parente (sous-tâches) |
| assignee_id | Integer | Utilisateur assigné |
| status | String | Statut (todo/in_progress/in_review/done/blocked) |
| priority | String | Priorité |
| progress | Integer | Avancement (0-100) |
| estimated_hours | Float | Heures estimées |
| actual_hours | Float | Heures réelles |
| due_date | Date | Date d'échéance |
| is_blocked | Boolean | Tâche bloquée |
| block_reason | Text | Raison du blocage |

### Jalon (ProjectMilestone)

| Champ | Type | Description |
|-------|------|-------------|
| id | Integer | Identifiant unique |
| name | String(255) | Nom du jalon |
| project_id | Integer | Projet associé |
| due_date | Date | Date d'échéance |
| completed_date | Date | Date de complétion |
| status | String | Statut (pending/in_progress/completed/delayed) |
| is_completed | Boolean | Jalon atteint |
| order | Integer | Ordre d'affichage |

---

## 🔧 Configuration

### Variables d'environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| DATABASE_URL | URL de connexion PostgreSQL | sqlite:///./projects.db |
| SECRET_KEY | Clé secrète pour JWT | dev-secret-key |
| DEBUG | Mode debug | false |
| PROJECT_NAME | Nom du projet | ERP Zone Projects |
| PROJECT_VERSION | Version | 1.0.0 |

### Base de données supportée

- **SQLite** - Pour le développement local
- **PostgreSQL** - Pour la production

---

## 📁 Structure des fichiers

```
gestion_projets/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── projects.py      # Routes projets
│   │       └── tasks.py         # Routes tâches
│   ├── core/
│   │   ├── config.py            # Configuration FastAPI
│   │   └── database.py          # Connexion SQLAlchemy
│   ├── models/
│   │   ├── __init__.py
│   │   ├── project.py           # Modèles projets
│   │   └── task.py              # Modèles tâches
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── project.py           # Schémas projets
│   │   └── task.py              # Schémas tâches
│   └── database/
│       ├── __init__.py
│       └── seeds.py              # Données initiales
├── tests/
│   ├── __init__.py
│   └── test_projects.py         # Tests unitaires
├── .github/
│   └── workflows/
│       └── ci.yml               # Pipeline CI/CD
├── cli.py                       # Interface CLI
├── main.py                      # Point d'entrée
├── Dockerfile                   # Image Docker
├── docker-compose.yml          # Orchestration
└── requirements.txt            # Dépendances Python
```

---

## 🔄 Opérations disponibles

### Projets

- Lister tous les projets avec pagination
- Filtrer par statut, priorité
- Rechercher par nom/description
- Créer, lire, mettre à jour, supprimer
- Archiver un projet
- Voir les statistiques globales

### Tâches

- Lister les tâches d'un projet
- Créer des tâches et sous-tâches
- Assigner des utilisateurs
- Mettre à jour le statut et la progression
- Bloquer/débloquer des tâches
- Ajouter des commentaires
- Suivre le temps passé

### Équipe

- Ajouter des membres à un projet
- Définir les rôles (lead, manager, member)
- Activer/désactiver des membres

### Documents

- Associer des documents aux projets
- Suivre les métadonnées (type, taille)

### Jalons

- Créer des jalons avec dates d'échéance
- Suivre le statut
- Marquer comme terminé

---

## 📄 License

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

---

## 👥 Contributeurs

- Équipe ERP Zone

---

## 📞 Support

Pour toute question ou problème:
- Créer une issue sur GitHub
- Consulter la documentation API à /docs

---

*Document généré automatiquement pour ERP Zone v1.0.0*
