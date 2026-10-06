import tkinter as tk
from tkinter import ttk

from Modules.Finanzas.Functions import functions_cartera as cartera
from Modules.Reportes.Functions import functions_reportes as reportes


class SeccionFinanzas:
    def _crear_finanzas(self):
        forms = ttk.Frame(self.pestana_finanzas)
        forms.pack(fill="x")
        movement = self._crear_panel(forms, "Movimiento de cartera de cliente")
        self.cliente_cartera = tk.StringVar()
        self.concepto_cartera = tk.StringVar()
        self.monto_cartera = tk.StringVar()
        self.tipo_movimiento = tk.StringVar(value="cargo")
        for label, variable in (
            ("Cliente", self.cliente_cartera), ("Concepto", self.concepto_cartera),
            ("Monto", self.monto_cartera),
        ):
            self._crear_campo(movement, label, variable)
        ttk.Combobox(
            movement, textvariable=self.tipo_movimiento, values=("cargo", "abono"), state="readonly"
        ).pack(fill="x", pady=3)
        ttk.Button(movement, text="Registrar movimiento", command=self.registrar_movimiento).pack(fill="x", pady=4)

        cash = self._crear_panel(forms, "Flujo de efectivo")
        self.concepto_efectivo, self.monto_efectivo = tk.StringVar(), tk.StringVar()
        self.tipo_efectivo = tk.StringVar(value="ingreso")
        self._crear_campo(cash, "Concepto", self.concepto_efectivo)
        self._crear_campo(cash, "Monto", self.monto_efectivo)
        ttk.Combobox(
            cash, textvariable=self.tipo_efectivo, values=("ingreso", "egreso"), state="readonly"
        ).pack(fill="x", pady=3)
        ttk.Button(cash, text="Registrar flujo", command=self.registrar_flujo).pack(fill="x", pady=4)

        report = self._crear_panel(self.pestana_finanzas, "Balance y reportes")
        ttk.Button(report, text="Actualizar balance", command=self.actualizar_finanzas).pack(side="left", padx=(0, 8))
        self.texto_balance = tk.Text(report, height=6, width=90, state="disabled", relief="flat", bg="white")
        self.texto_balance.pack(fill="x", pady=(10, 0))

    def registrar_movimiento(self):
        result = cartera.registrar_movimiento(
            self.cliente_cartera.get(), self.concepto_cartera.get(),
            self.monto_cartera.get(), self.tipo_movimiento.get(),
        )
        if self._mostrar_resultado(result, "Movimiento registrado"):
            self.actualizar_todo()

    def registrar_flujo(self):
        result = cartera.registrar_flujo_efectivo(
            self.tipo_efectivo.get(), self.concepto_efectivo.get(), self.monto_efectivo.get()
        )
        if self._mostrar_resultado(result, "Flujo registrado"):
            self.actualizar_todo()

    def actualizar_finanzas(self):
        balance = reportes.reporte_balance_financiero()
        text = (
            f"Fecha: {balance['fecha_corte']}\n"
            f"Efectivo neto: {balance['efectivo_neto']}\n"
            f"Cartera clientes: {balance['cartera_clientes']}\n"
            f"Deuda proveedores: {balance['deuda_proveedores']}\n"
            f"Posicion neta: {balance['posicion_neta']}"
        )
        self.texto_balance.config(state="normal")
        self.texto_balance.delete("1.0", "end")
        self.texto_balance.insert("end", text)
        self.texto_balance.config(state="disabled")
