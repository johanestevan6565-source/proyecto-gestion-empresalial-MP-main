from Debug.menu_clientes import menu_clientes
from Debug.menu_inventarios import menu_test_inventarios
from Debug.menu_productos import menu_productos
from Debug.menu_proveedores import menu_proveedores
from Debug.menu_cartera import menu_cartera
from Debug.menu_ventas import menu_ventas
from Debug.menu_reportes import menu_reportes


def main():
    while True:
        print("\n=== SISTEMA DE GESTIÓN EMPRESARIAL ===")
        print("1. Gestión de clientes")
        print("2. Gestión de productos")
        print("3. Gestión de ventas")
        print("4. Gestión de inventarios")
        print("5. Gestión de proveedores")
        print("6. Gestión de cartera")
        print("7. Gestión de reportes")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_clientes()
        elif opcion == "2":
            menu_productos()
        elif opcion == "3":
            menu_ventas()
        elif opcion == "4":
            menu_test_inventarios()
        elif opcion == "5":
            menu_proveedores()
        elif opcion == "6":
            menu_cartera()
        elif opcion == "7":
            menu_reportes()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()
