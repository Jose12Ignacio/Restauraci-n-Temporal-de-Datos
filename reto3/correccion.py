from reto3.crc import calcular_crc16
from common.formato import binario_a_bytes, limpiar_espacios_binario

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
    Retorna solo la cadena de texto para mantener compatibilidad con Menu.py
    """
    return datos_corruptos.decode("ascii", errors="replace")


def corregir_datos_segmentados(lista_segmentos, max_bits_rafaga=16):
    """
    Nueva función para el torneo: recibe la lista 'data' del JSON,
    repara cada segmento por separado y retorna los bytes totales limpios.
    """
    bytes_totales = bytearray()
    bloques_corregidos = 0
    bloques_sanos = 0
    bloques_fallidos = 0
    
    for seg in lista_segmentos:
        bits_actuales = seg["bits"].replace(" ", "")
        crc_esperado = seg.get("checksum", seg.get("residuo_crc", 0))
        datos_bloque_bytes = bytes([int(bits_actuales, 2)]) # Convierte los 8 bits directos a un byte
        
        # Si el bloque ya es correcto desde el inicio
        if calcular_crc16(datos_bloque_bytes) == crc_esperado:
            bytes_totales.extend(datos_bloque_bytes)
            bloques_sanos += 1
            continue
            
        # Reutiliza tus funciones existentes de inversión de bits
        datos_reparados, info = corregir_con_crc_original(datos_bloque_bytes, crc_esperado, max_bits_rafaga)
        
        bytes_totales.extend(datos_reparados)
        if info.get("corregido"):
            bloques_corregidos += 1
        else:
            bloques_fallidos += 1
            
    return bytes(bytes_totales), bloques_sanos, bloques_corregidos, bloques_fallidos