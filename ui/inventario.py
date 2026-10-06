import tkinter as tk
from tkinter import messagebox, ttk

from Modules.Inventarios.Functions import functions_inventarios as inventarios


class SeccionInventario:
    def _crear_inventario(self):
        form = self._crear_panel(self.pestana_inventario, "Registrar compra de producto")
        self.proveedor_compra = tk.StringVar()
        self.producto_compra = tk.StringVar()
        self.cantidad_compra = tk.StringVar()
        self.unidad_compra = tk.StringVar(value="unidad")
        self.precio_compra = tk.StringVar()
        for etiqueta, variable in (
            ("Proveedor", self.proveedor_compra), ("Producto", self.producto_compra),
            ("Cantidad", self.cantidad_compra), ("Unidad", self.unidad_compra),
            ("Precio unitario", self.precio_compra),
        ):
            self._crear_campo(form, etiqueta, variable, 28)
        ttk.Button(form, text="Registrar compra", style="Primary.TButton", command=self.registrar_compra).pack(anchor="e", pady=(10, 0))
        ttk.Label(self.pestana_inventario, text="Eventos de inventario", style="Section.TLabel").pack(anchor="w", pady=(4, 8))
        self.tabla_inventario = self._crear_tabla(
            self.pestana_inventario, ("timestamp", "tipo", "origen", "detalle"),
            [150, 180, 220, 420],
        )

    def registrar_compra(self):
        try:
            cantidad, precio = float(self.cantidad_compra.get()), float(self.precio_compra.get())
            if cantidad <= 0 or precio <= 0:
                raise ValueError
        except ValueError:
            return messagebox.showerror("Dato invalido", "Cantidad y precio deben ser numeros mayores que cero")
        inventarios.registrar_compra_producto(
            self.proveedor_compra.get(), self.producto_compra.get(),
            cantidad, self.unidad_compra.get(), precio,
        )
        self.estado.config(text="Compra registrada")
        self.actualizar_todo()

    def actualizar_inventario(self):
        self._limpiar_tabla(self.tabla_inventario)
        for evento in inventarios.listar_eventos_inventario():
            self.tabla_inventario.insert(
                "", "end",
                values=(
                    evento.get("timestamp", ""), evento.get("tipo", ""),
                    evento.get("origen", ""), str(evento.get("data", {})),
                ),
            )
