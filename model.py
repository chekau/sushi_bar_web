from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str

@dataclass
class Dish:
    id: int
    name: str
    describtion: str
    image: str
    price: float

@dataclass
class Orders:
    id: int
    user_id: int
    customer_name: str
    phone: str
    address: str
    delivery_time: str
    payment_method: str = "cash"
    status: str = "cart"  # Статус по умолчанию - "cart"



@dataclass
class DishToOrders:
    dish_id: int
    order_id: int