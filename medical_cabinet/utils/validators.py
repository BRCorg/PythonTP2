def validate_ssn(ssn):
    """
    Valide un numéro de sécurité sociale français (15 chiffres)
    
    Args:
        ssn (str): Numéro de sécurité sociale à valider
        
    Returns:
        bool: True si valide, False sinon
    """
    return isinstance(ssn, str) and ssn.isdigit() and len(ssn) == 15