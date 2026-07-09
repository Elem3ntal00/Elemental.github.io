import turtle
import random
import math
import time
from datetime import datetime

# =====================================================
# CONFIGURACIÓN
# =====================================================

WIDTH = 1000
HEIGHT = 650

wn = turtle.Screen()
wn.setup(WIDTH, HEIGHT)
wn.title("Bienvenido al Simulador de Caída Libre")
wn.bgcolor("#dff8d8")
wn.tracer(0)

lapiz = turtle.Turtle()
lapiz.hideturtle()
lapiz.speed(0)

# =====================================================
# FUNCIONES
# =====================================================

def escribir(texto,x,y,tam,color="black",fuente="Arial",negrita=True):

    lapiz.penup()
    lapiz.goto(x,y)
    lapiz.color(color)

    estilo="bold" if negrita else "normal"

    lapiz.write(
        texto,
        align="center",
        font=(fuente,tam,estilo)
    )

#----------------------------------------------------

def circulo(x,y,r,color):

    lapiz.penup()
    lapiz.goto(x,y-r)
    lapiz.color(color)
    lapiz.begin_fill()
    lapiz.circle(r)
    lapiz.end_fill()

#----------------------------------------------------

def rectangulo(x,y,w,h,color):

    lapiz.penup()
    lapiz.goto(x,y)

    lapiz.color(color)

    lapiz.begin_fill()

    for i in range(2):

        lapiz.forward(w)
        lapiz.right(90)

        lapiz.forward(h)
        lapiz.right(90)

    lapiz.end_fill()

#----------------------------------------------------

def nube(x,y):

    circulo(x,y,25,"white")
    circulo(x+25,y+10,30,"white")
    circulo(x+55,y,25,"white")
    circulo(x+15,y-10,20,"white")
    circulo(x+45,y-10,20,"white")

#----------------------------------------------------

def arbol(x,y):

    rectangulo(x,y,25,120,"#7b4f25")

    for dx,dy,r in [

        (-40,100,40),
        (10,120,45),
        (50,100,35),
        (0,70,45),
        (-20,150,30),
        (35,150,30)

    ]:

        circulo(x+dx,y+dy,r,"#4CAF50")

#----------------------------------------------------

def hoja(x,y,angulo):

    lapiz.penup()
    lapiz.goto(x,y)

    lapiz.setheading(angulo)

    lapiz.color("#5cb85c")

    lapiz.begin_fill()

    for i in range(2):

        lapiz.circle(8,90)
        lapiz.left(90)

    lapiz.end_fill()

# =====================================================
# PAISAJE
# =====================================================

# Césped

lapiz.penup()
lapiz.goto(-500,-180)

lapiz.color("#7ac943")
lapiz.begin_fill()

lapiz.goto(500,-180)
lapiz.goto(500,-320)
lapiz.goto(-500,-320)
lapiz.goto(-500,-180)

lapiz.end_fill()

# Colinas

for x,r in [(-350,220),(-50,180),(250,260)]:

    lapiz.penup()
    lapiz.goto(x,-180-r)

    lapiz.color("#98d87a")

    lapiz.begin_fill()
    lapiz.circle(r)
    lapiz.end_fill()

# Sol

circulo(340,220,45,"#FFD93D")

# Nubes

nube(-350,220)
nube(-100,180)
nube(150,240)

# Árbol

arbol(270,-180)

# =====================================================
# TEXTO
# =====================================================

escribir(
    "BIENVENIDO AL",
    0,
    160,
    20,
    "#2e7d32"
)

escribir(
    "SIMULADOR INTERACTIVO",
    0,
    120,
    30,
    "#1b5e20"
)

escribir(
    "DE CAÍDA LIBRE",
    0,
    75,
    32,
    "#388e3c"
)

escribir(
    "Explora la Física de forma interactiva",
    0,
    20,
    18,
    "#444444",
    False
)

escribir(
    "Universidad • Proyecto Educativo",
    0,
    -10,
    15,
    "#666666",
    False
)

# =====================================================
# FECHA
# =====================================================

fecha = datetime.now().strftime("%d/%m/%Y   %H:%M:%S")

escribir(
    fecha,
    320,
    -295,
    12,
    "#444444",
    False
)

# =====================================================
# PELOTA
# =====================================================

pelota = turtle.Turtle()

pelota.shape("circle")
pelota.color("#4CAF50")

pelota.shapesize(1.4)

pelota.penup()

# =====================================================
# HOJAS
# =====================================================

hojas=[]

for i in range(20):

    hojas.append([

        random.randint(-470,470),
        random.randint(-20,260),
        random.uniform(0.4,1.2),
        random.randint(0,360)

    ])

# =====================================================
# ANIMACIÓN
# =====================================================

g=9.81

altura=240

velocidad=0

for frame in range(500):

    pelota.goto(230,altura)

    velocidad+=g*0.06

    altura-=velocidad*0.18

    if altura<-150:

        altura=240
        velocidad=0

    # hojas

    lapiz.clear()

    # volver a escribir

    escribir(
        "BIENVENIDO AL",
        0,
        160,
        20,
        "#2e7d32"
    )

    escribir(
        "SIMULADOR INTERACTIVO",
        0,
        120,
        30,
        "#1b5e20"
    )

    escribir(
        "DE CAÍDA LIBRE",
        0,
        75,
        32,
        "#388e3c"
    )

    escribir(
        "Explora la Física de forma interactiva",
        0,
        20,
        18,
        "#444444",
        False
    )

    escribir(
        "Universidad • Proyecto Educativo",
        0,
        -10,
        15,
        "#666666",
        False
    )

    escribir(
        fecha,
        320,
        -295,
        12,
        "#444444",
        False
    )

    for h in hojas:

        hoja(h[0],h[1],h[3])

        h[1]-=h[2]
        h[0]+=math.sin(frame/10+h[2])*0.8
        h[3]+=5

        if h[1]<-180:

            h[1]=260
            h[0]=random.randint(-450,450)

    wn.update()

    time.sleep(0.02)

wn.mainloop()