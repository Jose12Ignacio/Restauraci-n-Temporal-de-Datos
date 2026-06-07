import tkinter as tk
from tkinter import filedialog, messagebox
from Menu import MenuLogico


class InterfazProyecto:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Proyecto 3 - Restauración Temporal de Datos")
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()

        self.ventana.geometry(f"{ancho_pantalla}x{alto_pantalla}")
        self.ventana.resizable(True, True)
        self.menu_logico = MenuLogico()

        self.ruta_archivo = tk.StringVar()
        self.clave_xor = tk.StringVar()
        self.algoritmo_compresion = tk.StringVar(value="Huffman")
        self.tipo_error = tk.StringVar(value="Single-bit error")

        self.crear_interfaz()

    def crear_interfaz(self):
        titulo = tk.Label(
            self.ventana,
            text="Torneo de Restauración Temporal de Datos",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=10)

        frame_archivo = tk.Frame(self.ventana)
        frame_archivo.pack(pady=10)

        tk.Label(frame_archivo, text="Archivo seleccionado:").grid(row=0, column=0, padx=5)

        entrada_archivo = tk.Entry(
            frame_archivo,
            textvariable=self.ruta_archivo,
            width=55,
            state="readonly"
        )
        entrada_archivo.grid(row=0, column=1, padx=5)

        boton_buscar = tk.Button(
            frame_archivo,
            text="Buscar archivo",
            command=self.buscar_archivo
        )
        boton_buscar.grid(row=0, column=2, padx=5)

        boton_limpiar_busqueda = tk.Button(
            frame_archivo,
            text="Limpiar búsqueda",
            command=self.limpiar_busqueda
        )
        boton_limpiar_busqueda.grid(row=0, column=3, padx=5)

        self.crear_seccion_compresion()
        self.crear_seccion_xor()
        self.crear_seccion_errores()
        self.crear_salida()

    def crear_seccion_compresion(self):
        frame = tk.LabelFrame(self.ventana, text="Reto 1: Compresión y Descompresión")
        frame.pack(fill="x", padx=20, pady=8)

        tk.Label(frame, text="Algoritmo:").grid(row=0, column=0, padx=5, pady=5)

        opciones = ["Huffman", "LZ77", "LZ78", "LZW"]

        menu_algoritmo = tk.OptionMenu(
            frame,
            self.algoritmo_compresion,
            *opciones
        )
        menu_algoritmo.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(
            frame,
            text="Comprimir",
            command=self.comprimir
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            frame,
            text="Descomprimir",
            command=self.descomprimir
        ).grid(row=0, column=3, padx=5)

    def crear_seccion_xor(self):
        frame = tk.LabelFrame(self.ventana, text="Reto 2: Cifrado XOR")
        frame.pack(fill="x", padx=20, pady=8)

        tk.Label(frame, text="Clave:").grid(row=0, column=0, padx=5, pady=5)

        tk.Entry(
            frame,
            textvariable=self.clave_xor,
            width=25
        ).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(
            frame,
            text="Cifrar XOR",
            command=self.cifrar_xor
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            frame,
            text="Descifrar XOR",
            command=self.descifrar_xor
        ).grid(row=0, column=3, padx=5)

    def crear_seccion_errores(self):
        frame = tk.LabelFrame(self.ventana, text="Reto 3: Errores y Validación")
        frame.pack(fill="x", padx=20, pady=8)

        tk.Label(frame, text="Tipo de error:").grid(row=0, column=0, padx=5, pady=5)

        opciones = ["Single-bit error", "Burst error"]

        menu_error = tk.OptionMenu(
            frame,
            self.tipo_error,
            *opciones
        )
        menu_error.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(
            frame,
            text="Corromper archivo",
            command=self.corromper
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            frame,
            text="Generar CRC",
            command=self.generar_crc
        ).grid(row=0, column=3, padx=5)

        tk.Button(
            frame,
            text="Verificar CRC",
            command=self.verificar_crc
        ).grid(row=0, column=4, padx=5)

    def crear_salida(self):
        frame = tk.LabelFrame(self.ventana, text="Salida del programa")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.texto_salida = tk.Text(frame, height=8, width=80)
        self.texto_salida.pack(padx=10, pady=10)

        tk.Button(
            self.ventana,
            text="Limpiar salida",
            command=self.limpiar_salida
        ).pack(pady=5)

    def buscar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Archivos binarios", "*.bin"),
                ("Todos los archivos", "*.*")
            ]
        )

        if ruta:
            self.ruta_archivo.set(ruta)
            mensaje = self.menu_logico.seleccionar_archivo(ruta)
            self.mostrar_mensaje(mensaje)

    def comprimir(self):
        algoritmo = self.algoritmo_compresion.get()
        mensaje = self.menu_logico.comprimir_archivo(algoritmo)
        self.mostrar_mensaje(mensaje)

    def descomprimir(self):
        algoritmo = self.algoritmo_compresion.get()
        mensaje = self.menu_logico.descomprimir_archivo(algoritmo)
        self.mostrar_mensaje(mensaje)

    def cifrar_xor(self):
        clave = self.clave_xor.get()
        mensaje = self.menu_logico.cifrar_xor(clave)
        self.mostrar_mensaje(mensaje)

    def descifrar_xor(self):
        clave = self.clave_xor.get()
        mensaje = self.menu_logico.descifrar_xor(clave)
        self.mostrar_mensaje(mensaje)

    def corromper(self):
        tipo_error = self.tipo_error.get()
        mensaje = self.menu_logico.corromper_archivo(tipo_error)
        self.mostrar_mensaje(mensaje)

    def generar_crc(self):
        mensaje = self.menu_logico.generar_crc()
        self.mostrar_mensaje(mensaje)

    def verificar_crc(self):
        mensaje = self.menu_logico.verificar_crc()
        self.mostrar_mensaje(mensaje)

    def mostrar_mensaje(self, mensaje):
        self.texto_salida.insert(tk.END, mensaje + "\n\n")

    def limpiar_salida(self):
        self.texto_salida.delete("1.0", tk.END)

    def limpiar_busqueda(self):
        self.ruta_archivo.set("")
        mensaje = self.menu_logico.limpiar_busqueda()
        self.mostrar_mensaje(mensaje)

    def ejecutar(self):
        self.ventana.mainloop()