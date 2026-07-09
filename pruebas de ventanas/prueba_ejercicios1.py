# =============================================================================
# EJERCICIOS DE CAIDA LIBRE CON RESISTENCIA DEL AIRE - FACILES
# =============================================================================
# Modulo pensado para integrarse en el proyecto Caida_libre, dentro de
# interfaz/ejercicios.py, siguiendo el mismo patron que Teoria, Intro y
# AplicacionCaidaLibre: recibe un Frame (panel) y construye toda la interfaz
# dentro de el.
#
# Requiere solo la biblioteca estandar de Python: tkinter, tkinter.ttk,
# turtle y math.
#
# Nota sobre turtle: el contenido principal de esta pantalla es una hoja de
# referencia estatica (como el afiche de la imagen), asi que los 6 iconos de
# los objetos se dibujan con tkinter.Canvas (mas simple y preciso para figuras
# pequenas). Turtle SI se usa, pero donde realmente aporta algo que Canvas no
# da facilmente: una mini animacion en vivo que muestra, con las formulas de
# resistencia del aire, como un objeto cae cada vez mas lento hasta acercarse
# a su velocidad limite.
# =============================================================================

import tkinter as tk
from tkinter import ttk
import turtle
import math


class Ejercicios:
    """
    Construye la pantalla "Ejercicios de Caida Libre con Resistencia del
    Aire" dentro de un panel (Frame) padre.
    """

    def __init__(self, panel):
        self.panel = panel

        # -------------------- Paleta general --------------------
        self.COLOR_HEADER = "#12213B"
        self.COLOR_GOLD = "#F4C542"
        self.COLOR_FONDO = "#EEF1F6"
        self.COLOR_TARJETA_BG = "#FFFFFF"
        self.COLOR_TEXTO = "#1F2D3D"
        self.COLOR_TEXTO_SUAVE = "#5A6B82"

        # (borde, fondo_claro) para cada uno de los 6 ejercicios
        self.COLORES_EJERCICIOS = [
            ("#1976D2", "#E3F2FD"),  # 1 azul
            ("#2E7D32", "#E8F5E9"),  # 2 verde
            ("#F57C00", "#FFF3E0"),  # 3 naranja
            ("#6A1B9A", "#F3E5F5"),  # 4 morado
            ("#00838F", "#E0F7FA"),  # 5 teal
            ("#C2185B", "#FCE4EC"),  # 6 rosa/magenta
        ]

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

        self.crear_interfaz()

    # =====================================================================
    # INTERFAZ PRINCIPAL (canvas con scroll, igual que en Teoria)
    # =====================================================================
    def crear_interfaz(self):
        for widget in self.panel.winfo_children():
            widget.destroy()

        self.canvas = tk.Canvas(self.panel, bg=self.COLOR_FONDO, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.panel, orient="vertical", command=self.canvas.yview)

        contenido = tk.Frame(self.canvas, bg=self.COLOR_FONDO)
        contenido.bind("<Configure>",
                        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.ventana_id = self.canvas.create_window((0, 0), window=contenido, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Igual que en teoria.py: que el contenido ocupe todo el ancho
        # disponible al maximizar la ventana.
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.ventana_id, width=e.width)
        )

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._crear_encabezado(contenido)
        self._crear_intro_y_formulas(contenido)
        self._crear_vista_previa(contenido)
        self._crear_grilla_ejercicios(contenido)
        self._crear_notas_finales(contenido)

        tk.Label(contenido, text="", bg=self.COLOR_FONDO).pack(pady=10)

        # Scroll con rueda del mouse y flechas
        self.canvas.bind("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        self.canvas.bind("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))
        self.canvas.bind("<Up>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind("<Down>", lambda e: self.canvas.yview_scroll(1, "units"))
        self.canvas.focus_set()
        self.canvas.bind("<Enter>", lambda e: self.canvas.focus_set())

    # =====================================================================
    # ENCABEZADO
    # =====================================================================
    def _crear_encabezado(self, contenido):
        header = tk.Frame(contenido, bg=self.COLOR_HEADER, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        contenedor_titulo = tk.Frame(header, bg=self.COLOR_HEADER)
        contenedor_titulo.pack(expand=True)

        partes = [
            ("\u2601 ", "white"),
            ("EJERCICIOS DE ", "white"),
            ("CA\u00cdDA LIBRE", self.COLOR_GOLD),
            (" CON ", "white"),
            ("RESISTENCIA", self.COLOR_GOLD),
            (" DEL AIRE \u2013 F\u00c1CILES ", "white"),
            ("\u2601", "white"),
        ]
        for texto, color in partes:
            tk.Label(contenedor_titulo, text=texto, font=("Arial", 19, "bold"),
                     bg=self.COLOR_HEADER, fg=color).pack(side="left")

    # =====================================================================
    # CAJA DE INTRODUCCION + CAJA DE FORMULAS
    # =====================================================================
    def _crear_intro_y_formulas(self, contenido):
        fila_intro = tk.Frame(contenido, bg=self.COLOR_FONDO)
        fila_intro.pack(fill="x", padx=20, pady=(16, 6))

        # ---------------- Caja izquierda: descripcion ----------------
        caja_intro = tk.Frame(fila_intro, bg=self.COLOR_TARJETA_BG,
                               highlightbackground="#1976D2", highlightthickness=2)
        caja_intro.pack(side="left", fill="both", expand=True, padx=(0, 8))

        tk.Label(caja_intro, text="CA\u00cdDA LIBRE CON RESISTENCIA DEL AIRE",
                 font=("Arial", 12, "bold"), fg="#1976D2",
                 bg=self.COLOR_TARJETA_BG).pack(pady=(12, 6))

        fila_txt_icono = tk.Frame(caja_intro, bg=self.COLOR_TARJETA_BG)
        fila_txt_icono.pack(fill="x", padx=14)

        tk.Label(
            fila_txt_icono,
            text="Al caer, los objetos se ven afectados por la resistencia del "
                 "aire, lo que hace que su velocidad aumente cada vez m\u00e1s "
                 "lentamente hasta alcanzar una velocidad l\u00edmite (v\u2097).",
            font=("Arial", 10), bg=self.COLOR_TARJETA_BG, fg=self.COLOR_TEXTO,
            justify="left", wraplength=260,
        ).pack(side="left", anchor="n", pady=4)

        icono_paracaidas = tk.Canvas(fila_txt_icono, width=70, height=70,
                                      bg=self.COLOR_TARJETA_BG, highlightthickness=0)
        icono_paracaidas.pack(side="right", anchor="n")
        self._dibujar_paracaidas(icono_paracaidas)

        badge_g = tk.Frame(caja_intro, bg="#E8F5E9")
        badge_g.pack(fill="x", padx=14, pady=(10, 14))
        tk.Label(badge_g, text="\u2705", bg="#E8F5E9", font=("Arial", 11)).pack(
            side="left", padx=(8, 4), pady=6)
        tk.Label(badge_g, text="Aceleraci\u00f3n de la gravedad:  g = 9.8 m/s\u00b2 (hacia abajo)",
                 bg="#E8F5E9", fg="#2E7D32", font=("Arial", 10, "bold")).pack(
            side="left", pady=6)

        # ---------------- Caja derecha: formulas ----------------
        caja_formulas = tk.Frame(fila_intro, bg=self.COLOR_TARJETA_BG,
                                  highlightbackground="#6A1B9A", highlightthickness=2)
        caja_formulas.pack(side="left", fill="both", expand=True, padx=(8, 0))

        tk.Label(caja_formulas, text="F\u00d3RMULAS \u00daTILES (con resistencia del aire)",
                 font=("Arial", 12, "bold"), fg="#6A1B9A",
                 bg=self.COLOR_TARJETA_BG).pack(pady=(12, 6))

        nota_modelo = tk.Frame(caja_formulas, bg="#F3E5F5")
        nota_modelo.pack(fill="x", padx=14, pady=(0, 8))
        tk.Label(nota_modelo,
                 text="Modelo sencillo (fuerza de arrastre proporcional a la velocidad)",
                 font=("Arial", 9, "italic"), bg="#F3E5F5", fg="#6A1B9A",
                 wraplength=190, justify="left").pack(side="left", padx=8, pady=6)
        tk.Label(nota_modelo, text="k = constante\nde arrastre (> 0)",
                 font=("Arial", 8, "bold"), bg="#F3E5F5", fg="#6A1B9A",
                 justify="right").pack(side="right", padx=8)

        fila_formulas = tk.Frame(caja_formulas, bg=self.COLOR_TARJETA_BG)
        fila_formulas.pack(fill="x", padx=14, pady=(0, 14))

        self._caja_formula(fila_formulas, "#FFF3E0", "#F57C00",
                            "v(t) = v\u2097\u00b7(1 \u2212 e^(\u2212kt/m))", "Velocidad")
        self._caja_formula(fila_formulas, "#E8F5E9", "#2E7D32",
                            "y(t)=y\u2080+(v\u2097m/k)\u00b7[t+(m/k)(e^(\u2212kt/m)\u22121)]",
                            "Posici\u00f3n")
        self._caja_formula(fila_formulas, "#F3E5F5", "#6A1B9A",
                            "v\u2097 = m\u00b7g / k", "Velocidad l\u00edmite")

    def _caja_formula(self, parent, bg, fg, formula, etiqueta):
        caja = tk.Frame(parent, bg=bg, highlightbackground=fg, highlightthickness=1)
        caja.pack(side="left", fill="both", expand=True, padx=4)
        tk.Label(caja, text=formula, font=("Consolas", 9, "bold"), bg=bg,
                  fg=self.COLOR_TEXTO, wraplength=150, justify="center").pack(padx=8, pady=(10, 2))
        tk.Label(caja, text=etiqueta, font=("Arial", 9, "bold"), bg=bg, fg=fg).pack(pady=(0, 8))

    def _dibujar_paracaidas(self, c):
        c.create_arc(5, 5, 65, 45, start=0, extent=180, fill="#1976D2", outline="#0D47A1", width=2)
        c.create_line(15, 25, 30, 55, fill="#616161")
        c.create_line(35, 25, 30, 55, fill="#616161")
        c.create_line(55, 25, 30, 55, fill="#616161")
        c.create_rectangle(24, 55, 36, 65, fill="#8D6E63", outline="")

    # =====================================================================
    # VISTA PREVIA ANIMADA (turtle) - unico lugar donde usamos turtle,
    # porque aqui si aporta algo que un dibujo estatico no puede: mostrar en
    # vivo como la velocidad se va "achatando" hacia la velocidad limite.
    # =====================================================================
    def _crear_vista_previa(self, contenido):
        marco = tk.Frame(contenido, bg=self.COLOR_TARJETA_BG,
                          highlightbackground="#90A4AE", highlightthickness=1)
        marco.pack(fill="x", padx=20, pady=(0, 16))

        tk.Label(marco, text="Vista previa animada: ca\u00edda con resistencia del aire "
                             "(datos del Ejercicio 1)",
                 font=("Arial", 9, "italic"), bg=self.COLOR_TARJETA_BG,
                 fg=self.COLOR_TEXTO_SUAVE).pack(pady=(8, 2))

        self.canvas_preview = tk.Canvas(marco, width=300, height=110,
                                         bg="#F4F8FB", highlightthickness=0)
        self.canvas_preview.pack(pady=(0, 10))
        # Suelo dibujado directamente en el Canvas (coordenadas normales, pixel arriba-izq)
        self.canvas_preview.create_rectangle(15, 95, 285, 103, fill="#8D6E63", outline="")

        self._iniciar_vista_previa()

    def _iniciar_vista_previa(self):
        screen = turtle.TurtleScreen(self.canvas_preview)
        screen.bgcolor("#F4F8FB")
        screen.tracer(0)
        self.screen_preview = screen

        self.t_preview = turtle.RawTurtle(screen)
        self.t_preview.shape("circle")
        self.t_preview.shapesize(0.9)
        self.t_preview.color("#1976D2")
        self.t_preview.penup()

        # Parametros fisicos (iguales al Ejercicio 1): y0, m, k, g
        self._prev_y0 = 20.0
        self._prev_m = 1.0
        self._prev_k = 0.20
        self._prev_g = 9.8
        self._prev_vl = self._prev_m * self._prev_g / self._prev_k  # velocidad limite
        self._prev_t = 0.0

        self._animar_vista_previa()

    def _prev_posicion(self, t):
        """y(t) = y0 - vl*t + (vl*m/k)*(1 - e^(-kt/m))  (altura restante, y=0 = suelo)."""
        vl, m, k = self._prev_vl, self._prev_m, self._prev_k
        return self._prev_y0 - vl * t + (vl * m / k) * (1 - math.exp(-k * t / m))

    def _animar_vista_previa(self):
        # Si el panel ya fue reconstruido (el usuario cambio de seccion),
        # el canvas fue destruido: dejamos de programar nuevos frames.
        if not self.canvas_preview.winfo_exists():
            return

        y = self._prev_posicion(self._prev_t)
        if y <= 0:
            self._prev_t = 0.0
            y = self._prev_y0
        else:
            self._prev_t += 0.05

        # y = y0 (arriba) -> pantalla_y = 40 ; y = 0 (suelo) -> pantalla_y = -40
        pantalla_y = -40 + 80 * (y / self._prev_y0)
        self.t_preview.goto(0, pantalla_y)
        self.screen_preview.update()

        self.canvas_preview.after(40, self._animar_vista_previa)

    # =====================================================================
    # GRILLA DE 6 TARJETAS DE EJERCICIOS
    # =====================================================================
    def _crear_grilla_ejercicios(self, contenido):
        grilla = tk.Frame(contenido, bg=self.COLOR_FONDO)
        grilla.pack(fill="x", padx=16, pady=6)
        for col in range(3):
            grilla.grid_columnconfigure(col, weight=1, uniform="col")

        for idx, info in enumerate(self.ejercicios_data):
            color_borde, color_claro = self.COLORES_EJERCICIOS[idx]
            tarjeta = self._tarjeta_ejercicio(grilla, info, color_borde, color_claro)
            fila, col = divmod(idx, 3)
            tarjeta.grid(row=fila, column=col, padx=8, pady=8, sticky="nsew")

    def _tarjeta_ejercicio(self, parent, info, color_borde, color_claro):
        tarjeta = tk.Frame(parent, bg=self.COLOR_TARJETA_BG,
                            highlightbackground=color_borde, highlightthickness=2)

        fila_top = tk.Frame(tarjeta, bg=self.COLOR_TARJETA_BG)
        fila_top.pack(fill="x", padx=12, pady=(12, 4))

        badge = tk.Canvas(fila_top, width=30, height=30, bg=self.COLOR_TARJETA_BG,
                           highlightthickness=0)
        badge.pack(side="left", padx=(0, 8))
        badge.create_oval(2, 2, 28, 28, fill=color_borde, outline="")
        badge.create_text(15, 15, text=str(info["numero"]), fill="white",
                           font=("Arial", 13, "bold"))

        tk.Label(fila_top, text=info["enunciado"], bg=self.COLOR_TARJETA_BG,
                 fg=self.COLOR_TEXTO, font=("Arial", 10, "bold"), justify="left",
                 anchor="w", wraplength=230).pack(side="left", fill="x", expand=True)

        fila_datos = tk.Frame(tarjeta, bg=self.COLOR_TARJETA_BG)
        fila_datos.pack(fill="x", padx=12, pady=4)

        col_datos = tk.Frame(fila_datos, bg=self.COLOR_TARJETA_BG)
        col_datos.pack(side="left", anchor="n", fill="y")

        tk.Label(col_datos, text="Datos:", font=("Arial", 10, "bold"),
                 bg=self.COLOR_TARJETA_BG, fg=color_borde, anchor="w").pack(anchor="w")
        for dato in info["datos"]:
            tk.Label(col_datos, text="\u2022 " + dato, font=("Arial", 9),
                     bg=self.COLOR_TARJETA_BG, fg=self.COLOR_TEXTO_SUAVE,
                     anchor="w", justify="left").pack(anchor="w")

        diagrama = self._dibujar_diagrama(fila_datos, info)
        diagrama.pack(side="right", padx=(6, 0), anchor="n")

        caja_pregunta = tk.Frame(tarjeta, bg=color_claro)
        caja_pregunta.pack(fill="x", padx=12, pady=(8, 12))
        tk.Label(caja_pregunta, text="\u2753", bg=color_claro, font=("Arial", 12)).pack(
            side="left", padx=(8, 4), pady=6)
        tk.Label(caja_pregunta, text="Pregunta:\n" + info["pregunta"], bg=color_claro,
                 fg=color_borde, font=("Arial", 9, "bold"), justify="left",
                 anchor="w", wraplength=210).pack(side="left", padx=(0, 8), pady=6, fill="x")

        return tarjeta

    # -------------------------------------------------------------------
    def _dibujar_diagrama(self, parent, info):
        c = tk.Canvas(parent, width=110, height=150, bg=self.COLOR_TARJETA_BG,
                      highlightthickness=0)
        cx = 40
        y_obj = 30
        y_ground = 128

        self._dibujar_objeto(c, info["objeto"], cx, y_obj)
        c.create_line(cx, y_obj + 20, cx, y_ground, dash=(4, 3), fill="#90A4AE", width=1)
        c.create_rectangle(cx - 28, y_ground, cx + 28, y_ground + 8, fill="#8D6E63", outline="")
        c.create_text(cx + 38, (y_obj + 20 + y_ground) / 2, text=info["altura"], anchor="w",
                      font=("Arial", 10, "bold"), fill=self.COLOR_TEXTO)

        if info["velocidad"]:
            c.create_line(cx + 14, y_obj + 2, cx + 14, y_obj + 24, fill="#E53935",
                          width=2, arrow=tk.LAST)
            c.create_text(cx + 38, y_obj + 12, text=info["velocidad"], anchor="w",
                          font=("Arial", 9, "bold"), fill="#E53935")
        return c

    def _dibujar_objeto(self, canvas, tipo, cx, cy, radio=15):
        if tipo == "piedra":
            canvas.create_oval(cx - radio, cy - radio * 0.8, cx + radio, cy + radio * 0.8,
                                fill="#9E9E9E", outline="#616161", width=2)
            canvas.create_oval(cx - radio * 0.4, cy - radio * 0.3, cx + radio * 0.1, cy,
                                fill="#BDBDBD", outline="")
        elif tipo == "pelota_naranja":
            canvas.create_oval(cx - radio, cy - radio, cx + radio, cy + radio,
                                fill="#F57C00", outline="#BF360C", width=2)
            canvas.create_line(cx - radio, cy, cx + radio, cy, fill="#BF360C", width=1)
            canvas.create_line(cx, cy - radio, cx, cy + radio, fill="#BF360C", width=1)
        elif tipo == "bola_azul":
            canvas.create_oval(cx - radio, cy - radio, cx + radio, cy + radio,
                                fill="#1E88E5", outline="#0D47A1", width=2)
        elif tipo == "pelota_verde":
            canvas.create_oval(cx - radio, cy - radio, cx + radio, cy + radio,
                                fill="#43A047", outline="#1B5E20", width=2)
            canvas.create_arc(cx - radio, cy - radio, cx + radio, cy + radio,
                              start=20, extent=140, style="arc", outline="white", width=2)

        # Lineas de viento (comunes a todos los objetos)
        for i, dx in enumerate((-radio - 8, -radio - 18)):
            y_linea = cy - radio * 0.3 + i * 10
            canvas.create_line(cx + dx, y_linea, cx + dx + 10, y_linea - 4,
                                cx + dx + 18, y_linea + 2, smooth=True,
                                fill="#64B5F6", width=2)

    # =====================================================================
    # NOTAS FINALES (3 franjas de color)
    # =====================================================================
    def _crear_notas_finales(self, contenido):
        fila_notas = tk.Frame(contenido, bg=self.COLOR_FONDO)
        fila_notas.pack(fill="x", padx=20, pady=(6, 20))

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
        for icono, bg, fg, texto in notas:
            caja = tk.Frame(fila_notas, bg=bg, highlightbackground=fg, highlightthickness=1)
            caja.pack(side="left", fill="both", expand=True, padx=6)
            fila = tk.Frame(caja, bg=bg)
            fila.pack(padx=10, pady=8)
            tk.Label(fila, text=icono, bg=bg, font=("Arial", 13)).pack(side="left", padx=(0, 8))
            tk.Label(fila, text=texto, bg=bg, fg=fg, font=("Arial", 9, "bold"),
                     wraplength=250, justify="left").pack(side="left")


# =============================================================================
# PRUEBA INDEPENDIENTE DEL MODULO
# =============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ejercicios de Ca\u00edda Libre")
    root.geometry("1300x900")

    contenedor = tk.Frame(root)
    contenedor.pack(fill="both", expand=True)

    app = Ejercicios(contenedor)

    root.mainloop()