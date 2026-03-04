from db.connection import get_connection
from models.dossier_medical import DossierMedical


class DossierDAO:

    # ======================================================
    #                      GET ALL
    # ======================================================
    @staticmethod
    def get_all():
        conn = get_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT d.id_dossier, d.id_eleve, e.nom, e.prenom, 
                       d.antecedents, d.allergies, d.note_medicale
                FROM DOSSIER_MEDICAL d
                JOIN ELEVE e ON d.id_eleve = e.id_eleve
            """)

            rows = cursor.fetchall()
            dossiers = []

            for row in rows:
                dossiers.append({
                    "id_dossier": row[0],
                    "id_eleve": row[1],
                    "nom": row[2],
                    "prenom": row[3],
                    "antecedents": row[4],
                    "allergies": row[5],
                    "note_medicale": row[6],
                })

            return dossiers

        except Exception as e:
            print("❌ ERREUR get_all dossier :", e)
            return []

        finally:
            cursor.close()
            conn.close()

    # ======================================================
    #                    GET BY ELEVE
    # ======================================================
    @staticmethod
    def get_by_eleve(id_eleve):
        conn = get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_dossier, id_eleve, antecedents, allergies, note_medicale
                FROM DOSSIER_MEDICAL
                WHERE id_eleve = %s
            """, (id_eleve,))

            row = cursor.fetchone()
            if row:
                return DossierMedical(*row)
            return None

        except Exception as e:
            print("❌ ERREUR get_by_eleve dossier :", e)
            return None

        finally:
            cursor.close()
            conn.close()

    # ======================================================
    #                        INSERT
    # ======================================================
    @staticmethod
    def insert(data):
        conn = get_connection()
        if not conn:
            return False

        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO DOSSIER_MEDICAL (id_eleve, antecedents, allergies, note_medicale)
                VALUES (%s, %s, %s, %s)
            """, (
                data["id_eleve"],
                data["antecedents"],
                data["allergies"],
                data["note_medicale"]
            ))
            conn.commit()
            return True

        except Exception as e:
            print("❌ ERREUR insert dossier :", e)
            return False

        finally:
            cur.close()
            conn.close()

    # ======================================================
    #                        DELETE
    # ======================================================
    @staticmethod
    def delete(id_dossier):
        conn = get_connection()
        if not conn:
            return False

        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM DOSSIER_MEDICAL WHERE id_dossier = %s", (id_dossier,))
            conn.commit()
            return True

        except Exception as e:
            print("❌ ERREUR delete dossier :", e)
            return False

        finally:
            cur.close()
            conn.close()
