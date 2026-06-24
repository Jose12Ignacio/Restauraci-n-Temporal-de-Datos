from pathlib import Path
import json
from common.funciones import leer_texto, guardar_texto, leer_bytes, guardar_bytes, copiar_archivo
from common.formato import bytes_a_binario, binario_a_bytes, limpiar_espacios_binario
from reto1.compress import comprimir
from reto1.decompress import descomprimir
from reto1.huffman import construir_arbol, construir_tabla, codificar
from reto1.lzw import comprimir_lzw
from reto1.lz77 import comprimir_lz77
from reto1.lz78 import comprimir_lz78
from reto2.xor_cifrador import cifrar, descifrar
from reto2.xor_ataque import atacar
from reto3.crc import calcular_crc16, guardar_crc, leer_crc, verificar_crc
from reto3.injector import insertar_error_un_bit, insertar_error_burst
from reto3.correccion import corregir_con_crc_original, corregir_datos_segmentados

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


    # RETO 1: COMPRESIÓN Y DESCOMPRESIÓN
    def comprimir_archivo(self, algoritmo):
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje

        try:
            from common.funciones import leer_texto, guardar_texto
            from reto1.compress import comprimir
            import json

            texto = leer_texto(self.archivo_actual)
            if not all(ord(c) < 128 for c in texto):
                return "Error: El archivo contiene caracteres especiales (tildes, n, etc). Use solo ASCII de 7 bits."
            resultado = comprimir(texto, algoritmo.lower())
        

            ruta_salida = self.archivo_actual + ".reto1.json"
            guardar_texto(ruta_salida, json.dumps(resultado, indent=2, ensure_ascii=False))

            if algoritmo.lower() == "huffman":
                arbol = construir_arbol(texto)
                tabla = construir_tabla(arbol)
                bits = codificar(texto, tabla)
                ruta_bin = self.archivo_actual + ".reto1.bin"
                guardar_bytes(ruta_bin, bits.encode('ascii'))
                vista_previa = f"Bits comprimidos: {bits[:60]}..."
            elif algoritmo.lower() == "lzw":
                salida, _ = comprimir_lzw(texto)
                ruta_bin = self.archivo_actual + ".reto1.bin"
                guardar_bytes(ruta_bin, ' '.join(str(c) for c in salida).encode('ascii'))
                vista_previa = f"Códigos LZW: {salida[:10]}..."
            elif algoritmo.lower() == "lz77":
                ruta_bin = self.archivo_actual + ".reto1.bin"
                guardar_bytes(ruta_bin, json.dumps(resultado).encode('ascii'))
                vista_previa = "Algoritmo: LZ77 (compresión por tripletas offset-longitud-siguiente)"
            elif algoritmo.lower() == "lz78":
                ruta_bin = self.archivo_actual + ".reto1.bin"
                guardar_bytes(ruta_bin, json.dumps(resultado).encode('ascii'))
                vista_previa = "Algoritmo: LZ78 (compresión por diccionario incremental)"
            else:
                ruta_bin = self.archivo_actual + ".reto1.bin"
                guardar_bytes(ruta_bin, json.dumps(resultado).encode('ascii'))
                vista_previa = f"Algoritmo: {algoritmo.upper()}"

            return (f"{vista_previa}\n\n"
                    f"Archivo comprimido guardado en:\n{ruta_salida}\n"
                    f"Archivo binario guardado en:\n{ruta_bin}")

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
            return f"Error al dscifrar o descomprimir: {e}"

    
    # RETO 2: CIFRADO Y ATAQUES XOR
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
            if not all(ord(c) < 128 for c in texto):
                return "Error: El archivo contiene caracteres especiales (tildes, n, etc). Use solo ASCII de 7 bits."
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

            ruta_bin = self.archivo_actual + ".xor.bin"
            guardar_bytes(ruta_bin, datos_cifrados)

            return (f"Clave usada: {clave}\n"
                    f"Bits cifrados: {bits[:40]}...\n\n"
                    f"Archivo cifrado guardado en:\n{ruta_salida}\n"
                    f"Archivo binario guardado en:\n{ruta_bin}")

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
    
            if self.archivo_actual.endswith('.bin'):
                cifrado = leer_bytes(self.archivo_actual)
            else:
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
                        f"Confianza: {confianza:.0%}\n\n"
                        f"Texto recuperado:\n{texto_recuperado}")
            else:
                texto_recuperado = descifrar(cifrado, clave)
                info = (f"Clave usada: {clave}\n\n"
                        f"Texto descifrado:\n{texto_recuperado}")
    
            if self.archivo_actual.endswith('.bin'):
                ruta_salida = self.archivo_actual.replace(".bin", "") + ".dec.txt"
            else:
                ruta_salida = self.archivo_actual.replace(".json", "") + ".dec.txt"
            guardar_texto(ruta_salida, texto_recuperado)
    
            return info + f"\n\nGuardado en: {ruta_salida}"
    
        except ValueError as e:
            return f"Error de validación: {e}"
        except KeyError:
            return "El archivo no tiene el formato JSON esperado para Reto 2."
        except Exception as e:
            return f"Error al descifrar: {e}"

   
    # RETO 3: ARCHIVO CORRUPTO (SEGMENTACIÓN Y VERIFICACIÓN)
    def generar_crc(self):
        """
        Genera el archivo JSON estructurado por segmentos con sus respectivas
        sumatorias (CRC) correctas antes de ser corrompido, usando bloques de 8 bits.
        Muestra un extracto de los CRC generados originalmente.
        """
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje

        try:
            datos_bytes = leer_bytes(self.archivo_actual)
            if not datos_bytes:
                return "Error: El archivo seleccionado está vacío."

            segmentos = []
            extracto_pantalla = []
            
            # Procesar bloque por bloque (8 bits = 1 byte según la rúbrica)
            for idx, byte in enumerate(datos_bytes):
                bits_cadena = format(byte, "08b")
                crc_segmento = calcular_crc16(bytes([byte]))
                
                segmentos.append({
                    "id": idx + 1,
                    "bits": bits_cadena,
                    "checksum": crc_segmento  
                })
                
                if idx < 5:
                    extracto_pantalla.append(f"  • Bloque {idx+1} ('{chr(byte)}'): CRC 0x{crc_segmento:04X}")

            resultado = {
                "metadata": {
                    "algorithm": "crc-16",
                    "bits_por_segmento": 8
                },
                "data": segmentos
            }

            ruta_salida = self.archivo_actual + ".reto3.json"
            guardar_texto(ruta_salida, json.dumps(resultado, indent=2))
            
            extracto_texto = '\n'.join(extracto_pantalla)
            msg_exito = (
                f" Estructura de verificación generada con éxito en:\n{ruta_salida}\n\n"
                f" Extracto de Sumatorias Originales (Primeros bloques):\n"
                f"{extracto_texto}\n"
                f"  ... (+ {len(datos_bytes) - min(len(datos_bytes), 5)} bloques guardados en el JSON)."
            )
            return msg_exito

        except Exception as e:
            return f"Error al generar la estructura de verificación: {e}"

    def corromper_archivo(self, tipo_error):
        """
        Lógica Avanzada: Convierte TODO el archivo a una tira continua de bytes
        para que el Burst Error pueda propagarse libremente a través de múltiples IDs (bloques).
        """
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje

        if not self.archivo_actual.endswith('.json'):
            return "Error: Para inyectar ruido por segmentos debe seleccionar un archivo .json estructurado."

        try:
            contenido = leer_texto(self.archivo_actual)
            datos_json = json.loads(contenido)
            
            if "data" not in datos_json:
                return "Error: El JSON no contiene la sección de segmentos ('data')."

            segmentos = datos_json["data"]
            
            # 1. Reconstruir TODOS los bytes del archivo en un solo array continuo
            bytes_completos = bytearray()
            for seg in segmentos:
                bytes_completos.extend(binario_a_bytes(seg["bits"]))
            
            # 2. Aplicar el error sobre el archivo completo
            if tipo_error == "Single-bit error":
                # Altera solo 1 bit en todo el archivo (afectará a 1 ID)
                datos_corruptos, info = insertar_error_un_bit(bytes(bytes_completos))
                
                # Averiguar cuál ID se vio afectado mapeando la posición del byte
                id_afectado = info["indice_byte"] + 1
                msg_detalle = f"Bit invertido en la posición {info['posicion_bit']} del bloque ID {id_afectado}."
            else:
                # Burst error: Definimos una ráfaga larga (ej: 16 bits = 2 bytes completos de daño secuencial)
                # Esto garantiza que destruirá bits que cruzaran entre 2 o 3 bloques seguidos
                datos_corruptos, info = insertar_error_burst(bytes(bytes_completos), cantidad_bits=16)
                
                # Averiguar el rango de IDs afectados
                id_inicio = (info["inicio_bit"] // 8) + 1
                id_fin = ((info["inicio_bit"] + info["cantidad_bits"] - 1) // 8) + 1
                
                if id_inicio == id_fin:
                    msg_detalle = f"Ráfaga de error aplicada en el bloque ID {id_inicio} (No logró cruzar la frontera del byte)."
                else:
                    msg_detalle = f" Ráfaga destructiva propagada secuencialmente a través de los bloques desde el ID {id_inicio} hasta el ID {id_fin}."

            # 3. Repartir los bytes ya corrompidos de vuelta a cada bloque del JSON
            for idx, seg in enumerate(segmentos):
                byte_modificado = datos_corruptos[idx]
                seg["bits"] = format(byte_modificado, "08b")

            # --- LÓGICA DE EXPORTACIÓN DEL ARCHIVO .BIN PARALELO ---
            ruta_bin_salida = self.archivo_actual.replace(".json", "") + ".corrupto.bin"
            guardar_bytes(ruta_bin_salida, datos_corruptos)
            # ---------------------------------------------------------------------

            # Guardar el JSON modificado para el torneo
            ruta_salida_json = self.archivo_actual.replace(".json", "") + ".corrupto.json"
            guardar_texto(ruta_salida_json, json.dumps(datos_json, indent=2))

            return (
                f" Ruido temporal inyectado ({tipo_error}).\n{msg_detalle}\n\n"
                f" Archivo JSON (Torneo) guardado en:\n{ruta_salida_json}\n\n"
                f" Archivo Binario Puro (.bin) guardado en:\n{ruta_bin_salida}"
            )

        except Exception as e:
            return f"Error al corromper el segmento: {e}"

    def verificar_crc(self):
        """
        Analiza cada segmento del JSON comparando sus bits actuales contra su sumatoria esperada.
        Muestra detalladamente los CRC originales vs corruptos en caso de fallo.
        """
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje

        if not self.archivo_actual.endswith('.json'):
            return "Error: Debe seleccionar un archivo .json de Reto 3 para verificar integridad."

        try:
            contenido = leer_texto(self.archivo_actual)
            datos_json = json.loads(contenido)
            
            segmentos = datos_json.get("data", [])
            if not segmentos:
                return "Error: Estructura de segmentos no encontrada en el JSON."

            bloques_corruptos_info = []
            for seg in segmentos:
                datos_bytes = binario_a_bytes(seg["bits"])
                crc_esperado = seg.get("checksum", seg.get("residuo_crc", 0))
                
                crc_actual = calcular_crc16(datos_bytes)
                if crc_actual != crc_esperado:
                    bloques_corruptos_info.append(
                        f"  -> Bloque ID {seg['id']}:\n"
                        f"     [CRC Original Esperado]: 0x{crc_esperado:04X} ({crc_esperado})\n"
                        f"     [CRC Corrupto Actual ]: 0x{crc_actual:04X} ({crc_actual})"
                    )

            if not bloques_corruptos_info:
                return "Integridad Perfecta: Todos los segmentos coinciden con sus sumatorias correctas."
            else:
                detalle_bloques = '\n'.join(bloques_corruptos_info)
                reporte_fallo = (
                    f" Inconsistencia Detectada en la Línea Temporal:\n"
                    f"==================================================\n"
                    f"{detalle_bloques}\n"
                    f"=================================================="
                )
                return reporte_fallo

        except Exception as e:
            return f"Error al verificar la integridad: {e}"

    def corregir_archivo_con_crc(self, ruta_crc_ignorada=None, max_bits_rafaga=16):
        """
        Lógica del Reto 3 adaptada al Torneo: Lee el archivo JSON por segmentos, invoca la 
        función por bloques de correccion.py, genera el archivo limpio (.txt) y muestra
        el mensaje de texto normal recuperado en el reporte.
        """
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje

        if not self.archivo_actual.endswith('.json'):
            return "Error: Para corregir por bloques debe cargar el archivo .json corrupto del torneo."

        try:
            contenido = leer_texto(self.archivo_actual)
            datos_json = json.loads(contenido)
            
            bits_por_segmento = datos_json.get("metadata", {}).get("bits_por_segmento", 8)
            segmentos = datos_json.get("data", [])
            
            if not segmentos:
                return "Error: No se encontró la lista de segmentos ('data') en el archivo."

            datos_sanos, sanos, corregidos, fallidos = corregir_datos_segmentados(segmentos, max_bits_rafaga)

            ruta_salida = self.archivo_actual.replace(".json", "") + ".restaurado.txt"
            
            try:
                texto_limpio = datos_sanos.decode('utf-8')
            except UnicodeDecodeError:
                texto_limpio = datos_sanos.decode('latin-1')

            guardar_texto(ruta_salida, texto_limpio)

            reporte = (
                f"--- Reporte del Torneo (Reto 3) ---\n"
                f"Tamaño de segmento: {bits_por_segmento} bits.\n"
                f"Bloques originales intactos: {sanos}\n"
                f"Bloques reparados por inversión: {corregidos}\n"
                f"Bloques no recuperables: {fallidos}\n\n"
                f"MENSAJE RECUPERADO:\n"
                f"========================================\n"
                f"{texto_limpio}\n"
                f"========================================\n\n"
                f"Resultado exportado a: {ruta_salida}"
            )
            return reporte

        except Exception as e:
            return f"Error crítico durante el proceso de restauración: {e}"

    # =========================================================================
    # FUNCIÓN DE ANÁLISIS DE ENTRADA (DETECCIÓN DE FORMATO)
    # =========================================================================
    def cargar_y_procesar_json(self):
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje

        if not self.archivo_actual.endswith('.json'):
            return "Error: El archivo seleccionado no tiene extensión .json"

        try:
            contenido = leer_texto(self.archivo_actual)
            datos_json = json.loads(contenido)
            
            reporte = ["--- Información del Archivo JSON ---"]
            
            if "compresion" in datos_json:
                reporte.append("\n[Reto 1: Compresión Detectada]")
                for idx, capa in enumerate(datos_json["compresion"]):
                    alg = capa.get("algoritmo", "Desconocido")
                    reporte.append(f"  Capa {idx + 1}: Algoritmo: {alg}")
                    if "estructura" in capa:
                        reporte.append("  -> Metadata estructural presente (Árbol/Tabla/Tripletas Válida)")
            
            elif "ciphertext" in datos_json:
                reporte.append("\n[Reto 2: Encripción Detectada]")
                metadata = datos_json.get("metadata", {})
                bits_segmento = metadata.get("bits_por_segmento", "No especificado")
                reporte.append(f"  Bits por segmento: {bits_segmento}")
                reporte.append(f"  Cantidad de bloques cifrados: {len(datos_json['ciphertext'])}")

            elif "data" in datos_json or "algoritmo" in datos_json or "polinomio" in datos_json:
                reporte.append("\n[Reto 3: Verificación/Corrupción Detectada]")
                metadata = datos_json.get("metadata", {})
                algo = datos_json.get("algoritmo", metadata.get("algorithm", "CRC-16"))
                bits_seg = datos_json.get("bits_por_segmento", metadata.get("bits_por_segmento", 8))
                
                reporte.append(f"  Algoritmo de control: {algo}")
                reporte.append(f"  Tamaño del segmento usado: {bits_seg} bits")
                
                segmentos = datos_json.get("data", [])
                if segmentos:
                    reporte.append(f"  Cantidad de segmentos a procesar: {len(segmentos)}")
                elif "verificacion" in datos_json:
                    reporte.append("  Estructura de transmisión única detectada.")

            else:
                reporte.append("\nFormato JSON desconocido o despiste del torneo.")

            return "\n".join(reporte)

        except json.JSONDecodeError:
            return "Error: El archivo no es un JSON válido o está corrupto estructuralmente."
        except Exception as e:
            return f"Ocurrió un error al procesar el JSON: {str(e)}"