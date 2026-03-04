# models/consultation.py
from dataclasses import dataclass

@dataclass
class Consultation:
    id_consultation: int | None = None
    id_eleve: int | None = None
    id_personnel: int | None = None
    date_consultation: str = ""
    type_consultation: str = ""
    symptomes: str = ""
    diagnostic: str = ""
    decisions: str = ""

    # Champs bonus pour l'affichage (JOIN)
    nom_eleve: str = ""
    nom_personnel: str = ""
