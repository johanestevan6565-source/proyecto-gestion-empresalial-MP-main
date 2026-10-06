from Modules.Proveedores.Functions import functions_proveedores
def menu_proveedores():

    while True:
        print("\n=== GESTIÓN DE PROVEEDORES ===")
        print("1. Añadir proveedor")
        print("2. Activar/Desactivar proveedor")
        print("3. Modificar proveedor")
        print("4. Listar proveedores")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")
       
        if opcion == "1": 
            nombre = input("Nombre del proveedor: ")
            contacto = input("Contacto del proveedor: ")
            telefono = input("Teléfono del proveedor: ")
            proveedor_id = functions_proveedores.registrar_proveedor(nombre, contacto, telefono)
            print(f"Proveedor registrado con ID: {proveedor_id}")
        elif opcion == "2":
            print("=== Lista de Proveedores ===")
            data = functions_proveedores.cargar_proveedores()
            proveedores = data.get("proveedores", [])
            for p in proveedores:
                print(f"ID: {p['id']}, Nombre: {p['nombre']}, Activo: {p[ 'activo']}")
            proveedor_id = input("ID del proveedor a activar/desactivar: ")
            if functions_proveedores.existe_proveedor(proveedor_id):
                data = functions_proveedores.cargar_proveedores()
                proveedor = next((p for p in data["proveedores"] if p["id"] == proveedor_id), None)
                nuevo_estado = not proveedor["activo"]
                functions_proveedores.cambiar_estado_proveedor(proveedor_id, nuevo_estado)
                estado_str = "activado" if nuevo_estado else "desactivado"
                print(f"Proveedor {estado_str}.")
            else:
                print("Proveedor no encontrado.")
        elif opcion == "3": 
            proveedor_id = input("ID del proveedor a modificar: ")
            if functions_proveedores.existe_proveedor(proveedor_id):
                nombre = input("Nuevo nombre (dejar vacío para no cambiar): ")
                contacto = input("Nuevo contacto (dejar vacío para no cambiar): ")
                telefono = input("Nuevo teléfono (dejar vacío para no cambiar): ")
                exito, mensaje = functions_proveedores.editar_proveedor(proveedor_id, nombre, contacto, telefono)
                print(mensaje)
            else:
                print("Proveedor no encontrado.")
        
        elif opcion == "4":
            data = functions_proveedores.cargar_proveedores()
            proveedores = data.get("proveedores", [])
            if not proveedores:
                print("No hay proveedores registrados.")
            else:
                print("\nLista de Proveedores:")
                for p in proveedores:
                    print(f"ID: {p['id']}, Nombre: {p['nombre']}, Contacto: {p['contacto']}, Teléfono: {p['telefono']}, Activo: {p['activo']}")
        elif opcion == "5":
            print("Saliendo del menú de proveedores...")
            break