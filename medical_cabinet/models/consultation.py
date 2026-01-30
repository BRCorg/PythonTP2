class Consultation:
    """
    Classe représentant une consultation médicale
    
    Attributs:
        date_heure (str): Date et heure du rendez-vous
        patient_ssn (str): Numéro de sécurité sociale du patient
        medecin (str): Nom du médecin
        motif (str): Motif de la consultation
        diagnostic (str): Diagnostic (None si non réalisée)
        prescriptions (list): Liste des prescriptions
        statut (str): Statut (planifiée, réalisée, annulée)
    """
    
    STATUTS = ["planifiée", "réalisée", "annulée"]

    def __init__(self, date_heure, patient_ssn, medecin, motif, diagnostic=None, prescriptions=None, statut="planifiée"):
        """
        Initialise une consultation
        
        Args:
            date_heure (str): Date et heure (format YYYY-MM-DD HH:MM)
            patient_ssn (str): SSN du patient concerné
            medecin (str): Nom du médecin
            motif (str): Motif de consultation
            diagnostic (str, optional): Diagnostic. Par défaut None
            prescriptions (list, optional): Liste de prescriptions. Par défaut None
            statut (str, optional): Statut. Par défaut "planifiée"
        """
        self.date_heure = date_heure
        self.patient_ssn = patient_ssn
        self.medecin = medecin
        self.motif = motif
        self.diagnostic = diagnostic
        self.prescriptions = prescriptions if prescriptions else []
        self.statut = statut

    def ajouter_diagnostic(self, diagnostic):
        """
        Ajoute un diagnostic à la consultation
        
        Args:
            diagnostic (str): Diagnostic à ajouter
            
        Raises:
            InvalidConsultationStatusError: Si la consultation n'est pas réalisée
        """
        if self.statut != "réalisée":
            from models import InvalidConsultationStatusError
            raise InvalidConsultationStatusError(
                "Le diagnostic ne peut être ajouté que si la consultation est réalisée."
            )
        self.diagnostic = diagnostic

    def ajouter_prescription(self, prescription):
        """
        Ajoute une prescription à la consultation
        
        Args:
            prescription: Objet Prescription à ajouter
        """
        self.prescriptions.append(prescription)

    def changer_statut(self, nouveau_statut):
        """
        Change le statut de la consultation
        
        Args:
            nouveau_statut (str): Nouveau statut (planifiée, réalisée, annulée)
            
        Raises:
            InvalidConsultationStatusError: Si le statut est invalide
        """
        if nouveau_statut not in self.STATUTS:
            from models import InvalidConsultationStatusError
            raise InvalidConsultationStatusError(f"Statut invalide : {nouveau_statut}")
        self.statut = nouveau_statut

    def __str__(self):
        """Représentation textuelle de la consultation"""
        return f"{self.date_heure} - Dr {self.medecin} - {self.motif} - [{self.statut}]"