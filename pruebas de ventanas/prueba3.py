import turtle
import random
import time

def setup_screen():
    screen = turtle.Screen()
    screen.title("Bienvenida de Partículas")
    screen.bgcolor("#e0f2f1") # Un verde azulado muy suave
    screen.setup(width=800, height=600)
    # screen.tracer(0) # Descomentar para un movimiento muy rápido
    return screen

def run_particle_animation(text, position, size=30, num_particles=20, color="#e91e63"):
    # NOTA: Turtle no es muy bueno para mover muchas partículas a la vez si no desactivamos el tracer.
    # Esta es una versión simplificada que mueve las letras, no partículas individuales de la forma de la letra.
    
    screen = turtle.Screen()
    original_tracer = screen.tracer()
    screen.tracer(0) # Apagar para dibujar rápido

    turtles = []
    
    # Crear una tortuga por cada letra
    for i, letter in enumerate(text):
        t = turtle.Turtle()
        t.shape("circle")
        t.shapesize(0.5)
        t.color(color)
        t.penup()
        # Posiciones de inicio aleatorias
        t.goto(random.randint(-400, 400), random.randint(-300, 300))
        turtles.append((t, letter))

    # Definir posiciones finales
    start_x = position[0] - (len(text) * size * 0.45)
    final_positions = []
    for i in range(len(text)):
        final_positions.append((start_x + (i * size * 0.9), position[1]))

    # Animar el movimiento hacia el destino
    steps = 40
    for step in range(steps):
        for i in range(len(turtles)):
            t, letter = turtles[i]
            fx, fy = final_positions[i]
            
            # Movimiento progresivo (interpolación lineal simple con un poco de aleatoriedad)
            new_x = t.xcor() + (fx - t.xcor()) * (1 / (steps - step))
            new_y = t.ycor() + (fy - t.ycor()) * (1 / (steps - step))
            
            t.goto(new_x, new_y)
            # screen.update() # Demasiado lento si actualizamos por cada micro-movimiento
        
        # Opcional: Pequeña vibración aleatoria al principio
        if step < steps // 2:
            for i in range(len(turtles)):
                t, letter = turtles[i]
                t.goto(t.xcor() + random.randint(-3, 3), t.ycor() + random.randint(-3, 3))
                
        screen.update()
        time.sleep(0.01)

    # Reemplazar tortugas por el texto final
    for i in range(len(turtles)):
        t, letter = turtles[i]
        t.clear()
        t.hideturtle()
        
    t_final = turtle.Turtle()
    t_final.hideturtle()
    t_final.speed(0)
    t_final.penup()
    t_final.color(color)
    t_final.goto(position)
    t_final.write(text, align="center", font=("Courier", size, "bold"))
    
    screen.update()
    screen.tracer(original_tracer) # Reactivar tracer original

def run_animation():
    screen = setup_screen()
    
    # Partículas formando "¡BIENVENIDO!"
    run_particle_animation("¡BIENVENIDO!", (0, 80), num_particles=30, color="#ff5722")
    
    time.sleep(0.5)
    
    # Texto de subtítulo estático
    t2 = turtle.Turtle()
    t2.hideturtle()
    t2.penup()
    t2.goto(0, 0)
    t2.color("#555")
    t2.write("Las partículas de la física se unen para ti.", align="center", font=("Arial", 16, "normal"))
    t2.goto(0, -30)
    t2.write("Selecciona una opción del menú.", align="center", font=("Arial", 16, "normal"))
    
    turtle.done()

if __name__ == "__main__":
    run_animation()