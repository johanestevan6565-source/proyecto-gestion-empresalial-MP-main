from Modules.Inventarios.Functions import functions_inventarios 

def menu_test_inventarios():
    while True:
        print("\n=== TEST INVENTARIOS ===")
        print("1. Registrar compra producto")
        print("2. Registrar ingreso empaque proveedor")
        print("3. Ver stock producto")
        print("4. Salir")

        op = input("Opción: ")

        if op == "1":
            proveedor = input("Proveedor ID: ")
            producto = input("Producto ID: ")
            cantidad = float(input("Cantidad: "))
            unidad = input("Unidad (kg/unidad): ")
            precio = float(input("Precio unitario: "))

            functions_inventarios.registrar_compra_producto(proveedor, producto, cantidad, unidad, precio)
            print("Compra registrada")

        elif op == "2":
            marca = input("Marca: ")
            cantidad = int(input("Cantidad: "))
            proveedor = input("Proveedor: ")

            functions_inventarios.registrar_ingreso_empaque_proveedor(marca, cantidad, proveedor)
            print("Empaque registrado")

        elif op == "3":
            producto = input("Producto ID: ")
            stock = functions_inventarios.calcular_stock_producto(producto)
            print(f"Stock actual: {stock}")

        elif op == "4":
            break
