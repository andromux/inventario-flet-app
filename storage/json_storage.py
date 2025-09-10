import json
import os
from typing import List, Dict
from storage.base_storage import BaseStorage
from utils.logger import get_logger

logger = get_logger()

class JSONStorage(BaseStorage):
    """
    Una clase de almacenamiento que maneja la carga y guardado de datos
    de productos y ventas en archivos JSON.
    """
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.products_file = os.path.join(self.data_dir, 'products.json')
        self.sales_file = os.path.join(self.data_dir, 'sales.json')
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Asegura que el directorio de datos exista."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"Directorio de datos creado: {self.data_dir}")

    def load_products(self) -> List[Dict]:
        """Carga productos del archivo JSON."""
        if not os.path.exists(self.products_file):
            logger.warning("Archivo products.json no encontrado. Devolviendo lista vacía.")
            return []
        try:
            with open(self.products_file, 'r', encoding='utf-8') as f:
                products = json.load(f)
                logger.info("Productos cargados exitosamente.")
                return products
        except json.JSONDecodeError as e:
            logger.error(f"Error al decodificar JSON en products.json: {e}")
            return []
        except Exception as e:
            logger.error(f"Error inesperado al cargar products.json: {e}")
            return []

    def save_products(self, products: List[Dict]):
        """Guarda productos en el archivo JSON."""
        logger.info(f"Intentando guardar {len(products)} productos en {self.products_file}")
        try:
            with open(self.products_file, 'w', encoding='utf-8') as f:
                json.dump(products, f, indent=4)
            logger.info("Productos guardados exitosamente.")
        except IOError as e:
            logger.error(f"Error de E/S al guardar products.json: {e}")
        except Exception as e:
            logger.error(f"Error inesperado al guardar products.json: {e}")

    def load_sales(self) -> List[Dict]:
        """Carga ventas del archivo JSON."""
        if not os.path.exists(self.sales_file):
            logger.warning("Archivo sales.json no encontrado. Devolviendo lista vacía.")
            return []
        try:
            with open(self.sales_file, 'r', encoding='utf-8') as f:
                sales = json.load(f)
                logger.info("Ventas cargadas exitosamente.")
                return sales
        except json.JSONDecodeError as e:
            logger.error(f"Error al decodificar JSON en sales.json: {e}")
            return []
        except Exception as e:
            logger.error(f"Error inesperado al cargar sales.json: {e}")
            return []

    def save_sales(self, sales: List[Dict]):
        """Guarda ventas en el archivo JSON."""
        logger.info(f"Intentando guardar {len(sales)} ventas en {self.sales_file}")
        try:
            with open(self.sales_file, 'w', encoding='utf-8') as f:
                json.dump(sales, f, indent=4)
            logger.info("Ventas guardadas exitosamente.")
        except IOError as e:
            logger.error(f"Error de E/S al guardar sales.json: {e}")
        except Exception as e:
            logger.error(f"Error inesperado al guardar sales.json: {e}")
