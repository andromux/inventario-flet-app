import uuid
from typing import List, Dict, Optional
from models.product import Product
from storage.base_storage import BaseStorage
from utils.logger import get_logger

logger = get_logger()

class InventoryService:
    def __init__(self, storage: BaseStorage):
        self._storage = storage
        self._products: Dict[str, Product] = {}
        self.load_products()

    def load_products(self):
        """Carga los productos desde el almacenamiento."""
        try:
            products_data = self._storage.load_products()
            self._products = {p['id']: Product(**p) for p in products_data}
            logger.info(f"Se cargaron {len(self._products)} productos.")
        except Exception as e:
            logger.error(f"Error al cargar productos: {e}")
            self._products = {}

    def save_products(self):
        """Guarda los productos en el almacenamiento."""
        try:
            products_data = [p.to_dict() for p in self._products.values()]
            self._storage.save_products(products_data)
            logger.info("Productos guardados.")
        except Exception as e:
            logger.error(f"Error al guardar productos: {e}")

    def get_all_products(self) -> List[Product]:
        return list(self._products.values())

    def get_product(self, product_id: str) -> Optional[Product]:
        return self._products.get(product_id)

    def add_product(self, name: str, cost: float, price: float, stock: int) -> bool:
        new_product = Product(str(uuid.uuid4()), name, cost, price, stock)
        if new_product.id in self._products:
            logger.warning(f"Intento de agregar producto duplicado: {new_product.id}")
            return False
        self._products[new_product.id] = new_product
        self.save_products()
        logger.info(f"Producto agregado: {name}")
        return True

    def update_product(self, product_id: str, **kwargs) -> bool:
        if product_id not in self._products:
            logger.warning(f"No se pudo actualizar el producto. ID no encontrado: {product_id}")
            return False
        product = self._products[product_id]
        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)
        self.save_products()
        logger.info(f"Producto actualizado: {product.name}")
        return True

    def delete_product(self, product_id: str) -> bool:
        if product_id not in self._products:
            logger.warning(f"No se pudo eliminar el producto. ID no encontrado: {product_id}")
            return False
        del self._products[product_id]
        self.save_products()
        logger.info(f"Producto eliminado: {product_id}")
        return True

    def update_stock(self, product_id: str, quantity: int) -> bool:
        if product_id not in self._products:
            logger.warning(f"No se pudo actualizar el stock. ID no encontrado: {product_id}")
            return False
        product = self._products[product_id]
        new_stock = product.stock - quantity
        if new_stock < 0:
            logger.warning(f"Stock insuficiente para el producto: {product.name}")
            return False
        product.stock = new_stock
        self.save_products()
        logger.info(f"Stock actualizado para {product.name}. Nuevo stock: {new_stock}")
        return True