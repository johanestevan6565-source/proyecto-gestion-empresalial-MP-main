import os

# ==============================
# RAÍZ DEL PROYECTO
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# ==============================
# CARPETAS PRINCIPALES
# ==============================

DATA_DIR = os.path.join(PROJECT_ROOT, "Data")
INVENTARIOS_DIR = os.path.join(DATA_DIR, "inventarios")

# Crear carpetas automáticamente si no existen
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(INVENTARIOS_DIR, exist_ok=True)

# ==============================
# ARCHIVOS PRINCIPALES
# ==============================

CLIENTES_FILE = os.path.join(DATA_DIR, "clientes.json")
PRODUCTOS_FILE = os.path.join(DATA_DIR, "productos.json")
PROVEEDORES_FILE = os.path.join(DATA_DIR, "proveedores.json")
CARTERA_FILE = os.path.join(DATA_DIR, "cartera.json")
VENTAS_FILE = os.path.join(DATA_DIR, "ventas.json")

# ==============================
# PATHS PARA MÓDULOS
# ==============================
PATHS = {
    "clientes": {
        "ruta": CLIENTES_FILE
    },
    "productos": {
        "ruta": PRODUCTOS_FILE
    },
    "proveedores": {
        "ruta": PROVEEDORES_FILE
    },
    "inventarios": {
        "ruta": INVENTARIOS_DIR
    },
    "cartera": {
        "ruta": CARTERA_FILE
    },
    "ventas": {
        "ruta": VENTAS_FILE
    }
}