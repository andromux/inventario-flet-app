# Gestion de Inventario Desktop app

Para agregar una nueva funcionalidad, como la gestión de proveedores, no necesitas modificar el código de las páginas existentes. Solo necesitas agregar nuevos archivos y conectarlos a tu vista principal.

1.  **Crea la nueva página**: En la carpeta `ui/pages/`, crea un nuevo archivo, por ejemplo, `suppliers_page.py`. Aquí, define la interfaz de usuario y la lógica de interacción para esa sección.
    ```python
    # ui/pages/suppliers_page.py
    import flet as ft

    class SuppliersPage(ft.UserControl):
        def __init__(self, service, page):
            super().__init__()
            self.service = service
            self.page = page
            # ... (Lógica de la UI para proveedores) ...

        def build(self):
            return ft.Column([
                ft.Text("Gestión de Proveedores", size=24, weight="bold"),
                # ... (Controles y lógica) ...
            ])
    ```
2.  **Crea el servicio de negocio**: Para la lógica de los proveedores, crea un nuevo archivo en la carpeta `services/`, por ejemplo, `suppliers_service.py`. Este servicio se encargará de todas las operaciones (agregar, editar, eliminar proveedores) sin saber nada de la interfaz.
    ```python
    # services/suppliers_service.py
    from storage.base_storage import BaseStorage

    class SuppliersService:
        def __init__(self, storage: BaseStorage):
            self._storage = storage
            # ... (Lógica de negocio para proveedores) ...
    ```
3.  **Actualiza el almacenamiento**: Modifica `storage/base_storage.py` para añadir los métodos abstractos `load_suppliers` y `save_suppliers`. Luego, implementa estos métodos en `storage/json_storage.py` para que los datos persistan en un nuevo archivo `suppliers.json`.
4.  **Integra en la vista principal**: En `ui/main_view.py`, añade la nueva página al diccionario de páginas y un `NavigationRailDestination` para que el usuario pueda acceder a ella.
    ```python
    # ui/main_view.py
    # ... (importa SuppliersPage y SuppliersService) ...

    class MainView(ft.UserControl):
        def __init__(self, page, inventory_service, sales_service):
            super().__init__()
            # Inicializa el nuevo servicio
            self.suppliers_service = SuppliersService(self.storage)
            
            self.pages = {
                "Catálogo": CatalogPage(...),
                "Ventas": SalesPage(...),
                "Reportes": ReportsPage(...),
                "Proveedores": SuppliersPage(self.suppliers_service, self.page) # <-- Nueva página
            }
            
            self.navigation_rail = ft.NavigationRail(
                # ... (agrega un nuevo destino) ...
                ft.NavigationRailDestination(
                    icon=ft.icons.GROUP,
                    selected_icon=ft.icons.GROUP_ROUNDED,
                    label="Proveedores"
                )
            )
            # ...
    ```

Este proceso garantiza que la nueva funcionalidad esté **desacoplada** del resto, evitando que los cambios en una sección afecten a otra.

-----

### 2\. Migrando a una Base de Datos (Mejora en la Persistencia)

Una de las mayores ventajas de la arquitectura actual es que puedes cambiar el backend de almacenamiento sin tocar la lógica de negocio ni la interfaz de usuario.

1.  **Crea un nuevo backend**: En la carpeta `storage/`, crea un archivo, por ejemplo, `sqlite_storage.py`.
2.  **Implementa la interfaz**: Esta nueva clase `SQLiteStorage` debe heredar de `BaseStorage` e implementar todos los métodos abstractos (`load_products`, `save_products`, etc.), pero esta vez usando consultas SQL en lugar de leer/escribir JSON.
    ```python
    # storage/sqlite_storage.py
    from storage.base_storage import BaseStorage
    import sqlite3

    class SQLiteStorage(BaseStorage):
        def __init__(self, db_path="data/app.db"):
            self.conn = sqlite3.connect(db_path)
            # ... (crea las tablas si no existen) ...
        
        def load_products(self):
            # ... (implementa la lógica de SQL) ...
            pass
            
        def save_products(self, products):
            # ... (implementa la lógica de SQL) ...
            pass
        # ... (implementa los demás métodos) ...
    ```
3.  **Cambia el backend en `main.py`**: El único cambio que necesitas para migrar es una sola línea en `main.py`. Simplemente importa la nueva clase y cámbiala por la anterior.
    ```python
    # main.py
    # ...
    from storage.sqlite_storage import SQLiteStorage # <-- Importa el nuevo backend

    def main(page: ft.Page):
        try:
            # data_storage = JSONStorage()
            data_storage = SQLiteStorage() # <-- Usa la nueva clase
            inventory_service = InventoryService(data_storage)
            # ...
    ```

Este patrón de diseño, conocido como **Inyección de Dependencias**, permite que las clases (`InventoryService`) dependan de una abstracción (`BaseStorage`) en lugar de una implementación concreta (`JSONStorage`), lo que hace que tu código sea extremadamente flexible y fácil de probar.

-----

### 3\. Consideraciones Adicionales y Buenas Prácticas

  * **Programación Asíncrona**: Para operaciones de I/O (lectura de archivos grandes, exportación a Excel, etc.), usa `asyncio` y `page.run_task` para evitar que la interfaz de usuario se congele.  El uso de tareas asíncronas mantiene la aplicación fluida y responsiva.
  * **Manejo de Errores**: Centraliza el manejo de errores. En lugar de tener `try/except` en cada función, puedes usar decoradores o un manejador de errores centralizado. Muestra mensajes de error claros y útiles en la interfaz de usuario (por ejemplo, con `SnackBar` o `AlertDialog`) y registra los errores técnicos en el archivo de `logs`.
  * **Componentes Reutilizables**: Si notas que estás escribiendo el mismo código de UI (como un formulario de producto o una tabla con opciones de filtro), conviértelo en un `ft.UserControl` en la carpeta `ui/components/`. Esto no solo reduce la duplicación de código, sino que también hace que tu UI sea más consistente.
