import tkinter as tk
from tkinter import ttk

from ui.clientes import SeccionClientes
from ui.inicio import SeccionInicio
from ui.finanzas import SeccionFinanzas
from ui.inventario import SeccionInventario
from ui.productos import SeccionProductos
from ui.proveedores import SeccionProveedores
from ui.ventas import SeccionVentas
from ui.utilidades import UtilidadesInterfaz


class AplicacionGestionEmpresarial(
    UtilidadesInterfaz,
    SeccionInicio,
    SeccionClientes,
    SeccionProductos,
    SeccionProveedores,
    SeccionVentas,
    SeccionInventario,
    SeccionFinanzas,
):
    def __init__(self, ventana):
        self.ventana = ventana
        ventana.title("Gestion empresarial")
        ventana.geometry("1280x780")
        ventana.minsize(1050, 650)
        ventana.configure(bg="#eef2f7")
        self._configurar_estilos()
        self._crear_interfaz()
        self.actualizar_todo()

    def _crear_interfaz(self):
        encabezado = ttk.Frame(self.ventana, padding=(22, 18, 22, 8))
        encabezado.pack(fill="x")
        ttk.Label(encabezado, text="Gestion empresarial", style="Title.TLabel").pack(side="left")
        self.estado = ttk.Label(encabezado, text="Listo", foreground="#516174")
        self.estado.pack(side="right", pady=8)

        self.pestanas = ttk.Notebook(self.ventana)
        self.pestanas.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        secciones = (
            ("inicio", "Inicio"),
            ("pestana_clientes", "Clientes"),
            ("pestana_productos", "Productos"),
            ("pestana_proveedores", "Proveedores"),
            ("pestana_ventas", "Ventas"),
            ("pestana_inventario", "Inventario"),
            ("pestana_finanzas", "Finanzas y reportes"),
        )
        for atributo, titulo in secciones:
            pestana = ttk.Frame(self.pestanas, padding=16)
            setattr(self, atributo, pestana)
            self.pestanas.add(pestana, text=titulo)

        for seccion in ("inicio", "clientes", "productos", "proveedores", "ventas", "inventario", "finanzas"):
            getattr(self, f"_crear_{seccion}")()

    def actualizar_todo(self):
        for seccion in ("clientes", "productos", "proveedores", "ventas", "inventario", "finanzas", "inicio"):
            getattr(self, f"actualizar_{seccion}")()
