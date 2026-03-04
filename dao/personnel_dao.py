from db.connection import get_connection
from models.personnel import Personnel


class PersonnelDAO:

    # ==============================================================
    #   GET ALL
    # ==============================================================
    @staticmethod
    def get_all():
        conn = get_connection()
        if not conn:
            print("❌ Connexion MySQL impossible")
            return []

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_personnel, nom, prenom, fonction, matricule, telephone
                FROM PERSONNEL_MEDICAL
                ORDER BY id_personnel ASC
            """)

            rows = cursor.fetchall()
            return [
                Personnel(
                    id_personnel=r[0],
                    nom=r[1],
                    prenom=r[2],
                    fonction=r[3],
                    matricule=r[4],
                    telephone=r[5]
                ) for r in rows
            ]

        except Exception as e:
            print("❌ ERREUR PersonnelDAO.get_all :", e)
            return []

        finally:
            cursor.close()
            conn.close()

    # ==============================================================
    #   GET BY ID
    # ==============================================================
    @staticmethod
    def get_by_id(id_personnel):
        conn = get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_personnel, nom, prenom, fonction, matricule, telephone
                FROM PERSONNEL_MEDICAL
                WHERE id_personnel = %s
            """, (id_personnel,))

            r = cursor.fetchone()

            if not r:
                return None

            return Personnel(
                id_personnel=r[0],
                nom=r[1],
                prenom=r[2],
                fonction=r[3],
                matricule=r[4],
                telephone=r[5]
            )

        except Exception as e:
            print("❌ ERREUR PersonnelDAO.get_by_id :", e)
            return None

        finally:
            cursor.close()
            conn.close()

    # ==============================================================
    #   INSERT
    # ==============================================================
    @staticmethod
    def insert(personnel: Personnel):
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO PERSONNEL_MEDICAL (nom, prenom, fonction, matricule, telephone)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                personnel.nom,
                personnel.prenom,
                personnel.fonction,
                personnel.matricule,
                personnel.telephone
            ))

            conn.commit()
            return True

        except Exception as e:
            print("❌ ERREUR PersonnelDAO.insert :", e)
            return False

        finally:
            cursor.close()
            conn.close()

    # ==============================================================
    #   UPDATE
    # ==============================================================
    @staticmethod
    def update(personnel: Personnel):
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE PERSONNEL_MEDICAL
                SET nom=%s, prenom=%s, fonction=%s, matricule=%s, telephone=%s
                WHERE id_personnel=%s
            """, (
                personnel.nom,
                personnel.prenom,
                personnel.fonction,
                personnel.matricule,
                personnel.telephone,
                personnel.id_personnel
            ))

            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            print("❌ ERREUR PersonnelDAO.update :", e)
            return False

        finally:
            cursor.close()
            conn.close()

    # ==============================================================
    #   DELETE
    # ==============================================================
    @staticmethod
    def delete(id_personnel: int):
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM PERSONNEL_MEDICAL WHERE id_personnel=%s", (id_personnel,))
            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            print("❌ ERREUR PersonnelDAO.delete :", e)
            return False

        finally:
            cursor.close()
            conn.close()
