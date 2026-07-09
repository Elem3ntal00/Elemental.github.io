import tkinter as tk


class Teoria:
    """
    Clase que construye la sección de teoría dentro de un
    panel padre. Muestra definiciones, fórmulas y ejemplos
    en tarjetas visualmente atractivas.
    """

    def __init__(self, panel):
        """
        Inicializa la interfaz dentro del panel proporcionado.

        Args:
            panel (tk.Frame): Frame donde se incrustará la teoría.
        """
        self.panel = panel

        # Paleta de colores moderna para el fondo y texto
        self.COLOR_FONDO = "#F2F6FC"           # azul muy claro
        self.COLOR_TEXTO = "#1E2A38"           # azul oscuro
        self.COLOR_TITULO_PRINCIPAL = "#0D47A1"  # azul intenso

        # Coleccion de esquemas de color para las tarjetas (rotan).
        # Reordenados y ampliados para que tarjetas consecutivas nunca
        # compartan la misma familia de color (antes las 2 primeras
        # eran ambas azules y se veian casi iguales).
        self.COLORES_TARJETAS = [
            {"bg": "#FFFFFF", "titulo_bg": "#1565C0", "titulo_fg": "#FFFFFF", "borde": "#90CAF9"},  # azul intenso
            {"bg": "#FFF8E1", "titulo_bg": "#F57C00", "titulo_fg": "#FFFFFF", "borde": "#FFE082"},  # naranja
            {"bg": "#F3E5F5", "titulo_bg": "#6A1B9A", "titulo_fg": "#FFFFFF", "borde": "#CE93D8"},  # morado
            {"bg": "#E8F5E9", "titulo_bg": "#2E7D32", "titulo_fg": "#FFFFFF", "borde": "#A5D6A7"},  # verde
            {"bg": "#FFEBEE", "titulo_bg": "#C62828", "titulo_fg": "#FFFFFF", "borde": "#EF9A9A"},  # rojo coral
            {"bg": "#E0F7FA", "titulo_bg": "#00695C", "titulo_fg": "#FFFFFF", "borde": "#80CBC4"},  # verde azulado
            {"bg": "#E8EAF6", "titulo_bg": "#283593", "titulo_fg": "#FFFFFF", "borde": "#9FA8DA"},  # indigo (nuevo)
            {"bg": "#FCE4EC", "titulo_bg": "#AD1457", "titulo_fg": "#FFFFFF", "borde": "#F48FB1"},  # rosa (nuevo)
            {"bg": "#F0F7FF", "titulo_bg": "#1976D2", "titulo_fg": "#FFFFFF", "borde": "#90CAF9"},  # azul claro
        ]
        self.indice_color = 0  # para rotar entre tarjetas

        # Construir toda la interfaz gráfica
        self.crear_interfaz()

    # ==================================================

    def crear_interfaz(self):
        """
        Construye la interfaz completa: canvas con scroll,
        título principal y todas las tarjetas de contenido.
        Agrega soporte para rueda del ratón y flechas del teclado.
        """
        # Limpiar el panel por si se recarga la vista
        for widget in self.panel.winfo_children():
            widget.destroy()

        # Crear Canvas (área desplazable) y su barra de scroll
        self.canvas = tk.Canvas(self.panel, bg=self.COLOR_FONDO, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.panel, orient="vertical", command=self.canvas.yview)

        # Frame interno que contendrá todos los widgets (se mueve con el scroll)
        contenido = tk.Frame(self.canvas, bg=self.COLOR_FONDO)
        contenido.bind("<Configure>",
                       lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Ubicar el frame dentro del canvas
        self.ventana_id = self.canvas.create_window((0, 0), window=contenido, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Cuando el canvas cambia de tamaño (p. ej. al maximizar la ventana),
        # estiramos el frame interno para que ocupe todo el ancho disponible,
        # dejando solo el espacio de la barra de scroll a la derecha.
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.ventana_id, width=e.width)
        )

        # Empaquetar canvas y scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ==================================================
        # ENCABEZADO PRINCIPAL
        # ==================================================
        # Barra azul con el título principal
        encabezado = tk.Frame(contenido, bg="#0D47A1", height=80)
        encabezado.pack(fill="x", pady=(0, 20))
        encabezado.pack_propagate(False)  # mantener altura fija

        titulo_ppal = tk.Label(
            encabezado,
            text="📘   CAÍDA LIBRE",
            font=("Arial", 28, "bold"),
            bg="#0D47A1",
            fg="white"
        )
        titulo_ppal.pack(expand=True)  # centrado verticalmente

        # Subtítulo debajo del encabezado
        subtitulo = tk.Label(
            contenido,
            text="Teoría interactiva para estudiantes de secundaria y universidad",
            font=("Arial", 14, "italic"),
            bg=self.COLOR_FONDO,
            fg="#455A64"
        )
        subtitulo.pack(pady=(0, 20))

        # ==================================================
        # TARJETAS DE CONTENIDO (cada una con su color)
        # ==================================================
        self.agregar_tarjeta(contenido,
            "¿Qué es la caída libre?",
            "La caída libre es un movimiento en el que un cuerpo "
            "desciende únicamente por la acción de la gravedad, "
            "despreciando la resistencia del aire.\n\n"
            "En condiciones ideales, todos los objetos caen con la "
            "misma aceleración, sin importar su masa."
        )

        self.agregar_tarjeta(contenido,
            "Características principales",
            "• La aceleración permanece constante (g = 9.81 m/s²).\n\n"
            "• Todos los cuerpos caen con la misma aceleración.\n\n"
            "• No se considera la resistencia del aire.\n\n"
            "• Es un movimiento rectilíneo uniformemente acelerado (MRUA)."
        )

        self.agregar_tarjeta(contenido,
            "Magnitudes importantes",
            "Altura inicial (h₀)\n"
            "Tiempo transcurrido (t)\n"
            "Velocidad en cada instante (v)\n"
            "Aceleración de la gravedad (g = 9.81 m/s²)"
        )

        self.agregar_tarjeta_formulas(contenido)

        self.agregar_tarjeta(contenido,
            "Ejemplo resuelto",
            "Un objeto se deja caer desde una altura de 80 metros.\n\n"
            "• Datos: h = 80 m, g = 9.81 m/s², v₀ = 0.\n"
            "• Tiempo de caída:\n"
            "  t = √(2 × 80 / 9.81) ≈ √16.31 ≈ 4.04 s\n"
            "• Velocidad al llegar al suelo:\n"
            "  v = 0 + 9.81 × 4.04 ≈ 39.6 m/s (≈ 143 km/h)"
        )

        self.agregar_tarjeta(contenido,
            "Aplicaciones en la vida real",
            "• Ingeniería civil (cálculo de estructuras).\n"
            "• Física (estudio del movimiento).\n"
            "• Astronomía (trayectorias de cuerpos celestes).\n"
            "• Deportes extremos (paracaidismo, salto BASE).\n"
            "• Diseño de sistemas de seguridad (airbags, ascensores)."
        )

        self.agregar_tarjeta(contenido,
            "Conclusión",
            "El estudio de la caída libre permite comprender cómo "
            "actúa la gravedad sobre los cuerpos y constituye uno "
            "de los fundamentos de la Mecánica Clásica. "
            "Gracias a Galileo y Newton, hoy podemos predecir "
            "con precisión estos movimientos."
        )

        # Pequeño espacio al final
        tk.Label(contenido, text="", bg=self.COLOR_FONDO).pack(pady=10)

        # ==================================================
        # CONFIGURACIÓN DE SCROLL CON RUEDA Y FLECHAS
        # ==================================================
        # Vincular eventos de ratón y teclado al canvas
        self.canvas.bind("<MouseWheel>", self._desplazar_con_rueda_windows)
        self.canvas.bind("<Button-4>", self._desplazar_con_rueda_linux)
        self.canvas.bind("<Button-5>", self._desplazar_con_rueda_linux)
        self.canvas.bind("<Up>", self._desplazar_arriba)
        self.canvas.bind("<Down>", self._desplazar_abajo)

        # Forzar el foco en el canvas para que las flechas funcionen sin clic previo
        self.canvas.focus_set()
        self.canvas.bind("<Enter>", lambda e: self.canvas.focus_set())

    # ==================================================
    # MÉTODOS PARA MANEJAR EL SCROLL
    # ==================================================

    def _desplazar_con_rueda_windows(self, event):
        """Desplaza el contenido al girar la rueda del ratón en Windows."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _desplazar_con_rueda_linux(self, event):
        """Desplaza el contenido al girar la rueda del ratón en Linux/macOS."""
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

    def _desplazar_arriba(self, event):
        """Sube el scroll al presionar la flecha arriba."""
        self.canvas.yview_scroll(-1, "units")

    def _desplazar_abajo(self, event):
        """Baja el scroll al presionar la flecha abajo."""
        self.canvas.yview_scroll(1, "units")

    # ==================================================

    def agregar_tarjeta(self, padre, titulo, texto):
        """
        Crea una tarjeta estilizada con sombra simulada, borde,
        título colorido y texto centrado. Cada tarjeta rota su color.

        Args:
            padre (tk.Frame): Frame contenedor donde se añadirá la tarjeta.
            titulo (str): Título de la tarjeta.
            texto (str): Contenido textual de la tarjeta.
        """
        # Seleccionar el siguiente color de la paleta circular
        color_info = self.COLORES_TARJETAS[self.indice_color % len(self.COLORES_TARJETAS)]
        self.indice_color += 1

        # Frame exterior que simula una sombra (color más oscuro)
        sombra = tk.Frame(padre, bg="#B0BEC5", bd=0)
        sombra.pack(fill="x", padx=30, pady=12, ipadx=2, ipady=2)

        # Frame interior (tarjeta real) con borde sutil
        tarjeta = tk.Frame(
            sombra,
            bg=color_info["bg"],
            bd=0,
            highlightbackground=color_info["borde"],
            highlightthickness=1
        )
        tarjeta.pack(padx=2, pady=2, fill="both", expand=True)

        # Franja de acento a la izquierda con el color del titulo, para
        # dar mas fuerza visual a cada tarjeta
        franja = tk.Frame(tarjeta, bg=color_info["titulo_bg"], width=6)
        franja.pack(side="left", fill="y")

        cuerpo = tk.Frame(tarjeta, bg=color_info["bg"])
        cuerpo.pack(side="left", fill="both", expand=True)

        # Título de la tarjeta con fondo coloreado
        titulo_lbl = tk.Label(
            cuerpo,
            text=titulo,
            font=("Arial", 16, "bold"),
            bg=color_info["titulo_bg"],
            fg=color_info["titulo_fg"],
            pady=10
        )
        titulo_lbl.pack(fill="x")  # ocupa todo el ancho

        # Contenido textual, centrado y con fuente grande
        texto_lbl = tk.Label(
            cuerpo,
            text=texto,
            font=("Arial", 13),
            bg=color_info["bg"],
            fg=self.COLOR_TEXTO,
            justify="center",
            wraplength=750,
            padx=25,
            pady=15
        )
        texto_lbl.pack(fill="both", expand=True)

        # El wraplength se recalcula cuando la tarjeta cambia de ancho
        # (por ejemplo al maximizar la ventana), para que el texto use
        # bien todo el espacio disponible en vez de quedar angosto.
        def _ajustar_wrap(event, lbl=texto_lbl):
            lbl.config(wraplength=max(300, event.width - 60))
        cuerpo.bind("<Configure>", _ajustar_wrap)

        # Efecto hover: la sombra se oscurece ligeramente al pasar el ratón
        def on_enter(e):
            sombra.config(bg="#90A4AE")
        def on_leave(e):
            sombra.config(bg="#B0BEC5")

        # Asociar el efecto a todos los elementos de la tarjeta
        tarjeta.bind("<Enter>", on_enter)
        tarjeta.bind("<Leave>", on_leave)
        titulo_lbl.bind("<Enter>", on_enter)
        titulo_lbl.bind("<Leave>", on_leave)
        texto_lbl.bind("<Enter>", on_enter)
        texto_lbl.bind("<Leave>", on_leave)

    # ==================================================

    def agregar_tarjeta_formulas(self, padre):
        """
        Tarjeta especial para las 'Formulas fundamentales'. En vez de
        amontonar las 3 formulas en un solo bloque de texto (dificil de
        leer), cada una va en su propia caja de color con: nombre,
        formula y una frase simple de que significa - igual que las
        cajas de 'Pregunta:' en el modulo de Ejercicios.
        """
        color_info = self.COLORES_TARJETAS[self.indice_color % len(self.COLORES_TARJETAS)]
        self.indice_color += 1

        sombra = tk.Frame(padre, bg="#B0BEC5", bd=0)
        sombra.pack(fill="x", padx=30, pady=12, ipadx=2, ipady=2)

        tarjeta = tk.Frame(
            sombra, bg=color_info["bg"], bd=0,
            highlightbackground=color_info["borde"], highlightthickness=1,
        )
        tarjeta.pack(padx=2, pady=2, fill="both", expand=True)

        franja = tk.Frame(tarjeta, bg=color_info["titulo_bg"], width=6)
        franja.pack(side="left", fill="y")

        cuerpo = tk.Frame(tarjeta, bg=color_info["bg"])
        cuerpo.pack(side="left", fill="both", expand=True)

        titulo_lbl = tk.Label(
            cuerpo, text="Fórmulas fundamentales", font=("Arial", 16, "bold"),
            bg=color_info["titulo_bg"], fg=color_info["titulo_fg"], pady=10,
        )
        titulo_lbl.pack(fill="x")

        fila_formulas = tk.Frame(cuerpo, bg=color_info["bg"])
        fila_formulas.pack(fill="x", padx=25, pady=20)

        # (fondo, color de texto, nombre, formula, que significa)
        formulas = [
            ("#FFF3E0", "#F57C00", "Velocidad",
             "v = v\u2080 + g\u00b7t",
             "Qu\u00e9 tan r\u00e1pido cae en el instante t"),
            ("#E8F5E9", "#2E7D32", "Posici\u00f3n",
             "h = h\u2080 + v\u2080\u00b7t \u2212 \u00bd\u00b7g\u00b7t\u00b2",
             "A qu\u00e9 altura est\u00e1 en el instante t"),
            ("#E3F2FD", "#1976D2", "Tiempo de ca\u00edda",
             "t = \u221a(2h / g)",
             "Cu\u00e1nto tarda en llegar al suelo desde una altura h"),
        ]

        cajas = []
        for bg, fg, nombre, formula, descripcion in formulas:
            caja = tk.Frame(fila_formulas, bg=bg, highlightbackground=fg,
                             highlightthickness=1)
            caja.pack(side="left", fill="both", expand=True, padx=8)
            tk.Label(caja, text=nombre, font=("Arial", 13, "bold"), bg=bg,
                     fg=fg).pack(pady=(14, 4))
            lbl_formula = tk.Label(caja, text=formula, font=("Arial", 15, "bold"),
                                    bg=bg, fg=self.COLOR_TEXTO, wraplength=200,
                                    justify="center")
            lbl_formula.pack(padx=10, pady=2)
            lbl_desc = tk.Label(caja, text=descripcion, font=("Arial", 10), bg=bg,
                                 fg=fg, wraplength=200, justify="center")
            lbl_desc.pack(padx=10, pady=(4, 14))
            cajas.append((caja, lbl_formula, lbl_desc))

        # Si las cajas quedan muy angostas (ventana chica) se apilan una
        # sobre otra en vez de comprimirse hasta ser ilegibles.
        def _ajustar_disposicion(event, cajas=cajas, fila=fila_formulas):
            angosto = event.width < 560
            for caja, lbl_formula, lbl_desc in cajas:
                caja.pack_forget()
                if angosto:
                    caja.pack(fill="x", padx=8, pady=4)
                else:
                    caja.pack(side="left", fill="both", expand=True, padx=8)
                ancho_wrap = max(160, event.width - 60) if angosto else 200
                lbl_formula.config(wraplength=ancho_wrap)
                lbl_desc.config(wraplength=ancho_wrap)
        fila_formulas.bind("<Configure>", _ajustar_disposicion)

        def on_enter(e):
            sombra.config(bg="#90A4AE")
        def on_leave(e):
            sombra.config(bg="#B0BEC5")
        tarjeta.bind("<Enter>", on_enter)
        tarjeta.bind("<Leave>", on_leave)
        titulo_lbl.bind("<Enter>", on_enter)
        titulo_lbl.bind("<Leave>", on_leave)


# ==================================================
# BLOQUE PARA PRUEBAS DIRECTAS DEL MÓDULO
# ==================================================
if __name__ == "__main__":
    # Crear ventana independiente para probar la teoría
    root = tk.Tk()
    root.title("Teoría Caída Libre")
    root.geometry("900x700")
    contenedor = tk.Frame(root)
    contenedor.pack(fill="both", expand=True)
    app = Teoria(contenedor)
    root.mainloop()