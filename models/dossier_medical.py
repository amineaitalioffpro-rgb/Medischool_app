from dataclasses import dataclass

@dataclass
class DossierMedical:
    id_dossier: int = None
    id_eleve: int = None
    antecedents: str = ""
    allergies: str = ""
    note_medicale: int = 0
