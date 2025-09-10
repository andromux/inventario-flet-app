import flet as ft
import asyncio
from services.inventory_service import InventoryService
from models.product import Product
from utils.logger import get_logger

logger = get_logger()

class CatalogPage(ft.Column):
    def __init__(self, inventory_service: InventoryService, page: ft.Page):
        super().__init__(
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        self.inventory_service = inventory_service
        self.page = page
        self.products = self.inventory_service.get_all_products()
        
        # Controles para agregar un nuevo producto
        self.product_name = ft.TextField(label="Nombre", col={"xs": 12, "sm": 6, "md": 4})
        self.product_cost = ft.TextField(label="Costo", value="0.00", col={"xs": 12, "sm": 6, "md": 4})
        self.product_price = ft.TextField(label="Precio", value="0.00", col={"xs": 12, "sm": 6, "md": 4})
        self.product_stock = ft.TextField(label="Stock", value="0", col={"xs": 12, "sm": 6, "md": 4})
        self.add_product_button = ft.ElevatedButton("Agregar Producto", on_click=self.add_product, col={"xs": 12, "sm": 12, "md": 4})
        
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Costo")),
                ft.DataColumn(ft.Text("Precio")),
                ft.DataColumn(ft.Text("Stock"))
            ],
            rows=[]
        )
        self.load_table()
        
        self.controls = [
            ft.Text("Catálogo de Productos", size=24, weight="bold"),
            # Contenedor para el formulario de agregar producto
            ft.Container(
                content=ft.ResponsiveRow(
                    [
                        self.product_name,
                        self.product_cost,
                        self.product_price,
                        self.product_stock,
                        self.add_product_button,
                    ],
                    run_spacing=10
                ),
                padding=ft.padding.all(10),
                border=ft.border.all(1, ft.Colors.OUTLINE),
                border_radius=8
            ),
            ft.Divider(),
            ft.Text("Productos existentes", size=18, weight="bold"),
            # Contenedor para la tabla de productos, usando ListView para scroll optimizado
            ft.Container(
                content=ft.ListView(
                    [self.data_table],
                    expand=True
                ),
                expand=True
            )
        ]

    def load_table(self):
        self.data_table.rows.clear()
        self.products = self.inventory_service.get_all_products()
        for p in self.products:
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(p.id[:8])),
                        ft.DataCell(ft.Text(p.name)),
                        ft.DataCell(ft.Text(f"${p.cost:.2f}")),
                        ft.DataCell(ft.Text(f"${p.price:.2f}")),
                        ft.DataCell(ft.Text(str(p.stock)))
                    ]
                )
            )
        self.update()

    async def add_product(self, e):
        # Validación: El nombre del producto no puede estar vacío
        if not self.product_name.value:
            self.page.overlay.append(ft.SnackBar(ft.Text("El nombre del producto no puede estar vacío.")))
            self.page.update()
            return

        try:
            # Manejo de formatos de números, eliminando comas
            cost_str = self.product_cost.value.replace(',', '')
            price_str = self.product_price.value.replace(',', '')
            stock_str = self.product_stock.value.replace(',', '')

            cost = float(cost_str)
            price = float(price_str)
            stock = int(stock_str)
            
            self.inventory_service.add_product(self.product_name.value, cost, price, stock)
            self.load_table()
            
            # Muestra el mensaje de éxito
            self.page.overlay.append(
                ft.SnackBar(content=ft.Text(f"Producto '{self.product_name.value}' agregado exitosamente."), open=True)
            )
            
            # Limpia los campos
            self.product_name.value = ""
            self.product_cost.value = "0.00"
            self.product_price.value = "0.00"
            self.product_stock.value = "0"

            self.page.update()

        except ValueError:
            # Muestra un mensaje de error específico
            self.page.overlay.append(
                ft.SnackBar(content=ft.Text("Error en los valores. Asegúrate de que costo, precio y stock sean números válidos."))
            )
            self.page.update()
