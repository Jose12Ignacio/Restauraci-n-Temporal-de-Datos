# Restauraci-n-Temporal-de-Datos

# Torneo de Restauración Temporal de Datos

Proyecto académico que implementa tres retos independientes de procesamiento de datos: compresión, cifrado XOR y detección/corrección de errores mediante CRC. Cuenta con una interfaz gráfica en Tkinter que integra los tres módulos.

---

## Estructura del proyecto

```
proyecto3/
│
├── common/
│   ├── __init__.py
│   ├── formato.py        # Conversiones binario ↔ bytes ↔ texto
│   └── funciones.py      # Utilidades de lectura/escritura de archivos
│
├── reto1/
│   ├── __init__.py
│   ├── huffman.py        # Árbol de Huffman: construcción, codificación y decodificación
│   ├── lzw.py            # Compresión y descompresión LZW
│   ├── compress.py       # API de compresión (Huffman y LZW)
│   └── decompress.py     # API de descompresión
│
├── reto2/
│   ├── __init__.py
│   ├── xor_cifrador.py   # Cifrado y descifrado XOR con clave repetida
│   ├── longitud_clave.py # Estimación de longitud de clave por índice de coincidencia
│   └── xor_ataque.py     # Ataque automático por análisis de frecuencia
│
├── reto3/
│   ├── __init__.py
│   ├── crc.py            # Cálculo, guardado y verificación de CRC-16
│   ├── injector.py       # Inyección de errores (single-bit y burst)
│   └── correccion.py     # Corrección por inversión de bits y corrección segmentada
│
├── tests/
│   ├── test_reto1.py     # Tests de compresión
│   ├── test_reto2.py     # Tests de cifrado XOR
│   └── test_reto3.py     # Tests de CRC y corrección de errores
│
├── Interfaz.py           # Interfaz gráfica en Tkinter
├── Menu.py               # Lógica de negocio de cada reto
├── Main.py               # Punto de entrada de la aplicación
└── README.md
```

---

## Requisitos

- Python 3.8 o superior
- Tkinter (incluido en la instalación estándar de Python)
- Sin dependencias externas adicionales

---

