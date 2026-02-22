"""
Configuration du module ecole

Ce module contient la configuration du projet
pour le module de gestion scolaire.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""

# Configuration du module ecole

# Paramètres de configuration
MODULE_NAME = "ecole"
MODULE_VERSION = "1.0.0"

# Niveaux d'études
EDUCATION_LEVELS = [
    "maternelle",
    "primaire",
    "college",
    "lycee",
    "superieur"
]

# Classes
CLASSES = [
    "maternelle-petite_section",
    "maternelle-moyenne_section",
    "maternelle-grande_section",
    "cp",
    "ce1",
    "ce2",
    "cm1",
    "cm2",
    "6e",
    "5e",
    "4e",
    "3e",
    "2nd",
    "1ere",
    "terminale"
]

# Années académiques
ACADEMIC_YEAR_START = 9  # Septembre
ACADEMIC_YEAR_END = 7   # Juillet

# Types de frais de scolarité
FEE_TYPES = {
    "inscription": 25000,
    "scolarite": 150000,
    "transport": 50000,
    "cantine": 30000,
    "uniforme": 20000,
    "livre": 15000
}

# Statuts des étudiants
STUDENT_STATUS = [
    "inscrit",
    "actif",
    "suspendu",
    "transfere",
    "diplome",
    "abandon"
]

# Types de paiements
PAYMENT_TYPES = [
    "especes",
    "cheque",
    "virement",
    "mobile_money"
]

# Statuts de paiement
PAYMENT_STATUS = [
    "en_attente",
    "partiel",
    "paye",
    "en_retard",
    "exonere"
]

# Systèmes de notation
GRADING_SYSTEMS = [
    {"name": "Sur 20", "min": 0, "max": 20},
    {"name": "Pourcentage", "min": 0, "max": 100},
    {"name": "Lettres", "min": 0, "max": 100}
]

# Configuration de la moyenne
AVERAGE_CONFIG = {
    "rounding": 2,
    "pass_mark": 10,
    "merit_bonus": 0.5
}

# Types d'examens
EXAM_TYPES = [
    "devoir",
    "composition",
    "examen_final",
    "rattrapage"
]

# Matières par défaut
SUBJECTS = {
    "primaire": ["Francais", "Mathematiques", "Histoire-Geo", "Sciences", "Anglais", "Education_Islamique", "Sport"],
    "college": ["Francais", "Mathematiques", "Histoire-Geo", "Physique-Chimie", "SVT", "Anglais", "Education_Islamique", "Sport", "EPS"],
    "lycee": ["Francais", "Mathematiques", "Histoire-Geo", "Physique", "Chimie", "SVT", "Anglais", "Philo", "Education_Islamique", "Sport"]
}

# Configuration de l'assiduité
ATTENDANCE_CONFIG = {
    "track_daily": True,
    "require_justification": True,
    "absence_threshold": 15  # jours
}

# Jours de la semaine
WEEKDAYS = [
    "lundi",
    "mardi",
    "mercredi",
    "jeudi",
    "vendredi",
    "samedi"
]

# Heures de cours
SCHOOL_HOURS = {
    "start": "08:00",
    "end": "16:00",
    "break_start": "12:00",
    "break_end": "13:00"
}

# Rôles et permissions
ROLE_PERMISSIONS = {
    "admin_ecole": [
        "student_create",
        "student_read",
        "student_update",
        "student_delete",
        "grade_manage",
        "fee_manage",
        "report_generate",
        "settings_manage"
    ],
    "professeur": [
        "student_read",
        "grade_create",
        "grade_update",
        "attendance_manage"
    ],
    "parent": [
        "student_read",
        "grade_read",
        "attendance_read",
        "payment_create"
    ],
    "etudiant": [
        "grade_read",
        "attendance_read",
        "schedule_read"
    ]
}

# Configuration des notifications
NOTIFICATION_CONFIG = {
    "absence_alert": True,
    "low_grade_alert": True,
    "payment_reminder": True,
    "report_card_available": True
}

# Intégrations
INTEGRATIONS = {
    "accounting": {
        "enabled": True,
        "module": "comptabilite"
    },
    "sms": {
        "enabled": False,
        "provider": ""
    }
}

# Configuration des bulletins
REPORT_CARD_CONFIG = {
    "include_ranks": True,
    "include_averages": True,
    "include_attendance": True,
    "signature_required": True
}

# Performance
PERFORMANCE_CONFIG = {
    "max_students_per_page": 50,
    "enable_caching": True
}

# Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "file": "logs/ecole.log",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}
