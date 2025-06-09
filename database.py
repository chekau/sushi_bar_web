import mysql.connector
from model import Dish
import hashlib

connection = mysql.connector.connect(
    
    host='109.206.169.221',
    user='seschool_01',
    password='seschool_01',
    database='seschool_01_pks1'
)

class Database: 
    __conection = None
    @classmethod
    def open(cls, 
             host='109.206.169.221', 
             user='seschool_01', 
             password='seschool_01', 
             database='seschool_01_pks1'):
        if cls.__conection is None:
            cls.__conection = mysql.connector.connect(
                user=user,
                password=password,
                host=host,
                database=database   
            )

            cls.__cursor = cls.__conection.cursor()
    @classmethod
    def query(cls, sql, values):

        cls.__cursor.execute(sql,values)
        cls.__conection.commit()
        result = cls.__cursor.fetchall()
        return result
       
    @classmethod
    def fetchall(cls, sql, params: tuple = ()):

        cls.__cursor.execute(sql,params)
        
        result = cls.__cursor.fetchall()
        return result
    
    
    
    @classmethod
    def close(cls):
        cls.__conection.close()

    @staticmethod
    def register_user(username,email,password):
        #есть ли пользователи у которых уже указан такой никнейм или электронная почта
        users = Database.fetchall("SELECT * FROM Users WHERE username = ? OR email = ?",
            [username, email]
         )
        print(users)
        if users:
            return False
         
        password_hash = hashlib.md5(password.encode()).hexdigest()

        Database.execute("INSERT INTO Users (username, email, password_hash)"
                          "VALUES (?,?,?)",
                          [username,email,password_hash]
        )
        return True

    @staticmethod
    def can_be_logged_in(user_or_email: str, password: str):
        # 1. Проверить, что пользователь с таким именем или электронной почтой есть
        users = Database.fetchall("SELECT * FROM Users WHERE username = ? OR email = ?",
            [user_or_email, user_or_email]
        )
        if not users:
            return False
        
        # 2. Берем хэш-пароля заданного пользователя
        # users = [ (1, "nnn", "nnn@ayndex.ru", "asfksdhfihsiuh523454534jh534kjkhk34j534") ]
        user = users[0]
        real_password_hash = user[3]

        # 3. Сравниваем хэш хранящийся в базе данных и хэш пароля,
        # который попытались ввести
        password_hash = hashlib.md5( password.encode() ).hexdigest()
        if real_password_hash != password_hash:
            return False
        return True

    

class DishTable:
    @classmethod
    def add(cls,name, describtion, image, price):
        sql = "INSERT INTO Dish (`name`, `describtion`, `image`, `price`) VALUE (%s,%s,%s,%s)"
        values = (name, describtion, image, price)
        print(name,describtion,image,price)
        Database.query(sql,values)

    @staticmethod
    def get_count_of_users():
        count = Database.fetchall(
            "SELECT COUNT(*) FROM Dish"
            )[0][0]        
        return count


    @staticmethod
    def get_all_dishes():
        dishes = []
        

        for (name,describtion,image,price) in Database.fetchall(

        "SELECT * FROM Dish"):
            dishes.append(Dish(
            name=name,
            describtion=describtion,
            image=image,
            price=price   
    ))

        return dishes

     

