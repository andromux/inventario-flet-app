import flet as ft
from services.inventory_service import InventoryService
from services.sales_service import SalesService
from ui.pages.catalog_page import CatalogPage
from ui.pages.sales_page import SalesPage
from ui.pages.reports_page import ReportsPage
from utils.logger import get_logger

logger = get_logger()

class MainView(ft.Column):
    def __init__(self, page: ft.Page, inventory_service: InventoryService, sales_service: SalesService):
        super().__init__(expand=True)

        self.page = page
        self.inventory_service = inventory_service
        self.sales_service = sales_service
        self.pages = {
            "Catálogo": CatalogPage(self.inventory_service, self.page),
            "Ventas": SalesPage(self.inventory_service, self.sales_service, self.page),
            "Reportes": ReportsPage(self.sales_service, self.page)
        }
        self.current_page = self.pages["Catálogo"]
        
        # Se usa ft.NavigationBar para la navegación horizontal en la parte inferior.
        self.navigation_bar = ft.NavigationBar(
            selected_index=0,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.INVENTORY,
                    selected_icon=ft.Icons.INVENTORY_ROUNDED,
                    label="Catálogo"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.POINT_OF_SALE,
                    selected_icon=ft.Icons.POINT_OF_SALE_ROUNDED,
                    label="Ventas"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.BAR_CHART,
                    selected_icon=ft.Icons.BAR_CHART_ROUNDED,
                    label="Reportes"
                )
            ],
            on_change=self.handle_navigation_change
        )
        
        self.page_container = ft.Column(
            controls=[self.current_page],
            expand=True,
            alignment=ft.MainAxisAlignment.START,
        )
        
        self.controls = [
            self.navigation_bar,
            ft.Divider(height=1),
            self.page_container
        ]

    def handle_navigation_change(self, e: ft.ControlEvent):
        """Maneja la navegación entre páginas y refresca la vista."""
        page_index = e.control.selected_index
        page_name = list(self.pages.keys())[page_index]

        self.page_container.controls.clear()
        self.page_container.opacity = 0
        self.page_container.update()
        
        self.current_page = self.pages[page_name]
        
        # Llama a un método de refresco si existe
        if hasattr(self.current_page, 'refresh_products'):
            self.current_page.refresh_products()
        
        self.page_container.controls.append(self.current_page)
        
        self.page_container.opacity = 1
        self.page_container.update()
        
        logger.info(f"Navegando a la página: {page_name}")
