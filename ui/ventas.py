import tkinter as tk
from tkinter import ttk

from Modules.Ventas.Functions import functions_ventas as ventas


class SeccionVentas:
    def _crear_ventas(self):
        form = self._crear_panel(self.pestana_ventas, "Procesar venta")
        self.cliente_venta = tk.StringVar()
        self.producto_venta = tk.StringVar()
        self.cantidad_venta = tk.StringVar(value="1")
        self.precio_venta = tk.StringVar()
        self.forma_pago_venta = tk.StringVar(value="contado")
        for label, variable in (
            ("Cliente", self.cliente_venta), ("Producto", self.producto_venta),
            ("Cantidad", self.cantidad_venta), ("Precio unitario", self.precio_venta),
        ):
            self._crear_campo(form, label, variable, 28)
        payment = ttk.Frame(form)
        payment.pack(fill="x", pady=3)
        ttk.Label(payment, text="Tipo de pago", width=17).pack(side="left")
        ttk.Combobox(
            payment, textvariable=self.forma_pago_venta, values=("contado", "credito"),
            state="readonly", width=25,
        ).pack(side="left")
        ttk.Button(form, text="Procesar venta", style="Primary.TButton", command=self.procesar_venta).pack(anchor="e", pady=(10, 0))
        ttk.Label(self.pestana_ventas, text="Ventas registradas", style="Section.TLabel").pack(anchor="w", pady=(0, 8))
        self.tabla_ventas = self._crear_tabla(
            self.pestana_ventas, ("id", "cliente_id", "fecha", "tipo_pago", "total"),
            [110, 120, 110, 100, 100],
        )

    def procesar_venta(self):
        item = {"producto_id": self.producto_venta.get(), "cantidad": self.cantidad_venta.get()}
        if price := self.precio_venta.get().strip():
            item["precio_unitario"] = price
        result = ventas.procesar_venta(self.cliente_venta.get(), [item], self.forma_pago_venta.get())
        if self._mostrar_resultado(result, "Venta procesada"):
            self.cantidad_venta.set("1")
            self.precio_venta.set("")
            self.actualizar_todo()

    def actualizar_ventas(self):
        self._limpiar_tabla(self.tabla_ventas)
        for sale in ventas.cargar_ventas().get("ventas", []):
            self.tabla_ventas.insert(
                "", "end",
                values=(sale["id"], sale["cliente_id"], sale["fecha"], sale["tipo_pago"], sale["total"]),
            )
