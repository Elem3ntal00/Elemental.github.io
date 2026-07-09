import tkinter as tk
from tkinter import messagebox
import secrets
import string
import re
import os
from PIL import Image, ImageTk

BG_COLOR = "#090A14"
CYAN = "#00E5FF"
MAGENTA = "#D500F9"
RED = "#FF3366"
BLUE = "#3366FF"
GREEN = "#00FF66"
YELLOW = "#FFD700"
TEXT_W = "#FFFFFF"
TEXT_G = "#8888AA"
FUENTE = "Courier"

def cargar_img(nombre_base, size):
    for ext in ['.png', '.jpg', '.jpeg']:
        ruta = nombre_base + ext
        if os.path.exists(ruta):
            try:
                img = Image.open(ruta).resize(size)
                return ImageTk.PhotoImage(img)
            except: pass
    return None

def crear_boton_neon(master, texto, color_borde, comando):
    marco = tk.Frame(master, bg=color_borde, bd=0)
    btn = tk.Button(marco, text=texto, bg=BG_COLOR, fg=TEXT_W, font=(FUENTE, 12, "bold"),
                    activebackground=color_borde, activeforeground="black", relief="flat", cursor="hand2", width=24, command=comando)
    btn.pack(padx=2, pady=2)
    btn.bind("<Enter>", lambda e: btn.config(bg=color_borde, fg="black"))
    btn.bind("<Leave>", lambda e: btn.config(bg=BG_COLOR, fg=TEXT_W))
    return marco

def dibujar_compu_feliz(c):
    c.create_rectangle(30, 15, 170, 105, fill="#A0A0A0", outline="#555555", width=3)
    c.create_rectangle(40, 25, 160, 95, fill="#050505", outline=CYAN, width=2)
    c.create_rectangle(65, 40, 85, 55, fill=GREEN, outline="")
    c.create_rectangle(115, 40, 135, 55, fill=GREEN, outline="")
    c.create_polygon(65, 70, 135, 70, 100, 85, fill=GREEN, outline="")
    c.create_rectangle(85, 105, 115, 135, fill="#808080", outline="#555555", width=2)
    c.create_polygon(50, 135, 150, 135, 165, 155, 35, 155, fill="#A0A0A0", outline="#555555", width=2)

def dibujar_icono_papelera(c, cmd):
    c.create_rectangle(14, 2, 22, 6, fill=RED, outline="")
    c.create_rectangle(4, 6, 32, 10, fill=RED, outline=MAGENTA, width=2)
    c.create_polygon(8, 10, 28, 10, 25, 33, 11, 33, fill="#442222", outline=RED, width=2)
    c.bind("<Button-1>", lambda e: cmd())

def dibujar_icono_guardar(c, cmd):
    c.create_rectangle(2, 2, 33, 33, fill=BLUE, outline=CYAN, width=2)
    c.create_rectangle(8, 2, 28, 12, fill="#e0e0e0", outline="")
    c.create_rectangle(10, 18, 26, 33, fill="white", outline="")
    c.bind("<Button-1>", lambda e: cmd())

def dibujar_cubo_amarillo(c, cmd):
    c.create_polygon(75, 15, 125, 40, 75, 65, 25, 40, fill="#FFFF33", outline="black", width=2)
    c.create_polygon(25, 40, 75, 65, 75, 115, 25, 90, fill="#FFCC00", outline="black", width=2)
    c.create_polygon(75, 65, 125, 40, 125, 90, 75, 115, fill="#D4AC0D", outline="black", width=2)
    c.create_text(75, 38, text="?", font=(FUENTE, 14, "bold"), fill="black")
    c.create_text(50, 76, text="?", font=(FUENTE, 14, "bold"), fill="black")
    c.create_text(100, 76, text="?", font=(FUENTE, 14, "bold"), fill="black")
    c.bind("<Button-1>", lambda e: cmd())

