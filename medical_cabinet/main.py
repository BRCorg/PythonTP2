from services.patient_service import (
    charger_patients, ajouter_patient, rechercher_patient,
    afficher_patients, afficher_historique_patient
)
from services.consultation_service import (
    charger_consultations, planifier_consultation,
    afficher_consultations_a_venir, marquer_consultation_realisee,
    annuler_consultation
)
from models import (
    PatientNotFoundError, ConsultationNotFoundError,
    InvalidSecurityNumberError, InvalidConsultationStatusError
)


def main():
    """Programme principal de gestion du cabinet médical"""
    
    # Chargement des données
    patients = charger_patients()
    consultations = charger_consultations()
    
    # Reconstruction des liens patient-consultations
    for consultation in consultations:
        for patient in patients:
            if patient.ssn == consultation.patient_ssn:
                patient.ajouter_consultation(consultation)
                break
    
    while True:
        print("\n" + "="*50)
        print("GESTION CABINET MÉDICAL")
        print("="*50)
        print("1. Ajouter patient")
        print("2. Rechercher patient")
        print("3. Afficher tous les patients")
        print("4. Afficher historique patient")
        print("5. Planifier consultation")
        print("6. Afficher consultations à venir")
        print("7. Marquer consultation réalisée")
        print("8. Annuler consultation")
        print("9. Quitter")
        print("="*50)
        
        choix = input("Votre choix : ").strip()
        
        try:
            if choix == "1":
                print("\n--- Ajouter un patient ---")
                ssn = input("Numéro sécu (15 chiffres) : ").strip()
                nom = input("Nom : ").strip()
                prenom = input("Prénom : ").strip()
                date_naissance = input("Date naissance (YYYY-MM-DD) : ").strip()
                adresse = input("Adresse : ").strip()
                telephone = input("Téléphone : ").strip()
                
                ajouter_patient(patients, consultations, ssn, nom, prenom, date_naissance, adresse, telephone)
                print("✓ Patient ajouté avec succès.")
                
            elif choix == "2":
                print("\n--- Rechercher un patient ---")
                ssn = input("Numéro sécu : ").strip()
                p = rechercher_patient(patients, ssn)
                print(f"\n✓ Patient trouvé : {p.nom} {p.prenom}, {p.age} ans")
                print(f"  Adresse : {p.adresse}")
                print(f"  Téléphone : {p.telephone}")
                
            elif choix == "3":
                afficher_patients(patients)
                
            elif choix == "4":
                print("\n--- Historique patient ---")
                ssn = input("Numéro sécu : ").strip()
                afficher_historique_patient(patients, ssn)
                
            elif choix == "5":
                print("\n--- Planifier une consultation ---")
                ssn = input("Numéro sécu patient : ").strip()
                patient = rechercher_patient(patients, ssn)
                date_heure = input("Date/heure (YYYY-MM-DD HH:MM) : ").strip()
                medecin = input("Nom du médecin : ").strip()
                motif = input("Motif : ").strip()
                
                planifier_consultation(consultations, patients, patient, date_heure, medecin, motif)
                print("✓ Consultation planifiée avec succès.")
                
            elif choix == "6":
                afficher_consultations_a_venir(consultations)
                
            elif choix == "7":
                print("\n--- Marquer consultation réalisée ---")
                afficher_consultations_a_venir(consultations)
                
                consultations_planifiees = [c for c in consultations if c.statut == "planifiée"]
                if not consultations_planifiees:
                    continue
                    
                idx_str = input("\nIndex de la consultation à marquer : ").strip()
                
                if not idx_str.isdigit():
                    print("✗ Erreur : Veuillez entrer un nombre valide.")
                    continue
                    
                idx = int(idx_str)
                
                if idx < 0 or idx >= len(consultations_planifiees):
                    print(f"✗ Erreur : Index invalide. Choisir entre 0 et {len(consultations_planifiees)-1}.")
                    continue
                
                marquer_consultation_realisee(consultations, patients, consultations_planifiees[idx])
                print("✓ Consultation marquée comme réalisée.")
                
            elif choix == "8":
                print("\n--- Annuler une consultation ---")
                afficher_consultations_a_venir(consultations)
                
                consultations_planifiees = [c for c in consultations if c.statut == "planifiée"]
                if not consultations_planifiees:
                    continue
                    
                idx_str = input("\nIndex de la consultation à annuler : ").strip()
                
                if not idx_str.isdigit():
                    print("✗ Erreur : Veuillez entrer un nombre valide.")
                    continue
                    
                idx = int(idx_str)
                
                if idx < 0 or idx >= len(consultations_planifiees):
                    print(f"✗ Erreur : Index invalide. Choisir entre 0 et {len(consultations_planifiees)-1}.")
                    continue
                
                annuler_consultation(consultations, patients, consultations_planifiees[idx])
                print("✓ Consultation annulée.")
                
            elif choix == "9":
                print("\nAu revoir !")
                break
                
            else:
                print("✗ Choix invalide. Veuillez choisir entre 1 et 9.")
                
        except PatientNotFoundError as e:
            print(f"✗ Erreur : {e}")
        except InvalidSecurityNumberError as e:
            print(f"✗ Erreur : {e}")
        except InvalidConsultationStatusError as e:
            print(f"✗ Erreur : {e}")
        except ValueError as e:
            print(f"✗ Erreur de format : {e}")
        except Exception as e:
            print(f"✗ Erreur inattendue : {e}")


if __name__ == "__main__":
    main()