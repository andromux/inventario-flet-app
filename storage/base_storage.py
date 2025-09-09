from abc import ABC, abstractmethod
from typing import List, Dict

class BaseStorage(ABC):
    @abstractmethod
    def load_products(self) -> List[Dict]:
        pass

    @abstractmethod
    def save_products(self, products: List[Dict]):
        pass

    @abstractmethod
    def load_sales(self) -> List[Dict]:
        pass

    @abstractmethod
    def save_sales(self, sales: List[Dict]):
        pass