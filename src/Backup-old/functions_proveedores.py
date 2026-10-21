import json
import re

from Modules.config import PROVEEDORES_FILE


def cargar_proveedores():
    try:
        with open(PROVEEDORES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        data_inicial = {"contador": 0, "proveedores": []}
        with open(PROVEEDORES_FILE, "w", encoding="utf-8") as f:
            json.dump(data_inicial, f, indent=4, ensure_ascii=False)
        return data_inicial


def generar_id_proveedor(data):
    data["contador"] += 1
    return f"PROV-{data['contador']:03d}"


def guardar_proveedores(data):
    with open(PROVEEDORES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def registrar_proveedor(nombre, contacto, telefono):
    data = cargar_proveedores()
    nuevo_id = generar_id_proveedor(data)

    proveedor = {
        "id": nuevo_id,
        "nombre": nombre,
        "contacto": contacto,
        "telefono": telefono,
        "activo": True,
    }

    data["proveedores"].append(proveedor)
    guardar_proveedores(data)

    return proveedor["id"]


def existe_proveedor(proveedor_id):
    data = cargar_proveedores()
    return any(p["id"] == proveedor_id for p in data["proveedores"])


def validar_email(email):
    if email == "" or email is None:
        return True
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(patron, email) is not None


def validar_telefono(telefono):
    if telefono == "" or telefono is None:
        return True
    return telefono.isdigit()


def proveedor_existe(nombre, data):
    nombre = nombre.strip().lower()
    for p in data["proveedores"]:
        if p["nombre"].strip().lower() == nombre:
            return True
    return False


def cambiar_estado_proveedor(proveedor_id, estado):
    data = cargar_proveedores()

    for p in data["proveedores"]:
        if p["id"] == proveedor_id:
            p["activo"] = estado
            guardar_proveedores(data)
            return True

    return False


def editar_proveedor(proveedor_id, nombre=None, contacto=None, telefono=None):
    data = cargar_proveedores()

    for p in data["proveedores"]:
        if p["id"] == proveedor_id:
            if nombre:
                if proveedor_existe(nombre, data):
                    return False, "Nombre ya existe"
                p["nombre"] = nombre.strip()

            if contacto is not None:
                if not validar_email(contacto):
                    return False, "Correo inválido"
                p["contacto"] = contacto.strip()

            if telefono is not None:
                if not validar_telefono(telefono):
                    return False, "Teléfono inválido"
                p["telefono"] = telefono.strip()

            guardar_proveedores(data)
            return True, "Proveedor actualizado"

    return False, "Proveedor no encontrado"


def buscar_proveedor_por_nombre(texto):
    data = cargar_proveedores()
    texto = texto.lower()
    return [p for p in data["proveedores"] if texto in p["nombre"].lower()]


def listar_proveedores(solo_activos=True):
    data = cargar_proveedores()
    if solo_activos:
        return [p for p in data["proveedores"] if p["activo"]]
    return data["proveedores"]
