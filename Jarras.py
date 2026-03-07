import tkinter as tk
from tkinter import messagebox
from collections import deque
import time

# ---------Definicion de Metodos------------


def generar_sucesores(estado, cap_a, cap_b):
    x, y = estado
    sucesores = []

    sucesores.append((cap_a, y))
    sucesores.append((x, cap_b))
    sucesores.append((0, y))
    sucesores.append((x, 0))

    transferir = min(x, cap_b - y)
    sucesores.append((x - transferir, y + transferir))

    transferir = min(y, cap_a - x)
    sucesores.append((x + transferir, y - transferir))

    return sucesores


def reconstruir_camino(padre, estado_final):
    camino = [estado_final]
    while estado_final in padre:
        estado_final = padre[estado_final]
        camino.append(estado_final)
    camino.reverse()
    return camino


def bfs(cap_a, cap_b, objetivo):
    inicio = time.time()
    cola = deque([(0, 0)])
    visitados = set()
    padre = {}

    while cola:
        estado = cola.popleft()

        if estado in visitados:
            continue

        visitados.add(estado)

        x, y = estado
        if x == objetivo or y == objetivo:
            fin = time.time()
            return reconstruir_camino(padre, estado), fin - inicio, len(visitados)

        for sucesor in generar_sucesores(estado, cap_a, cap_b):
            if sucesor not in visitados:
                cola.append(sucesor)
                padre[sucesor] = estado

    return None, None, None


def dfs(cap_a, cap_b, objetivo):
    inicio = time.time()
    pila = [(0, 0)]
    visitados = set()
    padre = {}

    while pila:
        estado = pila.pop()

        if estado in visitados:
            continue

        visitados.add(estado)

        x, y = estado
        if x == objetivo or y == objetivo:
            fin = time.time()
            return reconstruir_camino(padre, estado), fin - inicio, len(visitados)

        for sucesor in generar_sucesores(estado, cap_a, cap_b):
            if sucesor not in visitados:
                pila.append(sucesor)
                padre[sucesor] = estado

    return None, None, None


#------- FUNCION EJECUTAR (Metodo por colas o por pilas)--------


def ejecutar(tipo):
    try:
        cap_a = int(entry_a.get())
        cap_b = int(entry_b.get())
        objetivo = int(entry_obj.get())

        if tipo == "BFS":
            camino, tiempo, explorados = bfs(cap_a, cap_b, objetivo)
        else:
            camino, tiempo, explorados = dfs(cap_a, cap_b, objetivo)

        resultado_text.delete("1.0", tk.END)

        if camino:
            resultado_text.insert(tk.END, f"Algoritmo: {tipo}\n")
            resultado_text.insert(tk.END, f"Tiempo: {tiempo:.6f} segundos\n")
            resultado_text.insert(tk.END, f"Estados explorados: {explorados}\n\n")
            resultado_text.insert(tk.END, "Camino:\n\n")

            for paso in camino:
                resultado_text.insert(tk.END, f"{paso}\n")
        else:
            messagebox.showinfo("Resultado", "No hay solución.")

    except ValueError:
        messagebox.showerror("Error", "Ingresa solo números enteros.")

# -----------CONFIGURACION DE INTERFAZ--------------

ventana = tk.Tk()
ventana.geometry("900x550")
ventana.overrideredirect(True)
ventana.config(bg="#141421")

# -------- Barra superior --------
barra = tk.Frame(ventana, bg="#1f1f35", height=45)
barra.pack(fill="x")

titulo = tk.Label(barra, text="Problema de las Jarras  |  BFS vs DFS",
                  bg="#1f1f35", fg="white",
                  font=("Segoe UI", 12, "bold"))
titulo.pack(side="left", padx=15)

def cerrar():
    ventana.destroy()

def minimizar():
    ventana.iconify()

tk.Button(barra, text="—", bg="#1f1f35", fg="white",
          bd=0, command=minimizar,
          font=("Segoe UI", 14)).pack(side="right", padx=10)

tk.Button(barra, text="✕", bg="#1f1f35", fg="#ff4d4d",
          bd=0, command=cerrar,
          font=("Segoe UI", 12, "bold")).pack(side="right")

# Permitir arrastrar
def iniciar_movimiento(event):
    ventana.x = event.x
    ventana.y = event.y

def mover_ventana(event):
    x = event.x_root - ventana.x
    y = event.y_root - ventana.y
    ventana.geometry(f"+{x}+{y}")

barra.bind("<Button-1>", iniciar_movimiento)
barra.bind("<B1-Motion>", mover_ventana)

# -------- Contenedor principal --------
main_frame = tk.Frame(ventana, bg="#141421")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Configuración de columnas
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=2)

# -------- Columna izquierda --------
left_panel = tk.Frame(main_frame, bg="#1c1c2e")
left_panel.grid(row=0, column=0, sticky="nsew", padx=(0,15))

tk.Label(left_panel, text="Configuración",
         bg="#1c1c2e", fg="white",
         font=("Segoe UI", 13, "bold")).pack(pady=15)

label_style = {"bg":"#1c1c2e","fg":"#cccccc","font":("Segoe UI",10)}

tk.Label(left_panel, text="Capacidad Jarra A", **label_style).pack(pady=(10,0))
entry_a = tk.Entry(left_panel, font=("Segoe UI",11))
entry_a.pack(pady=5)

tk.Label(left_panel, text="Capacidad Jarra B", **label_style).pack(pady=(10,0))
entry_b = tk.Entry(left_panel, font=("Segoe UI",11))
entry_b.pack(pady=5)

tk.Label(left_panel, text="Objetivo", **label_style).pack(pady=(10,0))
entry_obj = tk.Entry(left_panel, font=("Segoe UI",11))
entry_obj.pack(pady=5)

tk.Button(left_panel, text="Ejecutar BFS",
          bg="#00c853", fg="white",
          font=("Segoe UI",10,"bold"),
          width=20,
          command=lambda: ejecutar("BFS")).pack(pady=15)

tk.Button(left_panel, text="Ejecutar DFS",
          bg="#2979ff", fg="white",
          font=("Segoe UI",10,"bold"),
          width=20,
          command=lambda: ejecutar("DFS")).pack()

# -------- Columna derecha --------
right_panel = tk.Frame(main_frame, bg="#1c1c2e")
right_panel.grid(row=0, column=1, sticky="nsew")

tk.Label(right_panel, text="Resultados",
         bg="#1c1c2e", fg="white",
         font=("Segoe UI", 13, "bold")).pack(pady=15)

resultado_text = tk.Text(right_panel,
                         bg="#111122",
                         fg="#e0e0e0",
                         font=("Consolas",10),
                         bd=0)
resultado_text.pack(fill="both", expand=True, padx=20, pady=10)

ventana.mainloop()