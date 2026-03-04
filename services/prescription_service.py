# services/prescription_service.py

from dao.prescription_dao import PrescriptionDAO
from models.prescription import Prescription


class PrescriptionService:

    @staticmethod
    def get_all():
        try:
            return PrescriptionDAO.get_all()
        except Exception as e:
            print("❌ ERREUR PrescriptionService.get_all :", e)
            return []

    @staticmethod
    def get_by_id(id_prescription: int):
        try:
            return PrescriptionDAO.get_by_id(id_prescription)
        except Exception as e:
            print("❌ ERREUR PrescriptionService.get_by_id :", e)
            return None

    @staticmethod
    def add(data: dict):
        try:
            p = Prescription(
                id_consultation=data["id_consultation"],
                instructions=data["instructions"]
            )
            return PrescriptionDAO.insert(p)
        except Exception as e:
            print("❌ ERREUR PrescriptionService.add :", e)
            return False

    @staticmethod
    def update(id_prescription: int, data: dict):
        try:
            p = Prescription(
                id_prescription=id_prescription,
                id_consultation=data["id_consultation"],
                instructions=data["instructions"]
            )
            return PrescriptionDAO.update(p)
        except Exception as e:
            print("❌ ERREUR PrescriptionService.update :", e)
            return False

    @staticmethod
    def delete(id_prescription: int):
        try:
            return PrescriptionDAO.delete(id_prescription)
        except Exception as e:
            print("❌ ERREUR PrescriptionService.delete :", e)
            return False
