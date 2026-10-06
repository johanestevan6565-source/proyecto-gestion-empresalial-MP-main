import sys
import os
import tkinter as tk
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

from productos_ui import AbrirProductosUI

ventana = tk.Tk()
ventana.title("Gestión de Gestion")
ventana.geometry("500x400")

tk.Label(ventana, text="Menu principal", font=("Arial", 16)).pack(pady=20) # Agrega un título al menú principal

tk.Button(ventana, text="productos", command=AbrirProductosUI).pack(pady=10) # Agrega un botón para abrir la interfaz de productos

ventana.mainloop()