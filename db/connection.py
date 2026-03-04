import pymysql

def get_connection():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="Amine5050",
            database="DBPRJ",
            port=3306,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.Cursor
        )
        return conn

    except Exception as e:
        print("❌ ERREUR get_connection :", e)
        return None
