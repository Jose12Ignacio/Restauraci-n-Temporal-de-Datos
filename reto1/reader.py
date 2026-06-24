import json
from pathlib import Path
from reto1.decompress import descomprimir


def _cargar_json_desde_texto(contenido: str):
    data = json.loads(contenido)
    if "compresion" not in data:
        raise ValueError("El archivo no contiene la clave 'compresion'. ¿Es un archivo de reto1?")
    return data


def _leer_archivo_json(ruta: Path):
    contenido = ruta.read_text(encoding="utf-8") 
    return _cargar_json_desde_texto(contenido)


def _leer_archivo_bin(ruta: Path) -> dict:
    try:
        contenido = ruta.read_text(encoding="utf-8")
        return _cargar_json_desde_texto(contenido)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
        pass

    try:
        contenido = ruta.read_bytes().decode("utf-8", errors="replace")
        return _cargar_json_desde_texto(contenido)
    except (json.JSONDecodeError, ValueError):
        pass

    raise ValueError(
        f"No se pudo interpretar '{ruta.name}' como un archivo de compresión válido. "
        "Asegúrate de que sea un JSON generado por el Reto 1."
    )


def _leer_archivo_generico(ruta: Path):
    try:
        contenido = ruta.read_text(encoding="utf-8") 
        return _cargar_json_desde_texto(contenido)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as e:
        raise ValueError(
            f"No se pudo leer '{ruta.name}' como archivo de compresión. "
            f"Detalle: {e}"
        )


def leer_y_descomprimir(ruta: str, algoritmo: str):
    archivo = Path(ruta)

    if not archivo.exists():
        raise FileNotFoundError(f"El archivo no existe: {ruta}")

    if not archivo.is_file():
        raise ValueError(f"La ruta no apunta a un archivo válido: {ruta}")

    extension = "".join(archivo.suffixes).lower()

    if ".json" in extension:
        json_data = _leer_archivo_json(archivo)
    elif extension == ".bin":
        json_data = _leer_archivo_bin(archivo)
    else:
        json_data = _leer_archivo_generico(archivo)

    return descomprimir(json_data, algoritmo)