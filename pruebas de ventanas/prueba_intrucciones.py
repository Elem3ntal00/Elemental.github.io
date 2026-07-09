# Importación de bibliotecas necesarias
import tkinter as tk                # Para crear la interfaz gráfica principal
from tkinter import ttk              # Para botones con estilo más moderno
import turtle                        # Para animaciones gráficas sobre un canvas


class Intro:
    """
    Clase que gestiona la pantalla de introducción/tutorial interactivo.
    Muestra un mapa de secciones animado con Turtle (estilo "guia de inicio")
    y texto descriptivo en Tkinter, siguiendo el diseño: cabecera azul marino,
    mapa en cuadricula 2x2 con el nodo activo resaltado, tortuga recorriendo
    un camino punteado, y panel derecho blanco con botones tipo "pill".
    """

    def __init__(self, panel, al_finalizar=None):
        """
        Constructor: recibe el panel (Frame) donde se construira toda la
        interfaz.

        Args:
            panel (tk.Frame): Frame donde se incrustara la introduccion.
            al_finalizar (callable, opcional): funcion que se ejecuta al
                terminar el tutorial (boton "Empezar" o "Saltar
                Introduccion"). Por ejemplo, desde menu.py:
                    Intro(self.panel, al_finalizar=self.teoria)
                Si no se proporciona, simplemente se limpia el panel.
        """
        self.panel = panel
        self.al_finalizar = al_finalizar

        # -------------------- Paleta de colores --------------------
        self.COLOR_HEADER = "#1B2A4A"          # cabecera azul marino
        self.COLOR_ACCENT = "#1ABC9C"          # verde-azulado de acento
        self.COLOR_ACCENT_GLOW = "#BDF3E6"     # halo suave detras del nodo activo
        self.COLOR_ACCENT_HOVER = "#149174"    # hover del boton "Siguiente"
        self.COLOR_FONDO = "#FFFFFF"           # fondo general (canvas y panel)
        self.COLOR_LINEA_GUIA = "#D7DEE7"      # cruz guia y separadores
        self.COLOR_NODO_INACTIVO = "#C9D3DE"   # borde de los nodos no activos
        self.COLOR_TEXTO_NODO_INACTIVO = "#33465E"
        self.COLOR_TITULO = "#1B2A4A"          # titulo del paso (texto oscuro)
        self.COLOR_TEXTO_CUERPO = "#5A6B82"    # parrafo descriptivo
        self.COLOR_ANTERIOR_BG = "#E4E8EE"     # boton "Anterior" (gris claro)
        self.COLOR_ANTERIOR_FG = "#98A2B3"

        # Lista de pasos del tutorial: cada paso tiene título y descripción
        self.pasos = [
            {"titulo": "¡Bienvenido!",
             "texto": "Este programa te ayudará a dominar el tema de forma "
                      "interactiva.\n\nA continuación, te daremos un breve "
                      "recorrido por las 4 secciones principales para que "
                      "sepas cómo manejarlo."},
            {"titulo": "Paso 1: Sección: Teoría",
             "texto": "Aquí encontrarás todo el fundamento conceptual. \n\n"
                      "Ideal para leer antes de empezar a experimentar. "
                      "Incluye definiciones, fórmulas y ejemplos clave."},
            {"titulo": "Paso 2: Sección: Simulación",
             "texto": "¡La teoría en acción! \n\nEn esta pestaña podrás "
                      "modificar variables en tiempo real y ver cómo se "
                      "comporta el sistema de forma dinámica."},
            {"titulo": "Paso 3: Sección: Gráfica",
             "texto": "Visualización de datos de última generación.\n\n"
                      "Aquí se generarán los gráficos detallados basados en "
                      "tus simulaciones para que analices el comportamiento "
                      "matemático."},
            {"titulo": "Paso 4: Sección: Ejercicios",
             "texto": "¿Listo para el reto?\n\nPreguntas y problemas "
                      "prácticos con sistema de puntuación para que evalúes "
                      "lo aprendido."},
        ]
        self.paso_actual = 0   # Comienza en el primer paso (índice 0)

        # Nombres cortos que se dibujan dentro de cada nodo del mapa
        self.nombres_secciones = {
            1: "1. Teoría",
            2: "2. Simulación",
            3: "3. Gráfica",
            4: "4. Ejercicios",
        }
        # Posicion (x, y) de cada nodo, en cuadricula 2x2 alrededor del centro.
        # El paso 0 (Bienvenida) no tiene nodo propio: se muestra el mapa
        # completo sin ningun nodo resaltado.
        self.posiciones_secciones = {
            1: (-120, 80),   # Teoría      (arriba-izquierda)
            2: (120, 80),    # Simulación  (arriba-derecha)
            3: (-120, -80),  # Gráfica     (abajo-izquierda)
            4: (120, -80),   # Ejercicios  (abajo-derecha)
        }

        self._configurar_estilos()
        self.crear_interfaz()
        self.inicializar_turtle()
        self.actualizar_pantalla()

    # =====================================================================
    def _configurar_estilos(self):
        """Define los estilos ttk para los botones tipo 'pill'."""
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Anterior.TButton",
            font=("Arial", 12, "bold"),
            background=self.COLOR_ANTERIOR_BG,
            foreground=self.COLOR_ANTERIOR_FG,
            padding=(20, 10),
            borderwidth=0,
        )
        style.map(
            "Anterior.TButton",
            background=[("disabled", self.COLOR_ANTERIOR_BG)],
            foreground=[("disabled", self.COLOR_ANTERIOR_FG)],
        )

        style.configure(
            "Siguiente.TButton",
            font=("Arial", 12, "bold"),
            background=self.COLOR_ACCENT,
            foreground="white",
            padding=(20, 10),
            borderwidth=0,
        )
        style.map(
            "Siguiente.TButton",
            background=[("active", self.COLOR_ACCENT_HOVER)],
        )

    # =====================================================================
    def crear_interfaz(self):
        """
        Crea todos los elementos de la interfaz gráfica:
          - Cabecera azul marino con icono y titulo.
          - Canvas izquierdo para Turtle (mapa de secciones).
          - Panel derecho con titulo, descripcion y botones.
        """
        # Limpiar cualquier widget existente en el panel (por si se reconstruye)
        for widget in self.panel.winfo_children():
            widget.destroy()

        # Contenedor propio: evitamos tocar el bg del 'panel' compartido
        # (asi no afecta a las demas secciones del menu si vuelven a usarlo).
        self.contenedor = tk.Frame(self.panel, bg=self.COLOR_FONDO)
        self.contenedor.pack(fill="both", expand=True)

        # ---- CABECERA ----
        self.frame_header = tk.Frame(self.contenedor, bg=self.COLOR_HEADER, height=64)
        self.frame_header.pack(side="top", fill="x")
        self.frame_header.pack_propagate(False)

        icono = tk.Label(
            self.frame_header, text="📘", font=("Arial", 22),
            bg=self.COLOR_HEADER, fg=self.COLOR_ACCENT,
        )
        icono.pack(side="left", padx=(22, 10))

        titulo_header = tk.Label(
            self.frame_header, text="Guía de Inicio - Simulador de Caída Libre",
            font=("Helvetica", 15, "bold"), bg=self.COLOR_HEADER, fg="white",
        )
        titulo_header.pack(side="left")

        # ---- CUERPO (mapa + panel derecho) ----
        self.frame_cuerpo = tk.Frame(self.contenedor, bg=self.COLOR_FONDO)
        self.frame_cuerpo.pack(side="top", fill="both", expand=True)

        # ---- PANEL IZQUIERDO: CANVAS PARA TURTLE ----
        self.canvas = tk.Canvas(
            self.frame_cuerpo,
            width=450, height=460,
            bg=self.COLOR_FONDO,
            highlightthickness=0,
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Separador vertical sutil entre el mapa y el panel de texto
        divisor = tk.Frame(self.frame_cuerpo, bg=self.COLOR_LINEA_GUIA, width=1)
        divisor.pack(side=tk.LEFT, fill=tk.Y)

        # ---- PANEL DERECHO: INFORMACIÓN TEXTUAL Y BOTONES ----
        self.frame_derecho = tk.Frame(
            self.frame_cuerpo,
            bg=self.COLOR_FONDO,
            width=420,
        )
        self.frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Etiqueta para el título del paso actual
        self.lbl_titulo = tk.Label(
            self.frame_derecho,
            text="",
            font=("Helvetica", 19, "bold"),
            fg=self.COLOR_TITULO,
            bg=self.COLOR_FONDO,
            justify=tk.LEFT,
        )
        self.lbl_titulo.pack(padx=34, pady=(40, 14), anchor="w")

        # Etiqueta para el texto descriptivo del paso
        self.lbl_texto = tk.Label(
            self.frame_derecho,
            text="",
            font=("Helvetica", 12),
            fg=self.COLOR_TEXTO_CUERPO,
            bg=self.COLOR_FONDO,
            justify=tk.LEFT,
            wraplength=340,
        )
        self.lbl_texto.pack(padx=34, pady=(0, 20), anchor="w")

        # ---- BOTONES DE NAVEGACIÓN ----
        self.frame_botones = tk.Frame(self.frame_derecho, bg=self.COLOR_FONDO)
        self.frame_botones.pack(side=tk.BOTTOM, fill=tk.X, padx=34, pady=(10, 6))

        self.btn_atras = ttk.Button(
            self.frame_botones, text="Anterior",
            style="Anterior.TButton", command=self.atras,
        )
        self.btn_atras.pack(side=tk.LEFT)

        self.btn_siguiente = ttk.Button(
            self.frame_botones, text="Siguiente",
            style="Siguiente.TButton", command=self.siguiente,
        )
        self.btn_siguiente.pack(side=tk.RIGHT)

        # Enlace centrado para saltar la introducción
        self.btn_saltar = tk.Button(
            self.frame_derecho,
            text="Saltar Introducción ✕",
            font=("Helvetica", 9, "underline"),
            bg=self.COLOR_FONDO,
            fg="#8A94A6",
            bd=0,
            activebackground=self.COLOR_FONDO,
            activeforeground=self.COLOR_ACCENT_HOVER,
            cursor="hand2",
            command=self.finalizar_intro,
        )
        self.btn_saltar.pack(side=tk.BOTTOM, pady=(0, 22))

    # =====================================================================
    def inicializar_turtle(self):
        """Configura el entorno de Turtle sobre el canvas de Tkinter."""
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.bgcolor(self.COLOR_FONDO)

        self.t = turtle.RawTurtle(self.screen)
        self.t.hideturtle()
        self.t.speed(0)

    # -------------------------------------------------------------------
    def _circulo_centrado(self, x, y, radio, color, relleno=False):
        """Dibuja con self.t un circulo centrado exactamente en (x, y)."""
        self.t.penup()
        self.t.setheading(0)
        self.t.goto(x, y - radio)
        self.t.pendown()
        self.t.color(color)
        if relleno:
            self.t.begin_fill()
        self.t.circle(radio)
        if relleno:
            self.t.end_fill()
        self.t.penup()

    # -------------------------------------------------------------------
    def dibujar_mapa_estatico(self):
        """
        Dibuja la cruz guia central y los 4 nodos de seccion. El nodo que
        corresponde al paso actual se resalta con relleno de color y un
        halo exterior; los demas se muestran como circulos vacios en gris.
        """
        t = self.t
        t.clear()
        t.hideturtle()

        # --- Cruz guia de fondo (conecta visualmente los 4 nodos) ---
        t.pensize(1)
        t.color(self.COLOR_LINEA_GUIA)
        t.penup(); t.goto(-170, 0); t.pendown(); t.goto(170, 0)
        t.penup(); t.goto(0, -150); t.pendown(); t.goto(0, 150)
        t.penup()

        # Punto central
        self._circulo_centrado(0, 0, 4, self.COLOR_LINEA_GUIA, relleno=True)

        # --- Nodos de seccion ---
        for paso_idx, (x, y) in self.posiciones_secciones.items():
            activo = (paso_idx == self.paso_actual)

            if activo:
                # Halo suave detras del nodo activo
                self._circulo_centrado(x, y, 48, self.COLOR_ACCENT_GLOW)
                # Nodo relleno de color de acento
                t.pensize(2)
                self._circulo_centrado(x, y, 42, self.COLOR_ACCENT, relleno=True)
                color_texto = "white"
            else:
                t.pensize(2)
                self._circulo_centrado(x, y, 42, self.COLOR_NODO_INACTIVO)
                color_texto = self.COLOR_TEXTO_NODO_INACTIVO

            t.penup()
            t.goto(x, y - 6)
            t.color(color_texto)
            t.write(self.nombres_secciones[paso_idx], align="center",
                    font=("Arial", 10, "bold"))
        t.penup()

    # -------------------------------------------------------------------
    def _linea_punteada(self, x0, y0, x1, y1, color, segmento=9, hueco=7):
        """Dibuja (y anima, gracias a la velocidad de la tortuga) una
        linea punteada desde (x0,y0) hasta (x1,y1)."""
        t = self.t
        t.penup()
        t.goto(x0, y0)
        t.setheading(t.towards(x1, y1))
        t.color(color)
        t.pensize(3)

        distancia_total = t.distance(x1, y1)
        recorrido = 0.0
        dibujando = True
        while recorrido < distancia_total:
            paso = min(segmento if dibujando else hueco, distancia_total - recorrido)
            if dibujando:
                t.pendown()
            else:
                t.penup()
            t.forward(paso)
            recorrido += paso
            dibujando = not dibujando
        t.penup()

    # -------------------------------------------------------------------
    def animar_tortuga(self, paso):
        """
        Redibuja el mapa resaltando el nodo del paso actual y anima una
        tortuga que recorre un camino punteado desde el centro hasta
        quedar junto al nodo activo. En el paso de bienvenida (0) no hay
        nodo propio, asi que la tortuga permanece oculta.
        """
        self.dibujar_mapa_estatico()

        if paso not in self.posiciones_secciones:
            self.t.hideturtle()
            return

        x, y = self.posiciones_secciones[paso]
        # Punto de destino: cerca del nodo, sin llegar a su centro
        destino_x, destino_y = x * 0.72, y * 0.72

        self.t.shape("turtle")
        self.t.speed(8)
        self.t.showturtle()
        self._linea_punteada(0, 0, destino_x, destino_y, self.COLOR_ACCENT)
        self.t.setheading(self.t.towards(x, y))

    # =====================================================================
    def actualizar_pantalla(self):
        """
        Refresca el texto del panel derecho según el paso actual y
        actualiza el estado de los botones de navegación.
        También lanza la animación correspondiente.
        """
        info_paso = self.pasos[self.paso_actual]
        self.lbl_titulo.config(text=info_paso["titulo"])
        self.lbl_texto.config(text=info_paso["texto"])

        if self.paso_actual == 0:
            self.btn_atras.state(["disabled"])
        else:
            self.btn_atras.state(["!disabled"])

        if self.paso_actual == len(self.pasos) - 1:
            self.btn_siguiente.config(text="¡Empezar!")
        else:
            self.btn_siguiente.config(text="Siguiente")

        self.animar_tortuga(self.paso_actual)

    def siguiente(self):
        """
        Avanza al siguiente paso del tutorial o, si es el último,
        finaliza la introducción y carga el programa principal.
        """
        if self.paso_actual < len(self.pasos) - 1:
            self.paso_actual += 1
            self.actualizar_pantalla()
        else:
            self.finalizar_intro()

    def atras(self):
        """Retrocede al paso anterior si no estamos en el primero."""
        if self.paso_actual > 0:
            self.paso_actual -= 1
            self.actualizar_pantalla()

    def finalizar_intro(self):
        """
        Termina la introduccion. Si se paso una funcion 'al_finalizar' al
        crear la clase (por ejemplo Intro(self.panel, al_finalizar=self.teoria)
        en menu.py), se invoca esa funcion para continuar hacia la siguiente
        pantalla. Si no se paso ninguna, simplemente se limpia el panel.
        """
        if callable(self.al_finalizar):
            self.al_finalizar()
        else:
            for widget in self.panel.winfo_children():
                widget.destroy()
            tk.Label(
                self.panel, text="Introducción finalizada.",
                font=("Arial", 16), bg="white",
            ).pack(expand=True)


# ---- EJECUCIÓN DEL PROGRAMA (prueba independiente del modulo) ----
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Introducción")
    root.geometry("900x560")

    panel_principal = tk.Frame(root)
    panel_principal.pack(fill="both", expand=True)

    app = Intro(panel_principal)

    root.mainloop()