import tkinter as tk
from tkinter import ttk
import turtle
import math
import random
import time
from datetime import datetime

# Intenta importar sonido (solo Windows sin librerías externas)
try:
    import winsound
    SONIDO_DISPONIBLE = True
except ImportError:
    SONIDO_DISPONIBLE = False

# =====================================================
# CLASE PRINCIPAL
# =====================================================
class SimuladorBienvenida:
    def __init__(self):
        self.raiz = tk.Tk()
        self.raiz.title("Bienvenido al Simulador de Caída Libre")
        self.raiz.geometry("1000x680")
        self.raiz.resizable(False, False)
        self.raiz.configure(bg="#2c3e50")

        # Frame para el canvas de turtle
        self.frame_turtle = tk.Frame(self.raiz, width=800, height=650, bg="black")
        self.frame_turtle.pack(side=tk.LEFT, padx=(10, 0), pady=10)

        # Canvas de turtle
        self.canvas = tk.Canvas(self.frame_turtle, width=800, height=650)
        self.canvas.pack()
        self.pantalla = turtle.TurtleScreen(self.canvas)
        self.pantalla.bgcolor("#87CEEB")  # color inicial, se cubre con degradado

        # Panel lateral con ttk
        self.panel = tk.Frame(self.raiz, width=180, height=650, bg="#2c3e50")
        self.panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        self.panel.pack_propagate(False)

        # Estilo ttk
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("TButton", font=("Arial", 11), padding=8)
        estilo.configure("TLabel", background="#2c3e50", foreground="white", font=("Arial", 10))

        ttk.Label(self.panel, text="SIMULADOR\nEDUCATIVO",
                  font=("Arial", 14, "bold"), justify=tk.CENTER).pack(pady=(30, 20))

        ttk.Label(self.panel, text="Caída libre\ncon resistencia\nopcional",
                  justify=tk.CENTER).pack(pady=10)

        self.boton_iniciar = ttk.Button(self.panel, text="▶  Iniciar simulación",
                                        command=self.iniciar_simulacion)
        self.boton_iniciar.pack(pady=20)

        ttk.Label(self.panel, text="Universidad\nProyecto Educativo",
                  justify=tk.CENTER).pack(side=tk.BOTTOM, pady=20)

        # Variables de la animación
        self.lapiz = turtle.RawTurtle(self.pantalla)
        self.lapiz.hideturtle()
        self.lapiz.speed(0)

        self.pelota = turtle.RawTurtle(self.pantalla)
        self.pelota.shape("circle")
        self.pelota.shapesize(1.6)
        self.pelota.penup()

        # Estado de la animación
        self.animacion_activa = True
        self.altura = 240
        self.velocidad = 0
        self.g = 9.81

        # Hojas
        self.hojas = []
        for _ in range(30):
            self.hojas.append([
                random.randint(-380, 380),
                random.randint(-20, 260),
                random.uniform(0.3, 1.0),
                random.randint(0, 360),
                random.uniform(0.5, 1.5)   # velocidad de caída
            ])

        # Partículas de luz
        self.particulas = []
        for _ in range(40):
            self.particulas.append([
                random.randint(-380, 380),
                random.randint(-160, 260),
                random.uniform(1, 2.5),     # tamaño
                random.uniform(0, 2*math.pi), # ángulo
                random.uniform(0.3, 1.0),   # velocidad
                random.randint(180, 255)    # opacidad
            ])

        # Nubes
        self.nubes = [
            {"x": -350, "y": 220, "vel": 0.3},
            {"x": -100, "y": 180, "vel": 0.2},
            {"x": 150, "y": 240, "vel": -0.25}
        ]

        # Texto animado (efecto máquina de escribir)
        self.texto_completo = [
            ("BIENVENIDO AL", 160, 20, "#2e7d32", True),
            ("SIMULADOR INTERACTIVO", 120, 30, "#1b5e20", True),
            ("DE CAÍDA LIBRE", 75, 32, "#388e3c", True),
            ("Explora la Física de forma interactiva", 20, 18, "#444444", False),
            ("Universidad • Proyecto Educativo", -10, 15, "#666666", False)
        ]
        self.indice_texto = 0
        self.letra_actual = 0
        self.tiempo_ultima_letra = 0

        # Fecha
        self.fecha_str = datetime.now().strftime("%d/%m/%Y   %H:%M:%S")

        # Sonido de bienvenida
        if SONIDO_DISPONIBLE:
            try:
                winsound.PlaySound("SystemWelcome", winsound.SND_ALIAS)
            except:
                pass

        # Iniciar bucle de animación
        self.actualizar()

    # ---------- DIBUJOS BÁSICOS ----------
    def circulo(self, x, y, r, color, relleno=True):
        self.lapiz.penup()
        self.lapiz.goto(x, y - r)
        self.lapiz.color(color)
        if relleno:
            self.lapiz.begin_fill()
        self.lapiz.circle(r)
        if relleno:
            self.lapiz.end_fill()

    def rectangulo(self, x, y, w, h, color):
        self.lapiz.penup()
        self.lapiz.goto(x, y)
        self.lapiz.color(color)
        self.lapiz.begin_fill()
        for _ in range(2):
            self.lapiz.forward(w)
            self.lapiz.right(90)
            self.lapiz.forward(h)
            self.lapiz.right(90)
        self.lapiz.end_fill()

    def escribir(self, texto, x, y, tam, color="black", negrita=True):
        self.lapiz.penup()
        self.lapiz.goto(x, y)
        self.lapiz.color(color)
        estilo = "bold" if negrita else "normal"
        self.lapiz.write(texto, align="center", font=("Arial", tam, estilo))

    # ---------- ELEMENTOS DECORATIVOS ----------
    def dibujar_degradado(self):
        """Degradado del cielo (azul claro a blanco)."""
        self.lapiz.penup()
        self.lapiz.goto(-400, 320)
        self.lapiz.pendown()
        for i in range(150):
            y = 320 - i * 2
            # Interpolar entre azul cielo y blanco
            r = 135 + int(120 * i / 150)
            g = 206 + int(49 * i / 150)
            b = 235 - int(40 * i / 150)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.lapiz.color(color)
            self.lapiz.penup()
            self.lapiz.goto(-400, y)
            self.lapiz.pendown()
            self.lapiz.forward(800)
        self.lapiz.penup()

    def dibujar_sol(self, x, y, angulo):
        """Sol con rayos giratorios."""
        self.circulo(x, y, 40, "#FFD93D")
        self.lapiz.penup()
        self.lapiz.goto(x, y)
        self.lapiz.color("#FFD93D")
        self.lapiz.pensize(3)
        for i in range(12):
            rad = math.radians(angulo + i * 30)
            self.lapiz.penup()
            self.lapiz.goto(x + 38 * math.cos(rad), y + 38 * math.sin(rad))
            self.lapiz.pendown()
            self.lapiz.goto(x + 55 * math.cos(rad), y + 55 * math.sin(rad))
        self.lapiz.pensize(1)

    def dibujar_nube(self, x, y):
        """Nube formada por círculos."""
        self.circulo(x, y, 20, "white")
        self.circulo(x + 25, y + 8, 25, "white")
        self.circulo(x + 50, y, 20, "white")
        self.circulo(x + 15, y - 8, 16, "white")
        self.circulo(x + 40, y - 8, 16, "white")

    def dibujar_arbol(self, x, y):
        """Árbol más detallado con tronco texturizado."""
        # Tronco con degradado marrón
        self.rectangulo(x, y, 25, 120, "#6b3e1b")
        self.lapiz.color("#8b5a2b")
        self.lapiz.penup()
        self.lapiz.goto(x + 8, y)
        self.lapiz.pendown()
        self.lapiz.goto(x + 8, y + 80)
        # Ramas principales
        self.lapiz.pensize(4)
        self.lapiz.color("#5c3a1e")
        self.lapiz.penup()
        self.lapiz.goto(x + 12, y + 100)
        self.lapiz.pendown()
        self.lapiz.goto(x - 30, y + 150)
        self.lapiz.penup()
        self.lapiz.goto(x + 12, y + 110)
        self.lapiz.pendown()
        self.lapiz.goto(x + 50, y + 160)
        self.lapiz.pensize(1)
        # Follaje con sombras
        for dx, dy, r, color in [
            (-35, 130, 35, "#2e7d32"),
            (10, 140, 40, "#388e3c"),
            (50, 120, 30, "#2e7d32"),
            (-5, 100, 35, "#4caf50"),
            (-25, 170, 25, "#1b5e20"),
            (40, 170, 25, "#1b5e20"),
            (10, 175, 30, "#2e7d32")
        ]:
            self.circulo(x + dx, y + dy, r, color)

    def dibujar_cesped_flores(self):
        """Césped con pequeños círculos de colores (flores)."""
        # Franja de césped
        self.rectangulo(-400, -180, 800, 140, "#7ac943")
        # Flores
        self.lapiz.penup()
        colores_flor = ["#FF69B4", "#FFD700", "#FF6347", "#DA70D6", "#FFA500"]
        for _ in range(40):
            x = random.randint(-380, 380)
            y = random.randint(-180, -120)
            color = random.choice(colores_flor)
            self.circulo(x, y, 4, color)
            self.circulo(x, y, 2, "yellow")

    def dibujar_esfera_3d(self, x, y, radio):
        """Esfera con sombreado y punto de luz."""
        # Sombra en el suelo (elipse)
        if y < -100:
            ancho_sombra = radio * 1.8 * (abs(y + 100) / 150)
            if ancho_sombra > 0:
                self.lapiz.penup()
                self.lapiz.goto(x, -175)
                self.lapiz.color("#555555")
                self.lapiz.begin_fill()
                self.lapiz.setheading(0)
                self.lapiz.circle(ancho_sombra, 90)
                self.lapiz.left(90)
                self.lapiz.circle(ancho_sombra, 90)
                self.lapiz.left(90)
                self.lapiz.circle(ancho_sombra, 90)
                self.lapiz.left(90)
                self.lapiz.circle(ancho_sombra, 90)
                self.lapiz.end_fill()

        # Esfera principal
        self.pelota.color("#4CAF50")
        self.pelota.goto(x, y)
        # Efecto 3D: dibujar una luna creciente blanca simulando brillo
        self.lapiz.penup()
        self.lapiz.goto(x - radio*0.3, y + radio*0.3)
        self.lapiz.color("white")
        self.lapiz.begin_fill()
        self.lapiz.setheading(60)
        self.lapiz.circle(radio*0.4, 120)
        self.lapiz.setheading(240)
        self.lapiz.circle(radio*1.2, -120)
        self.lapiz.end_fill()

    # ---------- ANIMACIÓN PRINCIPAL ----------
    def actualizar(self):
        if not self.animacion_activa:
            return

        self.lapiz.clear()

        # Degradado de fondo (solo la primera vez o mover?)
        self.dibujar_degradado()

        # Sol con rotación
        angulo_sol = (time.time() * 20) % 360
        self.dibujar_sol(340, 220, angulo_sol)

        # Nubes en movimiento
        for nube in self.nubes:
            nube["x"] += nube["vel"]
            if nube["x"] > 450:
                nube["x"] = -450
            elif nube["x"] < -450:
                nube["x"] = 450
            self.dibujar_nube(nube["x"], nube["y"])

        # Árbol y césped
        self.dibujar_arbol(270, -180)
        self.dibujar_cesped_flores()

        # Efecto máquina de escribir para el título
        if self.indice_texto < len(self.texto_completo):
            texto_completo, y, tam, color, negrita = self.texto_completo[self.indice_texto]
            if self.letra_actual < len(texto_completo):
                if time.time() - self.tiempo_ultima_letra > 0.05:
                    self.letra_actual += 1
                    self.tiempo_ultima_letra = time.time()
                texto_parcial = texto_completo[:self.letra_actual]
                self.escribir(texto_parcial, 0, y, tam, color, negrita)
            else:
                # Mostrar completo y pasar al siguiente texto
                self.escribir(texto_completo, 0, y, tam, color, negrita)
                if time.time() - self.tiempo_ultima_letra > 0.8:  # pausa entre líneas
                    self.indice_texto += 1
                    self.letra_actual = 0
                    self.tiempo_ultima_letra = time.time()
        else:
            # Una vez terminado, mostrar todo fijo
            for texto, y, tam, color, negrita in self.texto_completo:
                self.escribir(texto, 0, y, tam, color, negrita)

        # Fecha
        self.escribir(self.fecha_str, 320, -295, 12, "#444444", False)

        # Hojas cayendo con efecto de viento
        for h in self.hojas:
            self.dibujar_hoja(h[0], h[1], h[3])
            h[1] -= h[4]  # caída
            h[0] += math.sin(time.time() * 2 + h[2]) * 0.9  # oscilación lateral
            h[3] += 4  # rotación
            if h[1] < -180:
                h[1] = 260
                h[0] = random.randint(-400, 400)
                h[4] = random.uniform(0.3, 1.0)

        # Partículas de luz (brillo flotante)
        for p in self.particulas:
            x, y, tam, ang, vel, alpha = p
            x += math.cos(ang) * vel * 0.5
            y += math.sin(ang) * vel * 0.5
            p[3] += 0.02  # cambio de dirección lento
            # Mantener dentro de pantalla
            if x < -400: x = 400
            if x > 400: x = -400
            if y < -200: y = 260
            if y > 280: y = -200
            p[0], p[1] = x, y
            color = f"#{alpha:02x}{alpha:02x}00"  # tono amarillento
            self.circulo(x, y, tam*0.8, color)

        # Física de la pelota
        self.velocidad += self.g * 0.06
        self.altura -= self.velocidad * 0.18
        if self.altura < -150:
            self.altura = 240
            self.velocidad = 0

        # Dibujar pelota 3D
        self.dibujar_esfera_3d(230, self.altura, 18)

        self.pantalla.update()
        self.raiz.after(20, self.actualizar)

    def dibujar_hoja(self, x, y, angulo):
        self.lapiz.penup()
        self.lapiz.goto(x, y)
        self.lapiz.setheading(angulo)
        self.lapiz.color("#5cb85c")
        self.lapiz.begin_fill()
        for _ in range(2):
            self.lapiz.circle(8, 90)
            self.lapiz.left(90)
        self.lapiz.end_fill()

    def iniciar_simulacion(self):
        """Función placeholder para cuando se pulse el botón."""
        print("¡Iniciando simulación completa!")
        # Aquí podrías abrir otra ventana o cambiar de escena.
        # Por ahora solo detenemos la animación de bienvenida.
        self.animacion_activa = False
        self.boton_iniciar.config(text="Simulación iniciada", state="disabled")

    def ejecutar(self):
        self.raiz.mainloop()

# =====================================================
if __name__ == "__main__":
    app = SimuladorBienvenida()
    app.ejecutar()