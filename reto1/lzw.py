def comprimir_lzw(texto: str):
    diccionario = {chr(i): i for i in range(256)}
    siguiente_codigo = 256

    salida = []
    diccionario_generado = []

    if texto == "":
        return salida, diccionario_generado
    actual = texto[0]

    for ch in texto[1:]:
        combinado = actual + ch
        if combinado in diccionario:
            actual = combinado
        else:
            salida.append(diccionario[actual])
            diccionario[combinado] = siguiente_codigo
            diccionario_generado.append({"codigo": siguiente_codigo, "cadena": combinado})
            siguiente_codigo += 1
            actual = ch
    salida.append(diccionario[actual])
    return salida, diccionario_generado

def descomprimir_lzw(salida: list, diccionario_inicial: dict):
    if not salida:
        return ""
    diccionario = {}
    if diccionario_inicial:
        primera_clave = next(iter(diccionario_inicial))
        primer_valor = diccionario_inicial[primera_clave]
        if isinstance(primer_valor, int):
            for k, v in diccionario_inicial.items():
                diccionario[v] = k
        else:
            for k, v in diccionario_inicial.items():
                diccionario[int(k)] = v
    else:
        diccionario = {i: chr(i) for i in range(256)}

    if not diccionario:
        diccionario = {i: chr(i) for i in range(256)}
    
    siguiente_codigo = max(diccionario.keys()) + 1
    if siguiente_codigo < 256:
        siguiente_codigo = 256
    
    resultado = []
    
    codigo_anterior = salida[0]
    entrada = diccionario[codigo_anterior]
    resultado.append(entrada)

    for codigo in salida[1:]:
        if codigo in diccionario:
            actual = diccionario[codigo]
        elif codigo == siguiente_codigo:
            actual = entrada + entrada[0]
        else:
            raise ValueError(f"Código inválido durante la descompresión LZW: {codigo}")

        resultado.append(actual)
        
        diccionario[siguiente_codigo] = entrada + actual[0]
        siguiente_codigo += 1
        entrada = actual
    return "".join(resultado)