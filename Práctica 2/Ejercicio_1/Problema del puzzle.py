import tkinter as tk
from tkinter import ttk
import heapq
import time
import tracemalloc
import threading
import random
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.style as mstyle
import networkx as nx


C = {
    "bg":        "#f0f4f8",
    "panel":     "#ffffff",
    "border":    "#c9d6e3",
    "accent":    "#2563eb",
    "accent2":   "#16a34a",
    "accent3":   "#dc2626",
    "text":      "#1e293b",
    "muted":     "#64748b",
    "tile":      "#dbeafe",
    "tile_text": "#1e40af",
    "tile_empty":"#e2e8f0",
    "best_row":  "#dcfce7",
    "hover":     "#eff6ff",
}

FONT_TITLE  = ("Consolas", 15, "bold")
FONT_LABEL  = ("Consolas", 10)
FONT_SMALL  = ("Consolas",  9)
FONT_NUMBER = ("Consolas", 22, "bold")
FONT_BTN    = ("Consolas", 10, "bold")
FONT_MONO   = ("Consolas",  9)


class Puzzle:
    def __init__(self, board, size):
        self.board = tuple(board)
        self.size  = size
        self.goal  = tuple(list(range(1, size * size)) + [0])

    def get_neighbors(self, state):
        neighbors = []
        zero = state.index(0)
        x, y = divmod(zero, self.size)
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx_, ny_ = x + dx, y + dy
            if 0 <= nx_ < self.size and 0 <= ny_ < self.size:
                idx = nx_ * self.size + ny_
                new = list(state)
                new[zero], new[idx] = new[idx], new[zero]
                neighbors.append(tuple(new))
        return neighbors


def h_misplaced(b, g, s):
    return sum(1 for i in range(len(b)) if b[i] != 0 and b[i] != g[i])

def h_manhattan(b, g, s):
    d = 0
    for i, v in enumerate(b):
        if v == 0: continue
        gi = g.index(v)
        x1, y1 = divmod(i, s)
        x2, y2 = divmod(gi, s)
        d += abs(x1 - x2) + abs(y1 - y2)
    return d

def h_custom(b, g, s):
    return h_manhattan(b, g, s) + h_misplaced(b, g, s)


def is_solvable(board, size):
    inv = 0
    b = [x for x in board if x != 0]
    for i in range(len(b)):
        for j in range(i + 1, len(b)):
            if b[i] > b[j]:
                inv += 1
    if size % 2 == 1:
        return inv % 2 == 0
    else:
        row = board.index(0) // size
        return (inv + row) % 2 == 1

def generate_board(size):
    board = list(range(size * size))
    while True:
        random.shuffle(board)
        if is_solvable(board, size):
            return tuple(board)

def astar(start, size, heuristic):
    puzzle    = Puzzle(start, size)
    goal      = puzzle.goal
    open_list = []
    heapq.heappush(open_list, (0, start))
    g       = {start: 0}
    parent  = {}
    visited = set()
    edges   = []

    while open_list:
        _, current = heapq.heappop(open_list)
        if current in visited:
            continue
        visited.add(current)
        if current == goal:
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()
            return path, edges
        for n in puzzle.get_neighbors(current):
            edges.append((current, n))
            cost = g[current] + 1
            if n not in g or cost < g[n]:
                g[n]       = cost
                parent[n]  = current
                f          = cost + heuristic(n, goal, size)
                heapq.heappush(open_list, (f, n))
    return [], edges


def evaluate(start, size, h, name):
    tracemalloc.start()
    t0 = time.time()
    path, edges = astar(start, size, h)
    t1 = time.time()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "name":  name,
        "cost":  len(path),
        "nodes": len(edges),
        "time":  round(t1 - t0, 4),
        "mem":   round(peak / 1024, 2),
        "path":  path,
        "edges": edges,
    }

