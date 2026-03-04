# models/rendez_vous.py

class RendezVous:
    def __init__(
        self,
        id_rdv: int | None = None,
        id_eleve: int | None = None,
        id_personnel: int | None = None,
        date_rdv: str | None = None,
        type_rdv: str | None = None,
        statut: str | None = None,
        nom_eleve: str | None = None,
        nom_personnel: str | None = None
    ):
        self.id_rdv = id_rdv
        self.id_eleve = id_eleve
        self.id_personnel = id_personnel
        self.date_rdv = date_rdv
        self.type_rdv = type_rdv
        self.statut = statut

        # Infos jointes (affichage table)
        self.nom_eleve = nom_eleve
        self.nom_personnel = nom_personnel
