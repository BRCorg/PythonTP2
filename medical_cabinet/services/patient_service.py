"""
Fonctions métier pour la gestion des patients du cabinet médical
"""
import json
import os
from datetime import datetime
from models import Patient, PatientNotFoundError, InvalidSecurityNumberError
from utils.decorators import log_action, validate_patient

# Chemin absolu du fichier JSON, toujours correct quel que soit le dossier courant
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cabinet_data.json")


def charger_patients():
    """
    Charge la liste des patients depuis le fichier JSON
    
    Returns:
        list: Liste des objets Patient
    """
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            patients = []
            for p_data in data.get("patients", []):
                patient = Patient(
                    ssn=p_data.get("_ssn") or p_data.get("ssn"),
                    nom=p_data["nom"],
                    prenom=p_data["prenom"],
                    date_naissance=p_data["date_naissance"],
                    adresse=p_data["adresse"],
                    telephone=p_data.get("_telephone") or p_data.get("telephone")
                )
                patients.append(patient)
            return patients
    except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError):
        return []


def sauvegarder_donnees(patients, consultations):
    """
    Sauvegarde complète des patients et consultations dans le fichier JSON
    
    Args:
        patients (list): Liste des patients
        consultations (list): Liste des consultations
    """
    # Conversion des patients en dictionnaires
    patients_data = []
    for p in patients:
        p_dict = {
            "_ssn": p.ssn,
            "nom": p.nom,
            "prenom": p.prenom,
            "date_naissance": p.date_naissance.strftime("%Y-%m-%d"),
            "adresse": p.adresse,
            "_telephone": p.telephone
        }
        patients_data.append(p_dict)
    
    # Conversion des consultations en dictionnaires
    consultations_data = []
    for c in consultations:
        c_dict = {
            "date_heure": c.date_heure,
            "patient_ssn": c.patient_ssn,
            "medecin": c.medecin,
            "motif": c.motif,
            "diagnostic": c.diagnostic,
            "prescriptions": c.prescriptions,
            "statut": c.statut
        }
        consultations_data.append(c_dict)
    
    # Sauvegarde complète
    data = {
        "patients": patients_data,
        "consultations": consultations_data
    }
    
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@log_action("Ajout d'un patient")
def ajouter_patient(patients, consultations, ssn, nom, prenom, date_naissance, adresse, telephone):
    """
    Ajoute un nouveau patient au système
    
    Args:
        patients (list): Liste des patients
        consultations (list): Liste des consultations
        ssn (str): Numéro de sécurité sociale
        nom (str): Nom du patient
        prenom (str): Prénom du patient
        date_naissance (str): Date de naissance (YYYY-MM-DD)
        adresse (str): Adresse
        telephone (str): Téléphone
        
    Returns:
        Patient: Le patient créé
        
    Raises:
        InvalidSecurityNumberError: Si le SSN existe déjà
    """
    if any(p.ssn == ssn for p in patients):
        raise InvalidSecurityNumberError("Numéro de sécurité sociale déjà utilisé.")
    
    patient = Patient(ssn, nom, prenom, date_naissance, adresse, telephone)
    patients.append(patient)
    sauvegarder_donnees(patients, consultations)
    return patient


@log_action("Recherche d'un patient")
@validate_patient
def rechercher_patient(patients, ssn):
    """
    Recherche un patient par son numéro de sécurité sociale
    
    Args:
        patients (list): Liste des patients
        ssn (str): Numéro de sécurité sociale
        
    Returns:
        Patient: Le patient trouvé
        
    Raises:
        PatientNotFoundError: Si le patient n'existe pas
    """
    for p in patients:
        if p.ssn == ssn:
            return p
    raise PatientNotFoundError(f"Patient {ssn} non trouvé.")


@log_action("Affichage de la liste des patients")
def afficher_patients(patients):
    """
    Affiche la liste de tous les patients
    
    Args:
        patients (list): Liste des patients
    """
    if not patients:
        print("Aucun patient enregistré.")
    else:
        print("\n--- Liste des patients ---")
        for p in patients:
            print(f"{p.ssn} - {p.nom} {p.prenom} ({p.age} ans)")


@log_action("Affichage de l'historique d'un patient")
@validate_patient
def afficher_historique_patient(patients, ssn):
    """
    Affiche l'historique complet d'un patient
    
    Args:
        patients (list): Liste des patients
        ssn (str): Numéro de sécurité sociale
    """
    patient = rechercher_patient(patients, ssn)
    patient.afficher_historique()