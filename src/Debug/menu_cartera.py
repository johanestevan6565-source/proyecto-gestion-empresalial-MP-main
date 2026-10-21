import Modules.Finanzas.Functions.functions_cartera as cartera


def menu_cartera():
    while True:
        print("\n===== MÓDULO CARTERA =====")
        print("1. Registrar cargo cliente")
        print("2. Registrar abono cliente")
        print("3. Ver movimientos por cliente")
        print("4. Ver saldo de un cliente")
        print("5. Ver resumen cartera de clientes")
        print("6. Registrar deuda con proveedor (cargo)")
        print("7. Registrar pago a proveedor (abono)")
        print("8. Registrar movimiento de efectivo")
        print("9. Ver balance general")
        print("0. Volver")

        opcion = input("Seleccione una opción: ").strip()

        if opcion in {"1", "2"}:
            cliente_id = input("ID del cliente (ej. CLI-001): ").strip()
            concepto = input("Concepto del movimiento: ").strip()
            monto = input("Monto: ").strip()
            tipo = "cargo" if opcion == "1" else "abono"
            exito, resultado = cartera.registrar_movimiento(cliente_id, concepto, monto, tipo)
            print(f"Movimiento registrado: {resultado['id']}" if exito else f"Error: {resultado}")

        elif opcion == "3":
            cliente_id = input("ID del cliente: ").strip()
            movimientos = cartera.listar_movimientos(cliente_id=cliente_id)
            if not movimientos:
                print("No hay movimientos para este cliente.")
                continue
            for m in movimientos:
                print(f"{m['id']} | {m['fecha']} | {m['tipo'].upper()} | ${m['monto']:.2f} | {m['concepto']}")

        elif opcion == "4":
            cliente_id = input("ID del cliente: ").strip()
            exito, mensaje, saldo = cartera.calcular_saldo_cliente(cliente_id)
            print(f"Saldo actual de {cliente_id.upper()}: ${saldo:.2f}" if exito else f"Error: {mensaje}")

        elif opcion == "5":
            resumen = cartera.listar_saldos_clientes()
            if not resumen:
                print("No hay movimientos registrados en cartera.")
                continue
            for item in resumen:
                print(f"{item['cliente_id']}: ${item['saldo']:.2f}")

        elif opcion in {"6", "7"}:
            proveedor_id = input("ID proveedor: ").strip()
            concepto = input("Concepto: ").strip()
            monto = input("Monto: ").strip()
            tipo = "cargo" if opcion == "6" else "abono"
            exito, resultado = cartera.registrar_movimiento_proveedor(proveedor_id, concepto, monto, tipo)
            print(f"Movimiento proveedor: {resultado['id']}" if exito else f"Error: {resultado}")

        elif opcion == "8":
            tipo = input("Tipo (ingreso/egreso): ").strip()
            concepto = input("Concepto: ").strip()
            monto = input("Monto: ").strip()
            exito, resultado = cartera.registrar_flujo_efectivo(tipo, concepto, monto)
            print(f"Movimiento efectivo: {resultado['id']}" if exito else f"Error: {resultado}")

        elif opcion == "9":
            balance = cartera.calcular_balance_general()
            print(f"Efectivo neto: ${balance['efectivo_neto']:.2f}")
            print(f"Cartera clientes: ${balance['cartera_clientes']:.2f}")
            print(f"Deuda proveedores: ${balance['deuda_proveedores']:.2f}")
            print(f"Posición neta: ${balance['posicion_neta']:.2f}")

        elif opcion == "0":
            break
        else:
            print("Opción inválida.")
