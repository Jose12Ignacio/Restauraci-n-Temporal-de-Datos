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

    def comprimir_archivo(self, algoritmo):
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje

        return f"Se aplicará compresión con {algoritmo} al archivo:\n{self.archivo_actual}"

    def descomprimir_archivo(self, algoritmo):
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje

        return f"Se aplicará descompresión con {algoritmo} al archivo:\n{self.archivo_actual}"

    def cifrar_xor(self, clave):
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje

        if not clave:
            return "Debe ingresar una clave para cifrar con XOR."

        return f"Se cifrará el archivo con XOR usando la clave: {clave}"

    def descifrar_xor(self, clave):
        valido, mensaje = self.validar_archivo()
        if not valido:
            return mensaje

        if not clave:
            return "Debe ingresar una clave para descifrar con XOR."

        return f"Se descifrará el archivo con XOR usando la clave: {clave}"

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