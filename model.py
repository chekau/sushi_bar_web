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


