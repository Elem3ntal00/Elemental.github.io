import turtle
import random
import math
import time
from datetime import datetime

# =====================================================
# CONFIGURACIÓN DE LA VENTANA
# =====================================================
WIDTH, HEIGHT = 800, 650
wn = turtle.Screen()
wn.setup(WIDTH, HEIGHT)
wn.title("Bienvenido al Simulador de Caída Libre")
wn.bgcolor("#e0f7fa")
wn.tracer(0)

# Lápiz para dibujar
lapiz = turtle.Turtle()
lapiz.hideturtle()
lapiz.speed(0)

# Pelota
pelota = turtle.Turtle()
pelota.shape("circle")
pelota.shapesize(1.5)
pelota.color("#43a047")
pelota.penup()

# =====================================================
# FUNCIONES DE DIBUJO
# =====================================================
def circulo(x, y, r, color):
    lapiz.penup()
    lapiz.goto(x, y - r)
    lapiz.color(color)
    lapiz.begin_fill()
    lapiz.circle(r)
    lapiz.end_fill()

def rectangulo(x, y, w, h, color):
    lapiz.penup()
    lapiz.goto(x, y)
    lapiz.color(color)
    lapiz.begin_fill()
    for _ in range(2):
        lapiz.forward(w)
        lapiz.right(90)
        lapiz.forward(h)
        lapiz.right(90)
    lapiz.end_fill()

def escribir(texto, x, y, tam, color, negrita=True):
    lapiz.penup()
    lapiz.goto(x, y)
    lapiz.color(color)
    estilo = "bold" if negrita else "normal"
    lapiz.write(texto, align="center", font=("Segoe UI", tam, estilo))

def dibujar_nube(x, y):
    """Nube formada por círculos blancos."""
    circulo(x, y, 18, "white")
    circulo(x + 22, y + 8, 22, "white")
    circulo(x + 45, y, 18, "white")
    circulo(x + 12, y - 8, 14, "white")
    circulo(x + 35, y - 8, 14, "white")

def dibujar_hoja(x, y, angulo):
    lapiz.penup()
    lapiz.goto(x, y)
    lapiz.setheading(angulo)
    lapiz.color("#66bb6a")
    lapiz.begin_fill()
    lapiz.circle(7, 90)
    lapiz.left(90)
    lapiz.circle(7, 90)
    lapiz.end_fill()

# =====================================================
# DIBUJAR FONDO (UNA SOLA VEZ)
# =====================================================
def dibujar_fondo():
    # Cielo con degradado suave
    lapiz.penup()
    lapiz.goto(-400, 320)
    lapiz.pendown()
    lapiz.color("#81d4fa")
    lapiz.begin_fill()
    lapiz.goto(400, 320)
    lapiz.goto(400, 0)
    lapiz.goto(-400, 0)
    lapiz.end_fill()

    lapiz.penup()
    lapiz.goto(-400, 0)
    lapiz.pendown()
    lapiz.color("#e0f7fa")
    lapiz.begin_fill()
    lapiz.goto(400, 0)
    lapiz.goto(400, -180)
    lapiz.goto(-400, -180)
    lapiz.end_fill()

    # Sol
    circulo(340, 230, 35, "#FFD54F")
    lapiz.penup()
    lapiz.goto(340, 230)
    lapiz.color("#FFD54F")
    lapiz.pensize(2)
    for ang in range(0, 360, 30):
        rad = math.radians(ang)
        lapiz.goto(340 + 32 * math.cos(rad), 230 + 32 * math.sin(rad))
        lapiz.pendown()
        lapiz.goto(340 + 42 * math.cos(rad), 230 + 42 * math.sin(rad))
        lapiz.penup()
    lapiz.pensize(1)

    # Césped y flores
    rectangulo(-400, -180, 800, 140, "#7cb342")
    for _ in range(25):
        xf = random.randint(-380, 380)
        yf = random.randint(-180, -130)
        circulo(xf, yf, 4, "#ffb74d")
        circulo(xf, yf, 2, "#fff176")

    # Árbol
    rectangulo(270, -180, 20, 100, "#6d4c41")
    # sombra tronco
    lapiz.penup()
    lapiz.goto(273, -180)
    lapiz.pendown()
    lapiz.color("#5d4037")
    lapiz.pensize(3)
    lapiz.goto(273, -100)
    lapiz.pensize(1)
    # follaje
    for dx, dy, r, color in [
        (-30, 100, 35, "#388e3c"),
        (10, 110, 40, "#43a047"),
        (45, 95, 30, "#2e7d32"),
        (-10, 140, 30, "#2e7d32"),
        (30, 140, 28, "#1b5e20")
    ]:
        circulo(270 + dx, -180 + dy, r, color)

