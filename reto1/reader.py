import json
from pathlib import Path
from reto1.decompress import descomprimir

def _cargar_json_desde_texto(contenido: str):
    data = json.loads(contenido)
    if "compresion" not in data:
        raise ValueError("El archivo no contiene la clave 'compresion'. ¿Es un archivo de reto1?")
    return data

def _leer_archivo_json(ruta: Path):
    try:
        contenido = ruta.read_texto(encoding="utf-8")
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