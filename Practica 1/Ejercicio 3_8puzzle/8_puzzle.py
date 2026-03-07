import tkinter as tk
from tkinter import ttk
from collections import deque
import heapq
import random
import threading
import time
import tracemalloc

# ═══════════════════════════════════════════════
#  PALETA  —  azul claro / blanco
# ═══════════════════════════════════════════════
C_BG          = "#FFFFFF"   # fondo principal
C_PANEL       = "#D6EAF8"   # paneles / tarjetas
C_PANEL2      = "#C5DCF0"   # panel más profundo
C_HEADER      = "#39B2D1"   # azul oscuro (header, btn primario)
C_ACCENT      = "#00FF9D"   # azul medio (btn secundario)
C_ACCENT2     = "#5DADE2"   # azul claro (detalles)
C_TILE        = "#FFFFFF"   # ficha normal
C_TILE_HL     = "#FDD0D0"   # ficha animada (cálido)
C_TILE_DONE   = "#A6E3C1"   # ficha en estado resuelto
C_EMPTY       = "#E2E4E6"   # celda vacía
C_TILE_BORDER = "#2E9BD6"   # borde de ficha
C_TEXT_DARK   = "#000000"   # texto principal
C_TEXT_MID    = "#000000"   # texto secundario
C_TEXT_LIGHT  = "#FFFFFF"   # texto claro
C_BTN_RAND    = "#E62222"   # botón random 
C_BTN_STOP    = "#FF00AA"   # botón stop
C_TREE_NODE   = "#2E9BD6"   # nodo normal en árbol
C_TREE_DONE   = "#27AE60"   # nodo resuelto en árbol
C_STAT_BG     = "#EEFFFF"   # fondo de sección de métricas

OBJETIVO = (1, 2, 3, 4, 5, 6, 7, 8, 0)

MOVIMIENTOS = {
    "arriba":    -3,    
    "abajo":      3,    
    "izquierda": -1,    
    "derecha":    1,    
}

ARROW = {
    "arriba":    "↑",
    "abajo":     "↓",
    "izquierda": "←",
    "derecha":   "→",
}

# ═══════════════════════════════════════════════
#  LÓGICA DEL PUZZLE
# ═══════════════════════════════════════════════

def sucesores(estado):
    indice = estado.index(0)
    hijos = []
    for mov, cambio in MOVIMIENTOS.items():
        nuevo = indice + cambio
        if mov == "izquierda" and indice % 3 == 0: continue
        if mov == "derecha"   and indice % 3 == 2: continue
        if nuevo < 0 or nuevo > 8: continue
        lista = list(estado)
        lista[indice], lista[nuevo] = lista[nuevo], lista[indice]
        hijos.append((tuple(lista), mov))
    return hijos


def es_resoluble(estado):
    lista = [x for x in estado if x != 0]
    inv = sum(1 for i in range(len(lista))
                for j in range(i + 1, len(lista))
                if lista[i] > lista[j])
    return inv % 2 == 0


