"""
Configuration du logging pour les ressources humaines

Ce module définit la configuration du système de logging
pour le module des ressources humaines.

Ce fichier fait partie du projet ERP développé pour le Sénégal.
"""
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(module_name: str = "ressources_humaines", log_level: str = "INFO"):
    """
    Configure le système de logging pour le module.
    
    Args:
        module_name: Nom du module pour le logger
        log_level: Niveau de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Logger configuré
    """
    # Créer le logger
    logger = logging.getLogger(module_name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Créer le format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler pour la console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler pour le fichier
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    file_handler = RotatingFileHandler(
        log_dir / f"{module_name}.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


# Logger par défaut
logger = setup_logging()


def log_employee_action(action: str, employee_id: int, user_id: int, details: str = None):
    """
    Enregistre une action sur un employé.
    
    Args:
        action: Type d'action (create, update, delete)
        employee_id: ID de l'employé
        user_id: ID de l'utilisateur effectuant l'action
        details: Détails supplémentaires
    """
    message = f"Action: {action} | Employee: {employee_id} | User: {user_id}"
    if details:
        message += f" | Details: {details}"
    
    logger.info(message)


def log_attendance_action(action: str, attendance_id: int, user_id: int):
    """
    Enregistre une action sur une présence.
    
    Args:
        action: Type d'action
        attendance_id: ID de la présence
        user_id: ID de l'utilisateur
    """
    logger.info(f"Attendance {action}: {attendance_id} by User: {user_id}")


def log_leave_request_action(action: str, request_id: int, user_id: int, details: str = None):
    """
    Enregistre une action sur une demande decongé.
    
    Args:
        action: Type d'action (create, approve, reject)
        request_id: ID de la demande
        user_id: ID de l'utilisateur
        details: Détails supplémentaires
    """
    message = f"Leave Request {action}: {request_id} by User: {user_id}"
    if details:
        message += f" | Details: {details}"
    
    logger.info(message)


def log_salary_action(action: str, salary_id: int, user_id: int):
    """
    Enregistre une action sur un salaire.
    
    Args:
        action: Type d'action
        salary_id: ID du salaire
        user_id: ID de l'utilisateur
    """
    logger.info(f"Salary {action}: {salary_id} by User: {user_id}")
