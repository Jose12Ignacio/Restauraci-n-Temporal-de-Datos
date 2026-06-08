from pathlib import Path
import shutil


def validar_archivo(ruta):
    archivo = Path(ruta)

    if not archivo.exists():
        return False, "El archivo no existe."

    if not archivo.is_file():
        return False, "La ruta no corresponde a un archivo."

    return True, "Archivo válido."


def leer_texto(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return archivo.read()


def guardar_texto(ruta, contenido):
    ruta_archivo = Path(ruta)
    ruta_archivo.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)


def leer_bytes(ruta):
    with open(ruta, "rb") as archivo:
        return archivo.read()


def guardar_bytes(ruta, datos):
    ruta_archivo = Path(ruta)
    ruta_archivo.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta, "wb") as archivo:
        archivo.write(datos)


def obtener_nombre_archivo(ruta):
    return Path(ruta).name


def obtener_extension(ruta):
    return Path(ruta).suffix


def copiar_archivo(ruta_origen, ruta_destino):
    ruta_destino = Path(ruta_destino)
    ruta_destino.parent.mkdir(parents=True, exist_ok=True)

    shutil.copyfile(ruta_origen, ruta_destino)


def limpiar_pycache(ruta_base="."):
    ruta_base = Path(ruta_base)

    for carpeta in ruta_base.rglob("__pycache__"):
        shutil.rmtree(carpeta)