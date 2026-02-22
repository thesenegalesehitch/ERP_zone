"""
Configuration du module gestion des projets

Ce module contient la configuration du projet
pour le module de gestion de projets.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""

# Configuration du module gestion_projets

# Paramètres de configuration
MODULE_NAME = "gestion_projets"
MODULE_VERSION = "1.0.0"

# Configuration de la base de données
DATABASE_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "name": "erp_gestion_projets",
    "pool_size": 10,
    "max_overflow": 20
}

# Configuration du cache
CACHE_CONFIG = {
    "enabled": True,
    "ttl": 300,
    "prefix": "gp_"
}

# Configuration des notifications
NOTIFICATION_CONFIG = {
    "email_enabled": True,
    "sms_enabled": False,
    "in_app_enabled": True,
    "template_path": "templates/notifications/"
}

# Configuration des rôles
ROLE_PERMISSIONS = {
    "admin": [
        "project_create",
        "project_read",
        "project_update",
        "project_delete",
        "task_create",
        "task_read",
        "task_update",
        "task_delete",
        "milestone_create",
        "milestone_read",
        "milestone_update",
        "milestone_delete",
        "report_generate"
    ],
    "chef_projet": [
        "project_create",
        "project_read",
        "project_update",
        "task_create",
        "task_read",
        "task_update",
        "milestone_create",
        "milestone_read",
        "milestone_update",
        "report_generate"
    ],
    "membre_equipe": [
        "project_read",
        "task_create",
        "task_read",
        "task_update",
        "milestone_read"
    ],
    "client": [
        "project_read",
        "task_read",
        "milestone_read"
    ]
}

# Statuts de projet
PROJECT_STATUS = [
    "planifie",
    "en_cours",
    "en_pause",
    "termine",
    "annule"
]

# Priorités de tâche
TASK_PRIORITIES = [
    "basse",
    "moyenne",
    "haute",
    "urgente"
]

# Statuts de tâche
TASK_STATUS = [
    "a_faire",
    "en_cours",
    "en_revision",
    "terminee",
    "bloquee"
]

# Configuration des emails
EMAIL_CONFIG = {
    "smtp_host": "smtp.example.com",
    "smtp_port": 587,
    "smtp_user": "noreply@erp.sn",
    "smtp_password": "",
    "from_name": "Gestion de Projets ERP",
    "use_tls": True
}

# Configuration des intégrations
INTEGRATIONS = {
    "slack": {
        "enabled": False,
        "webhook_url": ""
    },
    "github": {
        "enabled": False,
        "api_token": ""
    },
    "jira": {
        "enabled": False,
        "api_url": "",
        "api_token": ""
    }
}

# Paramètres de performance
PERFORMANCE_CONFIG = {
    "max_tasks_per_page": 50,
    "default_timeout": 30,
    "enable_compression": True,
    "enable_caching": True
}

# Configuration de l'authentification
AUTH_CONFIG = {
    "jwt_secret": "your-secret-key-here",
    "jwt_algorithm": "HS256",
    "access_token_expire_minutes": 60,
    "refresh_token_expire_days": 7
}

# Configuration du logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "logs/gestion_projets.log",
    "max_bytes": 10485760,
    "backup_count": 5
}

# Paramètres par défaut
DEFAULT_SETTINGS = {
    "currency": "XOF",
    "date_format": "%d/%m/%Y",
    "time_format": "%H:%M",
    "timezone": "Africa/Dakar",
    "language": "fr"
}

# Configuration des notifications par défaut
DEFAULT_NOTIFICATIONS = {
    "project_created": {
        "enabled": True,
        "roles": ["chef_projet", "admin"]
    },
    "task_assigned": {
        "enabled": True,
        "roles": ["membre_equipe"]
    },
    "milestone_achieved": {
        "enabled": True,
        "roles": ["chef_projet", "admin", "client"]
    },
    "deadline_approaching": {
        "enabled": True,
        "roles": ["chef_projet", "membre_equipe"]
    }
}
