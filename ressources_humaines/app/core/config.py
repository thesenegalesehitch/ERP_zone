"""
Configuration du module ressources humaines

Ce module contient la configuration du projet
pour le module de ressources humaines.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""

# Configuration du module ressources_humaines

# Paramètres de configuration
MODULE_NAME = "ressources_humaines"
MODULE_VERSION = "1.0.0"

# Types de contrat
CONTRACT_TYPES = [
    "cdi",  # Contrat à Durée Indéterminée
    "cdd",  # Contrat à Durée Déterminée
    " Interim",
    "apprentissage",
    "stage",
    "consultant"
]

# Types de rémunération
SALARY_TYPES = [
    "mensuel",
    "horaire",
    "journalier",
    "forfaitaire"
]

# Modes de paiement
PAYMENT_MODES = [
    "virement_bancaire",
    "cheque",
    "especes",
    "mobile_money"
]

# Congés types
LEAVE_TYPES = [
    "conge_annuel",
    "conge_maladie",
    "conge_maternite",
    "conge_paternite",
    "conge_sans_solde",
    "conge_formation",
    "conge_exceptionnel",
    "rtt"
]

# Statuts des employés
EMPLOYEE_STATUS = [
    "actif",
    "inactif",
    "conge",
    "maladie",
    " suspension",
    "depart"
]

# Départements
DEPARTMENTS = [
    "direction",
    "ressources_humaines",
    "finance",
    "comptabilite",
    "informatique",
    "commercial",
    "marketing",
    "production",
    "logistique",
    "qualite"
]

# Niveaux d'études
EDUCATION_LEVELS = [
    "cep",
    "bepc",
    "bac",
    "bac_plus_2",
    "bac_plus_3",
    "bac_plus_4",
    "bac_plus_5",
    "doctorat"
]

# Configuration de la paie
PAYROLL_CONFIG = {
    "currency": "XOF",
    "pay_period": "mensuel",
    "pay_day": 25,
    "overtime_multiplier": 1.5,
    "night_shift_multiplier": 1.25,
    "holiday_multiplier": 2.0
}

# Cotisations sociales (Sénégal)
SOCIAL_CONTRIBUTIONS = {
    "employeur": {
        "cnsst": 0.084,  # Caisse Nationale de Prévoyance Sociale
        "ipm": 0.03,      # Institution de Prévoyance Maladie
        "formation": 0.015
    },
    "employe": {
        "cnsst": 0.024,
        "ipm": 0.03,
        "chomage": 0.02
    }
}

# Tranches d'imposition
TAX_BRACKETS = [
    {"min": 0, "max": 150000, "rate": 0},
    {"min": 150000, "max": 300000, "rate": 0.10},
    {"min": 300000, "max": 600000, "rate": 0.20},
    {"min": 600000, "max": float("inf"), "rate": 0.30}
]

# Jours fériés au Sénégal
HOLIDAYS = [
    "01-01",  # Nouvel An
    "04-04",  # Independence Day
    "01-05",  # Fête du Travail
    "15-08",  # Assomption
    "01-11",  # Toussaint
    "25-12",  # Noël
    "Aid El Fitr",  # Tabaski (variable)
    "Aid El Kebir"  # Tabaski (variable)
]

# Configuration des évaluations
EVALUATION_CONFIG = {
    "period": "annuel",
    "rating_scale": 5,
    "self_evaluation": True,
    "peer_evaluation": False,
    "manager_evaluation": True
}

# Configuration des objectifs
OBJECTIVE_CONFIG = {
    "smart_objectives": True,
    "quarterly_review": True,
    "max_objectives": 5
}

# Configuration des présences
ATTENDANCE_CONFIG = {
    "work_hours_per_day": 8,
    "work_days_per_week": 5,
    "flexible_hours": False,
    "remote_work": False,
    "break_time_minutes": 60
}

# Heures de travail
WORKING_HOURS = {
    "morning_start": "08:00",
    "morning_end": "12:00",
    "afternoon_start": "13:00",
    "afternoon_end": "17:00"
}

# Configuration des notifications
NOTIFICATION_CONFIG = {
    "contract_expiry_days": 30,
    "leave_request_reminder_days": 7,
    "birthday_reminder": True,
    "evaluation_due": True
}

# Paramètres de formation
TRAINING_CONFIG = {
    "max_training_hours_per_year": 40,
    "external_training_approval": True,
    "certification_tracking": True
}

# Rôles et permissions
ROLE_PERMISSIONS = {
    "admin_rh": [
        "employee_create",
        "employee_read",
        "employee_update",
        "employee_delete",
        "payroll_process",
        "leave_approve",
        "evaluation_manage",
        "report_generate"
    ],
    "manager": [
        "employee_read",
        "team_manage",
        "leave_approve",
        "evaluation_create",
        "report_team"
    ],
    "employee": [
        "profile_read",
        "profile_update",
        "leave_request",
        "view_own_payslip"
    ]
}

# Configuration de la confidentialité
PRIVACY_CONFIG = {
    "salary_visible_to_employee": True,
    "show_contact_info": True,
    "data_retention_years": 10
}

# Intégrations
INTEGRATIONS = {
    "banking": {
        "enabled": True,
        "format": "virment"
    },
    "social_security": {
        "enabled": True,
        "agency": "cnps"
    },
    "time_tracking": {
        "enabled": False
    }
}

# Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "file": "logs/ressources_humaines.log",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}
