"""
Fonctions métier pour la gestion des consultations du cabinet médical
"""
import json
import os
from models import Consultation, ConsultationNotFoundError, InvalidConsultationStatusError

from utils.decorators import log_action

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cabinet_data.json")


def charger_consultations():
    """
    Charge la liste des consultations depuis le fichier JSON
    
    Returns:
        list: Liste des objets Consultation
    """
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            consultations = []
            for c_data in data.get("consultations", []):
                consultation = Consultation(
                    date_heure=c_data["date_heure"],
                    patient_ssn=c_data["patient_ssn"],
                    medecin=c_data["medecin"],
                    motif=c_data["motif"],
                    diagnostic=c_data.get("diagnostic"),
                    prescriptions=c_data.get("prescriptions", []),
                    statut=c_data.get("statut", "planifiée")
                )
                consultations.append(consultation)
            return consultations
    except (FileNotFoundError, json.JSONDecodeError):
        return []


@log_action("Planification d'une consultation")
@log_action("Planification d'une consultation")
def planifier_consultation(consultations, patients, patient, date_heure, medecin, motif):
    """
    Planifie une nouvelle consultation pour un patient
    
    Args:
        consultations (list): Liste des consultations
        patients (list): Liste des patients
        patient (Patient): Patient concerné
        date_heure (str): Date et heure (YYYY-MM-DD HH:MM)
        medecin (str): Nom du médecin
        motif (str): Motif de consultation
        
    Returns:
        Consultation: La consultation créée
    """
    from services.patient_service import sauvegarder_donnees
    
    consultation = Consultation(date_heure, patient.ssn, medecin, motif)
    consultations.append(consultation)
    
    # IMPORTANT: Ajouter la consultation à l'historique du patient
    patient.ajouter_consultation(consultation)
    
    sauvegarder_donnees(patients, consultations)
    return consultation


@log_action("Affichage des consultations à venir")
def afficher_consultations_a_venir(consultations):
    """
    Affiche toutes les consultations planifiées
    
    Args:
        consultations (list): Liste des consultations
    """
    consultations_planifiees = [c for c in consultations if c.statut == "planifiée"]
    
    if not consultations_planifiees:
        print("Aucune consultation à venir.")
    else:
        print("\n--- Consultations à venir ---")
        for i, c in enumerate(consultations_planifiees):
            print(f"{i}. {c}")


@log_action("Consultation marquée réalisée")
@log_action("Consultation marquée réalisée")
def marquer_consultation_realisee(consultations, patients, consultation):
    """
    Marque une consultation comme réalisée
    
    Args:
        consultations (list): Liste des consultations
        patients (list): Liste des patients
        consultation (Consultation): Consultation à marquer
        
    Raises:
        InvalidConsultationStatusError: Si la consultation n'est pas planifiée
    """
    from services.patient_service import sauvegarder_donnees
    
    if consultation.statut != "planifiée":
        raise InvalidConsultationStatusError(
            "Seules les consultations planifiées peuvent être marquées comme réalisées."
        )
    consultation.changer_statut("réalisée")
    sauvegarder_donnees(patients, consultations)


@log_action("Consultation annulée")
@log_action("Consultation annulée")
def annuler_consultation(consultations, patients, consultation):
    """
    Annule une consultation
    
    Args:
        consultations (list): Liste des consultations
        patients (list): Liste des patients
        consultation (Consultation): Consultation à annuler
        
    Raises:
        InvalidConsultationStatusError: Si la consultation n'est pas planifiée
    """
    from services.patient_service import sauvegarder_donnees
    
    if consultation.statut != "planifiée":
        raise InvalidConsultationStatusError(
            "Seules les consultations planifiées peuvent être annulées."
        )
    consultation.changer_statut("annulée")
    sauvegarder_donnees(patients, consultations)


@log_action("Ajout d'un diagnostic")
@log_action("Ajout d'un diagnostic")
def ajouter_diagnostic(consultations, patients, consultation, diagnostic):
    """
    Ajoute un diagnostic à une consultation réalisée
    
    Args:
        consultations (list): Liste des consultations
        patients (list): Liste des patients
        consultation (Consultation): Consultation concernée
        diagnostic (str): Diagnostic à ajouter
    """
    from services.patient_service import sauvegarder_donnees
    
    consultation.ajouter_diagnostic(diagnostic)
    sauvegarder_donnees(patients, consultations)


@log_action("Ajout d'une prescription")
@log_action("Ajout d'une prescription")
def ajouter_prescription(consultations, patients, consultation, prescription):
    """
    Ajoute une prescription à une consultation
    
    Args:
        consultations (list): Liste des consultations
        patients (list): Liste des patients
        consultation (Consultation): Consultation concernée
        prescription (Prescription): Prescription à ajouter
    """
    from services.patient_service import sauvegarder_donnees
    
    consultation.ajouter_prescription(prescription)
    sauvegarder_donnees(patients, consultations)