import sqlite3
import hashlib
from dish import Dish

class Database:
    db_path = "database.db"
    schema_path = "schema.sql"

    @staticmethod
    def execute(sql_code: str, params: tuple = ()):
        conn = sqlite3.connect(Database.db_path)

        cursor = conn.cursor()
        cursor.execute(sql_code, params)
 
        conn.commit()


    @staticmethod
    def create_tables():
        
        with open(Database.schema_path) as schema_file:
            sql_code = schema_file.read()
            conn = sqlite3.connect(Database.db_path)

            cursor = conn.cursor()
            cursor.executescript(sql_code)

            conn.commit()
    
    @staticmethod
    def save(dish: Dish):
        # if Database.find_article_by_title(article.title) is not None:
        #      return False


        Database.execute(f"""
         INSERT INTO Dish (name, description, image, price) VALUES (?, ?, ?, ?)
         """, (dish.name, dish.description, dish.image, dish.price))
        return True