from Modules.Reportes.Functions import functions_reportes


def menu_reportes():
    while True:
        print("\n=== MÓDULO REPORTES ===")
        print("1. Stock de bodega al corte")
        print("2. Canastillas/empaque prestado por proveedor")
        print("3. Filtrar eventos de inventario")
        print("4. Balance financiero (efectivo/cartera/proveedores)")
        print("0. Volver")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            reporte = functions_reportes.reporte_stock_bodega_fin_dia()
            if not reporte:
                print("No hay movimientos de inventario.")
                continue
            for producto, stock in reporte.items():
                print(f"{producto}: {stock}")

        elif opcion == "2":
            proveedor = input("Proveedor ID: ").strip().upper()
            marca = input("Marca (opcional): ").strip() or None
            saldo = functions_reportes.reporte_canastillas_proveedor_fin_mes(proveedor, marca)
            print(f"Saldo neto empaque proveedor {proveedor}: {saldo}")

        elif opcion == "3":
            tipo = input("Tipo evento (opcional): ").strip() or None
            producto_id = input("Producto ID (opcional): ").strip() or None
            cliente_id = input("Cliente ID (opcional): ").strip() or None
            proveedor = input("Proveedor ID (opcional): ").strip() or None
            eventos = functions_reportes.reporte_eventos_filtrados(tipo, producto_id, cliente_id, proveedor)
            if not eventos:
                print("Sin resultados.")
                continue
            for evento in eventos:
                print(evento)

        elif opcion == "4":
            balance = functions_reportes.reporte_balance_financiero()
            print(f"Fecha corte: {balance['fecha_corte']}")
            print(f"Efectivo neto: ${balance['efectivo_neto']:.2f}")
            print(f"Cartera clientes: ${balance['cartera_clientes']:.2f}")
            print(f"Deuda proveedores: ${balance['deuda_proveedores']:.2f}")
            print(f"Posición neta: ${balance['posicion_neta']:.2f}")

        elif opcion == "0":
            break

        else:
            print("Opción inválida")
