import unittest
from reto3.crc import calcular_crc16, guardar_crc, leer_crc, verificar_crc
from reto3.injector import insertar_error_un_bit, insertar_error_burst, invertir_bit
from reto3.correccion import (
    invertir_bit_en_posicion,
    invertir_rango_bits,
    intentar_corregir_un_bit,
    intentar_corregir_burst,
    corregir_con_crc_original,
    corregir_datos_segmentados,
)
import tempfile
import os


class TestCRC16(unittest.TestCase):

    def test_crc_devuelve_entero(self):
        """calcular_crc16 debe devolver un entero."""
        resultado = calcular_crc16(b"hola")
        self.assertIsInstance(resultado, int)

    def test_crc_mismo_dato_mismo_resultado(self):
        """El mismo dato siempre debe producir el mismo CRC."""
        datos = b"datos de prueba"
        self.assertEqual(calcular_crc16(datos), calcular_crc16(datos))

    def test_crc_rango_valido(self):
        """El CRC-16 debe estar en el rango [0x0000, 0xFFFF]."""
        crc = calcular_crc16(b"test")
        self.assertGreaterEqual(crc, 0x0000)
        self.assertLessEqual(crc, 0xFFFF)

    def test_crc_datos_distintos_dan_crc_distinto(self):
        """Datos diferentes deben (casi siempre) producir CRC diferente."""
        crc1 = calcular_crc16(b"dato uno")
        crc2 = calcular_crc16(b"dato dos")
        self.assertNotEqual(crc1, crc2)

    def test_crc_datos_vacios(self):
        """calcular_crc16 de bytes vacíos no debe explotar."""
        resultado = calcular_crc16(b"")
        self.assertIsInstance(resultado, int)

    def test_verificar_crc_dato_integro(self):
        """verificar_crc devuelve True cuando los datos no fueron alterados."""
        datos = b"mensaje original"
        crc = calcular_crc16(datos)
        es_valido, _ = verificar_crc(datos, crc)
        self.assertTrue(es_valido)

    def test_verificar_crc_dato_corrupto(self):
        """verificar_crc devuelve False cuando los datos fueron alterados."""
        datos = b"mensaje original"
        crc = calcular_crc16(datos)
        datos_corruptos = bytearray(datos)
        datos_corruptos[0] ^= 0xFF
        es_valido, _ = verificar_crc(bytes(datos_corruptos), crc)
        self.assertFalse(es_valido)

    def test_guardar_y_leer_crc(self):
        """Guardar y leer un CRC debe devolver el mismo valor."""
        datos = b"guardar y leer"
        crc_original = calcular_crc16(datos)
        with tempfile.NamedTemporaryFile(suffix=".crc", delete=False, mode="w") as f:
            ruta = f.name
        try:
            guardar_crc(ruta, crc_original)
            crc_leido = leer_crc(ruta)
            self.assertEqual(crc_original, crc_leido)
        finally:
            os.unlink(ruta)


class TestInjector(unittest.TestCase):

    def test_invertir_bit_cambia_bit(self):
        """invertir_bit debe cambiar exactamente el bit indicado."""
        byte_original = 0b10101010
        byte_invertido = invertir_bit(byte_original, 0)
        self.assertEqual(byte_invertido, 0b10101011)

    def test_invertir_bit_dos_veces_restaura(self):
        """Invertir el mismo bit dos veces devuelve el byte original."""
        byte_original = 0b11001100
        intermedio = invertir_bit(byte_original, 3)
        restaurado = invertir_bit(intermedio, 3)
        self.assertEqual(restaurado, byte_original)

    def test_insertar_error_un_bit_cambia_datos(self):
        """El resultado de insertar un error de bit debe ser diferente al original."""
        datos = b"hola mundo de prueba"
        corruptos, info = insertar_error_un_bit(datos)
        self.assertNotEqual(datos, corruptos)

    def test_insertar_error_un_bit_misma_longitud(self):
        """Insertar error de un bit no debe cambiar la longitud."""
        datos = b"hola mundo"
        corruptos, _ = insertar_error_un_bit(datos)
        self.assertEqual(len(datos), len(corruptos))

    def test_insertar_error_un_bit_info_correcta(self):
        """El diccionario de info debe tener las claves esperadas."""
        datos = b"datos de prueba"
        _, info = insertar_error_un_bit(datos)
        self.assertIn("tipo", info)
        self.assertIn("indice_byte", info)
        self.assertIn("posicion_bit", info)
        self.assertEqual(info["tipo"], "single-bit")

    def test_insertar_error_un_bit_datos_vacios_lanza_error(self):
        """insertar_error_un_bit con datos vacíos debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            insertar_error_un_bit(b"")

    def test_insertar_error_burst_cambia_datos(self):
        """El resultado de insertar burst debe ser diferente al original."""
        datos = b"hola mundo de prueba burst"
        corruptos, info = insertar_error_burst(datos, cantidad_bits=4)
        self.assertNotEqual(datos, corruptos)

    def test_insertar_error_burst_misma_longitud(self):
        """Insertar burst no debe cambiar la longitud."""
        datos = b"longitud igual tras burst"
        corruptos, _ = insertar_error_burst(datos, cantidad_bits=4)
        self.assertEqual(len(datos), len(corruptos))

    def test_insertar_error_burst_info_correcta(self):
        """El diccionario de info del burst debe tener las claves esperadas."""
        datos = b"burst info test aqui"
        _, info = insertar_error_burst(datos, cantidad_bits=4)
        self.assertIn("tipo", info)
        self.assertIn("inicio_bit", info)
        self.assertIn("cantidad_bits", info)
        self.assertEqual(info["tipo"], "burst")

    def test_insertar_error_burst_datos_vacios_lanza_error(self):
        """insertar_error_burst con datos vacíos debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            insertar_error_burst(b"", cantidad_bits=4)

    def test_insertar_error_posicion_especifica(self):
        """Insertar error en posición fija debe ser determinista."""
        datos = b"determinista"
        c1, _ = insertar_error_un_bit(datos, indice_byte=0, posicion_bit=0)
        c2, _ = insertar_error_un_bit(datos, indice_byte=0, posicion_bit=0)
        self.assertEqual(c1, c2)