class FlatButton(tk.Label):
    def __init__(self, master, text, command, accent=False, **kw):
        color = C["accent"] if accent else C["muted"]
        super().__init__(
            master,
            text=text,
            font=FONT_BTN,
            fg=color,
            bg=C["panel"],
            cursor="hand2",
            padx=14, pady=8,
            **kw
        )
        self._cmd     = command
        self._accent  = accent
        self._color   = color
        self.bind("<Button-1>", lambda e: command())
        self.bind("<Enter>",    self._on_enter)
        self.bind("<Leave>",    self._on_leave)

    def _on_enter(self, _):
        self.config(bg=C["hover"], fg=C["text"])

    def _on_leave(self, _):
        self.config(bg=C["panel"], fg=self._color)


class SectionLabel(tk.Label):
    def __init__(self, master, text, **kw):
        super().__init__(
            master,
            text=text,
            font=("Consolas", 8),
            fg=C["muted"],
            bg=C["panel"],
            anchor="w",
            **kw
        )



class App:
    def __init__(self, root):
        self.root    = root
        self.results = None
        self.current_board = None

        root.title("Heurísticas")
        root.configure(bg=C["bg"])
        root.resizable(True, True)

        self._build_styles()
        self._build_layout()
        self.new_board()

    
    def _build_styles(self):
        s = ttk.Style()
        s.theme_use("clam")

        s.configure("Dark.TFrame",         background=C["bg"])
        s.configure("Panel.TFrame",        background=C["panel"])
        s.configure("Dark.TNotebook",      background=C["bg"],    borderwidth=0)
        s.configure("Dark.TNotebook.Tab",
                    background=C["panel"], foreground=C["muted"],
                    font=FONT_SMALL,       padding=[12, 6],
                    borderwidth=0)
        s.map("Dark.TNotebook.Tab",
              background=[("selected", C["bg"])],
              foreground=[("selected", C["accent"])])

        s.configure("Dark.Treeview",
                    background=C["panel"], foreground=C["text"],
                    fieldbackground=C["panel"], rowheight=28,
                    font=FONT_SMALL, borderwidth=0)
        s.configure("Dark.Treeview.Heading",
                    background=C["bg"], foreground=C["muted"],
                    font=("Consolas", 9, "bold"), relief="flat")
        s.map("Dark.Treeview",
              background=[("selected", C["accent"])])

        s.configure("Dark.TCombobox",
                    fieldbackground=C["tile"], background=C["panel"],
                    foreground=C["text"],      font=FONT_LABEL,
                    arrowcolor=C["accent"],    bordercolor=C["border"])


    
    def _build_layout(self):
        
        topbar = tk.Frame(self.root, bg=C["panel"], height=48)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        tk.Label(topbar, text="◈", font=("Consolas", 18),
                 fg=C["accent"], bg=C["panel"]).pack(side="left", padx=(16, 6), pady=8)
        tk.Label(topbar, text="Puzzle",
                 font=("Consolas", 13, "bold"),
                 fg=C["text"], bg=C["panel"]).pack(side="left", pady=8)

        self.status_dot = tk.Label(topbar, text="●", font=("Consolas", 10),
                                   fg=C["muted"], bg=C["panel"])
        self.status_dot.pack(side="right", padx=(0, 8))
        self.status_lbl = tk.Label(topbar, text="idle",
                                   font=FONT_SMALL, fg=C["muted"], bg=C["panel"])
        self.status_lbl.pack(side="right")

        
        tk.Frame(self.root, bg=C["border"], height=1).pack(fill="x")

        
        body = tk.Frame(self.root, bg=C["bg"])
        body.pack(fill="both", expand=True)

        
        self._build_sidebar(body)

        
        tk.Frame(body, bg=C["border"], width=1).pack(side="left", fill="y")

        
        self._build_right(body)

   
    def _build_sidebar(self, parent):
        sb = tk.Frame(parent, bg=C["panel"], width=500)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

       
        SectionLabel(sb, "  TAMAÑO DEL PUZZLE").pack(fill="x", padx=8, pady=(18, 4))

        self.size = tk.IntVar(value=3)
        size_frame = tk.Frame(sb, bg=C["panel"])
        size_frame.pack(fill="x", padx=10, pady=4)

        for val, label in [(3, "3×3  (8)"), (4, "4×4  (15)")]:
            rb = tk.Radiobutton(
                size_frame, text=label, variable=self.size, value=val,
                font=FONT_SMALL, fg=C["text"], bg=C["panel"],
                selectcolor=C["bg"], activebackground=C["panel"],
                activeforeground=C["accent"], cursor="hand2",
                command=self.new_board
            )
            rb.pack(anchor="w", pady=2)

        
        tk.Frame(sb, bg=C["border"], height=1).pack(fill="x", padx=10, pady=10)

        
        SectionLabel(sb, "  ACCIONES").pack(fill="x", padx=8, pady=(0, 6))

        FlatButton(sb, "⟳  Nuevo tablero",   self.new_board,  accent=True).pack(fill="x", padx=10, pady=3)
        FlatButton(sb, "▶  Comparar heurísticas", self.run).pack(fill="x", padx=10, pady=3)

        
        tk.Frame(sb, bg=C["border"], height=1).pack(fill="x", padx=10, pady=10)

        
        SectionLabel(sb, "  HEURÍSTICAS").pack(fill="x", padx=8, pady=(0, 6))

        h_info = [
            ("Misplaced", C["accent3"],  "Fichas fuera de lugar"),
            ("Manhattan", C["accent"],   "Distancia suma absoluta"),
            ("Custom",    C["accent2"],  "Manhattan + Misplaced"),
        ]
        for name, color, desc in h_info:
            row = tk.Frame(sb, bg=C["panel"])
            row.pack(fill="x", padx=10, pady=3)
            tk.Label(row, text="▪", fg=color,  bg=C["panel"], font=("Consolas", 12)).pack(side="left")
            tk.Label(row, text=name, fg=C["text"],  bg=C["panel"], font=FONT_SMALL).pack(side="left", padx=4)
            tk.Label(row, text=desc, fg=C["muted"], bg=C["panel"], font=("Consolas", 8)).pack(side="left")

        
        tk.Label(sb, text="v2.0",
                 font=("Consolas", 8), fg=C["border"], bg=C["panel"]).pack(side="bottom", pady=8)

    
    def _build_right(self, parent):
        right = tk.Frame(parent, bg=C["bg"])
        right.pack(side="right", fill="both", expand=True)

        
        puzzle_area = tk.Frame(right, bg=C["bg"])
        puzzle_area.pack(fill="x", padx=20, pady=(16, 0))

        self.puzzle_title = tk.Label(
            puzzle_area, text="",
            font=FONT_TITLE, fg=C["text"], bg=C["bg"]
        )
        self.puzzle_title.pack(anchor="w")

        self.puzzle_sub = tk.Label(
            puzzle_area, text="",
            font=FONT_SMALL, fg=C["muted"], bg=C["bg"]
        )
        self.puzzle_sub.pack(anchor="w")

        
        canvas_wrap = tk.Frame(right, bg=C["bg"])
        canvas_wrap.pack(pady=12)

        self.canvas = tk.Canvas(canvas_wrap, bg=C["bg"],
                                highlightthickness=0, bd=0)
        self.canvas.pack()

        
        tk.Frame(right, bg=C["border"], height=1).pack(fill="x", padx=20)

        
        nb = ttk.Notebook(right, style="Dark.TNotebook")
        nb.pack(fill="both", expand=True, padx=20, pady=(10, 0))

        
        tab_table_frame = tk.Frame(nb, bg=C["bg"])
        nb.add(tab_table_frame, text="  Resultados  ")
        self._build_table_tab(tab_table_frame)

        
        tab_vis = tk.Frame(nb, bg=C["bg"])
        nb.add(tab_vis, text="  Visualización  ")
        self._build_visual_tab(tab_vis)

        explain_frame = tk.Frame(right, bg=C["panel"])
        explain_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(explain_frame, text="  INTERPRETACIÓN",
                 font=("Consolas", 8), fg=C["muted"],
                 bg=C["panel"]).pack(anchor="w", pady=(6, 2))

        self.explain_box = tk.Text(
            explain_frame, height=5,
            bg=C["panel"], fg=C["text"],
            font=FONT_MONO, bd=0, padx=10, pady=6,
            relief="flat", state="disabled",
            insertbackground=C["accent"]
        )
        self.explain_box.pack(fill="x", padx=6, pady=(0, 8))

    
    def _build_table_tab(self, parent):
        cols = ("h", "c", "n", "t", "m")
        headers = {
            "h": "Heurística",
            "c": "Movimientos",
            "n": "Nodos explorados",
            "t": "Tiempo (s)",
            "m": "Memoria (KB)",
        }
        widths = {"h": 130, "c": 100, "n": 150, "t": 100, "m": 110}

        frame = tk.Frame(parent, bg=C["bg"])
        frame.pack(fill="both", expand=True, pady=10)

        self.tab_table = ttk.Treeview(
            frame, columns=cols, show="headings",
            style="Dark.Treeview", height=6
        )
        for col in cols:
            self.tab_table.heading(col, text=headers[col])
            self.tab_table.column(col, width=widths[col], anchor="center")

        sb = tk.Scrollbar(frame, orient="vertical",
                          command=self.tab_table.yview,
                          bg=C["border"], troughcolor=C["panel"],
                          activebackground=C["accent"])
        self.tab_table.configure(yscrollcommand=sb.set)

        self.tab_table.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

    
    def _build_visual_tab(self, parent):
        row = tk.Frame(parent, bg=C["bg"])
        row.pack(pady=16)

        FlatButton(row, "  ⬡  Ver Árbol de Búsqueda",
                   self.show_graph, accent=True).pack(side="left", padx=6)
        FlatButton(row, "  ▤  Ver Gráfica Comparativa",
                   self.show_plot).pack(side="left", padx=6)

  
    def _set_status(self, text, color=None):
        color = color or C["muted"]
        self.status_lbl.config(text=text)
        self.status_dot.config(fg=color)

    def new_board(self):
        size = self.size.get()
        self.current_board = generate_board(size)
        name = f"Puzzle {'8 (3×3)' if size == 3 else '15 (4×4)'}"
        self.puzzle_title.config(text=name)
        self.draw(self.current_board, size)
        self._set_status("tablero listo", C["accent2"])

    def draw(self, board, size):
        self.canvas.delete("all")
        gap     = 4
        cell    = 90 if size == 3 else 70
        canvas_px = cell * size + gap * (size + 1)
        self.canvas.config(width=canvas_px, height=canvas_px)

        for i, v in enumerate(board):
            row, col = divmod(i, size)
            x1 = col * cell + gap * (col + 1)
            y1 = row * cell + gap * (row + 1)
            x2, y2 = x1 + cell, y1 + cell

            if v == 0:
                # celda vacía
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=C["tile_empty"], outline=C["border"], width=1
                )
            else:
                # sombra sutil
                self.canvas.create_rectangle(
                    x1 + 3, y1 + 3, x2 + 3, y2 + 3,
                    fill="#000000", outline="", width=0
                )
                # ficha
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=C["tile"], outline=C["border"], width=1
                )
                # número
                font_size = 22 if size == 3 else 16
                self.canvas.create_text(
                    (x1 + x2) // 2, (y1 + y2) // 2,
                    text=str(v),
                    font=("Consolas", font_size, "bold"),
                    fill=C["tile_text"]
                )

    def animate(self, path, size):
        def run():
            self._set_status("animando...", C["accent"])
            for state in path:
                self.canvas.after(0, lambda s=state: self.draw(s, size))
                time.sleep(0.25)
            self._set_status("animación completa", C["accent2"])
        threading.Thread(target=run, daemon=True).start()

    def run(self):
        size  = self.size.get()
        board = self.current_board
        self._set_status("ejecutando A*...", C["accent3"])

        self.results = [
            evaluate(board, size, h_misplaced, "Misplaced"),
            evaluate(board, size, h_manhattan, "Manhattan"),
            evaluate(board, size, h_custom,    "Custom"),
        ]

        
        for i in self.tab_table.get_children():
            self.tab_table.delete(i)

        
        self.tab_table.tag_configure("best",     background=C["best_row"], foreground=C["accent2"])
        self.tab_table.tag_configure("normal",   background=C["panel"])
        self.tab_table.tag_configure("mid",      background=C["panel"])

        best = min(self.results, key=lambda x: x["nodes"])

        for r in self.results:
            tag = "best" if r["name"] == best["name"] else "normal"
            label = f"{'★ ' if tag == 'best' else '  '}{r['name']}"
            self.tab_table.insert("", "end",
                values=(label, r["cost"], r["nodes"], r["time"], r["mem"]),
                tags=(tag,))

        
        best_t = min(self.results, key=lambda x: x["time"])
        lines = (
            f"  Mejor eficiencia    →  {best['name']}  ({best['nodes']} nodos explorados)\n"
            f"  Más rápido         →  {best_t['name']}  ({best_t['time']} s)\n"
            f"  Movimientos óptimos →  {best['cost']} pasos\n\n"
            f"  ℹ  Un menor número de nodos explorados indica mayor eficiencia de la heurística.\n"
            f"     Manhattan domina en grids porque estima mejor el coste real restante."
        )
        self.explain_box.config(state="normal")
        self.explain_box.delete("1.0", tk.END)
        self.explain_box.insert(tk.END, lines)
        self.explain_box.config(state="disabled")

        self._set_status("comparación completa", C["accent2"])
        self.animate(best["path"], size)

    
    def _apply_dark_style(self, fig):
        fig.patch.set_facecolor(C["bg"])
        for ax in fig.axes:
            ax.set_facecolor(C["panel"])
            ax.tick_params(colors=C["muted"])
            ax.xaxis.label.set_color(C["muted"])
            ax.yaxis.label.set_color(C["muted"])
            ax.title.set_color(C["text"])
            for spine in ax.spines.values():
                spine.set_edgecolor(C["border"])

    def show_graph(self):
        if not self.results: return
        G = nx.DiGraph()
        for e in self.results[1]["edges"][:80]:
            G.add_edge(str(e[0])[:12], str(e[1])[:12])

        fig, ax = plt.subplots(figsize=(10, 7))
        self._apply_dark_style(fig)

        pos = nx.spring_layout(G, seed=42, k=0.6)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=60,
                               node_color=C["accent"], alpha=0.85)
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color=C["border"],
                               arrows=True, arrowsize=8, width=0.8)
        ax.set_title("Árbol de búsqueda — Manhattan (primeros 80 nodos)",
                     fontsize=11, pad=14)
        ax.axis("off")
        plt.tight_layout()
        plt.show()

    def show_plot(self):
        if not self.results: return
        names  = [r["name"]  for r in self.results]
        times  = [r["time"]  for r in self.results]
        nodes  = [r["nodes"] for r in self.results]
        colors = [C["accent3"], C["accent"], C["accent2"]]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
        self._apply_dark_style(fig)

        
        bars1 = ax1.bar(names, times, color=colors, edgecolor=C["border"], width=0.5)
        ax1.set_title("Tiempo de ejecución (s)")
        ax1.set_ylabel("segundos")
        for bar, val in zip(bars1, times):
            ax1.text(bar.get_x() + bar.get_width() / 2,
                     bar.get_height() + max(times) * 0.02,
                     f"{val:.4f}", ha="center", va="bottom",
                     color=C["text"], fontsize=9, fontfamily="Consolas")

        
        bars2 = ax2.bar(names, nodes, color=colors, edgecolor=C["border"], width=0.5)
        ax2.set_title("Nodos explorados")
        ax2.set_ylabel("nodos")
        for bar, val in zip(bars2, nodes):
            ax2.text(bar.get_x() + bar.get_width() / 2,
                     bar.get_height() + max(nodes) * 0.02,
                     str(val), ha="center", va="bottom",
                     color=C["text"], fontsize=9, fontfamily="Consolas")

        fig.suptitle("Comparación de Heurísticas A*",
                     fontsize=13, color=C["text"], fontfamily="Consolas")
        plt.tight_layout()
        plt.show()



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("980x720")
    root.minsize(820, 600)
    App(root)
    root.mainloop()
