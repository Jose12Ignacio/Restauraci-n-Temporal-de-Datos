
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

        return f"Se generará CRC/checksum para:\n{self.archivo_actual}"

    def verificar_crc(self):
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje

        return f"Se verificará integridad del archivo:\n{self.archivo_actual}"

    def corromper_archivo(self, tipo_error):
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje

        return f"Se introducirá un error tipo {tipo_error} en:\n{self.archivo_actual}"
    
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
    
    def descomprimir_archivos(self, algoritmo):
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
        

    #cifrar_xor
    def cifrar_xor(self, clave: str) -> str:
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje
        if not clave:
            return "Debe ingresar una clave para cifrar con XOR"

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
    #descifrar_xor    
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
            return "El archivo no tiene el formato JSON esperado para Reto 2"
        except Exception as e:
            return f"Error al descifrar: {e}"
