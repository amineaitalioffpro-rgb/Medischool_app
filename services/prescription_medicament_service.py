# services/prescription_medicament_service.py

from dao.prescription_medicament_dao import PrescriptionMedicamentDAO
from models.prescription_medicament import PrescriptionMedicament


class PrescriptionMedicamentService:

    @staticmethod
    def get_by_prescription(id_prescription: int):
        try:
            return PrescriptionMedicamentDAO.get_by_prescription(id_prescription)
        except Exception as e:
            print("❌ ERREUR PrescriptionMedicamentService.get_by_prescription :", e)
            return []

    @staticmethod
    def add(data: dict):
        """
        data = {
            "id_prescription": ...,
            "id_medicament": ...,
            "dose": "...",
            "frequence": "...",
            "duree": "..."
        }
        """
        try:
            pm = PrescriptionMedicament(
                id_prescription=data["id_prescription"],
                id_medicament=data["id_medicament"],
                dose=data["dose"],
                frequence=data["frequence"],
                duree=data["duree"]
            )
            return PrescriptionMedicamentDAO.insert(pm)
        except Exception as e:
            print("❌ ERREUR PrescriptionMedicamentService.add :", e)
            return False
