# dao/medicament_dao.py

from db.connection import get_connection
from models.medicament import Medicament


class MedicamentDAO:

    # ======================================================
    #                     GET ALL
    # ======================================================
    @staticmethod
    def get_all():
        conn = get_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id_medicament, nom_medicament, effets_secondaires FROM MEDICAMENT")
            rows = cursor.fetchall()

            return [
                Medicament(
                    id_medicament=row[0],
                    nom_medicament=row[1],
                    effets_secondaires=row[2]
                )
                for row in rows
            ]

        except Exception as e:
            print("❌ ERREUR MedicamentDAO.get_all :", e)
            return []

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass


    # ======================================================
    #                      GET BY ID
    # ======================================================
    @staticmethod
    def get_by_id(id_medicament: int):
        conn = get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_medicament, nom_medicament, effets_secondaires "
                "FROM MEDICAMENT WHERE id_medicament = %s",
                (id_medicament,)
            )
            row = cursor.fetchone()

            if not row:
                return None

            return Medicament(
                id_medicament=row[0],
                nom_medicament=row[1],
                effets_secondaires=row[2]
            )

        except Exception as e:
            print("❌ ERREUR MedicamentDAO.get_by_id :", e)
            return None

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass


    # ======================================================
    #                      INSERT
    # ======================================================
    @staticmethod
    def insert(medicament: Medicament):
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO MEDICAMENT (nom_medicament, effets_secondaires)
                VALUES (%s, %s)
                """,
                (medicament.nom_medicament, medicament.effets_secondaires)
            )
            conn.commit()
            return True

        except Exception as e:
            print("❌ ERREUR MedicamentDAO.insert :", e)
            return False

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass


    # ======================================================
    #                      UPDATE
    # ======================================================
    @staticmethod
    def update(medicament: Medicament):
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE MEDICAMENT
                SET nom_medicament = %s,
                    effets_secondaires = %s
                WHERE id_medicament = %s
                """,
                (
                    medicament.nom_medicament,
                    medicament.effets_secondaires,
                    medicament.id_medicament
                )
            )
            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            print("❌ ERREUR MedicamentDAO.update :", e)
            return False

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass


    # ======================================================
    #                      DELETE
    # ======================================================
    @staticmethod
    def delete(id_medicament: int):
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM MEDICAMENT WHERE id_medicament = %s",
                (id_medicament,)
            )
            conn.commit()
            return True

        except Exception as e:
            print("❌ ERREUR MedicamentDAO.delete :", e)
            return False

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass
