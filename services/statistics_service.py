from db.connection import get_connection

class StatisticsService:

    # ======================================================
    #  ÉLÈVES
    # ======================================================
    @staticmethod
    def eleves_par_sexe():
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("SELECT sexe, COUNT(*) FROM ELEVE GROUP BY sexe")
            rows = cur.fetchall()
        except:
            rows = []

        data = {"M": 0, "F": 0}
        total = 0

        for sexe, count in rows:
            if sexe in data:
                data[sexe] = count
            total += count

        data["percent_M"] = round(data["M"] * 100 / total, 2) if total else 0
        data["percent_F"] = round(data["F"] * 100 / total, 2) if total else 0

        cur.close()
        conn.close()
        return data

    @staticmethod
    def eleves_par_classe():
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("SELECT classe, COUNT(*) FROM ELEVE GROUP BY classe")
            rows = cur.fetchall()
        except:
            rows = []

        cur.close()
        conn.close()

        return [{"classe": r[0] or "—", "count": r[1]} for r in rows]

    @staticmethod
    def eleves_par_groupe_sanguin():
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("SELECT grp_sanguin, COUNT(*) FROM ELEVE GROUP BY grp_sanguin")
            rows = cur.fetchall()
        except:
            rows = []

        cur.close()
        conn.close()

        return [{"groupe": r[0] or "—", "count": r[1]} for r in rows]

    @staticmethod
    def note_medicale_stats():
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT 
                    AVG(note_medicale), 
                    MIN(note_medicale), 
                    MAX(note_medicale)
                FROM DOSSIER_MEDICAL
                WHERE note_medicale IS NOT NULL
            """)
            avg, mn, mx = cur.fetchone()
        except:
            avg = mn = mx = None

        cur.close()
        conn.close()

        return {
            "avg": round(avg, 2) if avg is not None else 0,
            "min": mn if mn is not None else 0,
            "max": mx if mx is not None else 0
        }

    @staticmethod
    def allergies_principales():
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT allergies, COUNT(*)
                FROM DOSSIER_MEDICAL
                WHERE allergies IS NOT NULL AND allergies != ''
                GROUP BY allergies
                ORDER BY COUNT(*) DESC
            """)
            rows = cur.fetchall()
        except:
            rows = []

        cur.close()
        conn.close()

        return [{"allergie": r[0] or "—", "count": r[1]} for r in rows]

    # ======================================================
    #  CONSULTATIONS
    # ======================================================
    @staticmethod
    def consultations_par_type():
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT type_consultation, COUNT(*)
                FROM CONSULTATION
                WHERE type_consultation IS NOT NULL AND type_consultation != ''
                GROUP BY type_consultation
            """)
            rows = cur.fetchall()
        except:
            rows = []

        cur.close()
        conn.close()

        return [{"type": r[0] or "—", "count": r[1]} for r in rows]

    # ======================================================
    #  ⭐ VERSION FINALE : TRI PAR ANNÉE + MOIS ⭐
    # ======================================================
    @staticmethod
    def consultations_par_mois():
        conn = get_connection()
        cur = conn.cursor()

        labels = []   # ex: ["2024-12", "2025-01"]
        count = []    # ex: [5, 12]

        try:
            cur.execute("""
                SELECT 
                    YEAR(date_consultation) AS y,
                    MONTH(date_consultation) AS m,
                    COUNT(*)
                FROM CONSULTATION
                WHERE date_consultation IS NOT NULL
                GROUP BY YEAR(date_consultation), MONTH(date_consultation)
                ORDER BY YEAR(date_consultation), MONTH(date_consultation)
            """)
            rows = cur.fetchall()

            for y, m, c in rows:
                if y is not None and m is not None:
                    labels.append(f"{y}-{m:02d}")
                    count.append(int(c))

        except Exception as e:
            print("❌ ERREUR consultations_par_mois :", e)

        finally:
            try: cur.close()
            except: pass
            try: conn.close()
            except: pass

        return {
            "labels": labels,
            "count": count
        }

    @staticmethod
    def top_symptomes():
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT symptomes, COUNT(*)
                FROM CONSULTATION
                WHERE symptomes IS NOT NULL AND symptomes != ''
                GROUP BY symptomes
                ORDER BY COUNT(*) DESC
                LIMIT 5
            """)
            rows = cur.fetchall()
        except:
            rows = []

        cur.close()
        conn.close()

        return [{"symptome": r[0] or "—", "count": r[1]} for r in rows]

    @staticmethod
    def decisions_stats():
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT decisions, COUNT(*)
                FROM CONSULTATION
                WHERE decisions IS NOT NULL AND decisions != ''
                GROUP BY decisions
            """)
            rows = cur.fetchall()
        except:
            rows = []

        cur.close()
        conn.close()

        return [{"decision": r[0] or "—", "count": r[1]} for r in rows]

    # ======================================================
    #  PRESCRIPTIONS
    # ======================================================
    @staticmethod
    def prescriptions_globales():
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("SELECT COUNT(*) FROM PRESCRIPTION")
            prescriptions = cur.fetchone()[0]
        except:
            prescriptions = 0

        try:
            cur.execute("SELECT COUNT(*) FROM CONSULTATION")
            consultations = cur.fetchone()[0]
        except:
            consultations = 0

        cur.close()
        conn.close()

        taux = round(prescriptions * 100 / consultations, 2) if consultations else 0

        return {
            "prescriptions": prescriptions,
            "consultations": consultations,
            "taux_prescription": taux
        }

    @staticmethod
    def top_medicaments():
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT nom_medicament, COUNT(*)
                FROM MEDICAMENT
                GROUP BY nom_medicament
                ORDER BY COUNT(*) DESC
                LIMIT 5
            """)
            rows = cur.fetchall()
        except:
            rows = []

        cur.close()
        conn.close()

        return [{"medicament": r[0] or "—", "count": r[1]} for r in rows]

    # ======================================================
    #  RENDEZ-VOUS
    # ======================================================
    @staticmethod
    def rdv_par_statut():
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT statut, COUNT(*)
                FROM RENDEZ_VOUS
                WHERE statut IS NOT NULL AND statut != ''
                GROUP BY statut
            """)
            rows = cur.fetchall()
        except:
            rows = []

        total = sum(r[1] for r in rows)
        annule = sum(r[1] for r in rows if str(r[0]).lower() == "annule")

        cur.close()
        conn.close()

        return {
            "raw": [{"statut": r[0] or "—", "count": r[1]} for r in rows],
            "taux_annulation": round(annule * 100 / total, 2) if total else 0
        }

    @staticmethod
    def rdv_par_type():
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT type_rdv, COUNT(*)
                FROM RENDEZ_VOUS
                WHERE type_rdv IS NOT NULL AND type_rdv != ''
                GROUP BY type_rdv
            """)
            rows = cur.fetchall()
        except:
            rows = []

        cur.close()
        conn.close()

        return [{"type": r[0] or "—", "count": r[1]} for r in rows]

    # ======================================================
    #  VACCINS
    # ======================================================
    @staticmethod
    def vaccins_par_nom():
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT nom_vaccin, COUNT(*)
                FROM VACCINATION
                WHERE nom_vaccin IS NOT NULL AND nom_vaccin != ''
                GROUP BY nom_vaccin
                ORDER BY COUNT(*) DESC
            """)
            rows = cur.fetchall()
        except:
            rows = []

        cur.close()
        conn.close()

        return [{"vaccin": r[0] or "—", "count": r[1]} for r in rows]

    @staticmethod
    def vaccins_rappel_stats():
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT rappel_necessaire, COUNT(*)
                FROM VACCINATION
                GROUP BY rappel_necessaire
            """)
            rows = cur.fetchall()
        except:
            rows = []

        cur.close()
        conn.close()

        data = {"OUI": 0, "NON": 0}
        total = 0

        for k, c in rows:
            key = k if k in ("OUI", "NON") else "NON"
            data[key] += c
            total += c

        return {
            "total": total,
            "OUI": data["OUI"],
            "NON": data["NON"],
            "percent_oui": round(data["OUI"] * 100 / total, 2) if total else 0,
            "percent_non": round(data["NON"] * 100 / total, 2) if total else 0
        }
