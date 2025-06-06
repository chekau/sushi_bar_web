import sqlite3
import hashlib


class Database:
    db_path = "database.db"
    schema_path = "schema.sql"

    @staticmethod
    def execute(sql_code: str, params: tuple = ()):
        conn = sqlite3.connect(Database.db_path)

        cursor = conn.cursor()
        cursor.execute(sql_code, params)
 
        conn.commit()

    