"""
Configuration du module librairie

Ce module contient la configuration du Projet
pour le module de gestion de librairie.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""

# Configuration du module librairie

# Paramètres de configuration
MODULE_NAME = "librairie"
MODULE_VERSION = "1.0.0"

# Types de membres
MEMBER_TYPES = [
    "standard",
    "premium",
    "etudiant",
    "famille",
    "institution"
]

# Statuts de membre
MEMBER_STATUS = [
    "actif",
    "suspendu",
    "expire",
    "resilie"
]

# Statuts des prêts
LOAN_STATUS = [
    "actif",
    "renouvele",
    "termine",
    "en_retard",
    "perdu"
]

# Types de documents
DOCUMENT_TYPES = [
    "livre",
    "revue",
    "journal",
    "mémoire",
    "cd_dvd",
    "autre"
]

# Genres littéraires
GENRES = [
    "roman",
    "nouvelle",
    "poesie",
    "theatre",
    "essai",
    "biographie",
    "histoire",
    "science_fiction",
    "policier",
    "enfant",
    "adolescent",
    "manuel",
    "dictionnaire"
]

# Statuts des documents
DOCUMENT_STATUS = [
    "disponible",
    "emprunte",
    "reserve",
    "maintenance",
    "perdu"
]

# Types d'amendes
FINE_TYPES = [
    "retard",
    "dommage",
    "perte"
]

# Durée de prêt par type de membre (en jours)
LOAN_DURATIONS = {
    "standard": 14,
    "premium": 21,
    "etudiant": 14,
    "famille": 14,
    "institution": 30
}

# Limites d'emprunt par type
BORROWING_LIMITS = {
    "standard": 3,
    "premium": 5,
    "etudiant": 2,
    "famille": 8,
    "institution": 20
}

# Frais de membership (annuel en XOF)
MEMBERSHIP_FEES = {
    "standard": 60000,
    "premium": 120000,
    "etudiant": 30000,
    "famille": 180000,
    "institution": 300000
}

# Configuration des amendes
FINE_CONFIG = {
    "late_fee_per_day": 200,
    "damage_fees": {
        "legers": 1000,
        "moyens": 5000,
        "graves": 15000,
        "perdu": 25000
    }
}

# Rôles et permissions
ROLE_PERMISSIONS = {
    "admin_librairie": [
        "book_manage",
        "member_manage",
        "loan_manage",
        "report_generate"
    ],
    "bibliothecaire": [
        "book_read",
        "member_create",
        "loan_create",
        "loan_return"
    ],
    "membre": [
        "book_search",
        "loan_request"
    ]
}

# Intégrations
INTEGRATIONS = {
    "accounting": {
        "enabled": True
    }
}

# Performance
PERFORMANCE_CONFIG = {
    "max_results": 50
}

# Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "file": "logs/librairie.log",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}
