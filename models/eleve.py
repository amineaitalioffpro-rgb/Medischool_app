# models/eleve.py

class Eleve:
    def __init__(self,
                 id_eleve=None,
                 nom="",
                 prenom="",
                 date_naissance="",
                 classe="",
                 sexe="",
                 grp_sanguin="",
                 telephone_parent=""):

        self.id_eleve = id_eleve
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.classe = classe
        self.sexe = sexe
        self.grp_sanguin = grp_sanguin
        self.telephone_parent = telephone_parent

    def __repr__(self):
        return f"<Eleve {self.id_eleve} - {self.nom} {self.prenom}>"
