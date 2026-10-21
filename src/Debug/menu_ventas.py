from Modules.Ventas.Functions import functions_ventas


def _capturar_items():
    items = []
    while True:
        producto_id = input("Producto ID (vacío para terminar): ").strip()
        if not producto_id:
            break

        cantidad = input("Cantidad: ").strip()
        precio_unitario = input("Precio unitario (vacío=precio global): ").strip()

        item = {"producto_id": producto_id, "cantidad": cantidad}
        if precio_unitario:
            item["precio_unitario"] = precio_unitario
        items.append(item)

    return items


def _capturar_empaques():
    empaques = []
    while True:
        marca = input("Marca empaque prestado (vacío para terminar): ").strip()
        if not marca:
            break
        cantidad = input("Cantidad de empaques: ").strip()
        proveedor = input("Proveedor ID del empaque (opcional): ").strip() or None
        empaques.append({"marca": marca, "cantidad": cantidad, "proveedor": proveedor})
    return empaques


def menu_ventas():
    while True:
        print("\n=== MÓDULO VENTAS ===")
        print("1. Procesar venta")
        print("0. Volver")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            cliente_id = input("ID cliente: ").strip()
            tipo_pago = input("Tipo de pago (contado/credito): ").strip().lower()
            print("\n--- Agregue productos de la venta ---")
            items = _capturar_items()
            if not items:
                print("Debe registrar al menos un producto.")
                continue

            agregar_empaque = input("¿Desea prestar empaque en esta venta? (s/n): ").strip().lower()
            empaques = _capturar_empaques() if agregar_empaque == "s" else []

            ok, mensaje, venta = functions_ventas.procesar_venta(
                cliente_id=cliente_id,
                items=items,
                tipo_pago=tipo_pago,
                empaques_prestados=empaques,
            )
            if ok:
                print(f"Venta {venta['id']} procesada. Total: ${venta['total']:.2f}")
            else:
                print(f"Error: {mensaje}")

        elif opcion == "0":
            break
        else:
            print("Opción inválida")
