# dao/consultation_dao.py

from db.connection import get_connection
from models.consultation import Consultation


class ConsultationDAO:

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
                c.id_consultation,
                c.id_eleve,
                c.id_personnel,
                c.date_consultation,
                c.type_consultation,
                c.symptomes,
                c.diagnostic,
                c.decisions,
                e.nom AS eleve_nom,
                e.prenom AS eleve_prenom,
                p.nom AS personnel_nom,
                p.prenom AS personnel_prenom
            FROM CONSULTATION c
            JOIN ELEVE e ON e.id_eleve = c.id_eleve
            JOIN PERSONNEL_MEDICAL p ON p.id_personnel = c.id_personnel
            ORDER BY c.id_consultation ASC
            """  # <<< ordre corrigé

            cursor.execute(query)
            rows = cursor.fetchall()

            result = []
            for row in rows:
                result.append(
                    Consultation(
                        id_consultation=row[0],
                        id_eleve=row[1],
                        id_personnel=row[2],
                        date_consultation=str(row[3]),
                        type_consultation=row[4],
                        symptomes=row[5],
                        diagnostic=row[6],
                        decisions=row[7],
                        nom_eleve=f"{row[8]} {row[9]}",
                        nom_personnel=f"{row[10]} {row[11]}",
                    )
                )

            return result

        except Exception as e:
            print("❌ ERREUR ConsultationDAO.get_all :", e)
            return []

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass

    # ======================================================
    #                GET BY ID
    # ======================================================
    @staticmethod
    def get_by_id(id_consultation: int):
        conn = get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()

            query = """
            SELECT 
                c.id_consultation,
                c.id_eleve,
                c.id_personnel,
                c.date_consultation,
                c.type_consultation,
                c.symptomes,
                c.diagnostic,
                c.decisions,
                e.nom,
                e.prenom,
                p.nom,
                p.prenom
            FROM CONSULTATION c
            JOIN ELEVE e ON e.id_eleve = c.id_eleve
            JOIN PERSONNEL_MEDICAL p ON p.id_personnel = c.id_personnel
            WHERE c.id_consultation = %s
            """

            cursor.execute(query, (id_consultation,))
            row = cursor.fetchone()

            if not row:
                return None

            return Consultation(
                id_consultation=row[0],
                id_eleve=row[1],
                id_personnel=row[2],
                date_consultation=str(row[3]),
                type_consultation=row[4],
                symptomes=row[5],
                diagnostic=row[6],
                decisions=row[7],
                nom_eleve=f"{row[8]} {row[9]}",
                nom_personnel=f"{row[10]} {row[11]}"
            )

        except Exception as e:
            print("❌ ERREUR ConsultationDAO.get_by_id :", e)
            return None

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass

    # ======================================================
    #            GET BY ELEVE (HISTORIQUE)
    # ======================================================
    @staticmethod
    def get_by_eleve(id_eleve: int):
        conn = get_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor()

            query = """
            SELECT 
                c.id_consultation,
                c.id_eleve,
                c.id_personnel,
                c.date_consultation,
                c.type_consultation,
                c.symptomes,
                c.diagnostic,
                c.decisions,
                e.nom,
                e.prenom,
                p.nom,
                p.prenom
            FROM CONSULTATION c
            JOIN ELEVE e ON e.id_eleve = c.id_eleve
            JOIN PERSONNEL_MEDICAL p ON p.id_personnel = c.id_personnel
            WHERE c.id_eleve = %s
            ORDER BY c.id_consultation ASC
            """

            cursor.execute(query, (id_eleve,))
            rows = cursor.fetchall()

            result = []
            for row in rows:
                result.append(
                    Consultation(
                        id_consultation=row[0],
                        id_eleve=row[1],
                        id_personnel=row[2],
                        date_consultation=str(row[3]),
                        type_consultation=row[4],
                        symptomes=row[5],
                        diagnostic=row[6],
                        decisions=row[7],
                        nom_eleve=f"{row[8]} {row[9]}",
                        nom_personnel=f"{row[10]} {row[11]}",
                    )
                )

            return result

        except Exception as e:
            print("❌ ERREUR ConsultationDAO.get_by_eleve :", e)
            return []

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass

    # ======================================================
    #                       INSERT
    # ======================================================
    @staticmethod
    def insert(consultation: Consultation):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO CONSULTATION (
                    id_eleve, id_personnel, date_consultation,
                    type_consultation, symptomes, diagnostic, decisions
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                consultation.id_eleve,
                consultation.id_personnel,
                consultation.date_consultation,
                consultation.type_consultation,
                consultation.symptomes,
                consultation.diagnostic,
                consultation.decisions
            ))

            conn.commit()
            return True

        except Exception as e:
            print("❌ ERREUR ConsultationDAO.insert :", e)
            return False

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass

    # ======================================================
    #                       UPDATE
    # ======================================================
    @staticmethod
    def update(consultation: Consultation):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE CONSULTATION
                SET id_eleve = %s,
                    id_personnel = %s,
                    date_consultation = %s,
                    type_consultation = %s,
                    symptomes = %s,
                    diagnostic = %s,
                    decisions = %s
                WHERE id_consultation = %s
            """, (
                consultation.id_eleve,
                consultation.id_personnel,
                consultation.date_consultation,
                consultation.type_consultation,
                consultation.symptomes,
                consultation.diagnostic,
                consultation.decisions,
                consultation.id_consultation
            ))

            conn.commit()
            return True

        except Exception as e:
            print("❌ ERREUR ConsultationDAO.update :", e)
            return False

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass

    # ======================================================
    #                       DELETE
    # ======================================================
    @staticmethod
    def delete(id_consultation: int):
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM CONSULTATION WHERE id_consultation = %s",
                (id_consultation,)
            )
            conn.commit()
            return True

        except Exception as e:
            print("❌ ERREUR ConsultationDAO.delete :", e)
            return False

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass
