from common.funciones import guardar_bytes, leer_bytes, guardar_texto
from reto3.crc import calcular_crc16, guardar_crc, leer_crc, verificar_crc
from reto3.injector import insertar_error_un_bit
from reto3.correccion import intentar_corregir_un_bit


def main():
    datos_originales = b"Hola mundo. Este es un mensaje de prueba para el reto 3."

    print("Datos originales:")
    print(datos_originales.decode("utf-8"))

    crc_original = calcular_crc16(datos_originales)
    guardar_crc("salida/mensaje.crc", crc_original)

    print("\nCRC original:")
    print(hex(crc_original))

    datos_corruptos, info_error = insertar_error_un_bit(datos_originales)

    guardar_bytes("salida/mensaje_corrupto.bin", datos_corruptos)

    print("\nError insertado:")
    print(info_error)

    crc_leido = leer_crc("salida/mensaje.crc")

    es_valido, crc_actual = verificar_crc(datos_corruptos, crc_leido)

    print("\n¿El archivo corrupto es válido?")
    print(es_valido)

    print("\nCRC actual:")
    print(hex(crc_actual))

    datos_corregidos, info_correccion = intentar_corregir_un_bit(datos_corruptos, crc_leido)

    print("\nResultado de corrección:")
    print(info_correccion)

    print("\nTexto recuperado:")
    print(datos_corregidos.decode("utf-8", errors="replace"))

    guardar_texto(
        "salida/mensaje_recuperado.txt",
        datos_corregidos.decode("utf-8", errors="replace")
    )


if __name__ == "__main__":
    main()