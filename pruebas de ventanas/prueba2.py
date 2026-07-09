import turtle
import time

def setup_screen():
    screen = turtle.Screen()
    screen.title("Bienvenida - Simulador de Caída Libre")
    screen.bgcolor("#f0f8ff") # Un color azul muy claro (pastel)
    screen.setup(width=800, height=600)
    return screen

def type_text(text, position, size=30, color="navy", speed=0.05):
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.penup()
    t.color(color)
    t.goto(position)
    
    for letter in text:
        t.write(letter, move=True, align="center", font=("Arial", size, "bold"))
        time.sleep(speed)

def draw_falling_object():
    obj = turtle.Turtle()
    obj.shape("circle")
    obj.color("orange")
    obj.penup()
    obj.goto(300, 200) # Inicio arriba a la derecha
    
    # Simulación simple de caída con Turtle
    for _ in range(30):
        obj.sety(obj.ycor() - 15)
        time.sleep(0.02)
    obj.hideturtle()

def draw_text_instantly(text, position, size=20, color="#555"):
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.penup()
    t.color(color)
    t.goto(position)
    t.write(text, align="center", font=("Arial", size, "normal"))

def run_animation():
    setup_screen()
    
    # Título principal con efecto de escritura
    type_text("¡BIENVENIDO!", (0, 100), size=40)
    
    # El objeto cae
    draw_falling_object()
    
    # Subtítulo (aparece de golpe para no tardar mucho)
    draw_text_instantly("Estamos listos para explorar las leyes de la física.", (0, 20))
    draw_text_instantly("Selecciona una opción del menú para comenzar.", (0, -20))
    
    turtle.done()

if __name__ == "__main__":
    run_animation()