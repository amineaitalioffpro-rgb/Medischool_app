# services/consultation_service.py

from dao.consultation_dao import ConsultationDAO
from models.consultation import Consultation

# from assets.settings import load_settings


class ConsultationService:

    def get_all():
        # settings = load_settings()
    # Autorise toujours l'accès aux consultations
    # ou ignore cette permission ici
        return ConsultationDAO.get_all()


    @staticmethod
    def get_by_id(id_consultation: int):
        return ConsultationDAO.get_by_id(id_consultation)

    @staticmethod
    def get_by_eleve(id_eleve: int):
        return ConsultationDAO.get_by_eleve(id_eleve)

    @staticmethod
    def add(data: dict):
        try:
            consultation = Consultation(**data)
            return ConsultationDAO.insert(consultation)
        except Exception as e:
            print("❌ ERREUR ConsultationService.add :", e)
            return False

    @staticmethod
    def update(id_consultation: int, data: dict):
        try:
            consultation = Consultation(
                id_consultation=id_consultation,
                **data
            )
            return ConsultationDAO.update(consultation)
        except Exception as e:
            print("❌ ERREUR ConsultationService.update :", e)
            return False

    @staticmethod
    def delete(id_consultation: int):
        try:
            return ConsultationDAO.delete(id_consultation)
        except Exception as e:
            print("❌ ERREUR ConsultationService.delete :", e)
            return False
    
    @staticmethod
    def get_by_id(id_consultation: int):
        return ConsultationDAO.get_by_id(id_consultation)
