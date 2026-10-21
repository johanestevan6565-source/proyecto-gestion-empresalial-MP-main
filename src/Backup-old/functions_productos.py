from dataclasses import dataclass
import json

from Modules.config import PRODUCTOS_FILE


@dataclass
class Producto:
    id: str
    nombre: str
    precio: float
    tipo_venta: str
    activo: bool = True

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            nombre=data["nombre"],
            precio=float(data["precio"]),
            tipo_venta=data.get("tipo_venta", "unidad"),
            activo=data.get("activo", True),
        )

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": round(float(self.precio), 2),
            "tipo_venta": self.tipo_venta,
            "activo": self.activo,
        }

    def actualizar_precio(self, nuevo_precio):
        self.precio = round(float(nuevo_precio), 2)


def cargar_productos():
    try:
        with open(PRODUCTOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        data_inicial = {"productos": []}
        with open(PRODUCTOS_FILE, "w", encoding="utf-8") as f:
            json.dump(data_inicial, f, indent=4, ensure_ascii=False)
        return data_inicial


def guardar_productos(data):
    with open(PRODUCTOS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def generar_id(data, nombre):
    letra = nombre.strip()[0].upper()
    contador = 1
    ids_existentes = [p["id"] for p in data["productos"] if p["id"].startswith(letra)]
    while True:
        nuevo_id = f"{letra}{contador:02}"
        if nuevo_id not in ids_existentes:
            return nuevo_id
        contador += 1


def validar_nombre(nombre):
    if not nombre or not nombre.strip():
        return False, "El nombre no puede estar vacío"
    if len(nombre.strip()) > 50:
        return False, "Máximo 50 caracteres"
    if not nombre.replace(" ", "").isalpha():
        return False, "Solo letras y espacios"
    return True, ""


def validar_precio(precio):
    try:
        precio = float(precio)
    except ValueError:
        return False, "Precio inválido"
    if precio <= 0:
        return False, "El precio debe ser mayor a 0"
    return True, ""


def validar_tipo_venta(tipo):
    tipo = tipo.lower()
    if tipo not in ["unidad", "kg"]:
        return False, "Tipo inválido. Debe ser 'unidad' o 'kg'"
    return True, ""


def producto_existe(nombre, data, excluir_id=None):
    for p in data["productos"]:
        if p["nombre"].lower() == nombre.lower():
            if excluir_id and p["id"].lower() == excluir_id.lower():
                continue
            return True
    return False


def agregar_producto(nombre, precio, tipo_venta):
    data = cargar_productos()

    valido, mensaje = validar_nombre(nombre)
    if not valido:
        return False, mensaje
    valido, mensaje = validar_precio(precio)
    if not valido:
        return False, mensaje
    valido, mensaje = validar_tipo_venta(tipo_venta)
    if not valido:
        return False, mensaje
    if producto_existe(nombre, data):
        return False, "El producto ya existe"

    producto = Producto(
        id=generar_id(data, nombre),
        nombre=nombre.strip().title(),
        precio=round(float(precio), 2),
        tipo_venta=tipo_venta.lower(),
        activo=True,
    )

    data["productos"].append(producto.to_dict())
    guardar_productos(data)
    return True, "Producto agregado correctamente"


def obtener_producto_por_id(producto_id):
    data = cargar_productos()
    for p in data["productos"]:
        if p["id"].lower() == producto_id.lower():
            return Producto.from_dict(p)
    return None


def editar_producto(producto_id, nombre=None, precio=None):
    data = cargar_productos()
    for i, p in enumerate(data["productos"]):
        if p["id"].lower() == producto_id.lower():
            producto = Producto.from_dict(p)
            if nombre is not None:
                valido, mensaje = validar_nombre(nombre)
                if not valido:
                    return False, mensaje
                if producto_existe(nombre, data, excluir_id=producto_id):
                    return False, "Nombre ya registrado"
                producto.nombre = nombre.strip().title()
            if precio is not None:
                valido, mensaje = validar_precio(precio)
                if not valido:
                    return False, mensaje
                producto.actualizar_precio(precio)

            data["productos"][i] = producto.to_dict()
            guardar_productos(data)
            return True, "Producto actualizado"
    return False, "Producto no encontrado"


def cambiar_estado_producto(producto_id, activo):
    data = cargar_productos()
    for p in data["productos"]:
        if p["id"].lower() == producto_id.lower():
            p["activo"] = activo
            guardar_productos(data)
            return True, "Estado actualizado"
    return False, "Producto no encontrado"


def listar_productos(activo=None):
    data = cargar_productos()
    resultados = []
    for p in data["productos"]:
        if activo is None or p["activo"] == activo:
            resultados.append(p)
    return resultados


def buscar_producto(entrada, activo=None):
    data = cargar_productos()
    entrada = entrada.strip().lower()
    resultados = []
    for p in data["productos"]:
        if activo is not None and p["activo"] != activo:
            continue
        if entrada == p["id"].lower():
            return [p]
        if entrada == p["nombre"].lower():
            return [p]
        if entrada in p["nombre"].lower():
            resultados.append(p)
    return resultados if resultados else None


def editar_precio_producto(producto_id, nuevo_precio):
    return editar_producto(producto_id, precio=nuevo_precio)
