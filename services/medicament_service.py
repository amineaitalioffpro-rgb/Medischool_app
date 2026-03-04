# services/medicament_service.py

from dao.medicament_dao import MedicamentDAO
from models.medicament import Medicament


class MedicamentService:

    # ======================================================
    #                    GET ALL
    # ======================================================
    @staticmethod
    def get_all():
        return MedicamentDAO.get_all()

    # ======================================================
    #                    GET BY ID
    # ======================================================
    @staticmethod
    def get_by_id(id_medicament: int):
        return MedicamentDAO.get_by_id(id_medicament)

    # ======================================================
    #                      ADD
    # ======================================================
    @staticmethod
    def add(data: dict):
        medicament = Medicament(
            nom_medicament=data["nom_medicament"],
            effets_secondaires=data["effets_secondaires"]
        )
        return MedicamentDAO.insert(medicament)

    # ======================================================
    #                     UPDATE
    # ======================================================
    @staticmethod
    def update(id_medicament: int, data: dict):
        medicament = Medicament(
            id_medicament=id_medicament,
            nom_medicament=data["nom_medicament"],
            effets_secondaires=data["effets_secondaires"]
        )
        return MedicamentDAO.update(medicament)

    # ======================================================
    #                     DELETE
    # ======================================================
    @staticmethod
    def delete(id_medicament: int):
        return MedicamentDAO.delete(id_medicament)
