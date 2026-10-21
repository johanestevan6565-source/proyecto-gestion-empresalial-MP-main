import tkinter as tk 
from Modules.Productos.Functions import functions_productos 

def AbrirProductosUI():
    ventana_productos = tk.Toplevel()
    ventana_productos.title("Productos")

    tk.Label(ventana_productos, text="Nombre").pack()
    entry_nombre = tk.Entry(ventana_productos)
    entry_nombre.pack()

    tk.Button(ventana, text="guardar").pack()