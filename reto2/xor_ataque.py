from collections import namedtuple
from typing import List, Tuple, Optional
from reto2.longitud_clave import estimar_long_clave


#se da el resultado
ResultadoAtaque = namedtuple("ResultadoAtaque", ["clave", "texto", "confianza", "longitud_clave"])


#constantes de frecuencia

chars_frecuentes = "eEaAoOsSnNiIrRlLtTdDuUcCmMpPgGbBfFyYhHvVqQjJzZxXkKwW"

chars_legibles = set(
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789"
    " .,;:!?-_()[]{}'\"\n\t"
    "áéíóúüñÁÉÍÓÚÜÑ" 
)

#longitudes para probar el ataque
mejores_longitudes = 5


#ataque por cada columna
def byte_clave_columna(columna: bytes):

    if not columna:
        return 0
    
    #se cuenta la frecuencia de los bytes en la columna
    frecuencias = [0] * 256
    for b in columna:
        frecuencias[b] += 1

    byte_frecuente = max(range(256), key=lambda i: frecuencias[i])

    #se prueba para cada caracter frecuente
    for char in chars_frecuentes:
        candidato = byte_frecuente ^ ord(char)

        #verifica que el candidato sea legible con sus caracteres
        resultado = [b ^ candidato for b in columna]
        legibles = sum(1 for r in resultado if chr(r) in chars_legibles)
        if legibles / len(columna) > 0.6:
            return candidato
        

    #usa el espacio de manera directa
    return byte_frecuente ^ ord(" ")

def recuperar_clave(cifrado: bytes, longitud: int):
    #alaque a la columna cifrada y construccion de clave
    columnas = [cifrado[i::longitud] for i in range(longitud)]
    return bytes(byte_clave_columna(col) for col in columnas)

#aplicar clave
def aplicar_xor(datos: bytes, clave: bytes):
    n = len(clave)
    return bytes(b ^ clave[i % n] for i, b in enumerate(datos))


#evalua la legibilidad
def puntuacion_legibilidad(texto: bytes):
    if not texto:
        return 0.0
    try:
        cadena = texto.decode("utf-8")
    except UnicodeDecodeError:
        legibles = sum(1 for b in texto if 32 <= b < 127 or b in (9, 10, 13))
        return legibles / len(texto) 
    legibles = sum(1 for c in cadena if c in chars_legibles)
    return legibles / len(cadena)
    

#funcion principal
def atacar(cifrado: bytes, max_long: int = mejores_longitudes):

    if not cifrado:
        raise ValueError("el cifrado no puede estar vacio")
    
    candidatos = estimar_long_clave(cifrado)
    mejores = candidatos[:max_long]

    mejor_resultado = None

    for longitud, score_ic in mejores:
        clave_bytes = recuperar_clave(cifrado, longitud)
        texto_bytes = aplicar_xor(cifrado, clave_bytes)
        confianza = puntuacion_legibilidad(texto_bytes)

        try:
            texto_str = texto_bytes.decode("utf-8")

        except UnicodeDecodeError:
            texto_str = texto_bytes.decode("latin-1")

        
        try:
            clave_str = clave_bytes.decode("utf-8")

        except UnicodeDecodeError:
            clave_str = clave_bytes.decode("latin-1")

        resultado = ResultadoAtaque(
            clave=clave_str,
            texto=texto_str,
            confianza=confianza,
            longitud_clave=longitud,
        )

        if mejor_resultado is None or confianza > mejor_resultado.confianza:
            mejor_resultado = resultado

        
    return mejor_resultado
