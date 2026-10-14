from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    id: int
    name: str
    description: str
    price: float
    stock: int
