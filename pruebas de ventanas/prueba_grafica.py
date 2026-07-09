
import tkinter as tk
from tkinter import ttk
import turtle
import math


# =============================================================================
# 1. CONSTANTES / CONFIGURACION FISICA Y VISUAL
# =============================================================================

COLOR_FONDO_APP   = "#eef2f7"
COLOR_PANEL_BG    = "#ffffff"
COLOR_BORDE       = "#c7d0da"

# Colores de las 4 tarjetas del panel de informacion
TARJETA_VERDE     = ("#dff5e1", "#1a6b34")
TARJETA_AZUL      = ("#d9edfb", "#0f5f8c")
TARJETA_AMARILLA  = ("#fdf1c4", "#8a6d00")
TARJETA_MORADA    = ("#f1e0f7", "#6b1f8c")

OBJ1_COLOR = "#3fae4a"   # Objeto 1 - Verde  (caida libre, sin resistencia)
OBJ2_COLOR = "#9b4fd1"   # Objeto 2 - Morado (con resistencia del aire)

G1 = 9.8   # aceleracion Objeto 1  (m/s^2)  -> gravedad terrestre real
G2 = 2.5   # aceleracion efectiva Objeto 2  (m/s^2) -> con resistencia del aire

Y_MIN = -8.0     # metros -> limite inferior del eje Y de la grafica
T_MAX = 3.0      # segundos -> limite del eje X de la grafica

# Tiempo en el que cada objeto llega al "suelo" (y = Y_MIN)
T_IMPACTO_1 = math.sqrt(2 * abs(Y_MIN) / G1)
T_IMPACTO_2 = math.sqrt(2 * abs(Y_MIN) / G2)

# Puntos destacados que se marcan sobre la curva (igual que en la referencia)
T_MARCA_1 = 0.8
T_MARCA_2 = 1.6

# Escala de la animacion cualitativa (panel 1)
ANIM_START_Y = 160                              # altura inicial en px (turtle)
ANIM_SCALE   = 40                                # px por metro
ANIM_GROUND_Y = ANIM_START_Y - abs(Y_MIN) * ANIM_SCALE   # y del "suelo"


def posicion(t, g):
    """Posicion vertical y(t) = -1/2 * g * t^2  (caida libre desde y=0)."""
    return -0.5 * g * t * t


# =============================================================================
# 2. APLICACION PRINCIPAL
# =============================================================================

