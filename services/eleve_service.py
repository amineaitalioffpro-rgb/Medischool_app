# services/eleve_service.py

from dao.eleve_dao import EleveDAO
from models.eleve import Eleve


class EleveService:

    # =====================================================
    #                     GET ALL
    # =====================================================
    @staticmethod
    def get_all():
        try:
            return EleveDAO.get_all()
        except Exception as e:
            print("❌ ERREUR EleveService.get_all :", e)
            return []

    # =====================================================
    #                      GET ONE
    # =====================================================
    @staticmethod
    def get_by_id(id_eleve: int):
        try:
            return EleveDAO.get_by_id(id_eleve)
        except Exception as e:
            print("❌ ERREUR EleveService.get_by_id :", e)
            return None

    # =====================================================
    #                        ADD
    # =====================================================
    @staticmethod
    def add(data: dict):
        """Ajoute un élève dans la BD."""
        try:
            eleve = Eleve(
                nom=data["nom"],
                prenom=data["prenom"],
                date_naissance=data["date_naissance"],
                classe=data["classe"],
                sexe=data["sexe"],
                grp_sanguin=data["grp_sanguin"],
                telephone_parent=data["telephone_parent"]
            )

            return EleveDAO.insert(eleve)

        except Exception as e:
            print("❌ ERREUR EleveService.add :", e)
            return False

    # =====================================================
    #                        UPDATE
    # =====================================================
    @staticmethod
    def update(id_eleve: int, data: dict):
        """Met à jour un élève existant."""
        try:
            return EleveDAO.update(id_eleve, data)
        except Exception as e:
            print("❌ ERREUR EleveService.update :", e)
            return False

    # =====================================================
    #                      DELETE
    # =====================================================
    @staticmethod
    def delete(id_eleve: int):
        """Supprime un élève par ID."""
        try:
            return EleveDAO.delete(id_eleve)
        except Exception as e:
            print("❌ ERREUR EleveService.delete :", e)
            return False
