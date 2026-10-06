from datetime import datetime

from Modules.Inventarios.Functions import functions_inventarios
from Modules.Finanzas.Functions import functions_cartera


def reporte_stock_bodega_fin_dia():
    return functions_inventarios.stock_bodega_actual()


def reporte_canastillas_proveedor_fin_mes(proveedor_id, marca=None):
    return functions_inventarios.empaque_prestado_proveedor_fin_mes(proveedor_id, marca)


def reporte_eventos_filtrados(tipo=None, producto_id=None, cliente_id=None, proveedor=None):
    resultados = []
    for evento in functions_inventarios.listar_eventos_inventario():
        data = evento.get("data", {})
        if tipo and evento.get("tipo") != tipo:
            continue
        if producto_id and data.get("producto_id") != producto_id:
            continue
        if cliente_id and data.get("cliente_id") != cliente_id:
            continue
        if proveedor and data.get("proveedor") != proveedor:
            continue
        resultados.append(evento)
    return resultados


def reporte_balance_financiero():
    balance = functions_cartera.calcular_balance_general()
    balance["fecha_corte"] = datetime.now().strftime("%Y-%m-%d")
    return balance
