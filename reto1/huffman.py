import heapq
import itertools

def construir_arbol(texto: str):
    if texto == "":
        return {"valor": None, "frecuencia": 0, "izquierda": None, "derecha": None}
    frecuencias = {}
    for ch in texto:
        frecuencias[ch] = frecuencias.get(ch, 0) + 1
    if len(frecuencias) == 1:
        (unico_char, frec), = frecuencias.items()
        hoja = {"valor": unico_char, "frecuencia": frec, 
                "izquierda": None, "derecha": None}
        return {"valor": None, "frecuencia": frec,
                "izquierda": hoja, "derecha": None}
    contador = itertools.count()
    heap = []
    for ch, frec in frecuencias.items():
        nodo = {"valor": ch, "frecuencia": frec, "izquierda": None, "derecha": None}
        heapq.heappush(heap, (frec, next(contador), nodo))
    while len(heap) > 1:
        frec1, _, nodo1 = heapq.heappop(heap)
        frec2, _, nodo2 = heapq.heappop(heap)

        nuevo = {
            "valor": None,
            "frecuencia": frec1 + frec2,
            "izquierda": nodo1,
            "derecha": nodo2,
        }
        heapq.heappush(heap, (nuevo["frecuencia"], next(contador), nuevo))
    _, _, arbol = heap[0]
    return arbol

def construir_tabla(arbol: dict):
    tabla = {}

    def recorrer(nodo, codigo):
        if nodo is None:
            return
        if nodo["izquierda"] is None and nodo["derecha"] is None:
            tabla[nodo["valor"]] = codigo if codigo != "" else "0"
            return
        recorrer(nodo["izquierda"], codigo + "0")
        recorrer(nodo["derecha"], codigo + "1")
    recorrer(arbol, "")
    return tabla

def codificar(texto: str, tabla: dict):
    return "".join(tabla[ch] for ch in texto)

def decodificar(binario: str, arbol: dict):
    if binario == "":
        return ""
    resultado = []
    nodo_actual = arbol

    if arbol["izquierda"] is not None and arbol["derecha"] is None \
            and arbol["izquierda"]["valor"] is not None:
        valor = arbol["izquierda"]["valor"]
        return valor * len(binario)
    for bit in binario:
        if bit == "0":
            nodo_actual = nodo_actual["izquierda"]
        else:
            nodo_actual = nodo_actual["derecha"]

        if nodo_actual["izquierda"] is None and nodo_actual["derecha"] is None:
            resultado.append(nodo_actual["valor"])
            nodo_actual = arbol

    return "".join(resultado)