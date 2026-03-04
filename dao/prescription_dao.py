# dao/prescription_dao.py

from db.connection import get_connection
from models.prescription import Prescription


class PrescriptionDAO:

    @staticmethod
    def get_all():
        conn = get_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_prescription, id_consultation, instructions
                FROM PRESCRIPTION
                ORDER BY id_prescription ASC
            """)
            rows = cursor.fetchall()

            return [
                Prescription(
                    id_prescription=row[0],
                    id_consultation=row[1],
                    instructions=row[2]
                )
                for row in rows
            ]

        except Exception as e:
            print("❌ ERREUR PrescriptionDAO.get_all :", e)
            return []

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass


    @staticmethod
    def get_by_id(id_prescription: int):
        conn = get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_prescription, id_consultation, instructions
                FROM PRESCRIPTION
                WHERE id_prescription = %s
            """, (id_prescription,))

            row = cursor.fetchone()
            if not row:
                return None

            return Prescription(
                id_prescription=row[0],
                id_consultation=row[1],
                instructions=row[2],
            )

        except Exception as e:
            print("❌ ERREUR PrescriptionDAO.get_by_id :", e)
            return None

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass


    @staticmethod
    def insert(p: Prescription):
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO PRESCRIPTION (id_consultation, instructions)
                VALUES (%s, %s)
            """, (p.id_consultation, p.instructions))

            conn.commit()
            return True

        except Exception as e:
            print("❌ ERREUR PrescriptionDAO.insert :", e)
            return False

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass


    @staticmethod
    def update(p: Prescription):
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE PRESCRIPTION
                SET id_consultation = %s,
                    instructions = %s
                WHERE id_prescription = %s
            """, (p.id_consultation, p.instructions, p.id_prescription))

            conn.commit()
            return True

        except Exception as e:
            print("❌ ERREUR PrescriptionDAO.update :", e)
            return False

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass


    # ---------------------------------------------------------
    #                  CORRECTION DU DELETE
    # ---------------------------------------------------------
    @staticmethod
    def delete(id_prescription: int):
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()

            # 1) supprimer les médicaments associés
            cursor.execute("""
                DELETE FROM PRESCRIPTION_MEDICAMENT
                WHERE id_prescription = %s
            """, (id_prescription,))

            # 2) supprimer la prescription
            cursor.execute("""
                DELETE FROM PRESCRIPTION
                WHERE id_prescription = %s
            """, (id_prescription,))

            conn.commit()

            # Vérifier qu’au moins UNE ligne a été supprimée
            if cursor.rowcount == 0:
                print("⚠️ Aucune prescription supprimée (ID introuvable).")
                return False

            return True

        except Exception as e:
            print("❌ ERREUR PrescriptionDAO.delete :", e)
            return False

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass
