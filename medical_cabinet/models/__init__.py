# Permet d'importer facilement toutes les classes depuis le package models
from .patient import Patient
from .consultation import Consultation
from .prescription import (
    Prescription,
    PrescriptionMedicamenteuse,
    PrescriptionExamen,
    PrescriptionKinesitherapie
)

# Exceptions personnalisées pour le projet
class PatientNotFoundError(Exception):
    """Exception levée quand un patient n'est pas trouvé"""
    pass

class ConsultationNotFoundError(Exception):
    """Exception levée quand une consultation n'est pas trouvée"""
    pass

class InvalidSecurityNumberError(Exception):
    """Exception levée quand le numéro de sécurité sociale est invalide"""
    pass

class InvalidConsultationStatusError(Exception):
    """Exception levée quand le statut de consultation est invalide"""
    pass