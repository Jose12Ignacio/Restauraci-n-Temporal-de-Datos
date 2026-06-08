import random


def invertir_bit(byte, posicion_bit):
    mascara = 1 << posicion_bit
    return byte ^ mascara


def insertar_error_un_bit(datos, indice_byte=None, posicion_bit=None):
    if len(datos) == 0:
        raise ValueError("No se puede corromper un archivo vacío.")

    datos_corruptos = bytearray(datos)

    if indice_byte is None:
        indice_byte = random.randint(0, len(datos_corruptos) - 1)

    if posicion_bit is None:
        posicion_bit = random.randint(0, 7)

    datos_corruptos[indice_byte] = invertir_bit(
        datos_corruptos[indice_byte],
        posicion_bit
    )

    informacion_error = {
        "tipo": "single-bit",
        "indice_byte": indice_byte,
        "posicion_bit": posicion_bit
    }

    return bytes(datos_corruptos), informacion_error


def insertar_error_burst(datos, inicio_bit=None, cantidad_bits=8):
    if len(datos) == 0:
        raise ValueError("No se puede corromper un archivo vacío.")

    datos_corruptos = bytearray(datos)
    total_bits = len(datos_corruptos) * 8

    if cantidad_bits <= 0:
        raise ValueError("La cantidad de bits debe ser mayor a 0.")

    if cantidad_bits > total_bits:
        raise ValueError("La cantidad de bits supera el tamaño del archivo.")

    if inicio_bit is None:
        inicio_bit = random.randint(0, total_bits - cantidad_bits)

    if inicio_bit < 0 or inicio_bit + cantidad_bits > total_bits:
        raise ValueError("La posición del burst error está fuera del archivo.")

    for posicion_global in range(inicio_bit, inicio_bit + cantidad_bits):
        indice_byte = posicion_global // 8
        posicion_bit = posicion_global % 8

        datos_corruptos[indice_byte] = invertir_bit(
            datos_corruptos[indice_byte],
            posicion_bit
        )

    informacion_error = {
        "tipo": "burst",
        "inicio_bit": inicio_bit,
        "cantidad_bits": cantidad_bits
    }

    return bytes(datos_corruptos), informacion_error