from dataclasses import dataclass


@dataclass
class Dish:
    name: str
    description: str
    image: str
    price: float
