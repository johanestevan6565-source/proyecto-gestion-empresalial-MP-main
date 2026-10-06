from dataclasses import dataclass
import json
from datetime import datetime

from Modules.config import VENTAS_FILE
from Modules.Clientes.Functions import functions_clientes
from Modules.Productos.Functions import functions_productos
from Modules.Inventarios.Functions import functions_inventarios
from Modules.Finanzas.Functions import functions_cartera


@dataclass
class ItemVenta:
    producto_id: str
    cantidad: float
    precio_unitario: float

    @property
    def subtotal(self):
        return round(self.cantidad * self.precio_unitario, 2)

    def to_dict(self):
        return {
            "producto_id": self.producto_id,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "subtotal": self.subtotal,
        }


def cargar_ventas():
    try:
        with open(VENTAS_FILE, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        data = {"contador": 0, "ventas": []}
        guardar_ventas(data)
        return data


def guardar_ventas(data):
    with open(VENTAS_FILE, "w", encoding="utf-8") as archivo:
        json.dump(data, archivo, indent=4, ensure_ascii=False)


def _generar_id_venta(data):
    data["contador"] += 1
    return f"VEN-{data['contador']:04d}"


def _cliente_valido(cliente_id):
    data = functions_clientes.cargar_clientes()
    for cliente in data.get("clientes", []):
        if cliente["id"].upper() == cliente_id.upper() and cliente.get("activo", True):
            return True
    return False


def _construir_item(item):
    producto_id = item.get("producto_id", "").strip().upper()
    if not producto_id:
        return False, "producto_id obligatorio", None

    producto = functions_productos.obtener_producto_por_id(producto_id)
    if not producto or not producto.activo:
        return False, f"Producto {producto_id} no existe o está inactivo", None

    try:
        cantidad = float(item.get("cantidad", 0))
    except ValueError:
        return False, f"Cantidad inválida para {producto_id}", None
    if cantidad <= 0:
        return False, f"Cantidad debe ser > 0 para {producto_id}", None

    precio_unitario = item.get("precio_unitario", producto.precio)
    try:
        precio_unitario = float(precio_unitario)
    except ValueError:
        return False, f"Precio inválido para {producto_id}", None
    if precio_unitario <= 0:
        return False, f"Precio debe ser > 0 para {producto_id}", None

    stock = functions_inventarios.calcular_stock_producto(producto_id)
    if stock < cantidad:
        return False, f"Stock insuficiente para {producto_id}. Disponible: {stock}", None

    return True, "", ItemVenta(producto_id=producto_id, cantidad=cantidad, precio_unitario=precio_unitario)


def procesar_venta(cliente_id, items, tipo_pago, empaques_prestados=None, fecha=None):
    if not _cliente_valido(cliente_id):
        return False, "Cliente no existe o está inactivo", None

    tipo_pago = tipo_pago.strip().lower()
    if tipo_pago not in {"contado", "credito"}:
        return False, "Tipo de pago inválido. Use contado o credito", None

    items_validos = []
    for item in items:
        ok, mensaje, item_venta = _construir_item(item)
        if not ok:
            return False, mensaje, None
        items_validos.append(item_venta)

    total = round(sum(i.subtotal for i in items_validos), 2)
    data = cargar_ventas()
    venta_id = _generar_id_venta(data)

    venta = {
        "id": venta_id,
        "cliente_id": cliente_id.strip().upper(),
        "fecha": fecha or datetime.now().strftime("%Y-%m-%d"),
        "tipo_pago": tipo_pago,
        "items": [i.to_dict() for i in items_validos],
        "empaques_prestados": empaques_prestados or [],
        "total": total,
    }

    for item in items_validos:
        functions_inventarios.registrar_salida_venta(
            venta_id=venta_id,
            cliente_id=venta["cliente_id"],
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            precio_unitario=item.precio_unitario,
        )

    for empaque in venta["empaques_prestados"]:
        functions_inventarios.registrar_prestamo_empaque_cliente(
            cliente_id=venta["cliente_id"],
            marca=empaque.get("marca", ""),
            cantidad=int(empaque.get("cantidad", 0)),
            proveedor=empaque.get("proveedor"),
            venta_id=venta_id,
        )

    if tipo_pago == "credito":
        functions_cartera.registrar_movimiento(
            cliente_id=venta["cliente_id"],
            concepto=f"Venta a crédito {venta_id}",
            monto=total,
            tipo="cargo",
            referencia=venta_id,
        )
    else:
        functions_cartera.registrar_flujo_efectivo(
            tipo="ingreso",
            concepto=f"Venta de contado {venta_id}",
            monto=total,
            referencia=venta_id,
        )

    data["ventas"].append(venta)
    guardar_ventas(data)
    return True, "Venta procesada correctamente", venta
