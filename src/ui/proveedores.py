import tkinter as tk
from tkinter import messagebox, ttk

from Modules.Proveedores.Functions import functions_proveedores as proveedores


class SeccionProveedores:
    def _crear_proveedores(self):
        left = ttk.Frame(self.pestana_proveedores)
        left.pack(side="left", fill="y", padx=(0, 14))
        form = self._crear_panel(left, "Registrar proveedor")
        self.nombre_proveedor, self.correo_proveedor, self.telefono_proveedor = (
            tk.StringVar(), tk.StringVar(), tk.StringVar()
        )
        self._crear_campo(form, "Nombre", self.nombre_proveedor)
        self._crear_campo(form, "Correo", self.correo_proveedor)
        self._crear_campo(form, "Telefono", self.telefono_proveedor)
        ttk.Button(form, text="Agregar proveedor", style="Primary.TButton", command=self.agregar_proveedor).pack(fill="x", pady=(10, 0))

        edit = self._crear_panel(left, "Editar proveedor seleccionado")
        self.nuevo_nombre_proveedor, self.nuevo_correo_proveedor, self.nuevo_telefono_proveedor = (
            tk.StringVar(), tk.StringVar(), tk.StringVar()
        )
        self._crear_campo(edit, "Nuevo nombre", self.nuevo_nombre_proveedor)
        self._crear_campo(edit, "Nuevo correo", self.nuevo_correo_proveedor)
        self._crear_campo(edit, "Nuevo telefono", self.nuevo_telefono_proveedor)
        ttk.Button(edit, text="Guardar cambios", command=self.editar_proveedor).pack(fill="x", pady=3)
        ttk.Button(edit, text="Activar / desactivar", command=self.cambiar_estado_proveedor).pack(fill="x", pady=3)
        self.tabla_proveedores = self._crear_tabla(
            self.pestana_proveedores, ("id", "nombre", "contacto", "telefono", "activo"),
            [100, 160, 230, 120, 80],
        )
        self.tabla_proveedores.bind("<<TreeviewSelect>>", self.seleccionar_proveedor)

    def agregar_proveedor(self):
        name, contact, phone = (
            self.nombre_proveedor.get().strip(),
            self.correo_proveedor.get().strip(),
            self.telefono_proveedor.get().strip(),
        )
        if not name or (contact and not proveedores.validar_email(contact)) or (phone and not proveedores.validar_telefono(phone)):
            return messagebox.showerror("Dato invalido", "Revise nombre, correo y telefono")
        if proveedores.proveedor_existe(name, proveedores.cargar_proveedores()):
            return messagebox.showerror("Dato duplicado", "Ya existe un proveedor con ese nombre")
        proveedores.registrar_proveedor(name, contact, phone)
        self.estado.config(text="Proveedor agregado")
        self.actualizar_todo()

    def seleccionar_proveedor(self, _event=None):
        if row := self._fila_seleccionada(self.tabla_proveedores):
            self.nuevo_nombre_proveedor.set(row[1])
            self.nuevo_correo_proveedor.set(row[2])
            self.nuevo_telefono_proveedor.set(row[3])

    def editar_proveedor(self):
        row = self._fila_seleccionada(self.tabla_proveedores)
        if not row:
            return messagebox.showwarning("Seleccion requerida", "Seleccione un proveedor")
        result = proveedores.editar_proveedor(
            row[0], self.nuevo_nombre_proveedor.get(), self.nuevo_correo_proveedor.get(), self.nuevo_telefono_proveedor.get()
        )
        if self._mostrar_resultado(result, "Proveedor actualizado"):
            self.actualizar_todo()

    def cambiar_estado_proveedor(self):
        row = self._fila_seleccionada(self.tabla_proveedores)
        if row and proveedores.cambiar_estado_proveedor(row[0], row[4].lower() != "true"):
            self.actualizar_todo()

    def actualizar_proveedores(self):
        self._limpiar_tabla(self.tabla_proveedores)
        for provider in proveedores.listar_proveedores(False):
            self.tabla_proveedores.insert(
                "", "end",
                values=(
                    provider["id"], provider["nombre"], provider.get("contacto", ""),
                    provider.get("telefono", ""), provider.get("activo", True),
                ),
            )
