from Modules.Clientes.Functions import functions_clientes

def menu_clientes():

    while True: # Bucle principal del programa

        print("\n=== MENU DE GESTION DE CLIENTES ===") # Menú de gestión de clientes
        print("1. Agregar cliente")
        print("2. Listar clientes")
        print("3. Cambiar estado de cliente")
        print("4. Editar cliente")
        print("0. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1": # Opción para agregar un cliente
            nombre = input("Ingrese el nombre del cliente: ")
            telefono = input("Ingrese el teléfono del cliente (opcional): ")
            exito, mensaje = functions_clientes.agregar_cliente(nombre, telefono)
            if exito:
                print(f"Cliente agregado con ID: {mensaje}")
            else:
                print(f"Error al agregar cliente: {mensaje}")

        elif opcion == "2": # Opción para listar clientes
            clientes = functions_clientes.listar_clientes()
            if not clientes["clientes"]:
                print("No hay clientes registrados.")
            else:
                print("\nLista de clientes:")
                for c in clientes["clientes"]:
                    estado = "Activo" if c["activo"] else "Inactivo"
                    print(f"ID: {c['id']} | Nombre: {c['nombre']} | Teléfono: {c['telefono']} | Estado: {estado}")

        elif opcion == "3": # Opción para cambiar el estado de un cliente  
            cliente_id = input("Ingrese el ID del cliente: ")
            nuevo_estado = input("Ingrese el nuevo estado (activo/inactivo): ").strip().lower()
            if nuevo_estado not in ["activo", "inactivo"]:
                print("Estado inválido. Use 'activo' o 'inactivo'.")
                continue
            estado_bool = True if nuevo_estado == "activo" else False
            exito = functions_clientes.cambiar_estado_cliente(cliente_id, estado_bool)
            if exito:
                print("Estado del cliente actualizado.")
            else:
                print("No se encontró un cliente con ese ID.")

        elif opcion == "4": # Opción para editar un cliente
            cliente_id = input("Ingrese el ID del cliente a editar: ")
            nombre = input("Ingrese el nuevo nombre (deje vacío para no cambiar): ")
            telefono = input("Ingrese el nuevo teléfono (deje vacío para no cambiar): ")
            if nombre == "":
                nombre = None
            if telefono == "":
                telefono = None
            exito, mensaje = functions_clientes.editar_cliente(cliente_id, nombre, telefono)
            if exito:
                print(mensaje)
            else:
                print(f"Error al editar cliente: {mensaje}")

        elif opcion == "0": # Opción para volver al menú principal
            print("Volviendo al menú principal...")
            break