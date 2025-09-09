import json
from pathlib import Path
from typing import List, Dict
from storage.base_storage import BaseStorage
from utils.logger import get_logger

logger = get_logger()

class JSONStorage(BaseStorage):
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.products_file = self.data_dir / "products.json"
        self.sales_file = self.data_dir / "sales.json"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._ensure_files_exist()

    def _ensure_files_exist(self):
        """Crea los archivos JSON si no existen."""
        for file in [self.products_file, self.sales_file]:
            if not file.exists():
                with open(file, 'w') as f:
                    json.dump([], f)
                logger.info(f"Archivo de datos creado: {file}")

    def load_products(self) -> List[Dict]:
        try:
            with open(self.products_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_products(self, products: List[Dict]):
        with open(self.products_file, 'w') as f:
            json.dump(products, f, indent=4)
        logger.info("Productos guardados exitosamente.")

    def load_sales(self) -> List[Dict]:
        try:
            with open(self.sales_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_sales(self, sales: List[Dict]):
        with open(self.sales_file, 'w') as f:
            json.dump(sales, f, indent=4)
        logger.info("Ventas guardadas exitosamente.")