class Grafica:

    def __init__(self, panel):
        self.root = panel
        ventana = self.root.winfo_children()
        for widget in self.root.winfo_children():
            widget.destroy()
        

        ventana.title("Caida Libre - Animacion vs Grafica de Datos")

        self.root.configure(bg=COLOR_FONDO_APP)
        ventana.resizable(False, False)

        self._configurar_estilos()

        # Estado de la animacion
        self.animando = False
        self.t_actual = 0.0
        self.siguiente_marca = 0.0
        self.after_id = None

        self._construir_layout()
        self._panel_animacion()
        self._panel_grafica()
        self._panel_info()

        self.root.after(50, self._centrar_ventana)

    # -------------------------------------------------------------------
    def _configurar_estilos(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(
            "Accion.TButton",
            font=("Arial", 10, "bold"),
            padding=6,
            background="#2f7a3d",
            foreground="white",
        )
        style.map("Accion.TButton",
                  background=[("active", "#245c2e")])

    # -------------------------------------------------------------------
    def _construir_layout(self):
        titulo = tk.Label(
            self.root,
            text="SIMULADOR DE CAIDA LIBRE",
            font=("Arial", 18, "bold"),
            bg=COLOR_FONDO_APP,
            fg="#1c2b3a",
        )
        titulo.grid(row=0, column=0, columnspan=3, pady=(14, 2))

        subtitulo = tk.Label(
            self.root,
            text="De la animacion cualitativa a la cuantificacion exacta con datos",
            font=("Arial", 10, "italic"),
            bg=COLOR_FONDO_APP,
            fg="#556270",
        )
        subtitulo.grid(row=1, column=0, columnspan=3, pady=(0, 10))

        self.frame1 = tk.Frame(self.root, bg=COLOR_PANEL_BG, bd=1,
                                relief="solid", highlightbackground=COLOR_BORDE)
        self.frame2 = tk.Frame(self.root, bg=COLOR_PANEL_BG, bd=1,
                                relief="solid", highlightbackground=COLOR_BORDE)
        self.frame3 = tk.Frame(self.root, bg=COLOR_PANEL_BG, bd=1,
                                relief="solid", highlightbackground=COLOR_BORDE)

        self.frame1.grid(row=2, column=0, padx=(14, 7), pady=6, sticky="n")
        self.frame2.grid(row=2, column=1, padx=7, pady=6, sticky="n")
        self.frame3.grid(row=2, column=2, padx=(7, 14), pady=6, sticky="n")

        pie = tk.Label(
            self.root,
            text="De ANIMACION (rapida, superficial)   \u2192   GRAFICA DE DATOS (metrica, precisa)",
            font=("Arial", 10, "bold"),
            bg=COLOR_FONDO_APP,
            fg="#2f5233",
        )
        pie.grid(row=3, column=0, columnspan=3, pady=(4, 14))

    # =====================================================================
    # PANEL 1 - VISTA CUALITATIVA DE LA ANIMACION (turtle)
    # =====================================================================
    def _panel_animacion(self):
        header = tk.Label(
            self.frame1, text="VISTA CUALITATIVA\nDE LA ANIMACION",
            font=("Arial", 12, "bold"), bg=TARJETA_VERDE[0], fg=TARJETA_VERDE[1],
            pady=10, justify="center",
        )
        header.pack(fill="x")

        canvas = tk.Canvas(self.frame1, width=280, height=400,
                            bg="#cfe8fb", highlightthickness=0)
        canvas.pack(padx=10, pady=10)

        screen = turtle.TurtleScreen(canvas)
        screen.bgcolor("#cfe8fb")
        screen.tracer(0)
        self.screen_anim = screen

        # --- Torre / edificio de referencia -----------------------------
        torre = turtle.RawTurtle(screen)
        torre.hideturtle()
        torre.speed(0)
        torre.penup()
        torre.color("#7d8b99", "#7d8b99")
        torre.goto(-140, ANIM_GROUND_Y)
        torre.pendown()
        torre.begin_fill()
        for _, _ in [(0, 0)] * 1:
            torre.goto(-100, ANIM_GROUND_Y)
            torre.goto(-100, ANIM_START_Y)
            torre.goto(-140, ANIM_START_Y)
            torre.goto(-140, ANIM_GROUND_Y)
        torre.end_fill()
        # ventanitas
        torre.color("#fbe98a", "#fbe98a")
        y_ventana = ANIM_START_Y - 25
        while y_ventana > ANIM_GROUND_Y + 15:
            torre.penup()
            torre.goto(-130, y_ventana)
            torre.pendown()
            torre.begin_fill()
            for _ in range(2):
                torre.forward(10)
                torre.left(90)
                torre.forward(10)
                torre.left(90)
            torre.end_fill()
            y_ventana -= 35
        # linea de suelo
        torre.penup()
        torre.color("#4a5a68")
        torre.goto(-140, ANIM_GROUND_Y)
        torre.pendown()
        torre.pensize(3)
        torre.goto(140, ANIM_GROUND_Y)
        torre.penup()

        # --- Bolas (Objeto 1 y Objeto 2) --------------------------------
        self.bola1 = turtle.RawTurtle(screen)
        self.bola1.shape("circle")
        self.bola1.shapesize(1.2)
        self.bola1.color(OBJ1_COLOR)
        self.bola1.penup()
        self.bola1.goto(-40, ANIM_START_Y)

        self.bola2 = turtle.RawTurtle(screen)
        self.bola2.shape("circle")
        self.bola2.shapesize(1.2)
        self.bola2.color(OBJ2_COLOR)
        self.bola2.penup()
        self.bola2.goto(40, ANIM_START_Y)

        # turtle auxiliar para escribir marcas de tiempo (t=0s, 0.5s, ...)
        self.escritor = turtle.RawTurtle(screen)
        self.escritor.hideturtle()
        self.escritor.penup()
        self.escritor.color("#20303d")

        screen.update()

        self.lbl_tiempo = tk.Label(
            self.frame1, text="t = 0.00 s", font=("Arial", 12, "bold"),
            bg=COLOR_PANEL_BG, fg="#20303d",
        )
        self.lbl_tiempo.pack(pady=(0, 4))

        self.btn_animar = ttk.Button(
            self.frame1, text="\u25B6  Iniciar animacion",
            style="Accion.TButton", command=self.iniciar_animacion,
        )
        self.btn_animar.pack(pady=(0, 8))

        nota = tk.Label(
            self.frame1,
            text="Dificil medir diferencias sutiles\na simple vista",
            font=("Arial", 9, "italic"), bg=COLOR_PANEL_BG, fg="#666666",
            justify="center",
        )
        nota.pack(pady=(0, 12))

    # -------------------------------------------------------------------
    def iniciar_animacion(self):
        if self.animando:
            return
        # reiniciar estado
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
        self.bola1.clearstamps()
        self.bola2.clearstamps()
        self.escritor.clear()
        self.bola1.goto(-40, ANIM_START_Y)
        self.bola2.goto(40, ANIM_START_Y)
        self.t_actual = 0.0
        self.siguiente_marca = 0.0
        self.animando = True
        self.btn_animar.state(["disabled"])
        self._paso_animacion()

    # -------------------------------------------------------------------
    def _paso_animacion(self):
        t = self.t_actual
        dt = 0.03

        # --- Objeto 1 ---
        if t <= T_IMPACTO_1:
            y1 = ANIM_START_Y + posicion(t, G1) * ANIM_SCALE
        else:
            y1 = ANIM_GROUND_Y
        self.bola1.sety(y1)

        # --- Objeto 2 ---
        if t <= T_IMPACTO_2:
            y2 = ANIM_START_Y + posicion(t, G2) * ANIM_SCALE
        else:
            y2 = ANIM_GROUND_Y
        self.bola2.sety(y2)

        # Marcas ("fotografias") cada 0.5 s, como en la vista compuesta
        if t + 1e-9 >= self.siguiente_marca:
            self.bola1.stamp()
            self.bola2.stamp()
            self.escritor.goto(70, (y1 + y2) / 2)
            self.escritor.write(f"{self.siguiente_marca:.1f}s",
                                 font=("Arial", 9, "bold"))
            self.siguiente_marca += 0.5

        self.lbl_tiempo.config(text=f"t = {t:.2f} s")

        # marcadores en vivo sobre la grafica del panel 2
        self._actualizar_marcadores_grafica(t)

        self.screen_anim.update()

        if t <= max(T_IMPACTO_1, T_IMPACTO_2):
            self.t_actual += dt
            self.after_id = self.root.after(30, self._paso_animacion)
        else:
            self.animando = False
            self.btn_animar.state(["!disabled"])

    # =====================================================================
    # PANEL 2 - GRAFICA DE DATOS DE CAIDA LIBRE (Canvas + math)
    # =====================================================================
    def _panel_grafica(self):
        header = tk.Label(
            self.frame2, text="GRAFICA DE DATOS DE CAIDA LIBRE",
            font=("Arial", 12, "bold"), bg="#d9edfb", fg="#0f5f8c",
            pady=10,
        )
        header.pack(fill="x")

        self.ancho_g = 560
        self.alto_g = 400
        self.margen_izq = 65
        self.margen_der = 25
        self.margen_sup = 70
        self.margen_inf = 55
        self.plot_w = self.ancho_g - self.margen_izq - self.margen_der
        self.plot_h = self.alto_g - self.margen_sup - self.margen_inf

        self.canvas_g = tk.Canvas(self.frame2, width=self.ancho_g, height=self.alto_g,
                                   bg="#ffffff", highlightthickness=0)
        self.canvas_g.pack(padx=10, pady=10)

        self._dibujar_ejes()
        self._dibujar_curvas()
        self._dibujar_anotaciones()
        self._dibujar_leyenda()

        # marcadores "en vivo" que se mueven durante la animacion
        p0 = self._t_a_px(0)
        y0 = self._y_a_px(0)
        self.marker1 = self.canvas_g.create_oval(p0 - 5, y0 - 5, p0 + 5, y0 + 5,
                                                   fill=OBJ1_COLOR, outline="#20303d")
        self.marker2 = self.canvas_g.create_oval(p0 - 5, y0 - 5, p0 + 5, y0 + 5,
                                                   fill=OBJ2_COLOR, outline="#20303d")

        leyenda_txt = tk.Label(
            self.frame2,
            text="COMO INTERPRETAR ESTA GRAFICA:  el eje Y es la posicion vertical (m)\n"
                 "y el eje X es el tiempo (s). La inclinacion (pendiente) de la curva\n"
                 "en cada punto es la velocidad instantanea del objeto.",
            font=("Arial", 9), bg=COLOR_PANEL_BG, fg="#444444", justify="left",
        )
        leyenda_txt.pack(padx=10, pady=(0, 10), anchor="w")

    # -------------------------------------------------------------------
    def _t_a_px(self, t):
        return self.margen_izq + (t / T_MAX) * self.plot_w

    def _y_a_px(self, y):
        return self.margen_sup + ((-y) / abs(Y_MIN)) * self.plot_h

    # -------------------------------------------------------------------
    def _dibujar_ejes(self):
        c = self.canvas_g
        x0 = self.margen_izq
        y0 = self.margen_sup
        x1 = self.margen_izq + self.plot_w
        y1 = self.margen_sup + self.plot_h

        # cuadricula vertical (cada 0.5 s)
        t = 0.0
        while t <= T_MAX + 1e-9:
            px = self._t_a_px(t)
            c.create_line(px, y0, px, y1, fill="#e3e7eb")
            c.create_text(px, y1 + 14, text=f"{t:.1f}", font=("Arial", 8), fill="#555")
            t += 0.5

        # cuadricula horizontal (cada -1 m)
        y = 0.0
        while y >= Y_MIN - 1e-9:
            py = self._y_a_px(y)
            c.create_line(x0, py, x1, py, fill="#e3e7eb")
            c.create_text(x0 - 14, py, text=f"{y:.0f}", font=("Arial", 8), fill="#555")
            y -= 1.0

        # ejes principales con flecha
        c.create_line(x0, y1, x1 + 8, y1, fill="#20303d", width=2, arrow=tk.LAST)
        c.create_line(x0, y1, x0, y0 - 8, fill="#20303d", width=2, arrow=tk.LAST)

        c.create_text((x0 + x1) / 2, y1 + 32, text="TIEMPO (t) en segundos",
                       font=("Arial", 9, "bold"), fill="#20303d")
        c.create_text(x0 - 45, (y0 + y1) / 2, text="POSICION\nVERTICAL\n(y) en m",
                       font=("Arial", 8, "bold"), fill="#20303d", justify="center")

    # -------------------------------------------------------------------
    def _dibujar_curvas(self):
        c = self.canvas_g
        dt = 0.02

        def puntos_curva(g, t_impacto):
            pts = []
            t = 0.0
            while t < t_impacto:
                pts.extend([self._t_a_px(t), self._y_a_px(posicion(t, g))])
                t += dt
            pts.extend([self._t_a_px(t_impacto), self._y_a_px(Y_MIN)])
            return pts

        pts1 = puntos_curva(G1, T_IMPACTO_1)
        pts2 = puntos_curva(G2, T_IMPACTO_2)

        c.create_line(*pts1, fill=OBJ1_COLOR, width=3)
        c.create_line(*pts2, fill=OBJ2_COLOR, width=3)

        # puntos destacados con su etiqueta (t, y)
        for t_m, g, color in ((T_MARCA_1, G1, OBJ1_COLOR), (T_MARCA_2, G2, OBJ2_COLOR)):
            y_m = posicion(t_m, g)
            px, py = self._t_a_px(t_m), self._y_a_px(y_m)
            c.create_oval(px - 4, py - 4, px + 4, py + 4, fill=color, outline="#20303d")
            c.create_text(px + 34, py - 12, text=f"({t_m:.1f}s, {y_m:.1f}m)",
                          font=("Arial", 8, "bold"), fill="#20303d")

    # -------------------------------------------------------------------
    def _dibujar_anotaciones(self):
        c = self.canvas_g

        # caja "pendiente = velocidad instantanea"
        c.create_rectangle(self.margen_izq + self.plot_w * 0.30,
                            self.margen_sup - 8,
                            self.margen_izq + self.plot_w * 0.30 + 150,
                            self.margen_sup + 14,
                            fill="#fdf1c4", outline="#c9a63a")
        c.create_text(self.margen_izq + self.plot_w * 0.30 + 75,
                      self.margen_sup + 3,
                      text="pendiente = velocidad\ninstantanea",
                      font=("Arial", 7, "bold"), fill="#8a6d00", justify="center")

        # "mayor pendiente" apuntando a la curva verde
        tx, ty = self._t_a_px(0.35), self._y_a_px(posicion(0.35, G1)) - 30
        c.create_text(tx, ty, text="MAYOR PENDIENTE\nCae mas rapido (Objeto 1)",
                      font=("Arial", 7, "bold"), fill="#1a6b34", justify="left", anchor="w")
        c.create_line(tx + 10, ty + 12, self._t_a_px(0.5), self._y_a_px(posicion(0.5, G1)),
                      fill="#1a6b34", arrow=tk.LAST)

        # "menor pendiente" apuntando a la curva morada
        tx2, ty2 = self._t_a_px(1.9), self._y_a_px(posicion(1.9, G2)) - 45
        c.create_text(tx2, ty2, text="MENOR PENDIENTE\nCae mas lento (Objeto 2)",
                      font=("Arial", 7, "bold"), fill="#6b1f8c", justify="left", anchor="w")
        c.create_line(tx2 + 10, ty2 + 12, self._t_a_px(2.0), self._y_a_px(posicion(2.0, G2)),
                      fill="#6b1f8c", arrow=tk.LAST)

    # -------------------------------------------------------------------
    def _dibujar_leyenda(self):
        c = self.canvas_g
        lx = self.ancho_g - self.margen_der - 5
        ly = self.margen_sup - 45

        c.create_oval(lx - 150, ly - 5, lx - 140, ly + 5, fill=OBJ1_COLOR, outline="")
        c.create_text(lx - 135, ly, text="Objeto 1 (Verde)", anchor="w",
                      font=("Arial", 8, "bold"), fill="#20303d")

        c.create_oval(lx - 150, ly + 15, lx - 140, ly + 25, fill=OBJ2_COLOR, outline="")
        c.create_text(lx - 135, ly + 20, text="Objeto 2 (Morado)", anchor="w",
                      font=("Arial", 8, "bold"), fill="#20303d")

    # -------------------------------------------------------------------
    def _actualizar_marcadores_grafica(self, t):
        t1 = min(t, T_IMPACTO_1)
        t2 = min(t, T_IMPACTO_2)
        px1, py1 = self._t_a_px(t1), self._y_a_px(posicion(t1, G1))
        px2, py2 = self._t_a_px(t2), self._y_a_px(posicion(t2, G2))
        self.canvas_g.coords(self.marker1, px1 - 5, py1 - 5, px1 + 5, py1 + 5)
        self.canvas_g.coords(self.marker2, px2 - 5, py2 - 5, px2 + 5, py2 + 5)

    # =====================================================================
    # PANEL 3 - PARA QUE SIRVE LA GRAFICA (tkinter / ttk)
    # =====================================================================
    def _panel_info(self):
        header = tk.Label(
            self.frame3, text="\u00bfPARA QUE SIRVE\nLA GRAFICA?",
            font=("Arial", 12, "bold"), bg="#e7e9ee", fg="#1c2b3a",
            pady=10, justify="center",
        )
        header.pack(fill="x")

        contenedor = tk.Frame(self.frame3, bg=COLOR_PANEL_BG)
        contenedor.pack(padx=12, pady=10)

        tarjetas = [
            ("1", TARJETA_VERDE, "CUANTIFICACION EXACTA",
             "Mide la posicion y el tiempo de cada objeto en intervalos "
             "precisos, imposible de percibir a simple vista."),
            ("2", TARJETA_AZUL, "CALCULO DE VELOCIDAD Y ACELERACION",
             "La forma y la pendiente de la curva permiten calcular la "
             "velocidad instantanea y la aceleracion en cualquier punto."),
            ("3", TARJETA_AMARILLA, "COMPARACION DIRECTA",
             "Revela diferencias sutiles en la trayectoria y la "
             "aceleracion entre los dos objetos."),
            ("4", TARJETA_MORADA, "PREDICCION Y ANALISIS",
             "Define matematicamente el movimiento, permitiendo predecir "
             "la posicion futura y analizar la fisica del fenomeno."),
        ]

        for numero, (bg, fg), titulo, texto in tarjetas:
            self._crear_tarjeta_info(contenedor, numero, bg, fg, titulo, texto)

    # -------------------------------------------------------------------
    def _crear_tarjeta_info(self, parent, numero, bg, fg, titulo, texto):
        tarjeta = tk.Frame(parent, bg=bg, bd=0, highlightthickness=0)
        tarjeta.pack(fill="x", pady=6)

        badge = tk.Canvas(tarjeta, width=34, height=34, bg=bg, highlightthickness=0)
        badge.grid(row=0, column=0, rowspan=2, padx=(10, 8), pady=10, sticky="n")
        badge.create_oval(2, 2, 32, 32, fill="#ffffff", outline=fg, width=2)
        badge.create_text(17, 17, text=numero, font=("Arial", 13, "bold"), fill=fg)

        lbl_titulo = tk.Label(tarjeta, text=titulo, font=("Arial", 10, "bold"),
                               bg=bg, fg=fg, justify="left", anchor="w",
                               wraplength=250)
        lbl_titulo.grid(row=0, column=1, sticky="w", pady=(10, 0))

        lbl_texto = tk.Label(tarjeta, text=texto, font=("Arial", 9),
                              bg=bg, fg="#333333", justify="left", anchor="w",
                              wraplength=250)
        lbl_texto.grid(row=1, column=1, sticky="w", pady=(2, 10))

    # -------------------------------------------------------------------
    def _centrar_ventana(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 3
        self.root.geometry(f"+{x}+{y}")


# =============================================================================
# 3. PUNTO DE ENTRADA
# =============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simulación de Caída Libre - Comparativa")
    root.geometry("1200x850")
    root.configure(bg="#050B14") # Fondo de la ventana principal
    panel_principal = tk.Frame(root, bg="#050B14")
    panel_principal.pack(fill="both", expand=True)
    app = Grafica(panel_principal)
    root.mainloop()