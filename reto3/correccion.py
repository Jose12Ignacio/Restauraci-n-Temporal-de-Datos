from reto3.crc import calcular_crc16


def invertir_bit_en_posicion(datos, posicion_global):
    datos_modificados = bytearray(datos)

    indice_byte = posicion_global // 8
    posicion_bit = posicion_global % 8

    datos_modificados[indice_byte] ^= 1 << posicion_bit

    return bytes(datos_modificados)


def invertir_rango_bits(datos, inicio_bit, cantidad_bits):
    datos_modificados = bytearray(datos)

    for posicion_global in range(inicio_bit, inicio_bit + cantidad_bits):
        indice_byte = posicion_global // 8
        posicion_bit = posicion_global % 8

        datos_modificados[indice_byte] ^= 1 << posicion_bit

    return bytes(datos_modificados)


def intentar_corregir_un_bit(datos_corruptos, crc_original):
    total_bits = len(datos_corruptos) * 8

    for posicion_global in range(total_bits):
        datos_prueba = invertir_bit_en_posicion(datos_corruptos, posicion_global)

        if calcular_crc16(datos_prueba) == crc_original:
            return datos_prueba, {
                "corregido": True,
                "tipo": "single-bit",
                "indice_byte": posicion_global // 8,
                "posicion_bit": posicion_global % 8,
                "posicion_global_bit": posicion_global
            }

    return datos_corruptos, {
        "corregido": False,
        "tipo": None,
        "mensaje": "No se pudo corregir como error de un solo bit."
    }


def intentar_corregir_burst(datos_corruptos, crc_original, max_bits_rafaga=16):
    total_bits = len(datos_corruptos) * 8

    for cantidad_bits in range(2, max_bits_rafaga + 1):
        for inicio_bit in range(0, total_bits - cantidad_bits + 1):
            datos_prueba = invertir_rango_bits(
                datos_corruptos,
                inicio_bit,
                cantidad_bits
            )

            if calcular_crc16(datos_prueba) == crc_original:
                return datos_prueba, {
                    "corregido": True,
                    "tipo": "burst",
                    "inicio_bit": inicio_bit,
                    "cantidad_bits": cantidad_bits
                }

    return datos_corruptos, {
        "corregido": False,
        "tipo": None,
        "mensaje": (
            "No se pudo corregir como burst error dentro del límite "
            f"de {max_bits_rafaga} bits."
        )
    }


def corregir_con_crc_original(datos_corruptos, crc_original, max_bits_rafaga=16):
    datos_corregidos, info = intentar_corregir_un_bit(
        datos_corruptos,
        crc_original
    )

    if info["corregido"]:
        return datos_corregidos, info

    datos_corregidos, info = intentar_corregir_burst(
        datos_corruptos,
        crc_original,
        max_bits_rafaga
    )

    if info["corregido"]:
        return datos_corregidos, info

    return datos_corruptos, {
        "corregido": False,
        "tipo": None,
        "mensaje": (
            "No se pudo corregir automáticamente. "
            "Puede que el archivo tenga varios errores separados, "
            "un burst mayor al límite permitido o que el CRC no corresponda."
        )
    }
def recuperar_texto_aproximado(datos_corruptos):
    """
    Intenta recuperar texto desde bytes corruptos sin usar CRC.
    No garantiza recuperación exacta.
    """

    texto = datos_corruptos.decode("utf-8", errors="replace")

    caracteres_invalidos = texto.count("�")

    return texto, {
        "recuperado": True,
        "metodo": "recuperacion_aproximada_utf8",
        "caracteres_invalidos": caracteres_invalidos,
        "advertencia": (
            "Esta recuperación no garantiza que el texto sea idéntico "
            "al original porque no usa CRC original."
        )
    }