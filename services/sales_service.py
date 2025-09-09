import uuid
from typing import List, Dict, Optional
from datetime import datetime
from models.sale import Sale, SaleItem
from services.inventory_service import InventoryService
from storage.base_storage import BaseStorage
from utils.logger import get_logger

logger = get_logger()

class SalesService:
    def __init__(self, storage: BaseStorage, inventory_service: InventoryService):
        self._storage = storage
        self._inventory = inventory_service
        self._sales: Dict[str, Sale] = {}
        self.load_sales()

    def load_sales(self):
        """Carga las ventas desde el almacenamiento."""
        try:
            sales_data = self._storage.load_sales()
            self._sales = {s['id']: Sale(id=s['id'], timestamp=s['timestamp'], total_revenue=s['total_revenue'], total_cost=s['total_cost'], total_profit=s['total_profit'], items=[SaleItem(**item) for item in s['items']]) for s in sales_data}
            logger.info(f"Se cargaron {len(self._sales)} ventas.")
        except Exception as e:
            logger.error(f"Error al cargar ventas: {e}")
            self._sales = {}

    def save_sales(self):
        """Guarda las ventas en el almacenamiento."""
        try:
            sales_data = [s.to_dict() for s in self._sales.values()]
            self._storage.save_sales(sales_data)
            logger.info("Ventas guardadas.")
        except Exception as e:
            logger.error(f"Error al guardar ventas: {e}")

    def get_all_sales(self) -> List[Sale]:
        return list(self._sales.values())

    def record_sale(self, sale_items: List[Dict]) -> Optional[Sale]:
        """
        Registra una venta y actualiza el inventario.
        sale_items: Lista de diccionarios, ej. [{'product_id': '...', 'quantity': 1}]
        """
        if not sale_items:
            logger.warning("Intento de registrar una venta vacía.")
            return None

        items: List[SaleItem] = []
        total_revenue = 0.0
        total_cost = 0.0

        for item in sale_items:
            product = self._inventory.get_product(item['product_id'])
            quantity = item['quantity']
            if not product or product.stock < quantity or quantity <= 0:
                logger.warning(f"No se pudo registrar la venta: stock insuficiente para el producto {product.name if product else 'ID no encontrado'}.")
                return None
            
            subtotal = product.price * quantity
            cost_subtotal = product.cost * quantity
            
            items.append(SaleItem(
                product_id=product.id,
                name=product.name,
                quantity=quantity,
                price=product.price,
                cost=product.cost,
                subtotal=subtotal
            ))
            total_revenue += subtotal
            total_cost += cost_subtotal
            
            self._inventory.update_stock(product.id, quantity)
        
        new_sale = Sale(
            id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            total_revenue=total_revenue,
            total_cost=total_cost,
            total_profit=total_revenue - total_cost,
            items=items
        )
        self._sales[new_sale.id] = new_sale
        self.save_sales()
        logger.info(f"Venta registrada con ID: {new_sale.id}")
        return new_sale