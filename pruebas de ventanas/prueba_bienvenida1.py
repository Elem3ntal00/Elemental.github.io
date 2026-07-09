# interfaz/bienvenida.py
import tkinter as tk
import random
import math
import time


class Bienvenida:
    def __init__(self, parent):
        self.parent = parent
        self.anim_id = None

        # Crear canvas
        self.canvas = tk.Canvas(parent, bg="#e0f7fa", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        parent.update_idletasks()  # Para tener dimensiones reales
        self.w = self.canvas.winfo_width()
        self.h = self.canvas.winfo_height()

        # Variables de estado
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
        self.altura = 240
        self.velocidad = 0
        self.gravedad = 9.81

        # Iniciar animación
        self.dibujar_fondo_estatico()
        self.animar()

    def dibujar_fondo_estatico(self):
        c = self.canvas
        w = self.w
        h = self.h
        if w < 10: w = 800  # fallback
        if h < 10: h = 650

        # Cielo (dos degradados)
        c.create_rectangle(0, 0, w, h*0.5, fill="#81d4fa", outline="")
        c.create_rectangle(0, h*0.5, w, h*0.78, fill="#e0f7fa", outline="")
        # Césped
        c.create_rectangle(0, h*0.78, w, h, fill="#7cb342", outline="")
        # Sol
        self._dibujar_sol(w*0.85, h*0.35, 35)
        # Flores
        for _ in range(25):
            xf = random.randint(10, w-10)
            yf = random.randint(int(h*0.78), int(h*0.85))
            self._circulo(xf, yf, 4, "#ffb74d")
            self._circulo(xf, yf, 2, "#fff176")
        # Árbol
        self._dibujar_arbol(w*0.65, h*0.78)

    def _dibujar_sol(self, x, y, r):
        c = self.canvas
        c.create_oval(x-r, y-r, x+r, y+r, fill="#FFD54F", outline="")
        for ang in range(0, 360, 30):
            rad = math.radians(ang)
            x1 = x + 32 * math.cos(rad)
            y1 = y - 32 * math.sin(rad)
            x2 = x + 42 * math.cos(rad)
            y2 = y - 42 * math.sin(rad)
            c.create_line(x1, y1, x2, y2, fill="#FFD54F", width=2)

    def _circulo(self, x, y, r, color):
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="")

    def _dibujar_arbol(self, x, y):
        c = self.canvas
        # Tronco
        c.create_rectangle(x, y-100, x+20, y, fill="#6d4c41", outline="")
        # Follaje
        self._circulo(x-30, y-80, 35, "#388e3c")
        self._circulo(x+10, y-70, 40, "#43a047")
        self._circulo(x+45, y-85, 30, "#2e7d32")
        self._circulo(x-10, y-40, 30, "#2e7d32")
        self._circulo(x+30, y-40, 28, "#1b5e20")

    def dibujar_nube(self, x, y):
        self._circulo(x, y, 18, "white")
        self._circulo(x+22, y+8, 22, "white")
        self._circulo(x+45, y, 18, "white")
        self._circulo(x+12, y-8, 14, "white")
        self._circulo(x+35, y-8, 14, "white")

    def dibujar_hoja(self, x, y, angulo):
        c = self.canvas
        # Hoja como dos arcos (forma simple)
        r = 7
        rad = math.radians(angulo)
        # Usamos un polígono aproximado en lugar de arcos complejos
        pts = []
        for i in range(0, 360, 30):
            a = math.radians(i)
            px = x + r * math.cos(a) * 0.6
            py = y - r * math.sin(a)
            # rotar
            rx = px - x
            ry = py - y
            nx = x + rx * math.cos(rad) - ry * math.sin(rad)
            ny = y + rx * math.sin(rad) + ry * math.cos(rad)
            pts.extend([nx, ny])
        c.create_polygon(pts, fill="#66bb6a", outline="")

    def animar(self):
        c = self.canvas
        c.delete("anim")
        ahora = time.time()

        # Nubes
        for n in self.nubes:
            n["x"] += n["v"]
            if n["x"] > self.w + 100:
                n["x"] = -100
            elif n["x"] < -100:
                n["x"] = self.w + 100
            self.dibujar_nube(n["x"], n["y"])

        # Hojas
        for h in self.hojas:
            self.dibujar_hoja(h[0], h[1], h[3])
            h[1] -= h[2]
            h[0] += math.sin(ahora * 2 + h[5]) * 0.7
            h[3] += h[4]
            if h[1] < self.h * 0.22:  # -180 en coord original
                h[1] = self.h * 0.7
                h[0] = random.randint(10, self.w-10)
                h[2] = random.uniform(0.3, 0.8)

        # Texto máquina de escribir
        if self.indice_texto < len(self.textos):
            txt, y_base, tam, color = self.textos[self.indice_texto]
            y = self.h * 0.35 + y_base  # ajuste para centrar en el canvas
            if self.letra_actual < len(txt):
                if ahora - self.tiempo_letra > 0.04:
                    self.letra_actual += 1
                    self.tiempo_letra = ahora
                parcial = txt[:self.letra_actual]
                c.create_text(self.w/2, y, text=parcial, font=("Segoe UI", tam, "bold"),
                              fill=color, tags="anim")
            else:
                c.create_text(self.w/2, y, text=txt, font=("Segoe UI", tam, "bold"),
                              fill=color, tags="anim")
                if ahora - self.tiempo_letra > 0.6:
                    self.indice_texto += 1
                    self.letra_actual = 0
                    self.tiempo_letra = ahora
        else:
            # Mostrar todos los textos fijos
            for txt, y_base, tam, color in self.textos:
                y = self.h * 0.35 + y_base
                negrita = self.textos.index((txt, y_base, tam, color)) < 3
                font = ("Segoe UI", tam, "bold" if negrita else "normal")
                c.create_text(self.w/2, y, text=txt, font=font, fill=color, tags="anim")

        # Fecha


        # Pelota
        self.velocidad += self.gravedad * 0.06
        self.altura -= self.velocidad * 0.18
        if self.altura < self.h * 0.22 - 150:  # suelo aproximado
            self.altura = self.h * 0.7
            self.velocidad = 0
        # Coordenada y en canvas: ajustar según altura original (240 -> parte superior)
        y_pelota = self.h * 0.35 + (240 - self.altura)  # mapeo simple
        c.create_oval(self.w*0.55-12, y_pelota-12, self.w*0.55+12, y_pelota+12,
                      fill="#43a047", tags="anim")

        self.anim_id = self.canvas.after(20, self.animar)

    def destruir(self):
        if self.anim_id:
            self.canvas.after_cancel(self.anim_id)
        self.canvas.destroy()