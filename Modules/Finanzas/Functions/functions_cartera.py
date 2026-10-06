import json
from datetime import datetime

from Modules.config import CARTERA_FILE


def cargar_cartera():
    try:
        with open(CARTERA_FILE, "r", encoding="utf-8") as archivo:
            data = json.load(archivo)
    except FileNotFoundError:
        data = {}

    data.setdefault("contador_movimientos", 0)
    data.setdefault("movimientos", [])
    data.setdefault("contador_flujo", 0)
    data.setdefault("flujo_efectivo", [])
    data.setdefault("contador_proveedores", 0)
    data.setdefault("cuentas_por_pagar_proveedores", [])
    return data


def guardar_cartera(data):
    with open(CARTERA_FILE, "w", encoding="utf-8") as archivo:
        json.dump(data, archivo, indent=4, ensure_ascii=False)


def _generar_id(data, key, prefijo):
    data[key] += 1
    return f"{prefijo}-{data[key]:04d}"


def validar_tipo_movimiento(tipo):
    tipo_normalizado = tipo.strip().lower()
    if tipo_normalizado not in {"cargo", "abono"}:
        return False, "Tipo inválido. Use 'cargo' o 'abono'."
    return True, tipo_normalizado


def validar_monto(monto):
    try:
        valor = float(monto)
    except ValueError:
        return False, "Monto inválido. Debe ser numérico."
    if valor <= 0:
        return False, "El monto debe ser mayor que 0."
    return True, round(valor, 2)


def registrar_movimiento(cliente_id, concepto, monto, tipo, fecha=None, referencia=None):
    if not cliente_id or not cliente_id.strip():
        return False, "Debe indicar un cliente_id válido."
    if not concepto or not concepto.strip():
        return False, "Debe indicar un concepto para el movimiento."

    valido_monto, monto_normalizado = validar_monto(monto)
    if not valido_monto:
        return False, monto_normalizado

    valido_tipo, tipo_normalizado = validar_tipo_movimiento(tipo)
    if not valido_tipo:
        return False, tipo_normalizado

    data = cargar_cartera()
    movimiento = {
        "id": _generar_id(data, "contador_movimientos", "MOV"),
        "cliente_id": cliente_id.strip().upper(),
        "concepto": concepto.strip(),
        "tipo": tipo_normalizado,
        "monto": monto_normalizado,
        "fecha": fecha or datetime.now().strftime("%Y-%m-%d"),
        "referencia": referencia,
    }
    data["movimientos"].append(movimiento)
    guardar_cartera(data)
    return True, movimiento


def registrar_flujo_efectivo(tipo, concepto, monto, fecha=None, referencia=None):
    tipo_normalizado = tipo.strip().lower()
    if tipo_normalizado not in {"ingreso", "egreso"}:
        return False, "Tipo inválido. Use 'ingreso' o 'egreso'."

    valido_monto, monto_normalizado = validar_monto(monto)
    if not valido_monto:
        return False, monto_normalizado

    data = cargar_cartera()
    movimiento = {
        "id": _generar_id(data, "contador_flujo", "EFE"),
        "tipo": tipo_normalizado,
        "concepto": concepto.strip(),
        "monto": monto_normalizado,
        "fecha": fecha or datetime.now().strftime("%Y-%m-%d"),
        "referencia": referencia,
    }
    data["flujo_efectivo"].append(movimiento)
    guardar_cartera(data)
    return True, movimiento


def registrar_movimiento_proveedor(proveedor_id, concepto, monto, tipo, fecha=None, referencia=None):
    valido_tipo, tipo_normalizado = validar_tipo_movimiento(tipo)
    if not valido_tipo:
        return False, tipo_normalizado

    valido_monto, monto_normalizado = validar_monto(monto)
    if not valido_monto:
        return False, monto_normalizado

    data = cargar_cartera()
    movimiento = {
        "id": _generar_id(data, "contador_proveedores", "CXP"),
        "proveedor_id": proveedor_id.strip().upper(),
        "concepto": concepto.strip(),
        "tipo": tipo_normalizado,
        "monto": monto_normalizado,
        "fecha": fecha or datetime.now().strftime("%Y-%m-%d"),
        "referencia": referencia,
    }
    data["cuentas_por_pagar_proveedores"].append(movimiento)
    guardar_cartera(data)
    return True, movimiento


def listar_movimientos(cliente_id=None, tipo=None):
    data = cargar_cartera()
    resultados = []
    for movimiento in data["movimientos"]:
        if cliente_id and movimiento["cliente_id"] != cliente_id.strip().upper():
            continue
        if tipo and movimiento["tipo"] != tipo.strip().lower():
            continue
        resultados.append(movimiento)
    return resultados


def calcular_saldo_cliente(cliente_id):
    if not cliente_id or not cliente_id.strip():
        return False, "Debe indicar un cliente_id válido.", 0.0

    saldo = 0.0
    for movimiento in listar_movimientos(cliente_id=cliente_id):
        if movimiento["tipo"] == "cargo":
            saldo += movimiento["monto"]
        elif movimiento["tipo"] == "abono":
            saldo -= movimiento["monto"]
    return True, "Saldo calculado correctamente.", round(saldo, 2)


def listar_saldos_clientes():
    acumulado = {}
    for movimiento in listar_movimientos():
        cliente_id = movimiento["cliente_id"]
        acumulado.setdefault(cliente_id, 0.0)
        acumulado[cliente_id] += movimiento["monto"] if movimiento["tipo"] == "cargo" else -movimiento["monto"]

    resultados = [{"cliente_id": cid, "saldo": round(saldo, 2)} for cid, saldo in acumulado.items()]
    resultados.sort(key=lambda item: item["saldo"], reverse=True)
    return resultados


def calcular_deuda_total_proveedores():
    data = cargar_cartera()
    total = 0.0
    for movimiento in data["cuentas_por_pagar_proveedores"]:
        total += movimiento["monto"] if movimiento["tipo"] == "cargo" else -movimiento["monto"]
    return round(total, 2)


def calcular_efectivo_neto():
    data = cargar_cartera()
    total = 0.0
    for movimiento in data["flujo_efectivo"]:
        total += movimiento["monto"] if movimiento["tipo"] == "ingreso" else -movimiento["monto"]
    return round(total, 2)


def calcular_balance_general():
    cartera_clientes = round(sum(item["saldo"] for item in listar_saldos_clientes()), 2)
    deuda_proveedores = calcular_deuda_total_proveedores()
    efectivo_neto = calcular_efectivo_neto()
    posicion_neta = round(efectivo_neto + cartera_clientes - deuda_proveedores, 2)

    return {
        "efectivo_neto": efectivo_neto,
        "cartera_clientes": cartera_clientes,
        "deuda_proveedores": deuda_proveedores,
        "posicion_neta": posicion_neta,
    }
