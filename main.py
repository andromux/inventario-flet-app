import flet as ft
from ui.main_view import MainView
from services.inventory_service import InventoryService
from services.sales_service import SalesService
from storage.json_storage import JSONStorage
from utils.logger import setup_logger

def main(page: ft.Page):
    """
    Punto de entrada de la aplicación.
    Inicializa la página, los servicios y la vista principal.
    """
    page.title = "Inventario Productos"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.window_width = 1200
    page.window_height = 800
    page.window_min_width = 800
    page.window_min_height = 600
    page.padding = 0
    
    # 1. Inicializar el logger
    logger = setup_logger()

    # 2. Inicializar la capa de almacenamiento y servicios
    try:
        data_storage = JSONStorage()
        inventory_service = InventoryService(data_storage)
        sales_service = SalesService(data_storage, inventory_service)
    except Exception as e:
        logger.error(f"Error al inicializar servicios: {e}")
        page.add(ft.Text(f"Error crítico al iniciar la aplicación: {e}", color="red"))
        page.update()
        return

    # 3. Crear y agregar la vista principal
    main_view = MainView(page, inventory_service, sales_service)
    page.add(main_view)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)