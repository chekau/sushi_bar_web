import mysql.connector
from src.model import Dish,User,Orders,Cart
from src.config import CONFIG
import hashlib



class Database: 
    __conection = None
    @classmethod
    def open(cls, 
             host=CONFIG['host'], 
             user=CONFIG['user'],
             password=CONFIG['password'],
             database=CONFIG['database']):
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
    def get_connection(cls):
        if cls.__conection is None:
            cls.connect()
        return cls.__conection
    
    @classmethod
    def execute(cls, query, params=None):
        connection = cls.get_connection()

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()  # Подтверждаем изменения, если это DML-запрос
            return cursor.fetchall()  # Возвращаем результат, если это 
    
    
    
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
    
    @staticmethod
    def find_dish_by_id(dish_id: int):
        dishes = Database.fetchall(
            "SELECT * FROM Dish WHERE id = %s", [dish_id])
        
        if not id:
            return None

        if not dishes:
            return None
        
        id, name, describtion, image, price = dishes[0]
        return Dish(id, name, describtion, image, price)
    

    
    @staticmethod
    def find_id_by_name(name: str):
        dish_id = Database.fetchall(
            "SELECT `id` FROM Dish WHERE name=%s", [name])
        
        if not name:
            return None
        
        if not dish_id:
            return None
        
        return dish_id
    
    @staticmethod
    def find_dish_by_id(dish_id: int):
        dishes = Database.fetchall(
            "SELECT * FROM Dish WHERE id = %s", [dish_id])
        
        if not dishes:
            return None
        
        id, name, describtion, image, price = dishes[0]
        return Dish(id, name, describtion, image, price)
    
    @staticmethod
    def delete_dish(dish_id: int) -> bool:
         # Если статьи с таким id нет, ничего не делаем и возвращаем False
        if DishTable.find_dish_by_id(dish_id) is None:
            return False

        Database.fetchall("DELETE FROM Dish WHERE id = %s", [dish_id])
        return True
    
    @staticmethod
    def update_dish(id: int, name: str, describtion: str, image: str, price: int) -> bool:
        # Если статьи с таким id нет, ничего не делаем и возвращаем False
        if DishTable.find_dish_by_id(id) is None:
            return False
        
        Database.execute(
            """
            UPDATE Dish
            SET name = %s,
                describtion = %s,
                image = %s,
                price = %s
            WHERE id = %s
            """,
            [name, describtion,image, price, id]
        )
        return True

    
    
    
        
    


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
    
    @staticmethod
    def find_order_id_by_user_id(user_id):
        order_id = Database.fetchall(
            "SELECT `id` FROM Orders WHERE user_id =%s", [user_id]
        )

        if not order_id:
            return None
        if not user_id:
            return None
        
        return order_id
    


class CartTable:
    @staticmethod
    def add_to_cart(user_id,dish_id, quantity=1):

    # Проверяем, есть ли уже это блюдо в корзине
        existing_item = Database.fetchall(
        "SELECT quantity FROM Cart WHERE user_id = %s AND dish_id = %s",
        (user_id, dish_id)
    )

        if existing_item:
        # Если блюдо уже есть в корзине, увеличиваем количество
            new_quantity = existing_item[0][0] + quantity
            Database.fetchall(
            "UPDATE Cart SET quantity = %s WHERE user_id = %s AND dish_id = %s",
            (new_quantity, user_id, dish_id)
        )
        else:
        # Если блюда нет в корзине, добавляем его
            Database.fetchall(
            "INSERT INTO Cart (user_id, dish_id, quantity) VALUES (%s, %s, %s)",
            (user_id, dish_id, quantity)
        )



    @staticmethod
    def get_dishes_from_user(user_id):
    

    # Получаем все блюда из корзины для данного пользователя
        dishes = Database.fetchall(
        "SELECT Dish.id,Dish.name,Dish.price,Cart.quantity FROM Cart JOIN Dish ON Cart.dish_id = Dish.id  WHERE Cart.user_id = %s",
        (user_id,)
    )

        return [{"id": dish[0], "name": dish[1], "price": dish[2], "quantity": dish[3]} for dish in dishes]

    @staticmethod
    def clear_cart(user_id):
        connection = Database.get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Cart WHERE user_id = %s", (user_id,))
            items = cursor.fetchall()  # Получаем все элементы в корзине
            
            cursor.execute("DELETE FROM Cart WHERE user_id = %s", (user_id,))
            connection.commit()
            
            return items

class DishToOrders:
    @staticmethod
    def add_dish_to_order(order_id, dish_id, quantity):

        sql = "INSERT INTO DishToOrders (`order_id`, `dish_id`, `quantity`) VALUE (%s,%s,%s)"
        values = (order_id, dish_id, quantity)
        Database.query(sql,values)


   