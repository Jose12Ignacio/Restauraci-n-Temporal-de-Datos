from pathlib import Path

def calcular_crc16(datos):
    crc = 0xFFFF
    polinomio = 0x1021

    for byte in datos:
        crc ^= byte << 8

        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ polinomio
            else:
                crc <<= 1

            crc &= 0xFFFF

    return crc


def guardar_crc(ruta_crc, valor_crc):
    ruta_archivo = Path(ruta_crc)
    ruta_archivo.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta_crc, "w", encoding="utf-8") as archivo:
        archivo.write(f"{valor_crc:04X}")


def leer_crc(ruta_crc):
    with open(ruta_crc, "r", encoding="utf-8") as archivo:
        contenido = archivo.read().strip()

    return int(contenido, 16)


def verificar_crc(datos, crc_esperado):
    crc_actual = calcular_crc16(datos)
    return crc_actual == crc_esperado, crc_actual