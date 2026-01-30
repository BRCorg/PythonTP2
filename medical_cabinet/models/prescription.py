from abc import ABC, abstractmethod


class Prescription(ABC):
    """
    Classe abstraite représentant une prescription médicale
    
    Attributs:
        posologie (str): Posologie du traitement
        duree (str): Durée du traitement
    """
    
    def __init__(self, posologie, duree):
        """
        Initialise une prescription
        
        Args:
            posologie (str): Posologie
            duree (str): Durée du traitement
        """
        self.posologie = posologie
        self.duree = duree

    @abstractmethod
    def afficher_details(self) -> str:
        """
        Méthode abstraite pour afficher les détails de la prescription
        
        Returns:
            str: Détails de la prescription
        """
        pass


class PrescriptionMedicamenteuse(Prescription):
    """
    Prescription de médicament
    
    Attributs:
        medicament (str): Nom du médicament
        posologie (str): Dosage
        frequence (str): Fréquence de prise
        duree (str): Durée du traitement
    """
    
    def __init__(self, medicament, posologie, frequence, duree):
        """
        Initialise une prescription médicamenteuse
        
        Args:
            medicament (str): Nom du médicament
            posologie (str): Dosage
            frequence (str): Fréquence (ex: "3 fois par jour")
            duree (str): Durée (ex: "7 jours")
        """
        super().__init__(posologie, duree)
        self.medicament = medicament
        self.frequence = frequence

    def afficher_details(self) -> str:
        """Affiche les détails de la prescription médicamenteuse"""
        return (f"Médicament : {self.medicament}, Posologie : {self.posologie}, "
                f"Fréquence : {self.frequence}, Durée : {self.duree}")


class PrescriptionExamen(Prescription):
    """
    Prescription d'examen médical
    
    Attributs:
        type_examen (str): Type d'examen (radio, analyse, etc.)
        laboratoire (str): Laboratoire recommandé
    """
    
    def __init__(self, type_examen, laboratoire, posologie="", duree=""):
        """
        Initialise une prescription d'examen
        
        Args:
            type_examen (str): Type d'examen
            laboratoire (str): Laboratoire recommandé
            posologie (str, optional): Non utilisé pour les examens
            duree (str, optional): Non utilisé pour les examens
        """
        super().__init__(posologie, duree)
        self.type_examen = type_examen
        self.laboratoire = laboratoire

    def afficher_details(self) -> str:
        """Affiche les détails de la prescription d'examen"""
        return f"Examen : {self.type_examen}, Laboratoire : {self.laboratoire}"


class PrescriptionKinesitherapie(Prescription):
    """
    Prescription de kinésithérapie
    
    Attributs:
        nb_seances (int): Nombre de séances
        zone (str): Zone à traiter
    """
    
    def __init__(self, nb_seances, zone, posologie="", duree=""):
        """
        Initialise une prescription de kinésithérapie
        
        Args:
            nb_seances (int): Nombre de séances
            zone (str): Zone à traiter
            posologie (str, optional): Non utilisé pour la kiné
            duree (str, optional): Non utilisé pour la kiné
        """
        super().__init__(posologie, duree)
        self.nb_seances = nb_seances
        self.zone = zone

    def afficher_details(self) -> str:
        """Affiche les détails de la prescription de kinésithérapie"""
        return f"Kinésithérapie : {self.nb_seances} séances sur {self.zone}"