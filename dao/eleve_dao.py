# dao/eleve_dao.py

from db.connection import get_connection
from models.eleve import Eleve


class EleveDAO:

    # ==========================================================
    #                     GET ALL
    # ==========================================================
    @staticmethod
    def get_all():
        conn = get_connection()
        if not conn:
            print("❌ Connexion MySQL introuvable")
            return []

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_eleve, nom, prenom, date_naissance,
                       classe, sexe, grp_sanguin, telephone_parent
                FROM ELEVE
                ORDER BY id_eleve ASC;
            """)

            rows = cursor.fetchall()
            result = []

            for row in rows:
                result.append(Eleve(
                    id_eleve=row[0],
                    nom=row[1],
                    prenom=row[2],
                    date_naissance=str(row[3]),
                    classe=row[4],
                    sexe=row[5],
                    grp_sanguin=row[6],
                    telephone_parent=row[7]
                ))

            return result

        except Exception as e:
            print("❌ ERREUR EleveDAO.get_all :", e)
            return []

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass

    # ==========================================================
    #                     GET BY ID
    # ==========================================================
    @staticmethod
    def get_by_id(id_eleve):
        conn = get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_eleve, nom, prenom, date_naissance,
                       classe, sexe, grp_sanguin, telephone_parent
                FROM ELEVE
                WHERE id_eleve = %s
            """, (id_eleve,))

            row = cursor.fetchone()
            if not row:
                return None

            return Eleve(
                id_eleve=row[0],
                nom=row[1],
                prenom=row[2],
                date_naissance=str(row[3]),
                classe=row[4],
                sexe=row[5],
                grp_sanguin=row[6],
                telephone_parent=row[7]
            )

        except Exception as e:
            print("❌ ERREUR EleveDAO.get_by_id :", e)
            return None

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass

    # ==========================================================
    #                     INSERT
    # ==========================================================
    @staticmethod
    def insert(eleve: Eleve):
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ELEVE 
                (nom, prenom, date_naissance, classe, sexe, grp_sanguin, telephone_parent)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                eleve.nom,
                eleve.prenom,
                eleve.date_naissance,
                eleve.classe,
                eleve.sexe,
                eleve.grp_sanguin,
                eleve.telephone_parent
            ))

            conn.commit()
            return True

        except Exception as e:
            print("❌ ERREUR EleveDAO.insert :", e)
            return False

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass

    # ==========================================================
    #                     UPDATE
    # ==========================================================
    @staticmethod
    def update(id_eleve: int, data: dict):
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE ELEVE SET 
                    nom = %s,
                    prenom = %s,
                    date_naissance = %s,
                    classe = %s,
                    sexe = %s,
                    grp_sanguin = %s,
                    telephone_parent = %s
                WHERE id_eleve = %s
            """, (
                data["nom"],
                data["prenom"],
                data["date_naissance"],
                data["classe"],
                data["sexe"],
                data["grp_sanguin"],
                data["telephone_parent"],
                id_eleve
            ))

            conn.commit()
            return True

        except Exception as e:
            print("❌ ERREUR EleveDAO.update :", e)
            return False

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass

    # ==========================================================
    #                     DELETE
    # ==========================================================
    @staticmethod
    def delete(id_eleve: int):
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ELEVE WHERE id_eleve = %s", (id_eleve,))
            conn.commit()
            return True

        except Exception as e:
            print("❌ ERREUR EleveDAO.delete :", e)
            return False

        finally:
            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass
