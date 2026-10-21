import Modules.Productos.Functions.functions_productos as productos


def menu_productos():
    while True:
        print("\n===== MÓDULO PRODUCTOS =====")
        print("1. Agregar producto")
        print("2. Editar producto")
        print("3. Editar precio de producto")
        print("4. Listar productos activos")
        print("5. Listar productos inactivos")
        print("6. Desactivar producto")
        print("7. Reactivar producto")
        print("0. Volver")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            nombre = input("Nombre del producto: ")
            precio = input("Precio del producto: ")
            tipo_venta = input("Tipo de venta (unidad/kg): ")

            exito, mensaje = productos.agregar_producto(nombre, precio, tipo_venta)
            print(mensaje)

        elif opcion == "2":
            print("Productos disponibles:")
            lista = productos.listar_productos()
            for p in lista:
                print(f"{p['id']} - {p['nombre']} - ${p['precio']:.2f}")
            producto_id = input("Ingrese ID del producto a editar: ")
            nombre = input("Nuevo nombre (deje vacío para no cambiar): ")
            precio = input("Nuevo precio (deje vacío para no cambiar): ")
            busqueda_producto = productos.buscar_producto(producto_id)
            if not busqueda_producto:
                print("Producto no encontrado.")
                continue
            if nombre == "":
                nombre = None
            if precio == "":
                precio = None
            exito, mensaje = productos.editar_producto(producto_id, nombre, precio)
            print(mensaje)
            
        elif opcion == "3":
            print("Productos disponibles:")
            lista = productos.listar_productos()
            for p in lista:
                print(f"{p['id']} - {p['nombre']} - ${p['precio']:.2f}")
            producto_id = input("Ingrese ID del producto para editar precio: ")
            nuevo_precio = input("Nuevo precio: ")
            busqueda_producto = productos.buscar_producto(producto_id)
            if not busqueda_producto:
                print("Producto no encontrado.")
                continue
            exito, mensaje = productos.editar_precio_producto(producto_id, nuevo_precio)
            print(mensaje)
        elif opcion == "4":
            lista = productos.listar_productos(activo=True)
            if not lista:
                print("No hay productos activos.")
            else:
                for p in lista:
                    print(f"{p['id']} - {p['nombre']} - ${p['precio']:.2f}")

        elif opcion == "5":
            lista = productos.listar_productos(activo=False)
            if not lista:
                print("No hay productos inactivos.")
            else:
                for p in lista:
                    print(f"{p['id']} - {p['nombre']} - ${p['precio']:.2f}")

        elif opcion == "6":
            producto_id = input("ID del producto a desactivar: ")
            exito, mensaje = productos.cambiar_estado_producto(producto_id, False)
            print(mensaje)

        elif opcion == "7":
            producto_id = input("ID del producto a reactivar: ")
            exito, mensaje = productos.cambiar_estado_producto(producto_id, True)
            print(mensaje)

        elif opcion == "0":
            break

        else:
            print("Opción inválida.")