class Personnel:
    def __init__(self,
                 id_personnel=None,
                 nom="",
                 prenom="",
                 fonction="",
                 matricule="",
                 telephone=""):

        self.id_personnel = id_personnel
        self.nom = nom
        self.prenom = prenom
        self.fonction = fonction
        self.matricule = matricule
        self.telephone = telephone

    def __repr__(self):
        return f"<Personnel {self.id_personnel} - {self.nom} {self.prenom}>"
