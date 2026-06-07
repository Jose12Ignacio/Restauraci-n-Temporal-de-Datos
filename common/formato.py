def limpiar_espacios_binario(binario):
    return binario.replace(" ", "").replace("\n", "").replace("\t", "")


def texto_a_binario(texto):
    return " ".join(format(ord(caracter), "08b") for caracter in texto)


def binario_a_texto(binario):
    binario = limpiar_espacios_binario(binario)

    if len(binario) % 8 != 0:
        raise ValueError("El binario debe tener una longitud múltiplo de 8.")

    texto = ""

    for i in range(0, len(binario), 8):
        byte = binario[i:i + 8]
        texto += chr(int(byte, 2))

    return texto


def bytes_a_binario(datos):
    return " ".join(format(byte, "08b") for byte in datos)


def binario_a_bytes(binario):
    binario = limpiar_espacios_binario(binario)

    if len(binario) % 8 != 0:
        raise ValueError("El binario debe tener una longitud múltiplo de 8.")

    lista_bytes = []

    for i in range(0, len(binario), 8):
        byte = binario[i:i + 8]
        lista_bytes.append(int(byte, 2))

    return bytes(lista_bytes)


def separar_binario_en_bytes(binario):
    binario = limpiar_espacios_binario(binario)

    if len(binario) % 8 != 0:
        raise ValueError("El binario debe tener una longitud múltiplo de 8.")

    grupos = []

    for i in range(0, len(binario), 8):
        grupos.append(binario[i:i + 8])

    return grupos