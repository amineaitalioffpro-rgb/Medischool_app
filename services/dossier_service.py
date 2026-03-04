from dao.dossier_dao import DossierDAO
from db.connection import get_connection


class DossierService:

    @staticmethod
    def get_all():
        return DossierDAO.get_all()

    @staticmethod
    def get_by_eleve(id_eleve):
        return DossierDAO.get_by_eleve(id_eleve)

    # ----------- AJOUT DOSSIER -----------
    @staticmethod
    def add(data):
        try:
            return DossierDAO.insert(data)
        except Exception as e:
            print("❌ ERREUR DossierService.add :", e)
            return False

    # ----------- SUPPRESSION -----------
    @staticmethod
    def delete(id_dossier):
        try:
            conn = get_connection()
            cur = conn.cursor()

            query = "DELETE FROM DOSSIER_MEDICAL WHERE id_dossier = %s"
            cur.execute(query, (id_dossier,))
            conn.commit()

            deleted = cur.rowcount  # nombre de lignes supprimées

            cur.close()
            conn.close()

            return deleted > 0

        except Exception as e:
            print("❌ ERREUR DossierService.delete :", e)
            return False