def dibujar_monitor_teclado(canvas):
    canvas.create_polygon(150, 120, 190, 120, 200, 145, 140, 145, fill="#A0A0A0", outline="#555555")
    canvas.create_rectangle(130, 145, 210, 153, fill="#808080")
    canvas.create_rectangle(70, 10, 270, 120, fill="#C0C0C0", outline="#888888", width=2)
    pantalla = canvas.create_rectangle(80, 20, 260, 110, fill="#050505", outline=CYAN, width=1)
    canvas.create_rectangle(250, 113, 260, 117, fill=GREEN)
    canvas.create_polygon(40, 170, 300, 170, 320, 265, 20, 265, fill="#222", outline=CYAN, width=2)
    return pantalla

def guardar_en_archivo(etiqueta, pwd):
    carpeta = "Mis_Contrasenas"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    ruta = os.path.join(carpeta, "claves.txt")
    with open(ruta, "a", encoding="utf-8") as f:
        f.write(f"{etiqueta}: {pwd}\n")

class PantallaInicio(tk.Frame):
    def __init__(self, master, ctrl):
        super().__init__(master, bg=BG_COLOR)
        centro = tk.Frame(self, bg=BG_COLOR)
        centro.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(centro, text="SISTEMA DE SEGURIDAD", font=(FUENTE, 18, "bold"), fg=TEXT_W, bg=BG_COLOR).pack()
        tk.Label(centro, text="GESTOR DE CREDENCIALES", font=(FUENTE, 12, "bold"), fg=CYAN, bg=BG_COLOR).pack(pady=(0, 15))
        
        c = tk.Canvas(centro, width=180, height=160, bg=BG_COLOR, highlightthickness=0)
        c.pack(pady=5)
        img = cargar_img("compu_feliz", (160, 160))
        if img: 
            c.create_image(90, 80, image=img)
            self.img = img
        else: 
            dibujar_compu_feliz(c)

        crear_boton_neon(centro, "1  INGRESAR CLAVE  >", CYAN, ctrl.mostrar_ingreso).pack(pady=10)
        crear_boton_neon(centro, "2  RECOMENDAR CLAVE >", MAGENTA, ctrl.mostrar_recomendacion).pack(pady=5)

        p_inf = tk.Frame(centro, bg=BG_COLOR, highlightbackground="#1A1F30", highlightthickness=2)
        p_inf.pack(fill="x", padx=15, pady=(20, 0))
        f1 = tk.Frame(p_inf, bg=BG_COLOR)
        f1.pack(side="left", expand=True, pady=8)
        tk.Label(f1, text="🛡️", font=(FUENTE, 16), bg=BG_COLOR, fg=CYAN).pack()
        tk.Label(f1, text="SEGURO", font=(FUENTE, 10, "bold"), bg=BG_COLOR, fg=CYAN).pack()
        tk.Label(f1, text="Con buena contraseña\ntus datos están a salvo", font=(FUENTE, 8), bg=BG_COLOR, fg=TEXT_G).pack()
        f2 = tk.Frame(p_inf, bg=BG_COLOR)
        f2.pack(side="left", expand=True, pady=8)
        tk.Label(f2, text="👤", font=(FUENTE, 16), bg=BG_COLOR, fg=YELLOW).pack()
        tk.Label(f2, text="PRIVACIDAD", font=(FUENTE, 10, "bold"), bg=BG_COLOR, fg=YELLOW).pack()
        tk.Label(f2, text="Evita robos de cuenta\ny protege tu identidad", font=(FUENTE, 8), bg=BG_COLOR, fg=TEXT_G).pack()

