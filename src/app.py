import tkinter as tk

from ui.aplicacion import AplicacionGestionEmpresarial


def iniciar_aplicacion():
    ventana = tk.Tk()
    AplicacionGestionEmpresarial(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    iniciar_aplicacion()
