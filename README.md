## Manual de Uso - Aplicación de Inventario de Escritorio

Esta aplicación de escritorio está desarrollada en Python usando el framework Flet para gestionar inventarios de productos, procesar ventas y generar reportes.

_________________________________________
<p align="center">
  <img rc="https://github.com/user-attachments/assets/ffb71ce1-9378-40e6-9576-238254822c47" width="250">
  <img src="https://github.com/user-attachments/assets/27fdf612-941b-45a8-b768-ed618a6bd411" width="250">
  <img src="https://github.com/user-attachments/assets/070eadbe-5cd8-4747-99e2-7c4631ebc8bb" width="250">
</p>
__________________________________________

## Nivel Técnico

### Arquitectura del Sistema

La aplicación sigue un patrón de arquitectura por capas con inyección de dependencias:

- **Capa de Presentación**: Interfaz de usuario con navegación por pestañas
- **Capa de Servicios**: Lógica de negocio (`InventoryService`, `SalesService`)
- **Capa de Almacenamiento**: Persistencia en archivos JSON

### Inicialización de la Aplicación

El punto de entrada configura la ventana principal con dimensiones específicas y inicializa todos los servicios. La aplicación maneja errores críticos durante la inicialización y muestra mensajes informativos al usuario.

### Navegación Principal

La interfaz utiliza un `NavigationBar` horizontal con tres secciones principales:

1. **Catálogo**: Gestión de productos
2. **Ventas**: Procesamiento de transacciones  
3. **Reportes**: Análisis de ventas

### Extensibilidad

Para agregar nuevas funcionalidades, el sistema permite crear nuevas páginas sin modificar código existente. También es posible migrar a bases de datos diferentes implementando la interfaz `BaseStorage`.

## Nivel Usuario Final

### Inicio de la Aplicación

1. Ejecute el archivo principal para abrir la ventana de la aplicación
2. La aplicación se abrirá con la pestaña "Catálogo" seleccionada por defecto

### Gestión de Catálogo

- **Navegación**: Haga clic en la pestaña "Catálogo" en la barra superior
- **Funciones disponibles**: Agregar, editar y eliminar productos del inventario
- **Datos del producto**: Nombre, precio, stock y descripción

### Procesamiento de Ventas

- **Navegación**: Seleccione la pestaña "Ventas"
- **Selección de productos**: Use el menú desplegable para elegir productos 
- **Carrito de compras**: Agregue productos con cantidades específicas
- **Validación**: El sistema verifica stock disponible antes de agregar al carrito 
- **Finalización**: Use el botón "Finalizar Venta" para completar la transacción

### Reportes y Análisis

- **Navegación**: Acceda a la pestaña "Reportes"
- **Historial de ventas**: Visualice todas las transacciones en formato tabla 
- **Información mostrada**: ID de venta, fecha, ingresos, costos y ganancias

### Mensajes del Sistema

La aplicación muestra notificaciones mediante `SnackBar` para informar sobre errores o confirmaciones de acciones.


La aplicación utiliza almacenamiento en archivos JSON para persistir datos de productos y ventas. El sistema incluye logging para monitoreo técnico y manejo centralizado de errores. La arquitectura modular permite futuras expansiones como integración con bases de datos o nuevos módulos de funcionalidad sin afectar el código existente.
_____________________________________________

## Guía para Desarrolladores: Extensión de Funcionalidades

La aplicación sigue una arquitectura modular con inyección de dependencias que facilita la adición de nuevas funcionalidades sin modificar código existente.

## Patrón de Extensión Recomendado

### 1. Crear Nueva Página UI

Para agregar funcionalidades como gestión de proveedores, cree un nuevo archivo en `ui/pages/` siguiendo el patrón establecido. La nueva página debe heredar de `ft.Column` y recibir servicios por inyección de dependencias.

### 2. Implementar Servicio de Negocio

Cree un nuevo servicio en `services/` que implemente la lógica de negocio específica. El servicio debe:

- Recibir `BaseStorage` como dependencia en el constructor
- Implementar logging usando `get_logger()`
- Manejar errores con try-catch y retornar valores apropiados

### 3. Extender Capa de Almacenamiento

Modifique la interfaz `BaseStorage` para agregar métodos abstractos necesarios. Luego implemente estos métodos en `JSONStorage` para persistir los nuevos datos.

### 4. Integrar en Vista Principal

Actualice `MainView` para incluir el nuevo servicio y página. Agregue la nueva página al diccionario de páginas y un `NavigationRailDestination` correspondiente.

### 5. Actualizar Bootstrap

Modifique `main.py` para instanciar el nuevo servicio con inyección de dependencias. Siga el patrón existente donde los servicios reciben sus dependencias en el constructor.

## Mejores Prácticas de Arquitectura

### Separación de Responsabilidades

- **UI**: Solo manejo de eventos y presentación
- **Servicios**: Lógica de negocio y validaciones 
- **Storage**: Persistencia de datos únicamente

### Manejo de Errores Consistente

Implemente logging y manejo de errores siguiendo el patrón establecido. Los servicios deben retornar `False` o `None` en caso de error y registrar mensajes descriptivos.

### Validación de Datos

Valide datos de entrada antes de procesarlos. Verifique existencia de entidades y reglas de negocio antes de realizar operaciones.

## Migración de Storage

Para cambiar el backend de almacenamiento, implemente una nueva clase que herede de `BaseStorage`. Luego modifique únicamente la instanciación en `main.py`.

## Consideraciones Adicionales

- Use `asyncio` para operaciones I/O pesadas 
- Centralice el manejo de errores
- Cree componentes reutilizables en `ui/components/`

## Notes

La arquitectura actual utiliza el patrón Strategy para el almacenamiento y dependency injection para los servicios, permitiendo extensibilidad sin modificar código existente. El sistema está diseñado para mantener bajo acoplamiento entre capas y alta cohesión dentro de cada módulo.