class TestCorreccion(unittest.TestCase):

    def test_invertir_bit_en_posicion_funciona(self):
        """Invertir bit en posición global debe cambiar exactamente ese bit."""
        datos = bytes([0b00000000])
        resultado = invertir_bit_en_posicion(datos, 0)
        self.assertEqual(resultado, bytes([0b00000001]))

    def test_invertir_bit_en_posicion_dos_veces_restaura(self):
        """Invertir el mismo bit dos veces restaura los datos originales."""
        datos = b"hola"
        intermedio = invertir_bit_en_posicion(datos, 5)
        restaurado = invertir_bit_en_posicion(intermedio, 5)
        self.assertEqual(restaurado, datos)

    def test_corregir_un_bit_recupera_datos(self):
        """intentar_corregir_un_bit debe recuperar los datos originales."""
        datos = b"mensaje corregible con un bit"
        crc = calcular_crc16(datos)
        corruptos, _ = insertar_error_un_bit(datos)
        corregidos, info = intentar_corregir_un_bit(corruptos, crc)
        self.assertTrue(info["corregido"])
        self.assertEqual(corregidos, datos)

    def test_corregir_un_bit_info_tiene_claves(self):
        """El resultado de corrección debe tener los campos esperados."""
        datos = b"info de correccion bit"
        crc = calcular_crc16(datos)
        corruptos, _ = insertar_error_un_bit(datos)
        _, info = intentar_corregir_un_bit(corruptos, crc)
        self.assertIn("corregido", info)
        self.assertIn("tipo", info)

    def test_corregir_un_bit_falla_con_multiples_errores(self):
        """Con múltiples bits corruptos, la corrección de un bit debe fallar."""
        datos = b"multiples errores aqui test"
        crc = calcular_crc16(datos)
        # Insertar burst de 4 bits (no corregible como un solo bit)
        corruptos, _ = insertar_error_burst(datos, inicio_bit=0, cantidad_bits=4)
        _, info = intentar_corregir_un_bit(corruptos, crc)
        self.assertFalse(info["corregido"])

    def test_corregir_burst_recupera_datos(self):
        """intentar_corregir_burst debe recuperar datos con error de ráfaga."""
        datos = b"burst error corregible aqui"
        crc = calcular_crc16(datos)
        corruptos, _ = insertar_error_burst(datos, cantidad_bits=4)
        corregidos, info = intentar_corregir_burst(corruptos, crc, max_bits_rafaga=8)
        self.assertTrue(info["corregido"])
        self.assertEqual(corregidos, datos)

    def test_corregir_con_crc_original_un_bit(self):
        """corregir_con_crc_original debe manejar error de un solo bit."""
        datos = b"correccion automatica un bit"
        crc = calcular_crc16(datos)
        corruptos, _ = insertar_error_un_bit(datos)
        corregidos, info = corregir_con_crc_original(corruptos, crc)
        self.assertTrue(info["corregido"])
        self.assertEqual(corregidos, datos)

    def test_corregir_con_crc_original_burst(self):
        """corregir_con_crc_original debe manejar burst error pequeño."""
        datos = b"correccion automatica burst error"
        crc = calcular_crc16(datos)
        corruptos, _ = insertar_error_burst(datos, cantidad_bits=3)
        corregidos, info = corregir_con_crc_original(corruptos, crc, max_bits_rafaga=8)
        self.assertTrue(info["corregido"])
        self.assertEqual(corregidos, datos)

    def test_corregir_datos_segmentados_sin_errores(self):
        """corregir_datos_segmentados con datos limpios: todos los bloques sanos."""
        datos = b"abc"
        segmentos = []
        for idx, byte in enumerate(datos):
            bits = format(byte, "08b")
            crc = calcular_crc16(bytes([byte]))
            segmentos.append({"id": idx + 1, "bits": bits, "checksum": crc})

        resultado, sanos, corregidos, fallidos = corregir_datos_segmentados(segmentos)
        self.assertEqual(resultado, datos)
        self.assertEqual(sanos, 3)
        self.assertEqual(corregidos, 0)
        self.assertEqual(fallidos, 0)

    def test_corregir_datos_segmentados_con_error(self):
        """corregir_datos_segmentados debe reparar un segmento corrupto."""
        datos = b"X"
        crc_original = calcular_crc16(datos)
        # Corromper el byte manualmente
        byte_corrupto = datos[0] ^ 0b00000001  # invertir bit 0
        bits_corruptos = format(byte_corrupto, "08b")

        segmentos = [{"id": 1, "bits": bits_corruptos, "checksum": crc_original}]
        resultado, sanos, corregidos, fallidos = corregir_datos_segmentados(segmentos)
        self.assertEqual(sanos, 0)
        self.assertEqual(corregidos, 1)
        self.assertEqual(fallidos, 0)
        self.assertEqual(resultado, datos)


if __name__ == "__main__":
    unittest.main()
