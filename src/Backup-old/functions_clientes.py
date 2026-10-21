from Modules.config import CLIENTES_FILE
import json

def cargar_clientes(): # Carga los datos de los clientes desde el archivo JSON, creando el archivo si no existe con una estructura inicial
    try:
        with open(CLIENTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        data_inicial = {"contador": 0, "clientes": []}
        with open(CLIENTES_FILE, "w", encoding="utf-8") as f:
            json.dump(data_inicial, f, indent=4, ensure_ascii=False)
        return data_inicial

def guardar_clientes(data): # Guarda los datos de los clientes en el archivo JSON
    with open(CLIENTES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def normalizar_nombre(nombre): # Normaliza el nombre del cliente
    return ' '.join(palabra.capitalize() for palabra in nombre.split())

def generar_id_cliente(data): # Genera un nuevo ID para el cliente incrementando el contador
    data["contador"] += 1
    return f"CLI-{data['contador']:03d}"

def validar_nombre(nombre):
    nombre = nombre.strip()
    if not nombre:
        return False, "El nombre no puede estar vacío"
    if nombre[0].isdigit():
        return False, "El nombre no puede iniciar con número"
    if len(nombre) < 2:
        return False, "El nombre debe tener mínimo 2 caracteres"
    return True, ""

def cliente_existe(nombre, data): # Verifica si ya existe un cliente con el mismo nombre (ignorando mayúsculas y espacios)
    nombre = nombre.strip().lower()
    for c in data["clientes"]:
        if c["nombre"].lower() == nombre:
            return True
    return False

def validar_telefono(telefono): # Valida que el teléfono contenga solo dígitos o esté vacío
    if telefono == "" or telefono is None:
        return True, ""
    if not telefono.isdigit():
        return False, "El teléfono debe contener solo dígitos"
    return True, "" 

def agregar_cliente(nombre, telefono=""): # Agrega un nuevo cliente después de validar los datos
    data = cargar_clientes()
    valido, mensaje = validar_nombre(nombre)
    if not valido:
        return False, mensaje
    if cliente_existe(nombre, data):
        return False, "Ya existe un cliente con ese nombre"
    if not validar_telefono(telefono):
        return False, "El teléfono solo debe contener números"
    nuevo_id = generar_id_cliente(data)
    cliente = {
        "id": nuevo_id,
        "nombre": nombre.strip(),
        "telefono": telefono.strip(),
        "activo": True
    }
    data["clientes"].append(cliente)
    guardar_clientes(data)
    return True, nuevo_id

def obtener_cliente(cliente_ID): # Obtiene un cliente por su ID
    cliente_ID = str(cliente_ID).strip()
    clientes = cargar_clientes()
    if cliente_ID not in clientes:
        return False, None, "No se encontró un cliente con ese ID."
    return True, clientes.get(cliente_ID), "Cliente encontrado."

def listar_clientes(): # Lista todos los clientes
    return cargar_clientes() 

def cambiar_estado_cliente(cliente_id, estado): # Cambia el estado activo/inactivo de un cliente
    data = cargar_clientes()
    for c in data["clientes"]:
        if c["id"] == cliente_id:
            c["activo"] = estado
            guardar_clientes(data)
            return True
    return False

def editar_cliente(cliente_id, nombre=None, telefono=None): # Edita la información de un cliente existente
    data = cargar_clientes()
    for c in data["clientes"]:
        if c["id"] == cliente_id:
            if nombre:
                valido, mensaje = validar_nombre(nombre)
                if not valido:
                    return False, mensaje
                if cliente_existe(nombre, data):
                    return False, "Nombre ya registrado"
                c["nombre"] = nombre.strip()
            if telefono is not None:
                valido, mensaje = validar_telefono(telefono)
                if not valido:
                    return False, mensaje
                c["telefono"] = telefono.strip()
            guardar_clientes(data)
            return True, "Cliente actualizado"

    return False, "Cliente no encontrado"