import unittest
from reto2.xor_cifrador import cifrar, descifrar, validarClave, validarMensaje
from reto2.longitud_clave import indice_coincidencia, ic_promedio, estimar_longitud_clave
from reto2.xor_ataque import atacar, byte_clave_columna, recuperar_clave, aplicar_xor, puntuacion_legibilidad


class TestXorCifrador(unittest.TestCase):

    def test_cifrar_devuelve_bytes(self):
        """cifrar() debe devolver bytes."""
        resultado = cifrar("hola mundo xor", "clave")
        self.assertIsInstance(resultado, bytes)

    def test_cifrar_longitud_igual_al_texto(self):
        """Los bytes cifrados deben tener la misma longitud que el texto original."""
        texto = "texto de prueba"
        resultado = cifrar(texto, "abc")
        self.assertEqual(len(resultado), len(texto.encode("utf-8")))

    def test_descifrar_ida_vuelta(self):
        """Cifrar y descifrar con la misma clave debe devolver el texto original."""
        texto = "mensaje secreto de prueba"
        clave = "miClave"
        cifrado = cifrar(texto, clave)
        recuperado = descifrar(cifrado, clave)
        self.assertEqual(recuperado, texto)

    def test_xor_es_simetrico(self):
        """Aplicar XOR dos veces con la misma clave devuelve los datos originales."""
        texto = "simetria xor test"
        clave = "key"
        primera_pasada = cifrar(texto, clave)
        segunda_pasada = descifrar(primera_pasada, clave)
        self.assertEqual(segunda_pasada, texto)

    def test_cifrar_clave_vacia_lanza_error(self):
        """Clave vacía debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            cifrar("texto suficientemente largo", "")

    def test_cifrar_clave_muy_larga_lanza_error(self):
        """Clave de más de 10 caracteres debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            cifrar("texto suficientemente largo", "clavemuylarga123")

    def test_cifrar_texto_muy_corto_lanza_error(self):
        """Texto más corto que 2*len(clave) debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            cifrar("hi", "claveLarga")

    def test_validar_clave_valida(self):
        """validarClave no debe lanzar error con clave válida."""
        try:
            validarClave("abc")
        except ValueError:
            self.fail("validarClave lanzó ValueError con clave válida")

    def test_cifrar_claves_diferentes_dan_resultado_diferente(self):
        """Cifrar el mismo texto con claves distintas debe dar resultados distintos."""
        texto = "texto de prueba para comparar claves"
        cifrado1 = cifrar(texto, "claveA")
        cifrado2 = cifrar(texto, "claveB")
        self.assertNotEqual(cifrado1, cifrado2)


class TestLongitudClave(unittest.TestCase):

    def test_indice_coincidencia_datos_vacios(self):
        """IC de datos muy cortos debe ser 0."""
        resultado = indice_coincidencia(b"a")
        self.assertEqual(resultado, 0.0)

    def test_indice_coincidencia_texto_uniforme(self):
        """IC de texto con un solo byte repetido debe ser 1."""
        resultado = indice_coincidencia(bytes([65] * 100))
        self.assertAlmostEqual(resultado, 1.0, places=2)

    def test_estimar_longitud_devuelve_lista(self):
        """estimar_longitud_clave debe devolver una lista de tuplas."""
        texto = "hola mundo cifrado con xor"
        clave = "abc"
        cifrado = cifrar(texto, clave)
        resultado = estimar_longitud_clave(cifrado)
        self.assertIsInstance(resultado, list)
        self.assertTrue(all(isinstance(t, tuple) and len(t) == 2 for t in resultado))

    def test_estimar_longitud_respeta_maximo(self):
        """El resultado no debe tener más longitudes que max_longitud."""
        texto = "a" * 100
        clave = "k"
        cifrado = cifrar(texto, clave)
        resultado = estimar_longitud_clave(cifrado, max_longitud=5)
        self.assertLessEqual(len(resultado), 5)

    def test_estimar_longitud_clave_conocida(self):
        """La longitud correcta de clave debe aparecer entre las primeras posiciones."""
        # Texto largo para que el análisis estadístico funcione bien
        texto = ("esto es un texto bastante largo para que el analisis "
                 "estadistico pueda funcionar correctamente en la prueba ") * 3
        clave = "abc"  # longitud 3
        cifrado = cifrar(texto, clave)
        resultado = estimar_longitud_clave(cifrado, max_longitud=8)
        longitudes = [r[0] for r in resultado]
        self.assertIn(3, longitudes[:4])  # debe estar entre las primeras 4

    def test_ic_promedio_calcula_sin_errores(self):
        """ic_promedio no debe lanzar errores con datos válidos."""
        texto = "datos de prueba para ic promedio"
        clave = "xy"
        cifrado = cifrar(texto, clave)
        resultado = ic_promedio(cifrado, 2)
        self.assertIsInstance(resultado, float)


class TestXorAtaque(unittest.TestCase):

    def test_atacar_devuelve_resultado_ataque(self):
        """atacar() debe devolver un ResultadoAtaque con los campos esperados."""
        texto = ("el ataque xor debe funcionar correctamente con este texto "
                 "que es suficientemente largo para el analisis") 
        clave = "clave"
        cifrado = cifrar(texto, clave)
        resultado = atacar(cifrado)
        self.assertIsNotNone(resultado)
        self.assertTrue(hasattr(resultado, "clave"))
        self.assertTrue(hasattr(resultado, "texto"))
        self.assertTrue(hasattr(resultado, "confianza"))
        self.assertTrue(hasattr(resultado, "longitud_clave"))

    def test_atacar_confianza_entre_0_y_1(self):
        """La confianza del ataque debe estar en el rango [0, 1]."""
        texto = "texto para verificar rango de confianza en el ataque"
        clave = "key"
        cifrado = cifrar(texto, clave)
        resultado = atacar(cifrado)
        self.assertGreaterEqual(resultado.confianza, 0.0)
        self.assertLessEqual(resultado.confianza, 1.0)

    def test_atacar_cifrado_vacio_lanza_error(self):
        """atacar() con bytes vacíos debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            atacar(b"")

    def test_puntuacion_legibilidad_texto_legible(self):
        """Texto legible en español debe tener puntuación alta."""
        texto = "hola esto es un texto legible en español"
        puntuacion = puntuacion_legibilidad(texto.encode("utf-8"))
        self.assertGreater(puntuacion, 0.8)

    def test_puntuacion_legibilidad_bytes_aleatorios(self):
        """Bytes aleatorios deben tener puntuación baja."""
        basura = bytes(range(0, 10)) + bytes(range(128, 200))
        puntuacion = puntuacion_legibilidad(basura)
        self.assertLess(puntuacion, 0.5)

    def test_aplicar_xor_simetrico(self):
        """aplicar_xor dos veces con la misma clave devuelve los datos originales."""
        datos = b"datos de prueba para xor"
        clave = b"abc"
        primera = aplicar_xor(datos, clave)
        segunda = aplicar_xor(primera, clave)
        self.assertEqual(segunda, datos)

    def test_recuperar_clave_longitud_correcta(self):
        """recuperar_clave debe devolver bytes de la longitud indicada."""
        texto = "texto cifrado para probar recuperacion de clave con xor"
        clave = "abc"
        cifrado = cifrar(texto, clave)
        clave_recuperada = recuperar_clave(cifrado, 3)
        self.assertEqual(len(clave_recuperada), 3)


if __name__ == "__main__":
    unittest.main()
