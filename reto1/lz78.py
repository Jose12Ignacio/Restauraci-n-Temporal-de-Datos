def comprimir_lz78(texto: str) -> dict:
    diccionario = {}
    salida = []
    entradas_dict = []
    buffer = ""
    codigo = 1

    for ch in texto:
        buffer_nuevo = buffer + ch
        if buffer_nuevo in diccionario:
            buffer = buffer_nuevo
        else:
            indice_prev = diccionario.get(buffer, 0)
            salida.append({"indice": indice_prev, "simbolo": ch})
            diccionario[buffer_nuevo] = codigo
            entradas_dict.append({"indice": codigo, "cadena": buffer_nuevo})
            codigo += 1
            buffer = ""

    if buffer:
        salida.append({"indice": diccionario.get(buffer, 0), "simbolo": ""})

    return {
        "diccionario": entradas_dict,
        "salida": salida
    }


def descomprimir_lz78(estructura: dict) -> str:
    diccionario = {0: ""}
    resultado = []

    for entrada in estructura["salida"]:
        cadena = diccionario.get(entrada["indice"], "") + entrada["simbolo"]
        resultado.append(cadena)
        diccionario[len(diccionario)] = cadena

    return "".join(resultado)