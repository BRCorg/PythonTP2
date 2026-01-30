import functools
from datetime import datetime


def log_action(action_desc):
    """
    Décorateur pour enregistrer les actions dans un fichier de logs
    
    Args:
        action_desc (str): Description de l'action à logger
        
    Returns:
        function: Fonction décorée
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open("logs.txt", "a", encoding="utf-8") as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"[{timestamp}] Action effectuée : {action_desc}\n")
            return result
        return wrapper
    return decorator


def validate_patient(func):
    """
    Décorateur pour valider qu'un patient existe avant d'exécuter une opération
    
    Attend que la fonction décorée ait comme paramètres:
    - patients (list): Liste des patients
    - ssn (str): Numéro de sécurité sociale du patient
    
    Raises:
        PatientNotFoundError: Si le patient n'existe pas
        
    Returns:
        function: Fonction décorée
    """
    @functools.wraps(func)
    def wrapper(patients, ssn, *args, **kwargs):
        if not any(p.ssn == ssn for p in patients):
            # Import local pour éviter l'import circulaire
            from models import PatientNotFoundError
            raise PatientNotFoundError(f"Patient {ssn} non trouvé")
        return func(patients, ssn, *args, **kwargs)
    return wrapper