## Instalación

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd proyecto3
```

No requiere instalación de paquetes. Todos los módulos son parte del proyecto o de la biblioteca estándar de Python.

---

## Ejecución

### Interfaz gráfica

```bash
python Main.py
```

---

## Retos

### Reto 1 — Compresión y Descompresión

Implementa dos algoritmos de compresión sin pérdida:

**Huffman**
- Construye un árbol de frecuencias a partir del texto.
- Genera una tabla de códigos binarios de longitud variable.
- Codifica el texto en una cadena de bits.
- La decodificación recorre el árbol según los bits leídos.

**LZW**
- Inicia con un diccionario de 256 símbolos base (ASCII).
- Construye entradas nuevas dinámicamente al comprimir.
- La descompresión reconstruye el diccionario en paralelo.

**Flujo de uso desde la interfaz:**
1. Seleccionar un archivo `.txt`.
2. Elegir algoritmo (Huffman o LZW).
3. Pulsar **Comprimir** → genera un `.reto1.json` con la estructura comprimida.
4. Seleccionar el `.reto1.json` generado.
5. Pulsar **Descomprimir** → genera un `.dec.txt` con el texto recuperado.

**Formato del JSON generado:**
```json
{
  "compresion": [
    { "algoritmo": "Huffman", "estructura": { "arbol": {}, "tabla_codigos": {}, "salida": "..." } },
    { "algoritmo": "LZ78",    "estructura": { ... } },
    { "algoritmo": "LZW",     "estructura": { "diccionario_inicial": {}, "salida": [] } }
  ]
}
```

---

### Reto 2 — Cifrado y Ataque XOR

Implementa cifrado simétrico XOR con análisis de clave.

**Cifrado XOR**
- La clave se repite cíclicamente sobre el mensaje (`texto[i] XOR clave[i % len(clave)]`).
- Validaciones: clave de 1–10 caracteres, mensaje mínimo de `2 × len(clave)` caracteres.
- El resultado se guarda en un `.json` con los bits cifrados en formato binario.

**Estimación de longitud de clave**
- Usa el **Índice de Coincidencia (IC)** para estimar la longitud más probable de la clave.
- Divide el cifrado en columnas y calcula el IC promedio para cada longitud candidata.

**Ataque automático por análisis de frecuencia**
- Para cada longitud candidata, ataca columna por columna buscando el byte de clave que maximiza la legibilidad.
- Evalúa el texto resultante con una función de puntuación de legibilidad en español.
- Devuelve la clave encontrada, el texto recuperado y una puntuación de confianza (0–1).

**Flujo de uso desde la interfaz:**
1. Seleccionar un archivo `.txt`.
2. Ingresar una clave (1–10 caracteres).
3. Pulsar **Cifrar XOR** → genera un `.json` con el texto cifrado.
4. Para descifrar con clave conocida: ingresar la clave y pulsar **Descifrar XOR**.
5. Para ataque automático: dejar la clave vacía y pulsar **Descifrar XOR**.

---

### Reto 3 — Detección y Corrección de Errores (CRC-16)

Implementa un pipeline completo de integridad de datos por segmentos.

**CRC-16**
- Polinomio: `0x1021` con valor inicial `0xFFFF`.
- Cada byte del archivo se procesa individualmente como un segmento de 8 bits.
- El CRC de cada segmento se guarda junto con los bits en el JSON estructurado.

**Inyección de errores**
- *Single-bit error*: invierte un bit aleatorio en un segmento.
- *Burst error*: invierte una ráfaga de bits consecutivos (por defecto 4 bits).

**Corrección**
- Primero intenta corrección de un solo bit (prueba las `n×8` posiciones posibles).
- Si falla, intenta corrección de burst (prueba rangos de 2 a `max_bits_rafaga` bits).
- Opera segmento a segmento, lo que reduce el espacio de búsqueda significativamente.

**Flujo de uso desde la interfaz:**
1. Seleccionar un archivo `.txt`.
2. Pulsar **Generar CRC** → genera `.reto3.json` con bits y checksums por segmento.
3. Seleccionar el `.reto3.json`.
4. Elegir tipo de error y pulsar **Corromper archivo** → genera `.corrupto.json`.
5. Seleccionar el `.corrupto.json`.
6. Pulsar **Verificar CRC** para detectar qué segmentos están corruptos.
7. Pulsar **Corregir con CRC** para reparar y exportar el texto restaurado.

**Formato del JSON estructurado:**
```json
{
  "metadata": { "algorithm": "crc-16", "bits_por_segmento": 8 },
  "data": [
    { "id": 1, "bits": "01101000", "checksum": 12345 },
    { "id": 2, "bits": "01101111", "checksum": 54321 }
  ]
}
```

---

## Tests

Los tests cubren los tres retos con casos normales, casos borde y casos de error esperados.

```bash
# Ejecutar todos los tests desde la raíz del proyecto
python -m unittest discover tests

# Ejecutar tests de un reto específico
python -m unittest tests.test_reto1
python -m unittest tests.test_reto2
python -m unittest tests.test_reto3
```

**Cobertura de los tests:**

| Módulo | Casos cubiertos |
|---|---|
| `huffman.py` | Árbol vacío, un solo carácter, tabla completa, ida y vuelta |
| `lzw.py` | Texto vacío, compresión y descompresión, integridad del diccionario |
| `compress.py` / `decompress.py` | JSON válido, tres algoritmos presentes, ida y vuelta completa |
| `xor_cifrador.py` | Simetría XOR, validaciones de clave y mensaje, claves distintas |
| `longitud_clave.py` | IC uniforme, respeto del máximo, detección de longitud conocida |
| `xor_ataque.py` | Campos del resultado, rango de confianza, legibilidad, simetría |
| `crc.py` | Determinismo, rango válido, guardar/leer, verificación correcta e incorrecta |
| `injector.py` | Longitud preservada, info correcta, posición fija, casos vacíos |
| `correccion.py` | Corrección de un bit, corrección burst, datos segmentados con y sin error |

---

## Integrantes

| Persona | Responsabilidad |
|---|---|
| Persona A | Infraestructura (`common/`) y Reto 3 (CRC, inyector, corrección) |
| Persona B | Reto 1 (Huffman, LZW, compresión, descompresión) |
| Persona C | Reto 2 (XOR, estimación de clave, ataque por frecuencia) |
| Persona D | Integración, tests, CLI/interfaz y documentación |
