from reto3.crc import calcular_crc16


def detectar_error(datos, crc_original):
    crc_actual = calcular_crc16(datos)

    if crc_actual == crc_original:
        return {
            "hay_error": False,
            "crc_actual": crc_actual,
            "mensaje": "No se detectaron errores."
        }

    return {
        "hay_error": True,
        "crc_actual": crc_actual,
        "mensaje": "Se detectó corrupción en el archivo."
    }


def intentar_corregir_un_bit(datos_corruptos, crc_original):
    datos = bytearray(datos_corruptos)

    for indice_byte in range(len(datos)):
        for posicion_bit in range(8):
            copia = bytearray(datos)
            copia[indice_byte] ^= 1 << posicion_bit

            if calcular_crc16(copia) == crc_original:
                return bytes(copia), {
                    "corregido": True,
                    "tipo": "single-bit",
                    "indice_byte": indice_byte,
                    "posicion_bit": posicion_bit
                }

    return datos_corruptos, {
        "corregido": False,
        "tipo": None,
        "mensaje": "No se pudo corregir como error de un solo bit."
    }