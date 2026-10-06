import tkinter as tk
from tkinter import ttk

from Modules.Clientes.Functions import functions_clientes as clientes
from Modules.Productos.Functions import functions_productos as productos
from Modules.Reportes.Functions import functions_reportes as reportes
from Modules.Ventas.Functions import functions_ventas as ventas


class SeccionInicio:
    def _crear_inicio(self):
        ttk.Label(self.inicio, text="Resumen del sistema", style="Section.TLabel").pack(anchor="w", pady=(0, 12))
        self.tarjetas_inicio = ttk.Frame(self.inicio)
        self.tarjetas_inicio.pack(fill="x", pady=(0, 16))
        self.tabla_ventas_recientes = self._crear_tabla(
            self.inicio, ("id", "cliente", "fecha", "tipo_pago", "total"),
            [120, 150, 110, 110, 110],
        )

    def actualizar_inicio(self):
        for child in self.tarjetas_inicio.winfo_children():
            child.destroy()

        balance = reportes.reporte_balance_financiero()
        lista_ventas = ventas.cargar_ventas().get("ventas", [])
        tarjetas = (
            ("Clientes activos", sum(c.get("activo", False) for c in clientes.listar_clientes().get("clientes", []))),
            ("Productos activos", len(productos.listar_productos(True))),
            ("Ventas", len(lista_ventas)),
            ("Posicion neta", balance["posicion_neta"]),
        )
        for titulo, valor in tarjetas:
            tarjeta = tk.Frame(self.tarjetas_inicio, bg="white", bd=1, relief="solid", padx=18, pady=12)
            tarjeta.pack(side="left", fill="x", expand=True, padx=(0, 10))
            tk.Label(tarjeta, text=titulo, bg="white", fg="#53657a", font=("Segoe UI", 9, "bold")).pack(anchor="w")
            tk.Label(tarjeta, text=str(valor), bg="white", fg="#10233f", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(5, 0))

        self._limpiar_tabla(self.tabla_ventas_recientes)
        for venta in reversed(lista_ventas[-8:]):
            self.tabla_ventas_recientes.insert(
                "", "end",
                values=(venta["id"], venta["cliente_id"], venta["fecha"], venta["tipo_pago"], venta["total"]),
            )
