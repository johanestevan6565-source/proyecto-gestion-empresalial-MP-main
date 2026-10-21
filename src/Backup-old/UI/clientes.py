import tkinter as tk
from tkinter import messagebox, ttk

from Modules.Clientes.Functions import functions_clientes as clientes


class SeccionClientes:
    def _crear_clientes(self):
        left = ttk.Frame(self.pestana_clientes)
        left.pack(side="left", fill="y", padx=(0, 14))
        form = self._crear_panel(left, "Registrar cliente")
        self.nombre_cliente, self.telefono_cliente = tk.StringVar(), tk.StringVar()
        self._crear_campo(form, "Nombre", self.nombre_cliente)
        self._crear_campo(form, "Telefono", self.telefono_cliente)
        ttk.Button(form, text="Agregar cliente", style="Primary.TButton", command=self.agregar_cliente).pack(fill="x", pady=(10, 0))

        edit = self._crear_panel(left, "Editar cliente seleccionado")
        self.nuevo_nombre_cliente, self.nuevo_telefono_cliente = tk.StringVar(), tk.StringVar()
        self._crear_campo(edit, "Nuevo nombre", self.nuevo_nombre_cliente)
        self._crear_campo(edit, "Nuevo telefono", self.nuevo_telefono_cliente)
        ttk.Button(edit, text="Guardar cambios", command=self.editar_cliente).pack(fill="x", pady=3)
        ttk.Button(edit, text="Activar / desactivar", command=self.cambiar_estado_cliente).pack(fill="x", pady=3)
        self.tabla_clientes = self._crear_tabla(self.pestana_clientes, ("id", "nombre", "telefono", "activo"), [110, 190, 130, 90])
        self.tabla_clientes.bind("<<TreeviewSelect>>", self.seleccionar_cliente)

    def agregar_cliente(self):
        telefono = self.telefono_cliente.get().strip()
        if telefono and not telefono.isdigit():
            return messagebox.showerror("Dato invalido", "El telefono solo debe contener numeros")
        if self._mostrar_resultado(clientes.agregar_cliente(self.nombre_cliente.get(), telefono), "Cliente agregado"):
            self.nombre_cliente.set("")
            self.telefono_cliente.set("")
            self.actualizar_todo()

    def seleccionar_cliente(self, _event=None):
        if fila := self._fila_seleccionada(self.tabla_clientes):
            self.nuevo_nombre_cliente.set(fila[1])
            self.nuevo_telefono_cliente.set(fila[2])

    def editar_cliente(self):
        fila = self._fila_seleccionada(self.tabla_clientes)
        if not fila:
            return messagebox.showwarning("Seleccion requerida", "Seleccione un cliente")
        nombre, telefono = self.nuevo_nombre_cliente.get().strip(), self.nuevo_telefono_cliente.get().strip()
        if telefono and not telefono.isdigit():
            return messagebox.showerror("Dato invalido", "El telefono solo debe contener numeros")
        nombre = None if nombre.lower() == fila[1].strip().lower() else nombre
        if self._mostrar_resultado(clientes.editar_cliente(fila[0], nombre, telefono), "Cliente actualizado"):
            self.actualizar_todo()

    def cambiar_estado_cliente(self):
        fila = self._fila_seleccionada(self.tabla_clientes)
        if fila and clientes.cambiar_estado_cliente(fila[0], fila[3].lower() != "true"):
            self.actualizar_todo()

    def actualizar_clientes(self):
        self._limpiar_tabla(self.tabla_clientes)
        for cliente in clientes.listar_clientes().get("clientes", []):
            self.tabla_clientes.insert(
                "", "end",
                values=(cliente["id"], cliente["nombre"], cliente.get("telefono", ""), cliente.get("activo", True)),
            )
