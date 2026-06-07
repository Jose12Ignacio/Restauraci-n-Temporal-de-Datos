from pathlib import Path


def leer_texto(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return archivo.read()


def guardar_texto(ruta, contenido):
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)


def leer_bytes(ruta):
    with open(ruta, "rb") as archivo:
        return archivo.read()


def guardar_bytes(ruta, datos):
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)

    with open(ruta, "wb") as archivo:
        archivo.write(datos)


def validar_archivo(ruta):
    archivo = Path(ruta)

    if not archivo.exists():
        return False, "El archivo no existe."

    if not archivo.is_file():
        return False, "La ruta no corresponde a un archivo."

    return True, "Archivo válido."