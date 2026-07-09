import tkinter as tk
from tkinter import ttk
import turtle
import math
import random
import time
from datetime import datetime


# =====================================================
# CLASE PRINCIPAL
# =====================================================
class Bienvenida:
    def __init__(self):
        self.raiz = tk.Tk()
        self.raiz.title("Bienvenido al Simulador de Caída Libre")
        self.raiz.geometry("1000x680")
        self.raiz.resizable(False, False)
        self.raiz.configure(bg="#1e2c3a")

        # Marco del canvas turtle
        self.marco = tk.Frame(self.raiz, width=800, height=650, bg="black")
        self.marco.pack(side=tk.LEFT, padx=(10, 0), pady=10)
        self.canvas = tk.Canvas(self.marco, width=800, height=650, highlightthickness=0)
        self.canvas.pack()
        self.pantalla = turtle.TurtleScreen(self.canvas)
        self.pantalla.bgcolor("#e0f7fa")  # color base, luego se pinta encima

        # Panel lateral
        self.panel = tk.Frame(self.raiz, width=180, height=650, bg="#1e2c3a")
        self.panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        self.panel.pack_propagate(False)

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("TButton", font=("Segoe UI", 11), padding=8)
        estilo.configure("TLabel", background="#1e2c3a", foreground="white",
                         font=("Segoe UI", 10))

        ttk.Label(self.panel, text="SIMULADOR\nEDUCATIVO",
                  font=("Segoe UI", 14, "bold"), justify=tk.CENTER).pack(pady=(30, 20))
        ttk.Label(self.panel, text="Caída libre\ncon animación\nde bienvenida",
                  justify=tk.CENTER).pack(pady=10)
        self.boton = ttk.Button(self.panel, text="▶  Iniciar simulación",
                                command=self.iniciar)
        self.boton.pack(pady=20)
        ttk.Label(self.panel, text="Universidad\nProyecto Educativo",
                  justify=tk.CENTER).pack(side=tk.BOTTOM, pady=20)

        # Turtle para dibujar
        self.lapiz = turtle.RawTurtle(self.pantalla)
        self.lapiz.hideturtle()
        self.lapiz.speed(0)

        # Pelota
        self.pelota = turtle.RawTurtle(self.pantalla)
        self.pelota.shape("circle")
        self.pelota.shapesize(1.5)
        self.pelota.penup()

        # Variables de animación
        self.activo = True
        self.altura = 240
        self.velocidad = 0
        self.gravedad = 9.81
        self.texto_indice = 0
        self.letra_indice = 0
        self.tiempo_letra = 0
        self.textos = [
            ("BIENVENIDO AL", 160, 20, "#1565c0"),
            ("SIMULADOR INTERACTIVO", 120, 30, "#0d47a1"),
            ("DE CAÍDA LIBRE", 75, 32, "#1976d2"),
            ("Explora la Física de forma interactiva", 20, 18, "#555555"),
            ("Universidad • Proyecto Educativo", -10, 15, "#777777"),
        ]
        self.fecha = datetime.now().strftime("%d/%m/%Y   %H:%M:%S")

        # Nubes: posición x, y, velocidad
        self.nubes = [
            {"x": -350, "y": 220, "v": 0.4},
            {"x": 0, "y": 190, "v": -0.3},
            {"x": 250, "y": 240, "v": 0.5}
        ]

        # Hojas: x, y, velocidad caída, ángulo, velocidad angular, fase viento
        self.hojas = []
        for _ in range(12):
            self.hojas.append([
                random.randint(-380, 380),
                random.randint(-20, 260),
                random.uniform(0.3, 0.8),
                random.randint(0, 360),
                random.uniform(2, 5),
                random.uniform(0, 2*math.pi)
            ])

        # Sonido de bie

        # Pintar el fondo fijo una sola vez
        self.dibujar_fondo()
        # Iniciar bucle de animación
        self.actualizar()

    # ---------- DIBUJO DE FONDO (estático) ----------
    def dibujar_fondo(self):
        """Dibuja el paisaje base que no cambia."""
        # Cielo con degradado simple (dos rectángulos)
        self.lapiz.penup()
        self.lapiz.goto(-400, 320)
        self.lapiz.pendown()
        # Color superior
        self.lapiz.color("#81d4fa")
        self.lapiz.begin_fill()
        self.lapiz.goto(400, 320)
        self.lapiz.goto(400, 0)
        self.lapiz.goto(-400, 0)
        self.lapiz.end_fill()
        # Color inferior del cielo
        self.lapiz.penup()
        self.lapiz.goto(-400, 0)
        self.lapiz.pendown()
        self.lapiz.color("#e0f7fa")
        self.lapiz.begin_fill()
        self.lapiz.goto(400, 0)
        self.lapiz.goto(400, -180)
        self.lapiz.goto(-400, -180)
        self.lapiz.end_fill()

        # Sol
        self.circulo(340, 230, 35, "#FFD54F")
        # Pequeños rayos simples
        self.lapiz.penup()
        self.lapiz.goto(340, 230)
        self.lapiz.color("#FFD54F")
        self.lapiz.pensize(2)
        for ang in range(0, 360, 30):
            rad = math.radians(ang)
            self.lapiz.goto(340 + 32*math.cos(rad), 230 + 32*math.sin(rad))
            self.lapiz.pendown()
            self.lapiz.goto(340 + 42*math.cos(rad), 230 + 42*math.sin(rad))
            self.lapiz.penup()
        self.lapiz.pensize(1)

        # Césped
        self.rectangulo(-400, -180, 800, 140, "#7cb342")
        # Algunas flores (estáticas)
        for _ in range(30):
            x = random.randint(-380, 380)
            y = random.randint(-180, -130)
            self.circulo(x, y, 4, "#ffb74d")
            self.circulo(x, y, 2, "#fff176")

        # Árbol (simplificado)
        self.dibujar_arbol(270, -180)

    def dibujar_arbol(self, x, y):
        # Tronco
        self.rectangulo(x, y, 20, 100, "#6d4c41")
        # Sombra del tronco
        self.lapiz.penup()
        self.lapiz.goto(x+3, y)
        self.lapiz.pendown()
        self.lapiz.color("#5d4037")
        self.lapiz.pensize(3)
        self.lapiz.goto(x+3, y+80)
        self.lapiz.pensize(1)
        # Follaje (menos círculos)
        for dx, dy, r, color in [
            (-30, 100, 35, "#388e3c"),
            (10, 110, 40, "#43a047"),
            (45, 95, 30, "#2e7d32"),
            (-10, 140, 30, "#2e7d32"),
            (30, 140, 28, "#1b5e20")
        ]:
            self.circulo(x+dx, y+dy, r, color)

    # ---------- DIBUJOS REUTILIZABLES ----------
    def circulo(self, x, y, r, color):
        self.lapiz.penup()
        self.lapiz.goto(x, y-r)
        self.lapiz.color(color)
        self.lapiz.begin_fill()
        self.lapiz.circle(r)
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

    def escribir(self, texto, x, y, tam, color, negrita=True):
        self.lapiz.penup()
        self.lapiz.goto(x, y)
        self.lapiz.color(color)
        estilo = "bold" if negrita else "normal"
        self.lapiz.write(texto, align="center", font=("Segoe UI", tam, estilo))

    def dibujar_nube(self, x, y):
        self.circulo(x, y, 18, "white")
        self.circulo(x+22, y+8, 22, "white")
        self.circulo(x+45, y, 18, "white")
        self.circulo(x+12, y-8, 14, "white")
        self.circulo(x+35, y-8, 14, "white")

    def dibujar_hoja(self, x, y, angulo):
        self.lapiz.penup()
        self.lapiz.goto(x, y)
        self.lapiz.setheading(angulo)
        self.lapiz.color("#66bb6a")
        self.lapiz.begin_fill()
        self.lapiz.circle(7, 90)
        self.lapiz.left(90)
        self.lapiz.circle(7, 90)
        self.lapiz.end_fill()

    # ---------- BUCLE DE ANIMACIÓN ----------
    def actualizar(self):
        if not self.activo:
            return

        # Limpiar solo los elementos móviles (borramos lo que dibuja el lápiz)
        self.lapiz.clear()

        # Redibujar las nubes (se mueven)
        for n in self.nubes:
            n["x"] += n["v"]
            if n["x"] > 450:
                n["x"] = -450
            elif n["x"] < -450:
                n["x"] = 450
            self.dibujar_nube(n["x"], n["y"])

        # Hojas cayendo
        for h in self.hojas:
            self.dibujar_hoja(h[0], h[1], h[3])
            h[1] -= h[2]                     # caída
            h[0] += math.sin(time.time()*2 + h[5]) * 0.7  # vaivén
            h[3] += h[4]                     # rotación
            if h[1] < -180:
                h[1] = 260
                h[0] = random.randint(-400, 400)
                h[2] = random.uniform(0.3, 0.8)

        # Efecto máquina de escribir
        if self.texto_indice < len(self.textos):
            txt, y, tam, color = self.textos[self.texto_indice]
            negrita = (self.texto_indice < 3)  # Los 3 primeros en negrita
            if self.letra_indice < len(txt):
                if time.time() - self.tiempo_letra > 0.04:
                    self.letra_indice += 1
                    self.tiempo_letra = time.time()
                parcial = txt[:self.letra_indice]
                self.escribir(parcial, 0, y, tam, color, negrita)
            else:
                self.escribir(txt, 0, y, tam, color, negrita)
                if time.time() - self.tiempo_letra > 0.6:
                    self.texto_indice += 1
                    self.letra_indice = 0
                    self.tiempo_letra = time.time()
        else:
            # Mostrar todo fijo
            for txt, y, tam, color in self.textos:
                negrita = (self.textos.index((txt,y,tam,color)) < 3)
                self.escribir(txt, 0, y, tam, color, negrita)

        # Fecha
        self.escribir(self.fecha, 320, -290, 11, "#555555", False)

        # Física de la pelota
        self.velocidad += self.gravedad * 0.06
        self.altura -= self.velocidad * 0.18
        if self.altura < -150:
            self.altura = 240
            self.velocidad = 0

        # Pelota (sin sombra 3D, más limpia)
        self.pelota.goto(230, self.altura)
        self.pelota.color("#43a047")

        self.pantalla.update()
        self.raiz.after(20, self.actualizar)

    def iniciar(self):
        """Acción al pulsar el botón (placeholder)."""
        self.activo = False
        self.boton.config(text="Cargando...", state="disabled")
        print("Simulación iniciada (puedes agregar la siguiente escena aquí).")
        # Aquí podrías destruir la ventana de bienvenida y abrir la simulación real.

    def ejecutar(self):
        self.raiz.mainloop()

# =====================================================
if __name__ == "__main__":
    app = Bienvenida()
    app.ejecutar()