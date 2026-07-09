# interfaz/bienvenida.py
import tkinter as tk
import turtle
import random
import math
import time

class Bienvenida:
    def __init__(self, parent):
        self.parent = parent
        self.activo = True

        # Canvas que llena todo el frame padre
        self.canvas = tk.Canvas(parent, bg="#e0f7fa", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # TurtleScreen sobre el canvas
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.bgcolor("#e0f7fa")
        self.screen.tracer(0)

        # Tortuga para el fondo estático (se dibuja una sola vez)
        self.bg_turtle = turtle.RawTurtle(self.screen)
        self.bg_turtle.hideturtle()
        self.bg_turtle.speed(0)

        # Tortuga para los elementos animados (nubes, hojas, texto)
        self.lapiz = turtle.RawTurtle(self.screen)
        self.lapiz.hideturtle()
        self.lapiz.speed(0)

        # Tortuga de la pelota
        self.pelota = turtle.RawTurtle(self.screen)
        self.pelota.shape("circle")
        self.pelota.shapesize(1.5)
        self.pelota.color("#43a047")
        self.pelota.penup()

        # Ajustar coordenadas del mundo al tamaño real del canvas
        def ajustar_mundo(event=None):
            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()
            if w > 1 and h > 1:
                aspecto = 800 / 650
                nuevo_alto = w / aspecto
                self.screen.setworldcoordinates(-400, -nuevo_alto/2,
                                                400, nuevo_alto/2)
                self._dibujar_fondo()
        self.canvas.bind("<Configure>", ajustar_mundo)

        # Datos de animación (nubes, hojas, texto, pelota)
        self.nubes = [
            {"x": -350, "y": 220, "v": 0.4},
            {"x": 0, "y": 190, "v": -0.3},
            {"x": 250, "y": 240, "v": 0.5}
        ]

        self.hojas = []
        for _ in range(12):
            self.hojas.append([
                random.randint(-380, 380),
                random.randint(-20, 260),
                random.uniform(0.3, 0.8),
                random.randint(0, 360),
                random.uniform(2, 5),
                random.uniform(0, 2 * math.pi)
            ])

        self.textos = [
            ("BIENVENIDO AL", 160, 20, "#1565c0"),
            ("SIMULADOR INTERACTIVO", 120, 30, "#0d47a1"),
            ("DE CAÍDA LIBRE", 75, 32, "#1976d2"),
            ("Explora la Física de forma interactiva", 20, 18, "#555555"),
            ("Universidad • Proyecto Educativo", -10, 15, "#777777"),
        ]
        self.indice_texto = 0
        self.letra_actual = 0
        self.tiempo_letra = time.time()

        # Pelota
        self.altura = 240
        self.velocidad = 0
        self.gravedad = 9.81

        # Arrancar el bucle de animación
        self.screen.ontimer(self._animar_frame, 20)

    def detener(self):
        """Limpia recursos para detener la animación de forma segura."""
        self.activo = False
        if hasattr(self, 'screen'):
            self.screen.bye()
        self.canvas.destroy()

    # -------------------------------------------------------
    # MÉTODOS DE DIBUJO (internos)
    # -------------------------------------------------------
    def _circulo(self, t, x, y, r, color):
        t.penup()
        t.goto(x, y - r)
        t.color(color)
        t.begin_fill()
        t.circle(r)
        t.end_fill()

    def _rectangulo(self, t, x, y, w, h, color):
        t.penup()
        t.goto(x, y)
        t.color(color)
        t.begin_fill()
        for _ in range(2):
            t.forward(w)
            t.right(90)
            t.forward(h)
            t.right(90)
        t.end_fill()

    def _escribir(self, t, texto, x, y, tam, color, negrita=True):
        t.penup()
        t.goto(x, y)
        t.color(color)
        estilo = "bold" if negrita else "normal"
        t.write(texto, align="center", font=("Segoe UI", tam, estilo))

    def _dibujar_nube(self, t, x, y):
        self._circulo(t, x, y, 18, "white")
        self._circulo(t, x + 22, y + 8, 22, "white")
        self._circulo(t, x + 45, y, 18, "white")
        self._circulo(t, x + 12, y - 8, 14, "white")
        self._circulo(t, x + 35, y - 8, 14, "white")

    def _dibujar_hoja(self, t, x, y, angulo):
        t.penup()
        t.goto(x, y)
        t.setheading(angulo)
        t.color("#66bb6a")
        t.begin_fill()
        t.circle(7, 90)
        t.left(90)
        t.circle(7, 90)
        t.end_fill()

    def _dibujar_fondo(self):
        """Fondo estático (cielo, sol, césped, árbol sin tronco)."""
        t = self.bg_turtle
        t.clear()

        # Cielo
        t.penup(); t.goto(-400, 320); t.pendown()
        t.color("#81d4fa"); t.begin_fill()
        t.goto(400, 320); t.goto(400, 0); t.goto(-400, 0)
        t.end_fill()

        t.penup(); t.goto(-400, 0); t.pendown()
        t.color("#e0f7fa"); t.begin_fill()
        t.goto(400, 0); t.goto(400, -180); t.goto(-400, -180)
        t.end_fill()

        # Sol
        self._circulo(t, 340, 230, 35, "#FFD54F")
        t.penup(); t.goto(340, 230); t.color("#FFD54F"); t.pensize(2)
        for ang in range(0, 360, 30):
            rad = math.radians(ang)
            t.goto(340 + 32 * math.cos(rad), 230 + 32 * math.sin(rad))
            t.pendown()
            t.goto(340 + 42 * math.cos(rad), 230 + 42 * math.sin(rad))
            t.penup()
        t.pensize(1)

        # Césped y flores
        self._rectangulo(t, -400, -180, 800, 140, "#7cb342")
        for _ in range(25):
            xf = random.randint(-380, 380)
            yf = random.randint(-180, -130)
            self._circulo(t, xf, yf, 4, "#ffb74d")
            self._circulo(t, xf, yf, 2, "#fff176")

        # Árbol (solo follaje verde, sin tronco café)
        for dx, dy, r, color in [
            (-30, 100, 35, "#388e3c"),
            (10, 110, 40, "#43a047"),
            (45, 95, 30, "#2e7d32"),
            (-10, 140, 30, "#2e7d32"),
            (30, 140, 28, "#1b5e20")
        ]:
            self._circulo(t, 270 + dx, -180 + dy, r, color)

    # -------------------------------------------------------
    # BUCLE DE ANIMACIÓN (sin hora)
    # -------------------------------------------------------
    def _animar_frame(self):
        if not self.activo:
            return
        self.lapiz.clear()

        # Nubes
        for n in self.nubes:
            n["x"] += n["v"]
            if n["x"] > 450: n["x"] = -450
            elif n["x"] < -450: n["x"] = 450
            self._dibujar_nube(self.lapiz, n["x"], n["y"])

        # Hojas
        for h in self.hojas:
            self._dibujar_hoja(self.lapiz, h[0], h[1], h[3])
            h[1] -= h[2]
            h[0] += math.sin(time.time() * 2 + h[5]) * 0.7
            h[3] += h[4]
            if h[1] < -180:
                h[1] = 260
                h[0] = random.randint(-400, 400)
                h[2] = random.uniform(0.3, 0.8)

        # Texto con efecto máquina de escribir
        if self.indice_texto < len(self.textos):
            txt, y, tam, color = self.textos[self.indice_texto]
            negrita = self.indice_texto < 3
            ahora = time.time()
            if self.letra_actual < len(txt):
                if ahora - self.tiempo_letra > 0.04:
                    self.letra_actual += 1
                    self.tiempo_letra = ahora
                parcial = txt[:self.letra_actual]
                self._escribir(self.lapiz, parcial, 0, y, tam, color, negrita)
            else:
                self._escribir(self.lapiz, txt, 0, y, tam, color, negrita)
                if ahora - self.tiempo_letra > 0.6:
                    self.indice_texto += 1
                    self.letra_actual = 0
                    self.tiempo_letra = ahora
        else:
            for txt, y, tam, color in self.textos:
                negrita = self.textos.index((txt, y, tam, color)) < 3
                self._escribir(self.lapiz, txt, 0, y, tam, color, negrita)

        # Física de la pelota
        self.velocidad += self.gravedad * 0.06
        self.altura -= self.velocidad * 0.18
        if self.altura < -150:
            self.altura = 240
            self.velocidad = 0
        self.pelota.goto(230, self.altura)

        self.screen.update()
        self.screen.ontimer(self._animar_frame, 20)