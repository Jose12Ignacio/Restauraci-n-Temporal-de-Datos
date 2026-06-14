from reto1.huffman import construir_arbol, construir_tabla, codificar
from reto1.lzw import comprimir_lzw

def _despiste_huffman(texto: str):
    if texto == "":
        texto = "A"
    arbol = construir_arbol(texto)
    tabla = construir_tabla(arbol)
    return {
        "arbol": arbol,
        "tabla_codigos": tabla,
    }

def _despiste_lz77(texto: str):
    tamano_buffer_busqueda = 10
    tamano_buffer_lectura = 5
    tripletas = []
    if texto == "":
        texto = "A"
    for i, ch in enumerate(texto):
        tripletas.append({
            "offset": 0 if i == 0 else (i % tamano_buffer_busqueda) + 1,
            "longitud": 0 if i == 0 else i % 3,
            "siguiente": ch
        })
    return {
        "tamano_buffer_busqueda": tamano_buffer_busqueda,
        "tamano_buffer_lectura": tamano_buffer_lectura,
        "tripletas": tripletas,
    }

def _despiste_lz78(texto: str):
    if texto == "":
        texto = "A"
    diccionario = []
    salida = []
    indice_actual = 1

    for i, ch in enumerate(texto):
        if i == 0:
            salida.append({"indice": 0, "simbolo": ch})
        else:
            diccionario.append({"indice": indice_actual, "cadena": ch})
            salida.append({"indice": indice_actual - 1, "simbolo": ch})
            indice_actual += 1
    return {
        "diccionario":diccionario,
        "salida": salida,
    }

def _despiste_lzw(texto: str):
    if texto == "":
        texto = "A"
    
    salida, diccionario_generado = comprimir_lzw(texto)
    diccionario_inicial = {ch: ord(ch) for ch in set(texto)}

    return {
        "diccionario_inicial": diccionario_inicial,
        "diccionario_generado": diccionario_generado,
        "salida": salida,
    }

def comprimir(texto: str, algoritmo: str):
    algoritmo = algoritmo.lower().strip()
    
    if algoritmo not in ("huffman", "lzw"):
        raise ValueError("Algoritmo no soportado. Usa 'huffman' o 'lzw'.")
    compresion = []

    if algoritmo == "huffman":
        arbol = construir_arbol(texto)
        tabla = construir_tabla(arbol)
        codigo = codificar(texto, tabla)
        estructura_huffman = {
            "arbol": arbol,
            "tabla_codigos": tabla,
            "salida": codigo,
        }
    else:
        estructura_huffman = _despiste_huffman(texto)
    
    compresion.append({
        "algoritmo": "Huffman",
        "estructura": estructura_huffman,
    })

    compresion.append({
        "algoritmo": "LZ78",
        "estructura": _despiste_lz78(texto),
    })

    if algoritmo == "lzw":
        salida, diccionario_generado = comprimir_lzw(texto)
        diccionario_inicial = {ch: ord(ch) for ch in set(texto)} if texto else {}
        estructura_lzw = {
            "diccionario_inicial": diccionario_inicial,
            "diccionario_generado": diccionario_generado,
            "salida": salida,
        }
    else:
        estructura_lzw = _despiste_lzw(texto)

    compresion.append({
        "algoritmo": "LZW",
        "estructura": estructura_lzw,
    })

    return {"compresion": compresion}