dibujar_fondo()

# =====================================================
# DATOS DE ANIMACIÓN
# =====================================================
# Nubes: x, y, velocidad
nubes = [
    {"x": -350, "y": 220, "v": 0.4},
    {"x": 0, "y": 190, "v": -0.3},
    {"x": 250, "y": 240, "v": 0.5}
]

# Hojas: x, y, vel caída, ángulo, vel angular, fase
hojas = []
for _ in range(12):
    hojas.append([
        random.randint(-380, 380),
        random.randint(-20, 260),
        random.uniform(0.3, 0.8),
        random.randint(0, 360),
        random.uniform(2, 5),
        random.uniform(0, 2 * math.pi)
    ])

# Texto animado
textos = [
    ("BIENVENIDO AL", 160, 20, "#1565c0"),
    ("SIMULADOR INTERACTIVO", 120, 30, "#0d47a1"),
    ("DE CAÍDA LIBRE", 75, 32, "#1976d2"),
    ("Explora la Física de forma interactiva", 20, 18, "#555555"),
    ("Universidad • Proyecto Educativo", -10, 15, "#777777"),
]
indice_texto = 0
letra_actual = 0
tiempo_letra = 0
fecha = datetime.now().strftime("%d/%m/%Y   %H:%M:%S")

# Pelota
altura = 240
velocidad = 0
gravedad = 9.81

# =====================================================
# BUCLE DE ANIMACIÓN
# =====================================================
while True:
    lapiz.clear()

    # Nubes
    for n in nubes:
        n["x"] += n["v"]
        if n["x"] > 450:
            n["x"] = -450
        elif n["x"] < -450:
            n["x"] = 450
        dibujar_nube(n["x"], n["y"])

    # Hojas
    for h in hojas:
        dibujar_hoja(h[0], h[1], h[3])
        h[1] -= h[2]
        h[0] += math.sin(time.time() * 2 + h[5]) * 0.7
        h[3] += h[4]
        if h[1] < -180:
            h[1] = 260
            h[0] = random.randint(-400, 400)
            h[2] = random.uniform(0.3, 0.8)

    # Efecto máquina de escribir
    if indice_texto < len(textos):
        txt, y, tam, color = textos[indice_texto]
        negrita = indice_texto < 3
        if letra_actual < len(txt):
            if time.time() - tiempo_letra > 0.04:
                letra_actual += 1
                tiempo_letra = time.time()
            parcial = txt[:letra_actual]
            escribir(parcial, 0, y, tam, color, negrita)
        else:
            escribir(txt, 0, y, tam, color, negrita)
            if time.time() - tiempo_letra > 0.6:
                indice_texto += 1
                letra_actual = 0
                tiempo_letra = time.time()
    else:
        # Mostrar texto fijo
        for txt, y, tam, color in textos:
            negrita = textos.index((txt, y, tam, color)) < 3
            escribir(txt, 0, y, tam, color, negrita)

    # Fecha
    escribir(fecha, 320, -290, 11, "#555555", False)

    # Física de la pelota
    velocidad += gravedad * 0.06
    altura -= velocidad * 0.18
    if altura < -150:
        altura = 240
        velocidad = 0

    pelota.goto(230, altura)

    wn.update()
    time.sleep(0.02)