from common.funciones import leer_bytes, guardar_bytes

#Se definen las validaciones para clave y mensaje
def validarClave (clave: str):

    if not clave:
        raise ValueError ("La clave no puede estar vacía")
    
    if len(clave) > 10:
        raise ValueError (
            f"La clabe no puede tener mas de 10 caracteres"
            f"(longitud de clave recibida: {len(clave)})"
        )


def validarMensaje (mensaje_len: int, clave_len: int):

    minimo = 2 * clave_len
    if mensaje_len < minimo:
        raise ValueError (
            f"El mensaje debe tener al menos {minimo} caracteres"
            f"(2 * longitud de clave = 2 * {clave_len})"
            f"Longitud actual: {mensaje_len}"
        )
    
#Creacion de la funcion XOR
def xor_con_clave (datos: bytes, clave: bytes):

    n = len(clave)
    return bytes (b ^ clave [i % n] for i, b in enumerate(datos))

#se define una API publica
def cifrar (texto: str, clave: str):

    validarClave(clave)
    validarMensaje(len(texto), len(clave))

    datos = texto.encode("utf-8")
    clave_bytes = clave.encode("utf-8")
    return xor_con_clave(datos, clave_bytes)

def descifrar (datos: bytes, clave: str):

    validarClave(clave)

    clave_bytes = clave.encode ("utf-8")
    texto_bytes = xor_con_clave(datos, clave_bytes)
    return texto_bytes.decode("utf-8")

def guardar_cifrado (datos: bytes, ruta: str):

    guardar_bytes (ruta, datos)

def cargar_cifrado (ruta: str):

    return leer_bytes(ruta)
