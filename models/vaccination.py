# models/vaccination.py

class Vaccination:
    def __init__(
        self,
        id_vaccination: int | None = None,
        id_eleve: int | None = None,
        id_personnel: int | None = None,
        nom_vaccin: str | None = None,
        date_vaccin: str | None = None,
        rappel_necessaire: str | None = None,
        nom_eleve: str | None = None,
        nom_personnel: str | None = None
    ):
        self.id_vaccination = id_vaccination
        self.id_eleve = id_eleve
        self.id_personnel = id_personnel
        self.nom_vaccin = nom_vaccin
        self.date_vaccin = date_vaccin
        self.rappel_necessaire = rappel_necessaire

        # Infos jointes (affichage table)
        self.nom_eleve = nom_eleve
        self.nom_personnel = nom_personnel
