from dataclasses import dataclass, asdict

@dataclass
class Product:
    id: str
    name: str
    cost: float
    price: float
    stock: int

    def to_dict(self):
        return asdict(self)