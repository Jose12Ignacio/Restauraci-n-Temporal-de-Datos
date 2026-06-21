def comprimir_lz77(texto: str, buffer_busqueda: int = 10, buffer_lectura: int = 5) -> dict:
    tripletas = []
    i = 0
    while i < len(texto):
        mejor_offset = 0
        mejor_longitud = 0
        inicio_busqueda = max(0, i - buffer_busqueda)
        ventana = texto[inicio_busqueda:i]
        for longitud in range(min(buffer_lectura, len(texto) - i), 0, -1):
            subcadena = texto[i:i + longitud]
            pos = ventana.find(subcadena)
            if pos != -1:
                mejor_offset = len(ventana) - pos
                mejor_longitud = longitud
                break
        siguiente = texto[i + mejor_longitud] if i + mejor_longitud < len(texto) else ""
        tripletas.append({
            "offset": "_" if mejor_offset == 0 and mejor_longitud == 0 else mejor_offset,
            "longitud": mejor_longitud,
            "siguiente": siguiente
        })
        i += mejor_longitud + 1
    return {
        "tamano_buffer_busqueda": buffer_busqueda,
        "tamano_buffer_lectura": buffer_lectura,
        "tripletas": tripletas
    }


def descomprimir_lz77(estructura: dict) -> str:
    resultado = []
    for t in estructura["tripletas"]:
        offset = t["offset"]
        longitud = t["longitud"]
        siguiente = t["siguiente"]
        if offset != "_" and offset > 0 and longitud > 0:
            inicio = len(resultado) - offset
            for j in range(longitud):
                resultado.append(resultado[inicio + j])
        if siguiente:
            resultado.append(siguiente)
    return "".join(resultado)