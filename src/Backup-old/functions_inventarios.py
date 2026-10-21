from datetime import datetime
import json
import os

from Modules.config import INVENTARIOS_DIR


def nombre_archivo_mensual(fecha=None):
    if fecha is None:
        fecha = datetime.now()
    return f"{fecha.year}_{fecha.month:02d}.json"


def ruta_archivo_inventario(fecha=None):
    return os.path.join(INVENTARIOS_DIR, nombre_archivo_mensual(fecha))


def obtener_archivo_mensual(fecha=None):
    ruta = ruta_archivo_inventario(fecha)
    if not os.path.exists(ruta):
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump({"eventos": []}, f, indent=4, ensure_ascii=False)
    return ruta


def registrar_evento_inventario(tipo, origen, data, fecha=None):
    ruta_archivo = obtener_archivo_mensual(fecha)
    timestamp = datetime.now().isoformat(timespec="seconds")
    evento = {"timestamp": timestamp, "tipo": tipo, "origen": origen, "data": data}

    with open(ruta_archivo, "r+", encoding="utf-8") as f:
        contenido = json.load(f)
        contenido["eventos"].append(evento)
        f.seek(0)
        json.dump(contenido, f, indent=4, ensure_ascii=False)
        f.truncate()


def registrar_compra_producto(proveedor_id, producto_id, cantidad, unidad, precio_unitario):
    total = float(cantidad) * float(precio_unitario)
    data_evento = {
        "proveedor_id": proveedor_id,
        "producto_id": producto_id,
        "cantidad": float(cantidad),
        "unidad": unidad,
        "precio_unitario": float(precio_unitario),
        "total": round(total, 2),
    }
    registrar_evento_inventario("compra", "registro_compra_producto", data_evento)


def registrar_salida_venta(venta_id, cliente_id, producto_id, cantidad, precio_unitario):
    data_evento = {
        "venta_id": venta_id,
        "cliente_id": cliente_id,
        "producto_id": producto_id,
        "cantidad": float(cantidad),
        "precio_unitario": float(precio_unitario),
    }
    registrar_evento_inventario("venta", "procesar_venta", data_evento)


def registrar_ingreso_empaque_proveedor(marca, cantidad, proveedor):
    data_evento = {"marca": marca, "cantidad": int(cantidad), "proveedor": proveedor}
    registrar_evento_inventario(
        tipo="ingreso_empaque_proveedor",
        origen="registro_ingreso_empaque_proveedor",
        data=data_evento,
    )


def registrar_prestamo_empaque_cliente(cliente_id, marca, cantidad, proveedor=None, venta_id=None):
    data_evento = {
        "cliente_id": cliente_id,
        "marca": marca,
        "cantidad": int(cantidad),
        "proveedor": proveedor,
        "venta_id": venta_id,
    }
    registrar_evento_inventario(
        tipo="prestamo_empaque_cliente",
        origen="procesar_venta",
        data=data_evento,
    )


def registrar_devolucion_empaque_cliente(cliente_id, marca, cantidad):
    data_evento = {"cliente_id": cliente_id, "marca": marca, "cantidad": int(cantidad)}
    registrar_evento_inventario(
        tipo="devolucion_empaque_cliente",
        origen="registro_devolucion_empaque_cliente",
        data=data_evento,
    )


def registrar_devolucion_empaque_proveedor(marca, cantidad, proveedor):
    data_evento = {"marca": marca, "cantidad": int(cantidad), "proveedor": proveedor}
    registrar_evento_inventario(
        tipo="devolucion_empaque_proveedor",
        origen="registro_devolucion_empaque_proveedor",
        data=data_evento,
    )


def obtener_archivos_inventario():
    if not os.path.exists(INVENTARIOS_DIR):
        return []
    return [
        os.path.join(INVENTARIOS_DIR, f)
        for f in os.listdir(INVENTARIOS_DIR)
        if f.endswith(".json")
    ]


def listar_eventos_inventario():
    eventos = []
    for archivo in obtener_archivos_inventario():
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = json.load(f)
            eventos.extend(contenido.get("eventos", []))
    return eventos


def calcular_stock_producto(producto_id):
    stock = 0.0
    for evento in listar_eventos_inventario():
        data = evento.get("data", {})
        if data.get("producto_id") != producto_id:
            continue
        if evento["tipo"] == "compra":
            stock += float(data.get("cantidad", 0))
        elif evento["tipo"] == "venta":
            stock -= float(data.get("cantidad", 0))
    return round(stock, 2)


def stock_bodega_actual():
    resumen = {}
    for evento in listar_eventos_inventario():
        data = evento.get("data", {})
        producto_id = data.get("producto_id")
        if not producto_id:
            continue
        if producto_id not in resumen:
            resumen[producto_id] = 0.0
        if evento["tipo"] == "compra":
            resumen[producto_id] += float(data.get("cantidad", 0))
        elif evento["tipo"] == "venta":
            resumen[producto_id] -= float(data.get("cantidad", 0))

    return {k: round(v, 2) for k, v in resumen.items()}


def empaque_prestado_proveedor_fin_mes(proveedor_id, marca=None):
    saldo = 0
    for evento in listar_eventos_inventario():
        data = evento.get("data", {})
        if data.get("proveedor") != proveedor_id:
            continue
        if marca and str(data.get("marca", "")).lower() != marca.lower():
            continue

        if evento["tipo"] == "ingreso_empaque_proveedor":
            saldo += int(data.get("cantidad", 0))
        elif evento["tipo"] in {"devolucion_empaque_proveedor", "prestamo_empaque_cliente"}:
            saldo -= int(data.get("cantidad", 0))

    return saldo
