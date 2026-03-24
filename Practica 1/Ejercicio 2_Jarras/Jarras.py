import tkinter as tk
from tkinter import messagebox
from collections import deque
import time
import tracemalloc

# ---------Definicion de Metodos------------

# Genera todas las posibles combinaciones a realizar desde un estado
# 1. Llenar por completo cualquiera de las jarras (A o B).
# 2. Vaciar por completo cualquiera de las jarras (A o B).
# 3. Transferir agua de la jarra A a la B (hasta vaciar A o llenar B).
# 4. Transferir agua de la jarra B a la A (hasta vaciar B o llenar A).
def generar_sucesores(estado, cap_a, cap_b):
    x, y = estado
    sucesores = []

    # 1. Llenar jarras
    sucesores.append((cap_a, y)) # Llenar jarra A
    sucesores.append((x, cap_b)) # Llenar jarra B
    
    # 2. Vaciar jarras
    sucesores.append((0, y))     # Vaciar jarra A
    sucesores.append((x, 0))     # Vaciar jarra B

    # 3. Transferir de A hacia B
    transferir = min(x, cap_b - y)
    sucesores.append((x - transferir, y + transferir))

    # 4. Transferir de B hacia A
    transferir = min(y, cap_a - x)
    sucesores.append((x + transferir, y - transferir))

    return sucesores

# Función para reconstruir el camino (para imprimir)
# Recibe al estado final y un diccionario con los padres de cada estado.
# 1. Iniciar el camino con el estado final (objetivo alcanzado).
# 2. Rastrear hacia atrás buscando el estado predecesor (el "padre") del estado actual.
# 3. Añadir cada estado predecesor a la lista del camino hasta llegar al estado inicial (que no tiene padre).
# 4. Invertir la lista para que el orden sea cronológico (del estado inicial al final).
def reconstruir_camino(padre, estado_final):
    # 1. Iniciar el camino
    camino = [estado_final]
    
    # 2 y 3. Rastrear hacia atrás y añadir a la lista
    while estado_final in padre:
        estado_final = padre[estado_final] # Padre de nodo actual
        camino.append(estado_final)
        
    # 4. Invertir el camino
    camino.reverse()
    
    return camino


# -------- BFS --------
# params
# cap_a: capacidad de la jarra A
# cap_b: capacidad de la jarra B
# objetivo: cantidad de agua que se desea obtener en alguna de las jarras
def bfs(cap_a, cap_b, objetivo):

    tracemalloc.start()
    inicio = time.time()

    cola = deque([(0, 0)])
    visitados = set()
    padre = {}

    while cola:
        # Obtener el estado actual de la cola
        estado = cola.popleft()

        # Si el estado ya ha sido visitado, se omite
        if estado in visitados:
            continue
        
        # Marcar el estado como visitado
        visitados.add(estado)

        # Verificar si el estado actual cumple con el objetivo
        x, y = estado
        if x == objetivo or y == objetivo:
            fin = time.time()

            memoria_actual, memoria_max = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            memoria_mb = memoria_max / (1024 * 1024)

            # Reconstruir el camino desde el estado final hasta el estado inicial 
            # Retorna camino, tiempo, nodos visitados, memoria
            return reconstruir_camino(padre, estado), fin - inicio, len(visitados), memoria_mb

        # Si el estado no es el objetivo, genera sucesores y agrega a la cola los no visitados
        for sucesor in generar_sucesores(estado, cap_a, cap_b):
            if sucesor not in visitados:
                cola.append(sucesor)
                padre[sucesor] = estado

    tracemalloc.stop()
    return None, None, None, None


# -------- DFS --------
# params
# cap_a: capacidad de la jarra A
# cap_b: capacidad de la jarra B
# objetivo: cantidad de agua que se desea obtener en alguna de las jarras
def dfs(cap_a, cap_b, objetivo):

    tracemalloc.start()
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

            memoria_actual, memoria_max = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            memoria_mb = memoria_max / (1024 * 1024)

            return reconstruir_camino(padre, estado), fin - inicio, len(visitados), memoria_mb

        for sucesor in generar_sucesores(estado, cap_a, cap_b):
            if sucesor not in visitados:
                pila.append(sucesor)
                padre[sucesor] = estado

    tracemalloc.stop()
    return None, None, None, None


#------- FUNCION EJECUTAR --------

def ejecutar(tipo):
    try:
        cap_a = int(entry_a.get())      # Capacidad de Jarra A
        cap_b = int(entry_b.get())      # Capacidad de Jarra B
        objetivo = int(entry_obj.get()) # Capacidad objetivo

        # Determinar algoritmo a ejecutar
        if tipo == "BFS":
            camino, tiempo, explorados, memoria = bfs(cap_a, cap_b, objetivo)
        else:
            camino, tiempo, explorados, memoria = dfs(cap_a, cap_b, objetivo)

        resultado_text.delete("1.0", tk.END)

        # Impresión de resultados
        if camino:
            resultado_text.insert(tk.END, f"Algoritmo: {tipo}\n")
            resultado_text.insert(tk.END, f"Tiempo: {tiempo:.6f} segundos\n")
            resultado_text.insert(tk.END, f"Memoria usada: {memoria:.6f} MB\n")
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
#ventana.overrideredirect(True)
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

# Permitir arrastrar ventana

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

main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=2)

# -------- Panel izquierdo --------

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

# -------- Panel derecho --------

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