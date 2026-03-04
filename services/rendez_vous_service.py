# services/rendez_vous_service.py

from dao.rendez_vous_dao import RendezVousDAO
from models.rendez_vous import RendezVous


class RendezVousService:

    # ======================================================
    #                    GET ALL
    # ======================================================
    @staticmethod
    def get_all():
        try:
            return RendezVousDAO.get_all()
        except Exception as e:
            print("❌ ERREUR RendezVousService.get_all :", e)
            return []

    # ======================================================
    #                    GET BY ID
    # ======================================================
    @staticmethod
    def get_by_id(id_rdv: int):
        try:
            return RendezVousDAO.get_by_id(id_rdv)
        except Exception as e:
            print("❌ ERREUR RendezVousService.get_by_id :", e)
            return None

    # ======================================================
    #                      AJOUT
    # ======================================================
    @staticmethod
    def add(data: dict):
        try:
            rdv = RendezVous(
                id_eleve=data["id_eleve"],
                id_personnel=data["id_personnel"],
                date_rdv=data["date_rdv"],
                type_rdv=data["type_rdv"],
                statut=data["statut"]
            )
            return RendezVousDAO.insert(rdv)

        except Exception as e:
            print("❌ ERREUR RendezVousService.add :", e)
            return False

    # ======================================================
    #                     MODIFICATION
    # ======================================================
    @staticmethod
    def update(data: dict):
        try:
            rdv = RendezVous(
                id_rdv=data["id_rdv"],
                id_eleve=data["id_eleve"],
                id_personnel=data["id_personnel"],
                date_rdv=data["date_rdv"],
                type_rdv=data["type_rdv"],
                statut=data["statut"]
            )
            return RendezVousDAO.update(rdv)

        except Exception as e:
            print("❌ ERREUR RendezVousService.update :", e)
            return False

    # ======================================================
    #                      SUPPRESSION
    # ======================================================
    @staticmethod
    def delete(id_rdv: int):
        try:
            return RendezVousDAO.delete(id_rdv)
        except Exception as e:
            print("❌ ERREUR RendezVousService.delete :", e)
            return False
