from datetime import datetime, date
from utils.validators import validate_ssn


class Patient:
    """
    Classe représentant un patient du cabinet médical
    
    Attributs:
        ssn (str): Numéro de sécurité sociale (15 chiffres)
        nom (str): Nom du patient
        prenom (str): Prénom du patient
        date_naissance (date): Date de naissance
        adresse (str): Adresse du patient
        telephone (str): Numéro de téléphone
        consultations (list): Liste des consultations du patient
    """
    
    def __init__(self, ssn, nom, prenom, date_naissance, adresse, telephone):
        """
        Initialise un patient
        
        Args:
            ssn (str): Numéro de sécurité sociale (15 chiffres)
            nom (str): Nom du patient
            prenom (str): Prénom du patient
            date_naissance (str ou date): Date de naissance (format YYYY-MM-DD si string)
            adresse (str): Adresse
            telephone (str): Téléphone
            
        Raises:
            InvalidSecurityNumberError: Si le SSN est invalide
        """
        if not validate_ssn(ssn):
            from models import InvalidSecurityNumberError
            raise InvalidSecurityNumberError(f"Numéro de sécurité sociale invalide : {ssn}")
        
        self._ssn = ssn  # attribut sensible
        self.nom = nom
        self.prenom = prenom
        
        # Conversion de la date de naissance si c'est un string
        if isinstance(date_naissance, str):
            self.date_naissance = datetime.strptime(date_naissance, "%Y-%m-%d").date()
        else:
            self.date_naissance = date_naissance
            
        self.adresse = adresse
        self._telephone = telephone  # attribut sensible
        self.consultations = []

    @property
    def ssn(self):
        """Getter pour le numéro de sécurité sociale (protégé)"""
        return self._ssn

    @property
    def telephone(self):
        """Getter pour le téléphone (protégé)"""
        return self._telephone

    @telephone.setter
    def telephone(self, new_number):
        """Setter pour le téléphone"""
        self._telephone = new_number

    @property
    def age(self):
        """Calcule automatiquement l'âge du patient"""
        today = date.today()
        return today.year - self.date_naissance.year - (
            (today.month, today.day) < (self.date_naissance.month, self.date_naissance.day)
        )

    def ajouter_consultation(self, consultation):
        """
        Ajoute une consultation à l'historique du patient
        
        Args:
            consultation: Objet Consultation à ajouter
        """
        self.consultations.append(consultation)

    def afficher_historique(self):
        """Affiche toutes les consultations du patient"""
        if not self.consultations:
            print("Aucune consultation pour ce patient.")
        else:
            print(f"\n--- Historique de {self.prenom} {self.nom} ---")
            for c in self.consultations:
                print(c)