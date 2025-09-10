import flet as ft
from services.sales_service import SalesService
from utils.logger import get_logger

logger = get_logger()

class ReportsPage(ft.Column):
    def __init__(self, sales_service: SalesService, page: ft.Page):
        super().__init__(
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        self.sales_service = sales_service
        self.page = page
        self.sales = []
        
        self.reports_text = ft.Text("Generando reporte...", size=16)
        
        self.sales_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID Venta")),
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Ingresos")),
                ft.DataColumn(ft.Text("Costo")),
                ft.DataColumn(ft.Text("Ganancia")),
            ],
            rows=[]
        )
        
        # Eliminada la llamada a self.load_sales_table_data() del constructor
        
        self.controls = [
            ft.Text("Reportes y Historial", size=24, weight="bold"),
            ft.Divider(),
            ft.ResponsiveRow([
                ft.Column(
                    [
                        self.reports_text,
                        ft.Container(
                            content=ft.ListView(
                                [self.sales_table],
                                expand=True
                            ),
                            expand=True
                        )
                    ],
                    expand=True,
                    col=12
                )
            ])
        ]
        
    def load_sales_table_data(self):
        """Carga los datos de la tabla."""
        self.sales = self.sales_service.get_all_sales()
        self.sales_table.rows.clear()
        
        for sale in self.sales:
            self.sales_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(sale.id[:8])),
                        ft.DataCell(ft.Text(sale.timestamp)),
                        ft.DataCell(ft.Text(f"${sale.total_revenue:.2f}")),
                        ft.DataCell(ft.Text(f"${sale.total_cost:.2f}")),
                        ft.DataCell(ft.Text(f"${sale.total_profit:.2f}"))
                    ]
                )
            )

    def refresh_products(self):
        """
        Método público para refrescar los datos. 
        Llamado por MainView al navegar a esta página.
        """
        self.load_sales_table_data()
        # Eliminada la llamada a self.update()
