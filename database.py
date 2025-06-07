import mysql.connector
from dish import Dish

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
    def close(cls):
        cls.__conection.close()

    

class DishTable:
    @classmethod
    def add(cls,name, describtion, image, price):
        sql = "INSERT INTO Dish (`name`, `describtion`, `image`, `price`) VALUE (%s,%s,%s,%s)"
        values = (name, describtion, image, price)
        Database.query(sql,values)

    @staticmethod
    def get_count_of_users():
        count = Database.query(
            "SELECT COUNT(*) FROM users"
            )[0][0]        
        return count


    @staticmethod
    def get_all_dishes():
        dishes = []
        

        for (name,describtion,image,price) in Database.query(

        "SELECT * FROM dishes"):
            dishes.append(Dish(
            name=name,
            describtion=describtion,
            image=image,
            price=price   
    ))

        return dishes

     