def manhattan(estado):
    dist = 0
    for i, v in enumerate(estado):
        if v == 0: continue
        r1, c1 = divmod(i, v - 1) if False else (i // 3, i % 3)
        r2, c2 = (v - 1) // 3, (v - 1) % 3
        dist += abs(r1 - r2) + abs(c1 - c2)
    return dist

# ═══════════════════════════════════════════════
#  ALGORITMOS
# ═══════════════════════════════════════════════

def bfs(inicial, callback=None):
    cola = deque([(inicial, [], [], 0)])
    visitados = {inicial}
    while cola:
        estado, camino, movs, prof = cola.popleft()
        if callback: callback()
        if estado == OBJETIVO:
            return camino + [estado], movs, prof
        for hijo, mov in sucesores(estado):
            if hijo not in visitados:
                visitados.add(hijo)
                cola.append((hijo, camino + [estado], movs + [mov], prof + 1))
    return None, None, None

def dfs(inicial, callback=None):
    pila = [(inicial, [], [], 0)]
    visitados = set()
    while pila:
        estado, camino, movs, prof = pila.pop()
        if callback: callback()
        if estado == OBJETIVO:
            return camino + [estado], movs, prof
        if estado not in visitados:
            visitados.add(estado)
            for hijo, mov in sucesores(estado):
                pila.append((hijo, camino + [estado], movs + [mov], prof + 1))
    return None, None, None

def astar(inicial, callback=None):
    heap = []
    heapq.heappush(heap, (0, inicial, [], [], 0))
    visitados = set()
    while heap:
        f, estado, camino, movs, prof = heapq.heappop(heap)
        if callback: callback()
        if estado == OBJETIVO:
            return camino + [estado], movs, prof
        if estado in visitados: continue
        visitados.add(estado)
        for hijo, mov in sucesores(estado):
            g = prof + 1
            h = manhattan(hijo)
            heapq.heappush(heap, (g + h, hijo, camino + [estado], movs + [mov], g))
    return None, None, None

# ═══════════════════════════════════════════════
#  INTERFAZ
# ═══════════════════════════════════════════════

class PuzzleGUI:

    TS = 96   # tile size

    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle")
        self.root.resizable(False, False)
        self.root.configure(bg=C_BG)

        self.estado     = (1, 2, 3, 4, 5, 6, 7, 0, 8)
        self.nodos      = 0
        self.solucion   = []
        self.movs       = []
        self.highlight  = None
        self._solved    = False

        self._build_ui()
        self._draw_board()

    # ─── construcción ────────────────────────────

    def _build_ui(self):
        # cabecera
        hdr = tk.Frame(self.root, bg=C_HEADER, pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="8-Puzzle",
                 font=("Georgia", 20, "bold"),
                 bg=C_HEADER, fg=C_TEXT_LIGHT).pack()

        # cuerpo
        body = tk.Frame(self.root, bg=C_BG, padx=16, pady=10)
        body.pack(fill="both", expand=True)

        # col 1 — tablero
        col1 = tk.Frame(body, bg=C_BG)
        col1.grid(row=0, column=0, padx=(0, 16), sticky="n")
        self._build_board(col1)
        self._build_buttons(col1)

        # col 2 — stats + scroll frame con árbol y movimientos
        col2 = tk.Frame(body, bg=C_BG)
        col2.grid(row=0, column=1, sticky="nsew")
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)
        
        self._build_stats(col2)
        self._build_scrollable_content(col2)

    def _build_board(self, parent):
        lbl = tk.Label(parent, text="TABLERO",
                       font=("Georgia", 10, "bold"),
                       bg=C_BG, fg=C_TEXT_DARK)
        lbl.pack(anchor="w", pady=(0, 4))

        self.canvas = tk.Canvas(
            parent,
            width=self.TS * 3 + 6,
            height=self.TS * 3 + 6,
            bg=C_BG, highlightthickness=0
        )
        self.canvas.pack()

    def _build_buttons(self, parent):
        f = tk.Frame(parent, bg=C_PANEL, pady=8, padx=8)
        f.pack(fill="x", pady=(12, 0))
        tk.Label(f, text="ALGORITMOS",
                 font=("Georgia", 9, "bold"),
                 bg=C_PANEL, fg=C_TEXT_DARK).grid(
            row=0, column=0, columnspan=4, pady=(0, 6))

        def btn(parent, text, cmd, bg):
            return tk.Button(
                parent, text=text, command=cmd,
                bg=bg, fg=C_TEXT_LIGHT,
                activebackground=bg, activeforeground=C_TEXT_LIGHT,
                font=("Georgia", 10, "bold"),
                relief="flat", cursor="hand2",
                padx=8, pady=5, bd=0
            )

        btn(f, "▶ BFS",    lambda: self.run_algo(bfs, "BFS"),    C_HEADER).grid(row=1, column=0, padx=3)
        btn(f, "▶ DFS",    lambda: self.run_algo(dfs, "DFS"),    C_ACCENT).grid(row=1, column=1, padx=3)
        btn(f, "▶ A★",    lambda: self.run_algo(astar, "A*"),   "#1A7A4A").grid(row=1, column=2, padx=3)
        btn(f, "🔀 Rand",  self.randomizar,                       C_BTN_RAND).grid(row=1, column=3, padx=3)

    def _build_stats(self, parent):
        f = tk.Frame(parent, bg=C_STAT_BG, pady=10, padx=12,
                     relief="flat", bd=1)
        f.pack(fill="x", pady=(0, 10))
        tk.Label(f, text="MÉTRICAS",
                 font=("Georgia", 10, "bold"),
                 bg=C_STAT_BG, fg=C_TEXT_DARK).pack(anchor="w")

        self._stat_labels = {}
        defs = [
            ("algo",  "Algoritmo",  "—"),
            ("pasos", "Pasos",      "0"),
            ("tiempo","Tiempo",     "0 s"),
            ("mem",   "Memoria",    "0 KB"),
            ("nodos", "Nodos exp.", "0"),
            ("prof",  "Profund.",   "0"),
        ]
        for key, label, val in defs:
            row = tk.Frame(f, bg=C_STAT_BG)
            row.pack(fill="x", pady=1)
            tk.Label(row, text=f"{label}:", width=12, anchor="w",
                     font=("Georgia", 9), bg=C_STAT_BG,
                     fg=C_TEXT_MID).pack(side="left")
            lbl = tk.Label(row, text=val, anchor="w",
                           font=("Courier", 9, "bold"),
                           bg=C_STAT_BG, fg=C_TEXT_DARK)
            lbl.pack(side="left")
            self._stat_labels[key] = lbl

        self.progress = ttk.Progressbar(f, orient="horizontal",
                                         length=220, mode="determinate")
        self.progress.pack(pady=(6, 0))

    def _build_scrollable_content(self, parent):
        # Frame contenedor para el canvas scrolleable
        scroll_frame = tk.Frame(parent, bg=C_BG)
        scroll_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Canvas y scrollbar
        canvas = tk.Canvas(scroll_frame, bg=C_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
        
        # Frame interno para contener los widgets
        content_frame = tk.Frame(canvas, bg=C_BG)
        content_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")
        
        # Configurar la región scrollable
        def on_frame_configure(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            if canvas.winfo_width() > 1:
                canvas.itemconfig(content_window, width=canvas.winfo_width())
        
        def on_canvas_configure(event):
            on_frame_configure()
        
        content_frame.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Soporte para mouse wheel
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Construir movimientos primero (arriba, pequeño) y luego árbol (abajo, grande)
        self._build_move_log(content_frame)
        self._build_tree_panel(content_frame)

    def _build_tree_panel(self, parent):
        tk.Label(parent, text="ÁRBOL DE BÚSQUEDA (profundidad)",
                 font=("Georgia", 9, "bold"),
                 bg=C_BG, fg=C_TEXT_DARK).pack(anchor="w", pady=(10, 4))
        self.tree_canvas = tk.Canvas(parent, width=310, height=500,
                                      bg=C_PANEL, highlightthickness=1,
                                      highlightbackground=C_TILE_BORDER)
        self.tree_canvas.pack(pady=(2, 10), fill="both", expand=True)

    def _build_move_log(self, parent):
        tk.Label(parent, text="SECUENCIA DE MOVIMIENTOS",
                 font=("Georgia", 9, "bold"),
                 bg=C_BG, fg=C_TEXT_DARK).pack(anchor="w", pady=(0, 4))
        f = tk.Frame(parent, bg=C_BG)
        f.pack(fill="x", pady=(0, 10), padx=(0, 15))
        sb = tk.Scrollbar(f)
        sb.pack(side="right", fill="y")
        self.log_box = tk.Listbox(
            f, yscrollcommand=sb.set,
            font=("Courier", 8),
            bg=C_PANEL, fg=C_TEXT_DARK,
            selectbackground=C_HEADER,
            selectforeground=C_TEXT_LIGHT,
            width=32, height=6,
            bd=0, relief="flat", activestyle="none"
        )
        self.log_box.pack(side="left", fill="both")
        sb.config(command=self.log_box.yview)

    # ─── tablero ─────────────────────────────────

    def _draw_board(self, highlight=None):
        self.canvas.delete("all")
        S = self.TS
        pad = 3
        for i, v in enumerate(self.estado):
            r, c = divmod(i, 3)
            x0 = c * S + pad
            y0 = r * S + pad
            x1 = x0 + S - pad * 2
            y1 = y0 + S - pad * 2
            if v == 0:
                self.canvas.create_rectangle(x0, y0, x1, y1,
                                              fill=C_EMPTY, outline=C_TILE_BORDER, width=2)
            else:
                is_hl   = (i == highlight)
                is_done = self._solved and v == i + 1
                color   = C_TILE_DONE if is_done else (C_TILE_HL if is_hl else C_TILE)
                # sombra
                self.canvas.create_rectangle(x0 + 4, y0 + 4, x1 + 4, y1 + 4,
                                              fill="#B3CCE0", outline="")
                self.canvas.create_rectangle(x0, y0, x1, y1,
                                              fill=color, outline=C_TILE_BORDER, width=2)
                self.canvas.create_text(
                    (x0 + x1) // 2, (y0 + y1) // 2,
                    text=str(v),
                    font=("Georgia", 26, "bold"),
                    fill=C_TEXT_DARK
                )

    # ─── árbol visual ────────────────────────────

    def _draw_tree(self, depth):
        c = self.tree_canvas
        c.delete("all")
        if depth == 0: return
        W, H = 310, 500
        node_r = 10
        levels = min(depth, 10)
        y_step = (H - 40) / max(levels, 1)

        prev_nodes = [(W // 2, 30)]
        c.create_oval(W//2 - node_r, 30 - node_r,
                      W//2 + node_r, 30 + node_r,
                      fill=C_TREE_DONE, outline="")

        for d in range(1, levels + 1):
            count  = min(2 ** d, 8)
            x_step = W / (count + 1)
            cur_nodes = [(int(x_step * (k + 1)), int(30 + d * y_step))
                         for k in range(count)]
            for px, py in prev_nodes:
                for nx, ny in cur_nodes[:2]:
                    c.create_line(px, py, nx, ny,
                                  fill=C_ACCENT2, width=1)
            for nx, ny in cur_nodes:
                col = C_TREE_DONE if d == levels else C_TREE_NODE
                c.create_oval(nx - node_r, ny - node_r,
                              nx + node_r, ny + node_r,
                              fill=col, outline="white", width=1)
            prev_nodes = cur_nodes

    # ─── log de movimientos ──────────────────────

    def _refresh_log(self):
        self.log_box.delete(0, "end")
        for i in range(len(self.solucion)):
            arrow = f"  {ARROW[self.movs[i-1]]}" if i > 0 and i <= len(self.movs) else ""
            self.log_box.insert("end", f" ○  Paso {i:>3}{arrow}  [{self.movs[i-1] if i>0 and i<=len(self.movs) else '':>9}]" if i > 0 and i <= len(self.movs) else f" ○  Paso   0  — inicial")
            self.log_box.itemconfig(i, bg=C_PANEL, fg=C_TEXT_DARK)

    # ─── animación ───────────────────────────────

    def _animate(self, idx=0):
        if idx >= len(self.solucion): return
        self.estado = self.solucion[idx]
        self._solved = (self.estado == OBJETIVO)
        hl = None
        if idx > 0:
            prev = self.solucion[idx - 1]
            for k in range(9):
                if prev[k] != self.solucion[idx][k] and self.solucion[idx][k] != 0:
                    hl = k
                    break
        self._draw_board(highlight=hl)
        self._refresh_log()
        self.root.after(500,
                        lambda: self._animate(idx + 1))

    # ─── callback nodos ──────────────────────────

    def _update_nodes(self):
        self.nodos += 1
        if self.nodos % 50 == 0:
            self.root.after(0, lambda: (
                self._stat_labels["nodos"].config(
                    text=str(self.nodos)),
                self.progress.step(1)
            ))

    # ─── randomizar ──────────────────────────────

    def randomizar(self):
        while True:
            lista = list(OBJETIVO)
            random.shuffle(lista)
            if es_resoluble(lista):
                self.estado = tuple(lista)
                break
        self.solucion    = []
        self.movs        = []
        self._solved     = False
        self.log_box.delete(0, "end")
        self._draw_board()

    # ─── correr algoritmo ────────────────────────

    def run_algo(self, algoritmo, nombre):
        self.nodos = 0
        self.progress["value"] = 0
        for k in self._stat_labels:
            self._stat_labels[k].config(text="calculando…")
        def task():
            tracemalloc.start()
            t0 = time.time()
            sol, movs, prof = algoritmo(self.estado, self._update_nodes)
            t1 = time.time()
            _, pico = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            tiempo  = t1 - t0
            memoria = pico / 1024
            pasos   = len(movs) if movs else 0
            def ui():
                self._stat_labels["algo"].config( text=nombre)
                self._stat_labels["pasos"].config(text=str(pasos))
                self._stat_labels["tiempo"].config(text=f"{tiempo:.4f} s")
                self._stat_labels["mem"].config(  text=f"{memoria:.1f} KB")
                self._stat_labels["nodos"].config( text=str(self.nodos))
                self._stat_labels["prof"].config(  text=str(prof) if prof is not None else "?")
                self._draw_tree(prof or 0)
                if sol:
                    self.solucion = sol
                    self.movs     = movs
                    self._animate(0)

            self.root.after(0, ui)

        threading.Thread(target=task, daemon=True).start()
# ═══════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    PuzzleGUI(root)
    root.mainloop()
