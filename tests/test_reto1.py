import unittest
import json
from reto1.huffman import construir_arbol, construir_tabla, codificar, decodificar
from reto1.lzw import comprimir_lzw, descomprimir_lzw
from reto1.compress import comprimir
from reto1.decompress import descomprimir


class TestHuffman(unittest.TestCase):

    def test_construir_arbol_texto_normal(self):
        """El árbol debe construirse sin errores para texto normal."""
        arbol = construir_arbol("hola mundo")
        self.assertIsInstance(arbol, dict)
        self.assertIn("izquierda", arbol)
        self.assertIn("derecha", arbol)

    def test_construir_arbol_texto_vacio(self):
        """Texto vacío devuelve nodo vacío sin explotar."""
        arbol = construir_arbol("")
        self.assertIsNone(arbol["valor"])

    def test_construir_arbol_un_solo_caracter(self):
        """Un solo carácter repetido no debe romper el árbol."""
        arbol = construir_arbol("aaaa")
        self.assertIsNotNone(arbol)

    def test_tabla_codigos_cubre_todos_los_caracteres(self):
        """La tabla debe tener un código para cada carácter único del texto."""
        texto = "abracadabra"
        arbol = construir_arbol(texto)
        tabla = construir_tabla(arbol)
        for char in set(texto):
            self.assertIn(char, tabla)

    def test_codigos_son_binarios(self):
        """Todos los códigos de la tabla deben ser cadenas de 0s y 1s."""
        arbol = construir_arbol("hola mundo")
        tabla = construir_tabla(arbol)
        for char, codigo in tabla.items():
            self.assertTrue(all(b in "01" for b in codigo), 
                            f"Código no binario para '{char}': {codigo}")

    def test_codificacion_y_decodificacion_ida_vuelta(self):
        """Codificar y luego decodificar debe devolver el texto original."""
        texto = "hola mundo"
        arbol = construir_arbol(texto)
        tabla = construir_tabla(arbol)
        bits = codificar(texto, tabla)
        recuperado = decodificar(bits, arbol)
        self.assertEqual(recuperado, texto)

    def test_codificacion_texto_largo(self):
        """La ida y vuelta debe funcionar con texto más largo."""
        texto = "el veloz murciélago hindú comía feliz cardillo y kiwi"
        arbol = construir_arbol(texto)
        tabla = construir_tabla(arbol)
        bits = codificar(texto, tabla)
        recuperado = decodificar(bits, arbol)
        self.assertEqual(recuperado, texto)

    def test_codificacion_texto_vacio(self):
        """Codificar texto vacío devuelve cadena vacía."""
        arbol = construir_arbol("")
        tabla = construir_tabla(arbol)
        bits = codificar("", tabla)
        self.assertEqual(bits, "")

    def test_decodificacion_texto_vacio(self):
        """Decodificar cadena vacía devuelve texto vacío."""
        arbol = construir_arbol("a")
        resultado = decodificar("", arbol)
        self.assertEqual(resultado, "")


class TestLZW(unittest.TestCase):

    def test_compresion_basica(self):
        """Comprimir texto simple devuelve lista de códigos enteros."""
        salida, _ = comprimir_lzw("aabbc")
        self.assertIsInstance(salida, list)
        self.assertTrue(all(isinstance(c, int) for c in salida))

    def test_compresion_texto_vacio(self):
        """Comprimir texto vacío devuelve lista vacía."""
        salida, diccionario = comprimir_lzw("")
        self.assertEqual(salida, [])
        self.assertEqual(diccionario, [])

    def test_descompresion_ida_vuelta(self):
        """Comprimir y descomprimir debe devolver el texto original."""
        texto = "abracadabra"
        salida, _ = comprimir_lzw(texto)
        dic_inicial = {ch: ord(ch) for ch in set(texto)}
        recuperado = descomprimir_lzw(salida, dic_inicial)
        self.assertEqual(recuperado, texto)

    def test_descompresion_texto_largo(self):
        """La ida y vuelta funciona con texto con repeticiones."""
        texto = "aaabbbcccaaabbbccc"
        salida, _ = comprimir_lzw(texto)
        dic_inicial = {ch: ord(ch) for ch in set(texto)}
        recuperado = descomprimir_lzw(salida, dic_inicial)
        self.assertEqual(recuperado, texto)

    def test_compresion_genera_diccionario(self):
        """El diccionario generado debe ser una lista de dicts con 'codigo' y 'cadena'."""
        _, diccionario = comprimir_lzw("abab")
        if diccionario:
            self.assertIn("codigo", diccionario[0])
            self.assertIn("cadena", diccionario[0])

    def test_descompresion_lista_vacia(self):
        """Descomprimir lista vacía devuelve string vacío."""
        resultado = descomprimir_lzw([], {})
        self.assertEqual(resultado, "")


class TestComprimir(unittest.TestCase):

    def test_comprimir_huffman_devuelve_json_valido(self):
        """comprimir() con huffman debe devolver dict con clave 'compresion'."""
        resultado = comprimir("hola mundo", "huffman")
        self.assertIn("compresion", resultado)
        self.assertIsInstance(resultado["compresion"], list)

    def test_comprimir_lzw_devuelve_json_valido(self):
        """comprimir() con lzw debe devolver dict con clave 'compresion'."""
        resultado = comprimir("hola mundo", "lzw")
        self.assertIn("compresion", resultado)

    def test_comprimir_incluye_tres_algoritmos(self):
        """El JSON siempre debe tener entradas para Huffman, LZ78 y LZW."""
        resultado = comprimir("test de compresion", "huffman")
        algoritmos = [e["algoritmo"] for e in resultado["compresion"]]
        self.assertIn("Huffman", algoritmos)
        self.assertIn("LZ78", algoritmos)
        self.assertIn("LZW", algoritmos)

    def test_comprimir_algoritmo_invalido(self):
        """Un algoritmo no soportado debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            comprimir("hola", "algoritmo_inventado")

    def test_descomprimir_huffman_ida_vuelta(self):
        """comprimir + descomprimir con Huffman debe devolver el texto original."""
        texto = "recuperar este texto con huffman"
        json_data = comprimir(texto, "huffman")
        recuperado = descomprimir(json_data, "huffman")
        self.assertEqual(recuperado, texto)

    def test_descomprimir_lzw_ida_vuelta(self):
        """comprimir + descomprimir con LZW debe devolver el texto original."""
        texto = "recuperar este texto con lzw"
        json_data = comprimir(texto, "lzw")
        recuperado = descomprimir(json_data, "lzw")
        self.assertEqual(recuperado, texto)

    def test_descomprimir_algoritmo_invalido(self):
        """descomprimir con algoritmo no soportado debe lanzar ValueError."""
        json_data = comprimir("hola", "huffman")
        with self.assertRaises(ValueError):
            descomprimir(json_data, "algoritmo_inventado")


if __name__ == "__main__":
    unittest.main()
