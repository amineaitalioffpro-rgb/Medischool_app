# dao/rendez_vous_dao.py

from db.connection import get_connection
from models.rendez_vous import RendezVous


class RendezVousDAO:

    # ======================================================
    #                    GET ALL
    # ======================================================
    @staticmethod
    def get_all():
        conn = get_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor()

            query = """
                SELECT
                    r.id_rdv,
                    r.id_eleve,
                    r.id_personnel,
                    r.date_rdv,
                    r.type_rdv,
                    r.statut,
                    e.nom AS eleve_nom,
                    e.prenom AS eleve_prenom,
                    p.nom AS personnel_nom,
                    p.prenom AS personnel_prenom
                FROM RENDEZ_VOUS r
                JOIN ELEVE e ON e.id_eleve = r.id_eleve
                JOIN PERSONNEL_MEDICAL p ON p.id_personnel = r.id_personnel
                ORDER BY r.id_rdv ASC
            """

            cursor.execute(query)
            rows = cursor.fetchall()

            result = []
            for row in rows:
                result.append(
                    RendezVous(
                        id_rdv=row[0],
                        id_eleve=row[1],
                        id_personnel=row[2],
                        date_rdv=str(row[3]),
                        type_rdv=row[4],
                        statut=row[5],
                        nom_eleve=f"{row[6]} {row[7]}",
                        nom_personnel=f"{row[8]} {row[9]}"
                    )
                )
            return result

        except Exception as e:
            print("❌ ERREUR RendezVousDAO.get_all :", e)
            return []

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass

    # ======================================================
    #                 GET BY ID
    # ======================================================
    @staticmethod
    def get_by_id(id_rdv: int):
        conn = get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()

            query = """
                SELECT
                    r.id_rdv,
                    r.id_eleve,
                    r.id_personnel,
                    r.date_rdv,
                    r.type_rdv,
                    r.statut,
                    e.nom,
                    e.prenom,
                    p.nom,
                    p.prenom
                FROM RENDEZ_VOUS r
                JOIN ELEVE e ON e.id_eleve = r.id_eleve
                JOIN PERSONNEL_MEDICAL p ON p.id_personnel = r.id_personnel
                WHERE r.id_rdv = %s
            """

            cursor.execute(query, (id_rdv,))
            row = cursor.fetchone()

            if not row:
                return None

            return RendezVous(
                id_rdv=row[0],
                id_eleve=row[1],
                id_personnel=row[2],
                date_rdv=str(row[3]),
                type_rdv=row[4],
                statut=row[5],
                nom_eleve=f"{row[6]} {row[7]}",
                nom_personnel=f"{row[8]} {row[9]}"
            )

        except Exception as e:
            print("❌ ERREUR RendezVousDAO.get_by_id :", e)
            return None

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass

    # ======================================================
    #                     INSERT
    # ======================================================
    @staticmethod
    def insert(rdv: RendezVous):
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()

            query = """
                INSERT INTO RENDEZ_VOUS
                    (id_eleve, id_personnel, date_rdv, type_rdv, statut)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(query, (
                rdv.id_eleve,
                rdv.id_personnel,
                rdv.date_rdv,
                rdv.type_rdv,
                rdv.statut
            ))

            conn.commit()
            return True

        except Exception as e:
            print("❌ ERREUR RendezVousDAO.insert :", e)
            return False

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass

    # ======================================================
    #                     UPDATE
    # ======================================================
    @staticmethod
    def update(rdv: RendezVous):
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()

            query = """
                UPDATE RENDEZ_VOUS
                SET id_eleve = %s,
                    id_personnel = %s,
                    date_rdv = %s,
                    type_rdv = %s,
                    statut = %s
                WHERE id_rdv = %s
            """

            cursor.execute(query, (
                rdv.id_eleve,
                rdv.id_personnel,
                rdv.date_rdv,
                rdv.type_rdv,
                rdv.statut,
                rdv.id_rdv
            ))

            conn.commit()
            return True

        except Exception as e:
            print("❌ ERREUR RendezVousDAO.update :", e)
            return False

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass

    # ======================================================
    #                     DELETE
    # ======================================================
    @staticmethod
    def delete(id_rdv: int):
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM RENDEZ_VOUS
                WHERE id_rdv = %s
            """, (id_rdv,))

            conn.commit()

            if cursor.rowcount == 0:
                print("⚠️ Aucun rendez-vous supprimé.")
                return False

            return True

        except Exception as e:
            print("❌ ERREUR RendezVousDAO.delete :", e)
            return False

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass
