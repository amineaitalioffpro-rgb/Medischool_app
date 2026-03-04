from dao.personnel_dao import PersonnelDAO
from models.personnel import Personnel


class PersonnelService:

    @staticmethod
    def get_all():
        try:
            return PersonnelDAO.get_all()
        except Exception as e:
            print("❌ ERREUR PersonnelService.get_all :", e)
            return []

    @staticmethod
    def get_by_id(id_personnel: int):
        try:
            return PersonnelDAO.get_by_id(id_personnel)
        except Exception as e:
            print("❌ ERREUR PersonnelService.get_by_id :", e)
            return None

    @staticmethod
    def add(data: dict):
        try:
            personnel = Personnel(
                nom=data["nom"],
                prenom=data["prenom"],
                fonction=data["fonction"],
                matricule=data["matricule"],
                telephone=data["telephone"]
            )
            return PersonnelDAO.insert(personnel)
        except Exception as e:
            print("❌ ERREUR PersonnelService.add :", e)
            return False

    @staticmethod
    def update(id_personnel: int, data: dict):
        try:
            personnel = Personnel(
                id_personnel=id_personnel,
                nom=data["nom"],
                prenom=data["prenom"],
                fonction=data["fonction"],
                matricule=data["matricule"],
                telephone=data["telephone"]
            )
            return PersonnelDAO.update(personnel)
        except Exception as e:
            print("❌ ERREUR PersonnelService.update :", e)
            return False

    @staticmethod
    def delete(id_personnel: int):
        try:
            return PersonnelDAO.delete(id_personnel)
        except Exception as e:
            print("❌ ERREUR PersonnelService.delete :", e)
            return False