class PantallaIngreso(tk.Frame):
    def __init__(self, master, ctrl):
        super().__init__(master, bg=BG_COLOR)
        self.ctrl = ctrl
        tk.Button(self, text="<- VOLVER", font=(FUENTE, 10, "bold"), bg=BG_COLOR, fg=CYAN, relief="flat", command=ctrl.mostrar_inicio).pack(anchor="nw", padx=10, pady=10)
        
        centro = tk.Frame(self, bg=BG_COLOR)
        centro.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(centro, text="ESCRIBA SU CLAVE", font=(FUENTE, 16, "bold"), fg=TEXT_W, bg=BG_COLOR).pack(pady=5)
        zona = tk.Frame(centro, bg=BG_COLOR)
        zona.pack(pady=5)
        marco_e = tk.Frame(zona, bg=CYAN, bd=0)
        marco_e.pack(side="left", padx=5)
        self.e = tk.Entry(marco_e, width=14, font=(FUENTE, 16, "bold"), bg=BG_COLOR, fg=TEXT_W, insertbackground=CYAN, relief="flat", justify="center", show="*")
        self.e.pack(padx=2, pady=2, ipady=3)
        self.vis = False
        self.c_ojo = tk.Canvas(zona, width=35, height=35, bg=BG_COLOR, highlightthickness=0, cursor="hand2")
        self.c_ojo.pack(side="left", padx=3)
        self.img_ojo = cargar_img("ojo", (35, 35))
        self.c_ojo.bind("<Button-1>", self.tog)
        self.dib_ojo()
        
        self.c_p = tk.Canvas(zona, width=35, height=35, bg=BG_COLOR, highlightthickness=0, cursor="hand2")
        self.c_p.pack(side="left", padx=3)
        img_p = cargar_img("papelera", (35, 35))
        if img_p:
            self.c_p.create_image(17, 17, image=img_p)
            self.img_p = img_p
            self.c_p.bind("<Button-1>", lambda e: self.e.delete(0, 'end') or self.eval())
        else:
            dibujar_icono_papelera(self.c_p, lambda: self.e.delete(0, 'end') or self.eval())
            
        self.c_g = tk.Canvas(zona, width=35, height=35, bg=BG_COLOR, highlightthickness=0, cursor="hand2")
        self.c_g.pack(side="left", padx=3)
        img_g = cargar_img("guardar", (35, 35))
        if img_g:
            self.c_g.create_image(17, 17, image=img_g)
            self.img_g = img_g
            self.c_g.bind("<Button-1>", lambda e: self.guardar_clave())
        else:
            dibujar_icono_guardar(self.c_g, self.guardar_clave)
            
        self.canvas = tk.Canvas(centro, width=340, height=270, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(pady=5)
        self.mon = dibujar_monitor_teclado(self.canvas)
        self.txt = self.canvas.create_text(170, 50, text="ESPERANDO\nCLAVE...", fill=GREEN, font=(FUENTE, 12, "bold"), justify="center")
        self.bar_f = self.canvas.create_rectangle(100, 85, 240, 95, fill="#222", outline=CYAN)
        self.bar_p = self.canvas.create_rectangle(100, 85, 100, 95, fill=GREEN, outline="")
        
        self.e.bind("<KeyPress>", self.press)
        self.e.bind("<KeyRelease>", self.rel)
        
        self.teclas = {}
        filas = ["1234567890", "qwertyuiop", "asdfghjklñ", "zxcvbnm.-_"]
        for i, fila in enumerate(filas):
            for j, k in enumerate(fila):
                r = self.canvas.create_rectangle(65+i*10 + j*21, 175+i*18, 65+i*10+j*21+17, 175+i*18+15, fill="#444", outline=CYAN)
                self.teclas[k] = r
                self.canvas.tag_bind(r, "<Enter>", lambda e, char=k: self.canvas.itemconfig(self.teclas[char], fill=MAGENTA))
                self.canvas.tag_bind(r, "<Leave>", lambda e, char=k: self.canvas.itemconfig(self.teclas[char], fill="#444"))
                self.canvas.tag_bind(r, "<Button-1>", lambda e, char=k: self.e.insert('end', char) or self.eval())
                
        r_sp = self.canvas.create_rectangle(125, 175+4*18, 235, 175+4*18+14, fill="#444", outline=CYAN)
        self.teclas[' '] = r_sp
        self.canvas.tag_bind(r_sp, "<Enter>", lambda e: self.canvas.itemconfig(self.teclas[' '], fill=MAGENTA))
        self.canvas.tag_bind(r_sp, "<Leave>", lambda e: self.canvas.itemconfig(self.teclas[' '], fill="#444"))
        self.canvas.tag_bind(r_sp, "<Button-1>", lambda e: self.e.insert('end', ' ') or self.eval())
        self.map_s = {'!':'1','@':'2','#':'3','$':'4','%':'5','^':'6','&':'7','*':'8','(':'9',')':'0','?':'-','¿':'.','=':'_','+':'-','<':',','>':'.'}
        
        p_inf = tk.Frame(centro, bg=BG_COLOR, highlightbackground="#1A1F30", highlightthickness=2)
        p_inf.pack(fill="x", padx=15, pady=(15, 0))
        tk.Label(p_inf, text="💡 CONSEJO:\nUsa combinaciones de letras, números\ny símbolos para crear una clave fuerte.", font=(FUENTE, 9), bg=BG_COLOR, fg=YELLOW, justify="left").pack(padx=10, pady=10)

    def guardar_clave(self, e=None):
        pwd = self.e.get()
        if pwd:
            self.clipboard_clear()
            self.clipboard_append(pwd)
            guardar_en_archivo("Clave Evaluada", pwd)
            messagebox.showinfo("Éxito", "¡Clave copiada y guardada en la carpeta 'Mis_Contrasenas'!")

    def dib_ojo(self):
        self.c_ojo.delete("all")
        if self.img_ojo:
            self.c_ojo.create_image(17, 17, image=self.img_ojo)
        else:
            self.c_ojo.create_polygon(4, 17, 17, 7, 30, 17, 17, 27, fill="", outline=CYAN, width=2)
            self.c_ojo.create_oval(12, 12, 22, 22, outline=CYAN, width=2)
            self.c_ojo.create_oval(15, 15, 19, 19, fill=CYAN)
        if not self.vis:
            self.c_ojo.create_line(4, 4, 31, 31, fill=RED, width=3)

    def tog(self, e):
        self.vis = not self.vis
        self.e.config(show="" if self.vis else "*")
        self.dib_ojo()

    def press(self, e):
        c = self.map_s.get(e.char.lower(), e.char.lower())
        if c in self.teclas: self.canvas.itemconfig(self.teclas[c], fill=MAGENTA)

    def rel(self, e):
        c = self.map_s.get(e.char.lower(), e.char.lower())
        if c in self.teclas: self.canvas.itemconfig(self.teclas[c], fill="#444")
        self.eval()

    def eval(self, e=None):
        pwd = self.e.get()
        l = len(pwd)
        low = bool(re.search(r'[a-z]', pwd))
        up = bool(re.search(r'[A-Z]', pwd))
        dig = bool(re.search(r'\d', pwd))
        sym = bool(re.search(r'[^a-zA-Z0-9\s]', pwd))
        pts = low + up + dig + sym

        if l == 0:
            self.canvas.itemconfig(self.txt, text="ESPERANDO\nCLAVE...", fill=GREEN)
            self.canvas.itemconfig(self.mon, fill="#050505")
            self.canvas.coords(self.bar_p, 100, 85, 100, 95)
        elif l < 8 or pts < 2:
            self.canvas.itemconfig(self.txt, text="CLAVE\nDEBIL", fill=RED)
            self.canvas.itemconfig(self.mon, fill="#220505")
            self.canvas.coords(self.bar_p, 100, 85, 146, 95)
            self.canvas.itemconfig(self.bar_p, fill=RED)
        elif l < 10 or pts < 3:
            self.canvas.itemconfig(self.txt, text="CLAVE\nREGULAR", fill=CYAN)
            self.canvas.itemconfig(self.mon, fill="#051C22")
            self.canvas.coords(self.bar_p, 100, 85, 193, 95)
            self.canvas.itemconfig(self.bar_p, fill=CYAN)
        else:
            self.canvas.itemconfig(self.txt, text="CLAVE\nFUERTE", fill=GREEN)
            self.canvas.itemconfig(self.mon, fill="#052205")
            self.canvas.coords(self.bar_p, 100, 85, 240, 95)
            self.canvas.itemconfig(self.bar_p, fill=GREEN)

class PantallaRecomendar(tk.Frame):
    def __init__(self, master, ctrl):
        super().__init__(master, bg=BG_COLOR)
        tk.Button(self, text="<- VOLVER", font=(FUENTE, 10, "bold"), bg=BG_COLOR, fg=CYAN, relief="flat", command=ctrl.mostrar_inicio).pack(anchor="nw", padx=10, pady=10)
        
        centro = tk.Frame(self, bg=BG_COLOR)
        centro.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(centro, text="RECOMENDACIÓN DE\nCONTRASEÑA SEGURA", font=(FUENTE, 14, "bold"), fg=TEXT_W, bg=BG_COLOR).pack(pady=5)
        tk.Label(centro, text="Haz clic en el cubo para generar\nuna contraseña", font=(FUENTE, 10), fg=TEXT_G, bg=BG_COLOR).pack()
        c = tk.Canvas(centro, width=150, height=130, bg=BG_COLOR, highlightthickness=0, cursor="hand2")
        c.pack(pady=10)
        img = cargar_img("cubo", (120, 120))
        if img:
            c.create_image(75, 65, image=img)
            self.img = img
            c.bind("<Button-1>", lambda e: self.gen())
        else:
            dibujar_cubo_amarillo(c, self.gen)
            
        marco = tk.Frame(centro, bg=BG_COLOR, highlightbackground=YELLOW, highlightthickness=2)
        marco.pack(pady=15, padx=40, fill="x")
        self.lbl = tk.Label(marco, text="Clic en el cubo", font=(FUENTE, 14, "bold"), fg=YELLOW, bg=BG_COLOR)
        self.lbl.pack(side="left", expand=True, pady=12, padx=10)
        
        c_g = tk.Canvas(marco, width=35, height=35, bg=BG_COLOR, highlightthickness=0, cursor="hand2")
        c_g.pack(side="right", padx=10)
        img_g = cargar_img("guardar", (35, 35))
        if img_g:
            c_g.create_image(17, 17, image=img_g)
            self.img_g = img_g
            c_g.bind("<Button-1>", lambda e: self.copiar())
        else:
            dibujar_icono_guardar(c_g, self.copiar)
            
        p_inf = tk.Frame(centro, bg=BG_COLOR, highlightbackground="#1A1F30", highlightthickness=2)
        p_inf.pack(fill="x", padx=15, pady=(15, 0))
        tk.Label(p_inf, text="🚀 ¡Anímate!\nContraseña generada aleatoriamente\nes casi imposible de hackear.\n¡Tu seguridad es lo primero!", font=(FUENTE, 9, "bold"), bg=BG_COLOR, fg=GREEN, justify="center").pack(padx=10, pady=12)

    def gen(self, e=None):
        self.lbl.config(text=''.join(secrets.choice(string.ascii_letters+string.digits+"!@#$%&*_") for _ in range(12)), fg=GREEN)

    def copiar(self, e=None):
        pwd = self.lbl.cget("text")
        if pwd and pwd != "Clic en el cubo":
            self.clipboard_clear()
            self.clipboard_append(pwd)
            guardar_en_archivo("Clave Generada", pwd)
            messagebox.showinfo("Éxito", "¡Clave copiada y guardada en la carpeta 'Mis_Contrasenas'!")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor Retro Cyberpunk")
        w, h = 460, 640
        x = (self.winfo_screenwidth()//2) - (w//2)
        y = (self.winfo_screenheight()//2) - (h//2)
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.configure(bg=BG_COLOR)
        cont = tk.Frame(self, bg=BG_COLOR)
        cont.pack(fill="both", expand=True)
        
        # MAGIA PARA QUE EL CENTRADO FUNCIONE AL MAXIMIZAR
        cont.grid_rowconfigure(0, weight=1)
        cont.grid_columnconfigure(0, weight=1)
        
        self.f = {PantallaInicio: PantallaInicio(cont, self), PantallaIngreso: PantallaIngreso(cont, self), PantallaRecomendar: PantallaRecomendar(cont, self)}
        for f in self.f.values(): f.grid(row=0, column=0, sticky="nsew")
        self.mostrar_inicio()
        
    def mostrar_inicio(self): self.f[PantallaInicio].tkraise()
    def mostrar_ingreso(self): self.f[PantallaIngreso].e.delete(0, 'end'); self.f[PantallaIngreso].eval(); self.f[PantallaIngreso].tkraise()
    def mostrar_recomendacion(self): self.f[PantallaRecomendar].lbl.config(text="Clic en el cubo", fg=YELLOW); self.f[PantallaRecomendar].tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()