from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str

@dataclass
class Dish:
    name: str
    describtion: str
    image: str
    price: float

@dataclass
class Order:
    id: int
    user_id: int
    phone: str
    address: str
    delivery_time: str
    pay: str = "cash"
    status: str = "cart"  # Статус по умолчанию - "cart"