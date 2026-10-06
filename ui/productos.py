import tkinter as tk
from tkinter import messagebox, ttk

from Modules.Inventarios.Functions import functions_inventarios as inventarios
from Modules.Productos.Functions import functions_productos as productos


class SeccionProductos:
    def _crear_productos(self):
        left = ttk.Frame(self.pestana_productos)
        left.pack(side="left", fill="y", padx=(0, 14))
        form = self._crear_panel(left, "Registrar producto")
        self.nombre_producto, self.precio_producto = tk.StringVar(), tk.StringVar()
        self.tipo_producto = tk.StringVar(value="unidad")
        self._crear_campo(form, "Nombre", self.nombre_producto)
        self._crear_campo(form, "Precio", self.precio_producto)
        ttk.Label(form, text="Tipo de venta").pack(anchor="w", pady=(6, 2))
        ttk.Combobox(form, textvariable=self.tipo_producto, values=("unidad", "kg"), state="readonly").pack(fill="x")
        ttk.Button(form, text="Agregar producto", style="Primary.TButton", command=self.agregar_producto).pack(fill="x", pady=(10, 0))

        edit = self._crear_panel(left, "Editar producto seleccionado")
        self.nuevo_nombre_producto, self.nuevo_precio_producto = tk.StringVar(), tk.StringVar()
        self._crear_campo(edit, "Nuevo nombre", self.nuevo_nombre_producto)
        self._crear_campo(edit, "Nuevo precio", self.nuevo_precio_producto)
        ttk.Button(edit, text="Guardar cambios", command=self.editar_producto).pack(fill="x", pady=3)
        ttk.Button(edit, text="Activar / desactivar", command=self.cambiar_estado_producto).pack(fill="x", pady=3)
        self.tabla_productos = self._crear_tabla(
            self.pestana_productos, ("id", "nombre", "precio", "tipo_venta", "activo", "stock"),
            [80, 190, 100, 100, 80, 80],
        )
        self.tabla_productos.bind("<<TreeviewSelect>>", self.seleccionar_producto)

    def agregar_producto(self):
        if self._mostrar_resultado(
            productos.agregar_producto(self.nombre_producto.get(), self.precio_producto.get(), self.tipo_producto.get()),
            "Producto agregado",
        ):
            self.nombre_producto.set("")
            self.precio_producto.set("")
            self.actualizar_todo()

    def seleccionar_producto(self, _event=None):
        if row := self._fila_seleccionada(self.tabla_productos):
            self.nuevo_nombre_producto.set(row[1])
            self.nuevo_precio_producto.set(row[2])

    def editar_producto(self):
        row = self._fila_seleccionada(self.tabla_productos)
        if not row:
            return messagebox.showwarning("Seleccion requerida", "Seleccione un producto")
        if self._mostrar_resultado(productos.editar_producto(row[0], self.nuevo_nombre_producto.get(), self.nuevo_precio_producto.get()), "Producto actualizado"):
            self.actualizar_todo()

    def cambiar_estado_producto(self):
        row = self._fila_seleccionada(self.tabla_productos)
        if row and self._mostrar_resultado(productos.cambiar_estado_producto(row[0], row[4].lower() != "true"), "Estado actualizado"):
            self.actualizar_todo()

    def actualizar_productos(self):
        self._limpiar_tabla(self.tabla_productos)
        for product in productos.listar_productos():
            self.tabla_productos.insert(
                "", "end",
                values=(
                    product["id"], product["nombre"], product["precio"],
                    product.get("tipo_venta", "unidad"), product.get("activo", True),
                    inventarios.calcular_stock_producto(product["id"]),
                ),
            )
