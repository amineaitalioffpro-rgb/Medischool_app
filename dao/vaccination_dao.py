# dao/vaccination_dao.py

from db.connection import get_connection
from models.vaccination import Vaccination


class VaccinationDAO:

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
                    v.id_vaccination,
                    v.id_eleve,
                    v.id_personnel,
                    v.nom_vaccin,
                    v.date_vaccin,
                    v.rappel_necessaire,
                    e.nom AS eleve_nom,
                    e.prenom AS eleve_prenom,
                    p.nom AS personnel_nom,
                    p.prenom AS personnel_prenom
                FROM VACCINATION v
                JOIN ELEVE e ON e.id_eleve = v.id_eleve
                JOIN PERSONNEL_MEDICAL p ON p.id_personnel = v.id_personnel
                ORDER BY v.id_vaccination ASC
            """

            cursor.execute(query)
            rows = cursor.fetchall()

            result = []
            for row in rows:
                result.append(
                    Vaccination(
                        id_vaccination=row[0],
                        id_eleve=row[1],
                        id_personnel=row[2],
                        nom_vaccin=row[3],
                        date_vaccin=str(row[4]),
                        rappel_necessaire=row[5],
                        nom_eleve=f"{row[6]} {row[7]}",
                        nom_personnel=f"{row[8]} {row[9]}"
                    )
                )
            return result

        except Exception as e:
            print("❌ ERREUR VaccinationDAO.get_all :", e)
            return []

        finally:
            try:
                cursor.close()
            except:
                pass
            try:
                conn.close()
            except:
                pass

    # ======================================================
    #                    GET BY ID
    # ======================================================
    @staticmethod
    def get_by_id(id_vaccination: int):
        conn = get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()

            query = """
                SELECT
                    v.id_vaccination,
                    v.id_eleve,
                    v.id_personnel,
                    v.nom_vaccin,
                    v.date_vaccin,
                    v.rappel_necessaire,
                    e.nom,
                    e.prenom,
                    p.nom,
                    p.prenom
                FROM VACCINATION v
                JOIN ELEVE e ON e.id_eleve = v.id_eleve
                JOIN PERSONNEL_MEDICAL p ON p.id_personnel = v.id_personnel
                WHERE v.id_vaccination = %s
            """

            cursor.execute(query, (id_vaccination,))
            row = cursor.fetchone()

            if not row:
                return None

            return Vaccination(
                id_vaccination=row[0],
                id_eleve=row[1],
                id_personnel=row[2],
                nom_vaccin=row[3],
                date_vaccin=str(row[4]),
                rappel_necessaire=row[5],
                nom_eleve=f"{row[6]} {row[7]}",
                nom_personnel=f"{row[8]} {row[9]}"
            )

        except Exception as e:
            print("❌ ERREUR VaccinationDAO.get_by_id :", e)
            return None

        finally:
            try:
                cursor.close()
            except:
                pass
            try:
                conn.close()
            except:
                pass

    # ======================================================
    #                       INSERT
    # ======================================================
    @staticmethod
    def insert(v: Vaccination):
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()

            query = """
                INSERT INTO VACCINATION
                    (id_eleve, id_personnel, nom_vaccin, date_vaccin, rappel_necessaire)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(query, (
                v.id_eleve,
                v.id_personnel,
                v.nom_vaccin,
                v.date_vaccin,
                v.rappel_necessaire
            ))

            conn.commit()
            return True

        except Exception as e:
            print("❌ ERREUR VaccinationDAO.insert :", e)
            return False

        finally:
            try:
                cursor.close()
            except:
                pass
            try:
                conn.close()
            except:
                pass

    # ======================================================
    #                       UPDATE
    # ======================================================
    @staticmethod
    def update(v: Vaccination):
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()

            query = """
                UPDATE VACCINATION
                SET id_eleve = %s,
                    id_personnel = %s,
                    nom_vaccin = %s,
                    date_vaccin = %s,
                    rappel_necessaire = %s
                WHERE id_vaccination = %s
            """

            cursor.execute(query, (
                v.id_eleve,
                v.id_personnel,
                v.nom_vaccin,
                v.date_vaccin,
                v.rappel_necessaire,
                v.id_vaccination
            ))

            conn.commit()
            return True

        except Exception as e:
            print("❌ ERREUR VaccinationDAO.update :", e)
            return False

        finally:
            try:
                cursor.close()
            except:
                pass
            try:
                conn.close()
            except:
                pass

    # ======================================================
    #                       DELETE
    # ======================================================
    @staticmethod
    def delete(id_vaccination: int):
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM VACCINATION WHERE id_vaccination = %s",
                (id_vaccination,)
            )

            conn.commit()

            if cursor.rowcount == 0:
                print("⚠️ Aucune vaccination supprimée.")
                return False

            return True

        except Exception as e:
            print("❌ ERREUR VaccinationDAO.delete :", e)
            return False

        finally:
            try:
                cursor.close()
            except:
                pass
            try:
                conn.close()
            except:
                pass
