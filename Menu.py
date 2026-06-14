from pathlib import Path

from common.funciones import leer_texto, guardar_texto, leer_bytes, guardar_bytes
from common.formato import bytes_a_binario, binario_a_bytes, limpiar_espacios_binario
from reto1.compress import comprimir
from reto1.decompress import descomprimir
from reto2.xor_cifrador import cifrar, descifrar
from reto2.xor_ataque import atacar
import json
from common.funciones import leer_bytes, guardar_bytes, copiar_archivo
from reto3.crc import calcular_crc16, guardar_crc, leer_crc, verificar_crc
from reto3.injector import insertar_error_un_bit, insertar_error_burst
from reto3.correccion import corregir_con_crc_original, recuperar_texto_aproximado

class MenuLogico:
    def __init__(self):
        self.archivo_actual = None

    def seleccionar_archivo(self, ruta):
        self.archivo_actual = ruta
        return f"Archivo seleccionado: {ruta}"
    def limpiar_busqueda(self):
        self.archivo_actual = None
        return "Búsqueda limpiada. Ya no hay archivo seleccionado."

    def validar_archivo(self):
        if not self.archivo_actual:
            return False, "Primero debe seleccionar un archivo."
        return True, "Archivo válido."

    #RETO 1
    def comprimir_archivo(self, algoritmo):
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje

        try:
            from common.funciones import leer_texto, guardar_texto
            from reto1.compress import comprimir
            import json

            texto = leer_texto(self.archivo_actual)
            resultado = comprimir(texto, algoritmo.lower())

            ruta_salida = self.archivo_actual + ".reto1.json"
            guardar_texto(ruta_salida, json.dumps(resultado, indent=2, ensure_ascii=False))

            return f"Archivo comprimido guardado en:\n{ruta_salida}"

        except Exception as e:
            return f"Error al comprimir: {e}"
        
    def descomprimir_archivo(self, algoritmo):
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje

        try:
            from common.funciones import leer_texto, guardar_texto
            from reto1.decompress import descomprimir
            import json

            contenido = leer_texto(self.archivo_actual)
            json_data = json.loads(contenido)
            texto_recuperado = descomprimir(json_data, algoritmo)

            ruta_salida = self.archivo_actual.replace(".reto1.json", "") + ".dec.txt"
            guardar_texto(ruta_salida, texto_recuperado)

            return f"Texto descomprimido:\n{texto_recuperado}\n\nGuardado en: {ruta_salida}"

        except Exception as e:
            return f"Error al descomprimir: {e}"


    #RETO 2
    def cifrar_xor(self, clave: str) -> str:
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje
        if not clave:
            return "Debe ingresar una clave para cifrar con XOR."

        try:
            from common.funciones import leer_texto, guardar_texto
            from common.formato import bytes_a_binario
            from reto2.xor_cifrador import cifrar
            import json

            texto = leer_texto(self.archivo_actual)
            datos_cifrados = cifrar(texto, clave)

            bits = bytes_a_binario(datos_cifrados).replace(" ", "")

            resultado = {
                "metadata": {
                    "encoding": "binario",
                    "method": "XOR",
                    "bits_por_segmento": 8,
                    "descripcion": "Texto cifrado usando XOR con clave repetida"
                },
                "ciphertext": [bits]
            }

            ruta_salida = self.archivo_actual + ".json"
            guardar_texto(ruta_salida, json.dumps(resultado, indent=2))

            return f"Archivo cifrado guardado en:\n{ruta_salida}"

        except ValueError as e:
            return f"Error de validación: {e}"
        except Exception as e:
            return f"Error al cifrar: {e}"
    
    def descifrar_xor(self, clave: str) -> str:
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje
    
        try:
            from common.funciones import leer_texto, guardar_texto
            from common.formato import binario_a_bytes, limpiar_espacios_binario
            from reto2.xor_cifrador import descifrar
            from reto2.xor_ataque import atacar
            import json
    
            contenido = leer_texto(self.archivo_actual)
            datos = json.loads(contenido)
            bits = limpiar_espacios_binario(datos["ciphertext"][0])
            cifrado = binario_a_bytes(bits)
    
            if clave == "":
                resultado = atacar(cifrado)
                texto_recuperado = resultado.texto
                confianza = resultado.confianza
                clave_encontrada = resultado.clave
                info = (f"Ataque automático completado.\n"
                        f"Clave encontrada: {clave_encontrada}\n"
                        f"Confianza: {confianza:.0%}\n"
                        f"Texto recuperado:\n{texto_recuperado}")
            else:
                texto_recuperado = descifrar(cifrado, clave)
                info = f"Texto descifrado:\n{texto_recuperado}"
    
            ruta_salida = self.archivo_actual.replace(".json", "") + ".dec.txt"
            guardar_texto(ruta_salida, texto_recuperado)
    
            return info + f"\n\nGuardado en: {ruta_salida}"
    
        except ValueError as e:
            return f"Error de validación: {e}"
        except KeyError:
            return "El archivo no tiene el formato JSON esperado para Reto 2."
        except Exception as e:
            return f"Error al descifrar: {e}"


    #RETO 3
    def generar_crc(self):
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje

        archivo = Path(self.archivo_actual)

        if "_corrupto" in archivo.stem:
            return (
                "Advertencia: está intentando generar CRC de un archivo corrupto.\n"
                "Para el reto, normalmente se debe generar el CRC del archivo original "
                "antes de corromperlo."
            )

        datos = leer_bytes(self.archivo_actual)
        crc = calcular_crc16(datos)

        ruta_crc = f"salida/{archivo.stem}.crc"

        guardar_crc(ruta_crc, crc)

        return (
            f"CRC generado correctamente.\n"
            f"Archivo analizado:\n{self.archivo_actual}\n\n"
            f"Archivo CRC guardado en:\n{ruta_crc}\n\n"
            f"Valor CRC: {crc:04X}"
        )


    def verificar_crc(self):
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje

        archivo = Path(self.archivo_actual)
        nombre_base = archivo.stem

        if nombre_base.endswith("_corrupto"):
            nombre_base = nombre_base.replace("_corrupto", "")

        ruta_crc = f"salida/{nombre_base}.crc"

        if not Path(ruta_crc).exists():
            return (
                f"No se encontró el archivo CRC esperado.\n"
                f"Primero debe generar el CRC del archivo original.\n\n"
                f"Ruta esperada:\n{ruta_crc}"
            )

        datos = leer_bytes(self.archivo_actual)
        crc_esperado = leer_crc(ruta_crc)

        es_valido, crc_actual = verificar_crc(datos, crc_esperado)

        if es_valido:
            return (
                f"El archivo es válido.\n"
                f"No se detectaron errores.\n\n"
                f"CRC esperado: {crc_esperado:04X}\n"
                f"CRC actual: {crc_actual:04X}"
            )

        return (
            f"El archivo está corrupto o fue modificado.\n\n"
            f"CRC esperado: {crc_esperado:04X}\n"
            f"CRC actual: {crc_actual:04X}"
        )


    def corromper_archivo(self, tipo_error):
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje

        datos = leer_bytes(self.archivo_actual)

        if tipo_error == "Single-bit error":
            datos_corruptos, info_error = insertar_error_un_bit(datos)

        elif tipo_error == "Burst error":
            datos_corruptos, info_error = insertar_error_burst(
                datos,
                cantidad_bits=8
            )

        else:
            return "Tipo de error no reconocido."

        archivo = Path(self.archivo_actual)
        nombre_base = archivo.stem.replace("_corrupto", "")
        ruta_salida = f"salida/{nombre_base}_corrupto.bin"

        guardar_bytes(ruta_salida, datos_corruptos)

        self.archivo_actual = ruta_salida

        return (
            f"Archivo corrupto generado correctamente.\n"
            f"Archivo original:\n{archivo}\n\n"
            f"Archivo corrupto guardado en:\n{ruta_salida}\n\n"
            f"Información del error:\n{info_error}\n\n"
            f"Ahora el archivo seleccionado es el corrupto."
        )


    def corregir_archivo_con_crc(self, ruta_crc, max_bits_rafaga=16):
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje

        if not ruta_crc:
            return "Debe seleccionar el archivo CRC original."

        if not Path(ruta_crc).exists():
            return "El archivo CRC indicado no existe."

        datos_corruptos = leer_bytes(self.archivo_actual)
        crc_original = leer_crc(ruta_crc)

        datos_corregidos, info_correccion = corregir_con_crc_original(
            datos_corruptos,
            crc_original,
            max_bits_rafaga=max_bits_rafaga
        )

        if not info_correccion["corregido"]:
            return (
                "No se pudo corregir el archivo automáticamente.\n\n"
                f"Información:\n{info_correccion}"
            )

        archivo = Path(self.archivo_actual)
        nombre_base = archivo.stem.replace("_corrupto", "")

        try:
            texto = datos_corregidos.decode("utf-8")
            ruta_salida = f"salida/{nombre_base}_recuperado.txt"

            with open(ruta_salida, "w", encoding="utf-8") as archivo_salida:
                archivo_salida.write(texto)

        except UnicodeDecodeError:
            ruta_salida = f"salida/{nombre_base}_recuperado.bin"
            guardar_bytes(ruta_salida, datos_corregidos)

        self.archivo_actual = ruta_salida

        return (
            f"Archivo corregido correctamente usando el CRC original.\n\n"
            f"Archivo corrupto analizado:\n{archivo}\n\n"
            f"CRC utilizado:\n{ruta_crc}\n\n"
            f"Archivo recuperado guardado en:\n{ruta_salida}\n\n"
            f"Información de corrección:\n{info_correccion}\n\n"
            f"Ahora el archivo seleccionado es el archivo recuperado."
        )


    def recuperar_sin_crc(self):
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje

        datos_corruptos = leer_bytes(self.archivo_actual)
        texto_recuperado, info = recuperar_texto_aproximado(datos_corruptos)

        archivo = Path(self.archivo_actual)
        nombre_base = archivo.stem.replace("_corrupto", "")

        ruta_salida = f"salida/{nombre_base}_recuperado_aproximado.txt"

        with open(ruta_salida, "w", encoding="utf-8") as archivo_salida:
            archivo_salida.write(texto_recuperado)

        self.archivo_actual = ruta_salida

        return (
            f"Recuperación aproximada realizada.\n\n"
            f"Archivo recuperado guardado en:\n{ruta_salida}\n\n"
            f"Información:\n{info}\n\n"
            f"Advertencia: esta recuperación no garantiza exactitud porque no usa CRC original."
        )


    def guardar_como(self, ruta_destino):
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje

        if not ruta_destino:
            return "No se seleccionó una ruta de destino."

        copiar_archivo(self.archivo_actual, ruta_destino)

        return (
            f"Archivo guardado correctamente.\n\n"
            f"Archivo original:\n{self.archivo_actual}\n\n"
            f"Archivo guardado en:\n{ruta_destino}"
        )
