from dataclasses import dataclass

@dataclass
class Medicament:
    id_medicament: int = None
    nom_medicament: str = ""
    effets_secondaires: str = ""
