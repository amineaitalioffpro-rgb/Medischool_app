# models/prescription_medicament.py

from dataclasses import dataclass

@dataclass
class PrescriptionMedicament:
    id_prescription: int
    id_medicament: int
    dose: str
    frequence: str
    duree: str

    # champ bonus pour affichage joint avec MEDICAMENT
    nom_medicament: str = ""
