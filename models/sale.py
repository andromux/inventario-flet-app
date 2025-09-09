from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List

@dataclass
class SaleItem:
    product_id: str
    name: str
    quantity: int
    price: float
    cost: float
    subtotal: float

    def to_dict(self):
        return asdict(self)

@dataclass
class Sale:
    id: str
    timestamp: str
    total_revenue: float
    total_cost: float
    total_profit: float
    items: List[SaleItem]

    def to_dict(self):
        return asdict(self)
