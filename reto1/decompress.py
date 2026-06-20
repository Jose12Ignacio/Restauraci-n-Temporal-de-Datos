from reto1.huffman import decodificar
from reto1.lzw import descomprimir_lzw
from reto1.lz77 import descomprimir_lz77
from reto1.lz78 import descomprimir_lz78


def _buscar_estructura(json_data: dict, nombre_algoritmo: str) -> dict:
    """Busca dentro de json_data["compresion"] la estructura del algoritmo dado."""
    for entrada in json_data.get("compresion", []):
        if entrada.get("algoritmo", "").lower() == nombre_algoritmo.lower():
            return entrada.get("estructura", {})
    raise ValueError(f"No se encontró el algoritmo '{nombre_algoritmo}' en el JSON.")

def descomprimir(json_data: dict, algoritmo: str) -> str:
    """
    Recibe el JSON completo y el nombre del algoritmo real ("huffman" o "lzw"),
    extrae la estructura correcta y reconstruye el texto original.
    """
    algoritmo = algoritmo.lower().strip()

    if algoritmo == "huffman":
        estructura = _buscar_estructura(json_data, "Huffman")
        arbol = estructura["arbol"]
        codigo = estructura["salida"]
        return decodificar(codigo, arbol)

    elif algoritmo == "lzw":
        estructura = _buscar_estructura(json_data, "LZW")
        salida = estructura["salida"]
        diccionario_inicial = estructura["diccionario_inicial"]
        return descomprimir_lzw(salida, diccionario_inicial)

    elif algoritmo == "lz77":
        estructura = _buscar_estructura(json_data, "LZ77")
        return descomprimir_lz77(estructura)

    elif algoritmo == "lz78":
        estructura = _buscar_estructura(json_data, "LZ78")
        return descomprimir_lz78(estructura)

    else:
        raise ValueError("Algoritmo no soportado. Usa 'huffman', 'lzw', 'lz77' o 'lz78'.")