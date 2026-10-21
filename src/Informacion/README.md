# Sistema de Gestión Empresarial

## 📌 Descripción

Sistema de gestión empresarial en Python para controlar operación comercial y contable:
clientes, productos, ventas, inventario, cartera, proveedores y reportes.

## ✅ Qué se puede hacer ahora

- Gestión de clientes, productos y proveedores.
- Gestión de inventarios basada en eventos (compras, ventas y movimientos de empaque).
- Módulo de ventas ligado a cliente con validación de stock antes de procesar.
- Edición de precio/cantidad por ítem durante la venta **sin alterar** el precio global del producto.
- Registro de empaque prestado al cliente dentro de la venta.
- Cartera y finanzas:
  - Cuentas por cobrar de clientes (cargo/abono).
  - Flujo de efectivo (ingresos/egresos).
  - Cuentas por pagar a proveedores (cargo/abono).
  - Balance general (efectivo vs cartera vs deuda proveedores).
- Reportes operativos:
  - Stock de bodega al corte.
  - Saldo neto de canastillas/empaque por proveedor.
  - Búsqueda de eventos de inventario con filtros.

## 🧩 Arquitectura base para pasar a interfaz gráfica

El proyecto quedó preparado para una UI (Tkinter, PySide o Web) porque:

- La lógica principal está encapsulada por módulos de dominio.
- Productos y ventas ya usan clases (`Producto`, `ItemVenta`) para facilitar mantenimiento.
- Los menús CLI son una capa delgada sobre funciones de negocio reutilizables.

## 📂 Estructura principal

```text
Modules/
├── Clientes/Functions/
├── Productos/Functions/          # Clase Producto
├── Ventas/Functions/             # Clase ItemVenta + procesar_venta
├── Inventarios/Functions/        # Kardex por eventos y stock
├── Finanzas/Functions/           # Cartera, flujo efectivo, CxP proveedores
├── Proveedores/Functions/
└── Reportes/Functions/           # Reportes operativos y financieros
```

## 🚀 Siguiente paso recomendado

La interfaz gráfica Tkinter consume estas funciones de dominio, sin reescribir reglas
de negocio. Iníciala desde la raíz del proyecto con `python app.py`. La CLI anterior
continúa disponible con `python main.py`.

```text
ui/
├── aplicacion.py
├── utilidades.py
├── inicio.py
├── clientes.py
├── productos.py
├── proveedores.py
├── ventas.py
├── inventario.py
└── finanzas.py
```
