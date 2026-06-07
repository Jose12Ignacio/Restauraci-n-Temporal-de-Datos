import random


def invertir_bit(byte, posicion):
    mascara = 1 << posicion
    return byte ^ mascara


def insertar_error_un_bit(datos, indice_byte=None, posicion_bit=None):
    datos = bytearray(datos)

    if indice_byte is None:
        indice_byte = random.randint(0, len(datos) - 1)

    if posicion_bit is None:
        posicion_bit = random.randint(0, 7)

    datos[indice_byte] = invertir_bit(datos[indice_byte], posicion_bit)

    informacion_error = {
        "tipo": "single-bit",
        "indice_byte": indice_byte,
        "posicion_bit": posicion_bit
    }

    return bytes(datos), informacion_error


def insertar_error_burst(datos, inicio=None, cantidad_bits=8):
    datos = bytearray(datos)

    total_bits = len(datos) * 8

    if inicio is None:
        inicio = random.randint(0, total_bits - cantidad_bits)

    for posicion_global in range(inicio, inicio + cantidad_bits):
        indice_byte = posicion_global // 8
        posicion_bit = posicion_global % 8

        datos[indice_byte] = invertir_bit(datos[indice_byte], posicion_bit)

    informacion_error = {
        "tipo": "burst",
        "inicio_bit": inicio,
        "cantidad_bits": cantidad_bits
    }

    return bytes(datos), informacion_error