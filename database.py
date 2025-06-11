import mysql.connector
from model import Dish,User,Orders
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

    @classmethod
    def register_user(cls,email, password):
        users = cls.fetchall("SELECT * FROM Users WHERE email = %s", (email,))
        if users:
            return False

        password_hash = hashlib.md5(password.encode()).hexdigest()
        cls.__cursor.execute("INSERT INTO Users (email, password_hash) VALUES (%s, %s)", (email, password_hash))
        cls.__conection.commit()
        return True

    @classmethod
    def can_be_logged_in(cls,email: str, password: str):
        # 1. Проверить, что пользователь с таким именем или электронной почтой есть
        users = Database.fetchall("SELECT * FROM Users WHERE email = %s",
            [email]
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
        

        for (id,name,describtion,image,price) in Database.fetchall(

        "SELECT * FROM Dish"):
            dishes.append(Dish(
            id=id,
            name=name,
            describtion=describtion,
            image=image,
            price=price   
    ))

        return dishes

     
    @staticmethod
    def find_dish_by_name(name: str):
        dishes = Database.fetchall(
            "SELECT * FROM Dish WHERE name = %s", [name])
        
        if not name:
            return None

        if not dishes:
            return None
        
        id, name, describtion, image, price = dishes[0]
        return Dish(id, name, describtion, image, price)
    
        
    


class OrdersTable:
    @staticmethod
    def create_new_order(user_id, customer_name,phone, address, delivery_time, payment_method, status):
        sql = "INSERT INTO Orders (`user_id`, `customer_name`, `phone`, `address`,`delivery_time`, `payment_method`, `status`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (user_id,customer_name, phone, address,delivery_time, payment_method, status)
        Database.query(sql,values)


    @staticmethod
    def checkout_order(order):
        # Обработка оплаты заказа
        order.status = "cooking"  # Меняем статус на "cooking"
    
        # Создаем новый заказ с тем же пользователем и статусом "cart"
        new_order = OrdersTable.create_new_order(order.id,order.user_id, order.phone, order.address, order.delivery_time)
    
        return order, new_order