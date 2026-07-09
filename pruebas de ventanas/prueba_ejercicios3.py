# =============================================================================
# EJERCICIOS DE CAIDA LIBRE CON RESISTENCIA DEL AIRE - FACILES
# =============================================================================
# Modulo pensado para integrarse en el proyecto Caida_libre, dentro de
# interfaz/ejercicios.py, siguiendo el mismo patron que Teoria, Intro y
# AplicacionCaidaLibre: recibe un Frame (panel) y construye toda la interfaz
# dentro de el.
#
# Requiere solo la biblioteca estandar de Python: tkinter y tkinter.ttk.
# Los 6 iconos de los objetos se dibujan con tkinter.Canvas.
# =============================================================================

import tkinter as tk
from tkinter import ttk


class Ejercicios:
    """
    Construye la pantalla "Ejercicios de Caída Libre con Resistencia del Aire"
    dentro de un panel (Frame) padre.

    Utiliza un lienzo (Canvas) con barra de desplazamiento para alojar todo el
    contenido y permitir el scroll en ventanas pequeñas.
    """

    def __init__(self, panel):
        """
        Inicializa la pantalla de ejercicios.

        Args:
            panel (tk.Frame): Contenedor padre donde se dibujará toda la interfaz.
        """
        self.panel = panel

        # -------------------- Paleta general --------------------
        # Definición de colores corporativos para reutilización y mantenimiento.
        self.COLOR_HEADER = "#12213B"          # Azul oscuro para encabezados
        self.COLOR_GOLD = "#F4C542"            # Dorado para resaltar palabras clave
        self.COLOR_FONDO = "#EEF1F6"           # Gris claro de fondo
        self.COLOR_TARJETA_BG = "#FFFFFF"      # Blanco para tarjetas
        self.COLOR_TEXTO = "#1F2D3D"           # Texto principal oscuro
        self.COLOR_TEXTO_SUAVE = "#5A6B82"     # Texto secundario grisáceo

        # (borde, fondo_claro) para cada uno de los 6 ejercicios
        self.COLORES_EJERCICIOS = [
            ("#1976D2", "#E3F2FD"),  # 1 azul
            ("#2E7D32", "#E8F5E9"),  # 2 verde
            ("#F57C00", "#FFF3E0"),  # 3 naranja
            ("#6A1B9A", "#F3E5F5"),  # 4 morado
            ("#00838F", "#E0F7FA"),  # 5 teal
            ("#C2185B", "#FCE4EC"),  # 6 rosa/magenta
        ]

        # Datos de los ejercicios: cada diccionario representa un problema
        # con sus condiciones iniciales, enunciado, datos y pregunta.
        self.ejercicios_data = [
            {
                "numero": 1, "objeto": "piedra", "altura": "20 m", "velocidad": None,
                "enunciado": "Se deja caer una piedra desde una altura de 20 m.",
                "datos": ["y\u2080 = 20 m", "v\u2080 = 0 m/s", "m = 1.0 kg",
                          "k = 0.20 kg/s", "g = 9.8 m/s\u00b2"],
                "pregunta": "\u00bfCu\u00e1l es el tiempo que tarda en llegar al suelo?",
            },
            {
                "numero": 2, "objeto": "pelota_naranja", "altura": "45 m", "velocidad": None,
                "enunciado": "Se deja caer una pelota desde una altura de 45 m.",
                "datos": ["y\u2080 = 45 m", "v\u2080 = 0 m/s", "m = 0.5 kg",
                          "k = 0.10 kg/s", "g = 9.8 m/s\u00b2"],
                "pregunta": "\u00bfCon qu\u00e9 velocidad llega al suelo?",
            },
            {
                "numero": 3, "objeto": "bola_azul", "altura": "30 m", "velocidad": "10 m/s",
                "enunciado": "Se lanza hacia abajo una bola con velocidad inicial de "
                              "10 m/s desde una altura de 30 m.",
                "datos": ["y\u2080 = 30 m", "v\u2080 = 10 m/s (hacia abajo)", "m = 0.2 kg",
                          "k = 0.05 kg/s", "g = 9.8 m/s\u00b2"],
                "pregunta": "\u00bfCu\u00e1l es el tiempo que tarda en llegar al suelo?",
            },
            {
                "numero": 4, "objeto": "piedra", "altura": "80 m", "velocidad": None,
                "enunciado": "Se deja caer una piedra desde una altura de 80 m.",
                "datos": ["y\u2080 = 80 m", "v\u2080 = 0 m/s", "m = 2.0 kg",
                          "k = 0.25 kg/s", "g = 9.8 m/s\u00b2"],
                "pregunta": "\u00bfQu\u00e9 distancia ha recorrido luego de 2 segundos?",
            },
            {
                "numero": 5, "objeto": "pelota_verde", "altura": "25 m", "velocidad": "5 m/s",
                "enunciado": "Se lanza hacia abajo una pelota con velocidad de 5 m/s "
                              "desde una altura de 25 m.",
                "datos": ["y\u2080 = 25 m", "v\u2080 = 5 m/s (hacia abajo)", "m = 0.3 kg",
                          "k = 0.08 kg/s", "g = 9.8 m/s\u00b2"],
                "pregunta": "\u00bfCon qu\u00e9 velocidad llega al suelo?",
            },
            {
                "numero": 6, "objeto": "piedra", "altura": "h = ?", "velocidad": None,
                "enunciado": "Se deja caer una piedra y tarda 3 segundos en llegar al suelo.",
                "datos": ["v\u2080 = 0 m/s", "t = 3 s", "m = 1.0 kg",
                          "k = 0.15 kg/s", "g = 9.8 m/s\u00b2"],
                "pregunta": "\u00bfDesde qu\u00e9 altura fue soltada?",
            },
        ]

        # Construir toda la interfaz gráfica.
        self.crear_interfaz()

    # =====================================================================
    # INTERFAZ PRINCIPAL (canvas con scroll, igual que en Teoria)
    # =====================================================================
    def crear_interfaz(self):
        """
        Crea la estructura base: un Canvas con barra de scroll vertical que
        contiene un Frame interno. Así todo el contenido es desplazable.
        """
        # Eliminar cualquier widget anterior del panel (por si se reinicia)
        for widget in self.panel.winfo_children():
            widget.destroy()

        # Crear el Canvas que servirá como área desplazable.
        self.canvas = tk.Canvas(self.panel, bg=self.COLOR_FONDO, highlightthickness=0)
        # Barra de desplazamiento vertical vinculada al canvas.
        scrollbar = tk.Scrollbar(self.panel, orient="vertical", command=self.canvas.yview)

        # Frame interno que contendrá todos los widgets y que se mueve con el scroll.
        contenido = tk.Frame(self.canvas, bg=self.COLOR_FONDO)
        # Cuando cambie el tamaño del contenido, ajustar la región de scroll del canvas.
        contenido.bind("<Configure>",
                        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Crear una ventana dentro del canvas que muestra el frame 'contenido'.
        self.ventana_id = self.canvas.create_window((0, 0), window=contenido, anchor="nw")
        # Configurar el canvas para que su scroll sea controlado por la barra.
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Hacer que el contenido ocupe todo el ancho del canvas al redimensionar la ventana.
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.ventana_id, width=e.width)
        )

        # Empaquetar canvas y scrollbar en el panel.
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Construir las secciones del contenido.
        self._crear_encabezado(contenido)
        self._crear_intro_y_formulas(contenido)
        self._crear_grilla_ejercicios(contenido)
        self._crear_notas_finales(contenido)

        # Espacio final para mejorar la estética.
        tk.Label(contenido, text="", bg=self.COLOR_FONDO).pack(pady=10)

        # ----- Eventos de scroll con rueda del mouse y teclas de flecha -----
        # Windows / Linux (rueda vertical)
        self.canvas.bind("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        # macOS (Button-4 y Button-5)
        self.canvas.bind("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))
        # Flechas arriba/abajo
        self.canvas.bind("<Up>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind("<Down>", lambda e: self.canvas.yview_scroll(1, "units"))
        # Asegurar que el canvas tenga el foco para recibir eventos de teclado.
        self.canvas.focus_set()
        self.canvas.bind("<Enter>", lambda e: self.canvas.focus_set())

    # =====================================================================
    # ENCABEZADO
    # =====================================================================
    def _crear_encabezado(self, contenido):
        """
        Crea una barra superior con el título del tema, combinando colores
        para resaltar términos importantes.
        """
        header = tk.Frame(contenido, bg=self.COLOR_HEADER, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)  # Mantener altura fija

        # Frame centrador para el texto.
        contenedor_titulo = tk.Frame(header, bg=self.COLOR_HEADER)
        contenedor_titulo.pack(expand=True)

        # Partes del título con diferente color (dorado para palabras clave).
        partes = [
            ("\u2601 ", "white"),
            ("EJERCICIOS DE ", "white"),
            ("CA\u00cdDA LIBRE", self.COLOR_GOLD),
            (" CON ", "white"),
            ("RESISTENCIA", self.COLOR_GOLD),
            (" DEL AIRE \u2013 F\u00c1CILES ", "white"),
            ("\u2601", "white"),
        ]
        # Construir cada etiqueta y apilar horizontalmente.
        for texto, color in partes:
            tk.Label(contenedor_titulo, text=texto, font=("Arial", 12, "bold"),
                     bg=self.COLOR_HEADER, fg=color).pack(side="left")

    # =====================================================================
    # CAJA DE INTRODUCCIÓN + CAJA DE FÓRMULAS
    # =====================================================================
    def _crear_intro_y_formulas(self, contenido):
        """
        Sección con dos columnas: una introducción descriptiva (izquierda) y
        un resumen de fórmulas (derecha).
        """
        # Fila que contendrá las dos cajas.
        fila_intro = tk.Frame(contenido, bg=self.COLOR_FONDO)
        fila_intro.pack(fill="x", padx=20, pady=(16, 6))

        # ---------------- Caja izquierda: descripción ----------------
        caja_intro = tk.Frame(fila_intro, bg=self.COLOR_TARJETA_BG,
                               highlightbackground="#1976D2", highlightthickness=2)
        caja_intro.pack(side="left", fill="both", expand=True, padx=(0, 8))

        # Título de la caja introductoria.
        tk.Label(caja_intro, text="CA\u00cdDA LIBRE CON RESISTENCIA DEL AIRE",
                 font=("Arial", 12, "bold"), fg="#1976D2",
                 bg=self.COLOR_TARJETA_BG).pack(pady=(12, 6))

        # Fila que contiene el texto descriptivo y un dibujo de paracaídas.
        fila_txt_icono = tk.Frame(caja_intro, bg=self.COLOR_TARJETA_BG)
        fila_txt_icono.pack(fill="x", padx=14)

        # Texto explicativo.
        tk.Label(
            fila_txt_icono,
            text="Al caer, los objetos se ven afectados por la resistencia del "
                 "aire, lo que hace que su velocidad aumente cada vez m\u00e1s "
                 "lentamente hasta alcanzar una velocidad l\u00edmite (v\u2097).",
            font=("Arial", 12), bg=self.COLOR_TARJETA_BG, fg=self.COLOR_TEXTO,
            justify="left", wraplength=260,
        ).pack(side="left", anchor="n", pady=4)

        # Canvas para el ícono decorativo (paracaídas).
        icono_paracaidas = tk.Canvas(fila_txt_icono, width=70, height=70,
                                      bg=self.COLOR_TARJETA_BG, highlightthickness=0)
        icono_paracaidas.pack(side="right", anchor="n")
        self._dibujar_paracaidas(icono_paracaidas)

        # Badge informativo con el valor de g.
        badge_g = tk.Frame(caja_intro, bg="#E8F5E9")
        badge_g.pack(fill="x", padx=14, pady=(10, 14))
        tk.Label(badge_g, text="\u2705", bg="#E8F5E9", font=("Arial", 12)).pack(
            side="left", padx=(8, 4), pady=6)
        tk.Label(badge_g, text="Aceleraci\u00f3n de la gravedad:  g = 9.8 m/s\u00b2 (hacia abajo)",
                 bg="#E8F5E9", fg="#2E7D32", font=("Arial", 12, "bold")).pack(
            side="left", pady=6)

        # ---------------- Caja derecha: fórmulas ----------------
        caja_formulas = tk.Frame(fila_intro, bg=self.COLOR_TARJETA_BG,
                                  highlightbackground="#6A1B9A", highlightthickness=2)
        caja_formulas.pack(side="left", fill="both", expand=True, padx=(8, 0))

        # Título de la caja de fórmulas.
        tk.Label(caja_formulas, text="F\u00d3RMULAS \u00daTILES (con resistencia del aire)",
                 font=("Arial", 12, "bold"), fg="#6A1B9A",
                 bg=self.COLOR_TARJETA_BG).pack(pady=(12, 6))

        # Nota sobre el modelo simple usado.
        nota_modelo = tk.Frame(caja_formulas, bg="#F3E5F5")
        nota_modelo.pack(fill="x", padx=14, pady=(0, 8))
        tk.Label(nota_modelo,
                 text="Modelo sencillo (fuerza de arrastre proporcional a la velocidad)",
                 font=("Arial", 12, "italic"), bg="#F3E5F5", fg="#6A1B9A",
                 wraplength=190, justify="left").pack(side="left", padx=8, pady=6)
        tk.Label(nota_modelo, text="k = constante\nde arrastre (> 0)",
                 font=("Arial", 12, "bold"), bg="#F3E5F5", fg="#6A1B9A",
                 justify="right").pack(side="right", padx=8)

        # Contenedor para las tres fórmulas (velocidad, posición, velocidad límite).
        fila_formulas = tk.Frame(caja_formulas, bg=self.COLOR_TARJETA_BG)
        fila_formulas.pack(fill="x", padx=14, pady=(0, 14))

        # Cada fórmula se dibuja como una pequeña tarjeta coloreada.
        self._caja_formula(fila_formulas, "#FFF3E0", "#F57C00",
                            "v(t) = v\u2097\u00b7(1 \u2212 e^(\u2212kt/m))", "Velocidad")
        self._caja_formula(fila_formulas, "#E8F5E9", "#2E7D32",
                            "y(t)=y\u2080+(v\u2097m/k)\u00b7[t+(m/k)(e^(\u2212kt/m)\u22121)]",
                            "Posici\u00f3n")
        self._caja_formula(fila_formulas, "#F3E5F5", "#6A1B9A",
                            "v\u2097 = m\u00b7g / k", "Velocidad l\u00edmite")

    def _caja_formula(self, parent, bg, fg, formula, etiqueta):
        """
        Crea una pequeña tarjeta con una fórmula y su etiqueta descriptiva.

        Args:
            parent: widget padre.
            bg: color de fondo de la tarjeta.
            fg: color del borde y del texto de la etiqueta.
            formula: texto de la fórmula matemática.
            etiqueta: nombre de la magnitud (ej. "Velocidad").
        """
        caja = tk.Frame(parent, bg=bg, highlightbackground=fg, highlightthickness=1)
        caja.pack(side="left", fill="both", expand=True, padx=4)
        tk.Label(caja, text=formula, font=("Arial", 12, "bold"), bg=bg,
                  fg=self.COLOR_TEXTO, wraplength=150, justify="center").pack(padx=8, pady=(10, 2))
        tk.Label(caja, text=etiqueta, font=("Arial", 12, "bold"), bg=bg, fg=fg).pack(pady=(0, 8))

    def _dibujar_paracaidas(self, c):
        """
        Dibuja un pequeño ícono de paracaídas en un canvas.

        Args:
            c (tk.Canvas): canvas donde se dibujará.
        """
        # Cúpula del paracaídas (semicírculo).
        c.create_arc(5, 5, 65, 45, start=0, extent=180, fill="#1976D2", outline="#0D47A1", width=2)
        # Cuerdas.
        c.create_line(15, 25, 30, 55, fill="#616161")
        c.create_line(35, 25, 30, 55, fill="#616161")
        c.create_line(55, 25, 30, 55, fill="#616161")
        # Persona simplificada (rectángulo pequeño).
        c.create_rectangle(24, 55, 36, 65, fill="#8D6E63", outline="")

    # =====================================================================
    # GRILLA DE 6 TARJETAS DE EJERCICIOS
    # =====================================================================
    def _crear_grilla_ejercicios(self, contenido):
        """
        Construye una cuadrícula de 2 filas x 3 columnas con las tarjetas
        de los 6 ejercicios, usando los colores predefinidos.
        """
        grilla = tk.Frame(contenido, bg=self.COLOR_FONDO)
        grilla.pack(fill="x", padx=16, pady=6)
        # Configurar las 3 columnas para que se expandan uniformemente.
        for col in range(3):
            grilla.grid_columnconfigure(col, weight=1, uniform="col")

        # Por cada ejercicio, crear su tarjeta y colocarla en la grilla.
        for idx, info in enumerate(self.ejercicios_data):
            color_borde, color_claro = self.COLORES_EJERCICIOS[idx]
            tarjeta = self._tarjeta_ejercicio(grilla, info, color_borde, color_claro)
            fila, col = divmod(idx, 3)  # Convertir índice lineal a (fila, columna)
            tarjeta.grid(row=fila, column=col, padx=8, pady=8, sticky="nsew")

    def _tarjeta_ejercicio(self, parent, info, color_borde, color_claro):
        """
        Crea una tarjeta individual para un ejercicio.

        Args:
            parent: widget padre (la grilla).
            info: diccionario con los datos del ejercicio.
            color_borde: color del borde de la tarjeta.
            color_claro: color de fondo suave para la pregunta.

        Returns:
            tk.Frame: la tarjeta construida.
        """
        # Marco principal de la tarjeta con borde coloreado.
        tarjeta = tk.Frame(parent, bg=self.COLOR_TARJETA_BG,
                            highlightbackground=color_borde, highlightthickness=2)

        # ----- Fila superior: número del ejercicio + enunciado -----
        fila_top = tk.Frame(tarjeta, bg=self.COLOR_TARJETA_BG)
        fila_top.pack(fill="x", padx=12, pady=(12, 4))

        # Insignia circular con el número del ejercicio.
        badge = tk.Canvas(fila_top, width=30, height=30, bg=self.COLOR_TARJETA_BG,
                           highlightthickness=0)
        badge.pack(side="left", padx=(0, 8))
        badge.create_oval(2, 2, 28, 28, fill=color_borde, outline="")
        badge.create_text(15, 15, text=str(info["numero"]), fill="white",
                           font=("Arial", 12, "bold"))

        # Enunciado del problema.
        tk.Label(fila_top, text=info["enunciado"], bg=self.COLOR_TARJETA_BG,
                 fg=self.COLOR_TEXTO, font=("Arial", 12, "bold"), justify="left",
                 anchor="w", wraplength=230).pack(side="left", fill="x", expand=True)

        # ----- Fila de datos y diagrama -----
        fila_datos = tk.Frame(tarjeta, bg=self.COLOR_TARJETA_BG)
        fila_datos.pack(fill="x", padx=12, pady=4)

        # Columna izquierda con los datos iniciales.
        col_datos = tk.Frame(fila_datos, bg=self.COLOR_TARJETA_BG)
        col_datos.pack(side="left", anchor="n", fill="y")

        tk.Label(col_datos, text="Datos:", font=("Arial", 12, "bold"),
                 bg=self.COLOR_TARJETA_BG, fg=color_borde, anchor="w").pack(anchor="w")
        # Cada dato se muestra con un bullet y color secundario.
        for dato in info["datos"]:
            tk.Label(col_datos, text="\u2022 " + dato, font=("Arial", 12),
                     bg=self.COLOR_TARJETA_BG, fg=self.COLOR_TEXTO_SUAVE,
                     anchor="w", justify="left").pack(anchor="w")

        # Diagrama del objeto cayendo (derecha).
        diagrama = self._dibujar_diagrama(fila_datos, info)
        diagrama.pack(side="right", padx=(6, 0), anchor="n")

        # ----- Caja de pregunta (fondo coloreado) -----
        caja_pregunta = tk.Frame(tarjeta, bg=color_claro)
        caja_pregunta.pack(fill="x", padx=12, pady=(8, 12))
        tk.Label(caja_pregunta, text="\u2753", bg=color_claro, font=("Arial", 12)).pack(
            side="left", padx=(8, 4), pady=6)
        tk.Label(caja_pregunta, text="Pregunta:\n" + info["pregunta"], bg=color_claro,
                 fg=color_borde, font=("Arial", 12, "bold"), justify="left",
                 anchor="w", wraplength=210).pack(side="left", padx=(0, 8), pady=6, fill="x")

        return tarjeta

    # -------------------------------------------------------------------
    def _dibujar_diagrama(self, parent, info):
        """
        Dibuja un pequeño esquema del objeto a una altura, con opción de
        flecha de velocidad inicial y líneas de viento (resistencia).

        Args:
            parent: contenedor donde se empaquetará el canvas.
            info: diccionario con 'objeto', 'altura' y 'velocidad'.

        Returns:
            tk.Canvas: el canvas con el diagrama.
        """
        c = tk.Canvas(parent, width=110, height=150, bg=self.COLOR_TARJETA_BG,
                      highlightthickness=0)
        # Posiciones fijas: centro del objeto (cx) y coordenadas verticales.
        cx = 40
        y_obj = 30      # Posición Y del objeto
        y_ground = 128  # Línea del suelo

        # Dibujar el objeto según su tipo.
        self._dibujar_objeto(c, info["objeto"], cx, y_obj)

        # Línea punteada que conecta el objeto con el suelo.
        c.create_line(cx, y_obj + 20, cx, y_ground, dash=(4, 3), fill="#90A4AE", width=1)

        # Suelo (rectángulo marrón).
        c.create_rectangle(cx - 28, y_ground, cx + 28, y_ground + 8, fill="#8D6E63", outline="")

        # Etiqueta de altura al lado de la línea.
        c.create_text(cx + 38, (y_obj + 20 + y_ground) / 2, text=info["altura"], anchor="w",
                      font=("Arial", 12, "bold"), fill=self.COLOR_TEXTO)

        # Si hay velocidad inicial, dibujar flecha hacia abajo y el valor.
        if info["velocidad"]:
            c.create_line(cx + 14, y_obj + 2, cx + 14, y_obj + 24, fill="#E53935",
                          width=2, arrow=tk.LAST)
            c.create_text(cx + 38, y_obj + 12, text=info["velocidad"], anchor="w",
                          font=("Arial", 12, "bold"), fill="#E53935")
        return c

    def _dibujar_objeto(self, canvas, tipo, cx, cy, radio=15):
        """
        Dibuja la representación gráfica del objeto (piedra, pelota, etc.)
        y las líneas de viento que indican resistencia del aire.

        Args:
            canvas: tk.Canvas donde se pinta.
            tipo: string con el identificador del objeto.
            cx, cy: coordenadas del centro.
            radio: radio del objeto (por defecto 15 px).
        """
        if tipo == "piedra":
            # Piedra irregular (óvalo con sombra).
            canvas.create_oval(cx - radio, cy - radio * 0.8, cx + radio, cy + radio * 0.8,
                                fill="#9E9E9E", outline="#616161", width=2)
            canvas.create_oval(cx - radio * 0.4, cy - radio * 0.3, cx + radio * 0.1, cy,
                                fill="#BDBDBD", outline="")
        elif tipo == "pelota_naranja":
            # Pelota con líneas cruzadas (como de baloncesto).
            canvas.create_oval(cx - radio, cy - radio, cx + radio, cy + radio,
                                fill="#F57C00", outline="#BF360C", width=2)
            canvas.create_line(cx - radio, cy, cx + radio, cy, fill="#BF360C", width=1)
            canvas.create_line(cx, cy - radio, cx, cy + radio, fill="#BF360C", width=1)
        elif tipo == "bola_azul":
            # Esfera azul lisa.
            canvas.create_oval(cx - radio, cy - radio, cx + radio, cy + radio,
                                fill="#1E88E5", outline="#0D47A1", width=2)
        elif tipo == "pelota_verde":
            # Esfera verde con arco decorativo.
            canvas.create_oval(cx - radio, cy - radio, cx + radio, cy + radio,
                                fill="#43A047", outline="#1B5E20", width=2)
            canvas.create_arc(cx - radio, cy - radio, cx + radio, cy + radio,
                              start=20, extent=140, style="arc", outline="white", width=2)

        # Líneas de viento (comunes a todos los objetos) para indicar resistencia.
        for i, dx in enumerate((-radio - 8, -radio - 18)):
            y_linea = cy - radio * 0.3 + i * 10
            # Pequeña curva que simula flujo de aire.
            canvas.create_line(cx + dx, y_linea, cx + dx + 10, y_linea - 4,
                                cx + dx + 18, y_linea + 2, smooth=True,
                                fill="#64B5F6", width=2)

    # =====================================================================
    # NOTAS FINALES (3 franjas de color)
    # =====================================================================
    def _crear_notas_finales(self, contenido):
        """
        Crea una fila con tres tarjetas de colores que contienen notas
        adicionales o recordatorios sobre el tema.
        """
        fila_notas = tk.Frame(contenido, bg=self.COLOR_FONDO)
        fila_notas.pack(fill="x", padx=20, pady=(6, 20))

        # Definición de las tres notas: (icono, color_fondo, color_texto, texto)
        notas = [
            ("\U0001F4A1", "#FFF9C4", "#F9A825",
             "NOTA: La resistencia del aire depende de la forma del objeto, su "
             "tama\u00f1o, la velocidad y la densidad del aire."),
            ("\U0001F4A8", "#E3F2FD", "#1976D2",
             "La resistencia del aire hace que el objeto alcance una velocidad "
             "l\u00edmite (v\u2097) y caiga m\u00e1s lentamente."),
            ("\u2B50", "#F3E5F5", "#6A1B9A",
             "Estos ejercicios usan un modelo sencillo de resistencia del aire "
             "(fuerza proporcional a la velocidad)."),
        ]
        # Construir cada nota como un frame coloreado.
        for icono, bg, fg, texto in notas:
            caja = tk.Frame(fila_notas, bg=bg, highlightbackground=fg, highlightthickness=1)
            caja.pack(side="left", fill="both", expand=True, padx=6)
            fila = tk.Frame(caja, bg=bg)
            fila.pack(padx=10, pady=8)
            tk.Label(fila, text=icono, bg=bg, font=("Arial", 12)).pack(side="left", padx=(0, 8))
            tk.Label(fila, text=texto, bg=bg, fg=fg, font=("Arial", 12, "bold"),
                     wraplength=250, justify="left").pack(side="left")


# =============================================================================
# PRUEBA INDEPENDIENTE DEL MÓDULO
# =============================================================================
if __name__ == "__main__":
    # Crear la ventana principal para probar la clase de forma aislada.
    root = tk.Tk()
    root.title("Ejercicios de Ca\u00edda Libre")
    root.geometry("1300x900")

    # Frame contenedor que ocupará toda la ventana.
    contenedor = tk.Frame(root)
    contenedor.pack(fill="both", expand=True)

    # Instanciar la pantalla de ejercicios dentro del contenedor.
    app = Ejercicios(contenedor)

    # Iniciar el bucle principal de la interfaz gráfica.
    root.mainloop()