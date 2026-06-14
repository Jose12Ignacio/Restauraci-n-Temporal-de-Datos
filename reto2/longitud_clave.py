from typing import List, Tuple

IC_REFERENCIA = 0.0667

def indice_coincidencia (datos: bytes):

    n = len(datos)
    if n < 2:
        return 0.0
    
    frecuencias = [0] * 256
    for b in datos:
        frecuencias [b] += 1

    numerador = sum(f* (f - 1) for f in frecuencias)
    denominador = n * (n - 1)
    return numerador / denominador

def ic_promedio(cifrado: bytes, longitud: int):

    columnas = [cifrado [i::longitud] for i in range (longitud)]
    ics = [indice_coincidencia(col) for col in columnas if len(col) >= 2]

    if not ics:
        return 0.0
    return sum(ics) / len(ics)

def estimar_long_clave(cifrado: bytes, max_long: int = 10):
    
    max_long = min(max_long, 10)  #restringe la clave a 10 o menos
    max_long = min(max_long, len(cifrado) // 2)  #suficientes datos necesarios
    max_long = max(max_long, 1)

    resultados: List[Tuple[int, float]] = []
    for longitud in range(1, max_long + 1):
        score = ic_promedio(cifrado, longitud)
        resultados.append((longitud, score))

    
    #orden por score descendente, con IC mas alto una long mas probable
    resultados.sort(key=lambda x: x[1], reverse=True)
    return resultados
