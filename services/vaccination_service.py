# services/vaccination_service.py

from dao.vaccination_dao import VaccinationDAO
from models.vaccination import Vaccination


class VaccinationService:

    # ======================================================
    #                    GET ALL
    # ======================================================
    @staticmethod
    def get_all():
        try:
            return VaccinationDAO.get_all()
        except Exception as e:
            print("❌ ERREUR VaccinationService.get_all :", e)
            return []

    # ======================================================
    #                    GET BY ID
    # ======================================================
    @staticmethod
    def get_by_id(id_vaccination: int):
        try:
            return VaccinationDAO.get_by_id(id_vaccination)
        except Exception as e:
            print("❌ ERREUR VaccinationService.get_by_id :", e)
            return None

    # ======================================================
    #                      AJOUT
    # ======================================================
    @staticmethod
    def add(data: dict):
        try:
            v = Vaccination(
                id_eleve=data["id_eleve"],
                id_personnel=data["id_personnel"],
                nom_vaccin=data["nom_vaccin"],
                date_vaccin=data["date_vaccin"],
                rappel_necessaire=data["rappel_necessaire"]
            )
            return VaccinationDAO.insert(v)

        except Exception as e:
            print("❌ ERREUR VaccinationService.add :", e)
            return False

    # ======================================================
    #                     MODIFICATION
    # ======================================================
    @staticmethod
    def update(data: dict):
        try:
            v = Vaccination(
                id_vaccination=data["id_vaccination"],
                id_eleve=data["id_eleve"],
                id_personnel=data["id_personnel"],
                nom_vaccin=data["nom_vaccin"],
                date_vaccin=data["date_vaccin"],
                rappel_necessaire=data["rappel_necessaire"]
            )
            return VaccinationDAO.update(v)

        except Exception as e:
            print("❌ ERREUR VaccinationService.update :", e)
            return False

    # ======================================================
    #                      SUPPRESSION
    # ======================================================
    @staticmethod
    def delete(id_vaccination: int):
        try:
            return VaccinationDAO.delete(id_vaccination)
        except Exception as e:
            print("❌ ERREUR VaccinationService.delete :", e)
            return False
