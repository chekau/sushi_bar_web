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

class Dish:
    @classmethod
    def add(cls,name, describtion, image, price):
        sql = "INSERT INTO Dish (`name`, `describtion`, `image`, `price`) VALUE (%s,%s,%s,%s)"
        values = (name, describtion, image, price)
        Database.query(sql,values)

