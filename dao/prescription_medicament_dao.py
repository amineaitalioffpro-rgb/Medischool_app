# dao/prescription_medicament_dao.py

from db.connection import get_connection
from models.prescription_medicament import PrescriptionMedicament


class PrescriptionMedicamentDAO:

    @staticmethod
    def get_by_prescription(id_prescription: int):
        conn = get_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    pm.id_prescription,
                    pm.id_medicament,
                    pm.dose,
                    pm.frequence,
                    pm.duree,
                    m.nom_medicament
                FROM PRESCRIPTION_MEDICAMENT pm
                JOIN MEDICAMENT m ON m.id_medicament = pm.id_medicament
                WHERE pm.id_prescription = %s
            """, (id_prescription,))
            rows = cursor.fetchall()

            result = []
            for row in rows:
                result.append(
                    PrescriptionMedicament(
                        id_prescription=row[0],
                        id_medicament=row[1],
                        dose=row[2],
                        frequence=row[3],
                        duree=row[4],
                        nom_medicament=row[5]
                    )
                )
            return result

        except Exception as e:
            print("❌ ERREUR PrescriptionMedicamentDAO.get_by_prescription :", e)
            return []

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass

    @staticmethod
    def insert(pm: PrescriptionMedicament):
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO PRESCRIPTION_MEDICAMENT
                    (id_prescription, id_medicament, dose, frequence, duree)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                pm.id_prescription,
                pm.id_medicament,
                pm.dose,
                pm.frequence,
                pm.duree
            ))
            conn.commit()
            return True

        except Exception as e:
            print("❌ ERREUR PrescriptionMedicamentDAO.insert :", e)
            return False

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass
