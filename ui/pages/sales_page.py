import flet as ft
import asyncio
from services.inventory_service import InventoryService
from services.sales_service import SalesService
from utils.logger import get_logger

logger = get_logger()

class SalesPage(ft.Column):
    def __init__(self, inventory_service: InventoryService, sales_service: SalesService, page: ft.Page):
        super().__init__()
        self.inventory_service = inventory_service
        self.sales_service = sales_service
        self.page = page
        
        self.selected_product = ft.Dropdown(
            label="Seleccionar Producto",
            expand=True,
            on_change=self.update_product_info
        )
        self.quantity_field = ft.TextField(label="Cantidad", value="1", width=150)
        self.add_to_cart_btn = ft.ElevatedButton("Agregar al Carrito", on_click=self.add_to_cart)
        self.cart_list = ft.ListView(expand=True)
        self.total_text = ft.Text("Total: $0.00", size=20, weight="bold")
        self.checkout_btn = ft.ElevatedButton("Finalizar Venta", on_click=self.checkout, style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN))
        
        self.cart = []
        self.load_products_dropdown()
        
        self.controls = [
            ft.Text("Registro de Ventas", size=24, weight="bold"),
            ft.Row([
                self.selected_product,
                self.quantity_field,
                self.add_to_cart_btn
            ]),
            ft.Divider(),
            ft.Text("Carrito de Compras", size=18, weight="bold"),
            self.cart_list,
            ft.Row([
                self.total_text,
                self.checkout_btn
            ], alignment=ft.MainAxisAlignment.END)
        ]

    def load_products_dropdown(self):
        products = self.inventory_service.get_all_products()
        self.selected_product.options = [ft.dropdown.Option(p.id, p.name) for p in products]
        self.update()

    def update_product_info(self, e):
        pass

    def add_to_cart(self, e):
        product_id = self.selected_product.value
        try:
            quantity = int(self.quantity_field.value)
            product = self.inventory_service.get_product(product_id)
            
            if not product or product.stock < quantity or quantity <= 0:
                self.page.show_snack_bar(ft.SnackBar(ft.Text("Cantidad inválida o stock insuficiente.", color="red"), open=True))
                return
            
            item_found = False
            for item in self.cart:
                if item['product_id'] == product_id:
                    item['quantity'] += quantity
                    item_found = True
                    break
            
            if not item_found:
                self.cart.append({'product_id': product_id, 'quantity': quantity})
            
            self.render_cart()
            self.quantity_field.value = "1"
        except (ValueError, TypeError):
            self.page.show_snack_bar(ft.SnackBar(ft.Text("Selecciona un producto y una cantidad válida.", color="red"), open=True))
        
        self.update()
        
    def render_cart(self):
        self.cart_list.controls.clear()
        total = 0.0
        for item in self.cart:
            product = self.inventory_service.get_product(item['product_id'])
            subtotal = product.price * item['quantity']
            total += subtotal
            self.cart_list.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{product.name} x {item['quantity']}"),
                    trailing=ft.Text(f"${subtotal:.2f}")
                )
            )
        self.total_text.value = f"Total: ${total:.2f}"
        self.update()

    async def checkout(self, e):
        if not self.cart:
            self.page.show_snack_bar(ft.SnackBar(ft.Text("El carrito está vacío.", color="red"), open=True))
            return
            
        sale = await self.page.run_task(lambda: self.sales_service.record_sale(self.cart))
        
        if sale:
            self.cart.clear()
            self.render_cart()
            self.page.show_snack_bar(ft.SnackBar(ft.Text("Venta registrada exitosamente."), open=True))
        else:
            self.page.show_snack_bar(ft.SnackBar(ft.Text("Error al registrar la venta."), open=True))
        
        self.update()