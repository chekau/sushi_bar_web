from dataclasses import dataclass


@dataclass
class Dish:
    name: str
    describtion: str
    image: str
    price: float
