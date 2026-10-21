from tkinter import messagebox, ttk


class UtilidadesInterfaz:
    def _configurar_estilos(self):
        style = ttk.Style(self.ventana)
        style.theme_use("clam")
        style.configure("TFrame", background="#eef2f7")
        style.configure("TLabel", background="#eef2f7", foreground="#172033", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), foreground="#10233f")
        style.configure("Section.TLabel", font=("Segoe UI", 12, "bold"), foreground="#10233f")
        style.configure("Primary.TButton", background="#1769aa", foreground="white", padding=7, font=("Segoe UI", 10, "bold"))
        style.map("Primary.TButton", background=[("active", "#0f4f83")])
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        style.configure("TNotebook", background="#eef2f7", borderwidth=0)
        style.configure("TNotebook.Tab", padding=(14, 8), font=("Segoe UI", 10, "bold"))

    def _crear_campo(self, contenedor, etiqueta, variable, ancho=22):
        marco = ttk.Frame(contenedor)
        marco.pack(fill="x", pady=3)
        ttk.Label(marco, text=etiqueta, width=17).pack(side="left")
        campo = ttk.Entry(marco, textvariable=variable, width=ancho)
        campo.pack(side="left", fill="x", expand=True)
        return campo

    def _crear_tabla(self, contenedor, columnas, anchos=None):
        tabla = ttk.Treeview(contenedor, columns=columnas, show="headings", selectmode="browse")
        for indice, columna in enumerate(columnas):
            tabla.heading(columna, text=columna.replace("_", " ").title())
            tabla.column(columna, width=(anchos or [120] * len(columnas))[indice], anchor="w")
        barra_desplazamiento = ttk.Scrollbar(contenedor, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=barra_desplazamiento.set)
        tabla.pack(side="left", fill="both", expand=True)
        barra_desplazamiento.pack(side="right", fill="y")
        return tabla

    def _crear_panel(self, contenedor, titulo):
        panel = ttk.LabelFrame(contenedor, text=titulo, padding=12)
        panel.pack(fill="x", pady=(0, 12))
        return panel

    @staticmethod
    def _fila_seleccionada(tabla):
        seleccion = tabla.selection()
        return tabla.item(seleccion[0], "values") if seleccion else None

    def _mostrar_resultado(self, resultado, texto_exito="Operacion realizada"):
        correcto, mensaje = (
            resultado[:2] if isinstance(resultado, tuple)
            else (bool(resultado), texto_exito)
        )
        if not correcto:
            messagebox.showerror("No se pudo completar", str(mensaje))
            return False
        self.estado.config(text=texto_exito)
        return True

    @staticmethod
    def _limpiar_tabla(tabla):
        for elemento in tabla.get_children():
            tabla.delete(elemento)
