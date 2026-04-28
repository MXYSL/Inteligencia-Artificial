```import tkinter as tk
from tkinter import font as tkfont
import math
import copy

SIZE = 4
EMPTY = "."
PLAYER_HUMAN = "O"
PLAYER_AI = "X"
MAX_DEPTH = 3
nodes_count = 0

# ─────────────────────────────────────────────
# PALETA DE COLORES
# ─────────────────────────────────────────────
C_FONDO      = "#dee6e0" # Fondo
G_FONDO       = "#ffffff" # Panel derecho (árbol)
DETT  = "#867EBE" # Líneas, botones, bordes
IA  = "#1721DD" # Texto IA
HUMAN  = "#ff2d6c" # Texto humano
TEXT   = "#000000" # Texto general

# ─────────────────────────────────────────────
# LÓGICA DEL TABLERO
# ─────────────────────────────────────────────
def create_board(): # tablero vacío
    return [[EMPTY]*SIZE for _ in range(SIZE)] 

def get_moves(board): # lista de movimientos posibles
    return [(i, j) for i in range(SIZE) for j in range(SIZE) if board[i][j] == EMPTY]

def check_winner(board): # devuelve el ganador ("X" o "O") o None si no hay ganador
    lines = []
    for i in range(SIZE): # filas y columnas
        lines.append(board[i]) 
        lines.append([board[j][i] for j in range(SIZE)]) 
    lines.append([board[i][i] for i in range(SIZE)]) 
    lines.append([board[i][SIZE-i-1] for i in range(SIZE)]) 
    for line in lines: # revisar si todos los elementos son iguales y no están vacíos
        if line.count(line[0]) == SIZE and line[0] != EMPTY:
            return line[0]
    return None

def is_terminal(board): # el juego terminó (ganador o empate)
    return check_winner(board) is not None or len(get_moves(board)) == 0

# ─────────────────────────────────────────────
# HEURÍSTICA
# ─────────────────────────────────────────────
def evaluate(board): # puntuación heurística del tablero para el jugador IA (positivo es bueno para IA, negativo para humano)
    score = 0
    lines = []
    for i in range(SIZE): # filas y columnas
        lines.append(board[i])
        lines.append([board[j][i] for j in range(SIZE)])
    lines.append([board[i][i] for i in range(SIZE)])
    lines.append([board[i][SIZE-i-1] for i in range(SIZE)])

    for line in lines:  # contar cuántas X y O hay en la línea
        x = line.count(PLAYER_AI)
        o = line.count(PLAYER_HUMAN)
        if o == 0: # solo X, mejor para IA
            score += 10**x # más X's en la línea, mejor para IA
        if x == 0: # solo O, mejor para humano
            score -= 10**o # más O's en la línea, peor para IA
        if o == 3 and x == 1: # línea casi ganadora para humano, pero IA tiene una ficha ahí, es muy bueno para IA
            score += 50 # mucho mejor que 3 O's sin interrupción
        if x == 3 and o == 1: # línea casi ganadora para IA, pero humano tiene una ficha ahí, es muy malo para IA
            score -= 50 # mucho peor que 3 X's sin interrupción

    centers = [(1,1),(1,2),(2,1),(2,2)]
    for i, j in centers:
        if board[i][j] == PLAYER_AI:
            score += 5
        elif board[i][j] == PLAYER_HUMAN:
            score -= 5
    return score

# ─────────────────────────────────────────────
# MINIMAX (con árbol)
# ─────────────────────────────────────────────
def minimax(board, depth, maximizing, tree, parent_id):
    global nodes_count
    nodes_count += 1

    node_id = len(tree)
    val_now = evaluate(board)
    tree.append({"parent": parent_id, "value": val_now, "pruned": False,
                 "is_max": maximizing, "depth": MAX_DEPTH - depth})

    winner = check_winner(board)
    if winner == PLAYER_AI:
        tree[node_id]["value"] = 10000 
        return 10000 
    if winner == PLAYER_HUMAN:
        tree[node_id]["value"] = -10000
        return -10000 
    if depth == 0 or is_terminal(board):
        return val_now

    if maximizing:
        value = -math.inf
        for move in get_moves(board):
            new_board = copy.deepcopy(board)
            new_board[move[0]][move[1]] = PLAYER_AI
            value = max(value, minimax(new_board, depth-1, False, tree, node_id))
        tree[node_id]["value"] = value
        return value
    else:
        value = math.inf
        for move in get_moves(board):
            new_board = copy.deepcopy(board)
            new_board[move[0]][move[1]] = PLAYER_HUMAN
            value = min(value, minimax(new_board, depth-1, True, tree, node_id))
        tree[node_id]["value"] = value
        return value

# ─────────────────────────────────────────────
# ALPHA-BETA (con árbol)
# ─────────────────────────────────────────────
def alphabeta(board, depth, alpha, beta, maximizing, tree, parent_id):
    global nodes_count
    nodes_count += 1

    node_id = len(tree)
    val_now = evaluate(board)
    tree.append({"parent": parent_id, "value": val_now, "pruned": False,
                 "is_max": maximizing, "depth": MAX_DEPTH - depth})

    winner = check_winner(board)
    if winner == PLAYER_AI:
        tree[node_id]["value"] = 10000
        return 10000
    if winner == PLAYER_HUMAN:
        tree[node_id]["value"] = -10000
        return -10000
    if depth == 0 or is_terminal(board):
        return val_now

    if maximizing:
        value = -math.inf
        for move in get_moves(board):
            new_board = copy.deepcopy(board)
            new_board[move[0]][move[1]] = PLAYER_AI
            value = max(value, alphabeta(new_board, depth-1, alpha, beta, False, tree, node_id))
            alpha = max(alpha, value)
            if beta <= alpha:
                # marcar nodos podados
                tree.append({"parent": node_id, "value": "✂", "pruned": True,
                             "is_max": False, "depth": MAX_DEPTH - depth + 1})
                break
        tree[node_id]["value"] = value
        return value
    else:
        value = math.inf
        for move in get_moves(board):
            new_board = copy.deepcopy(board)
            new_board[move[0]][move[1]] = PLAYER_HUMAN
            value = min(value, alphabeta(new_board, depth-1, alpha, beta, True, tree, node_id))
            beta = min(beta, value)
            if beta <= alpha:
                tree.append({"parent": node_id, "value": "✂", "pruned": True,
                             "is_max": True, "depth": MAX_DEPTH - depth + 1})
                break
        tree[node_id]["value"] = value
        return value

# ─────────────────────────────────────────────
# INTERFAZ PRINCIPAL
# ─────────────────────────────────────────────
class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego del Gato ")
        self.root.configure(bg=C_FONDO)
        self.root.resizable(True, True)

        self.board = create_board()
        self.algorithm = "alphabeta"
        self.game_over = False

        # Fuentes
        self.font_title  = tkfont.Font(family="Courier New", size=15, weight="bold")
        self.font_cell   = tkfont.Font(family="Courier New", size=22, weight="bold")
        self.font_label  = tkfont.Font(family="Courier New", size=9)
        self.font_btn    = tkfont.Font(family="Courier New", size=9, weight="bold")
        self.font_status = tkfont.Font(family="Courier New", size=10, weight="bold")

        self._build_ui()

    # ── construcción de la UI ──────────────────
    def _build_ui(self):
        # Título
        title_bar = tk.Frame(self.root, bg=C_FONDO)
        title_bar.pack(fill="x", padx=20, pady=(14, 4))
        tk.Label(title_bar, text="Juego del Gato", bg=C_FONDO,
                 fg=TEXT, font=self.font_title).pack(side="left")

        sep = tk.Frame(self.root, bg=DETT, height=1)
        sep.pack(fill="x", padx=20, pady=(0, 10))

        # Contenedor principal
        main = tk.Frame(self.root, bg=C_FONDO)
        main.pack(fill="both", expand=True, padx=20, pady=0)

        # ── Panel izquierdo ──
        left = tk.Frame(main, bg=C_FONDO)
        left.pack(side="left", fill="y", padx=(0, 20))

        # Etiqueta de turno / estado
        self.status_label = tk.Label(left, text="TU TURNO  [ O ]",
                                     bg=C_FONDO, fg=TEXT,
                                     font=self.font_status)
        self.status_label.pack(pady=(0, 10))

        # Tablero
        board_outer = tk.Frame(left, bg=TEXT, bd=0)
        board_outer.pack()
        board_inner = tk.Frame(board_outer, bg=TEXT)
        board_inner.pack(padx=2, pady=2)

        self.buttons = [[None]*SIZE for _ in range(SIZE)]
        for i in range(SIZE):
            for j in range(SIZE):
                cell = tk.Frame(board_inner, bg=TEXT, bd=1, relief="flat")
                cell.grid(row=i, column=j, padx=1, pady=1)
                btn = tk.Button(cell, text=" ", width=4, height=2,
                                bg=C_FONDO, fg=TEXT,
                                activebackground=DETT,
                                activeforeground=IA,
                                relief="flat", bd=0,
                                font=self.font_cell,
                                cursor="hand2",
                                command=lambda r=i, c=j: self.play(r, c))
                btn.pack()
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=DETT) if b["text"]==" " else None)
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=C_FONDO) if b["text"]==" " else None)
                self.buttons[i][j] = btn

        # Selector de algoritmo
        algo_frame = tk.Frame(left, bg=C_FONDO)
        algo_frame.pack(pady=(14, 4))
        tk.Label(algo_frame, text="ALGORITMO:", bg=C_FONDO,
                 fg=TEXT, font=self.font_label).pack(side="left", padx=(0,8))

        self.algo_var = tk.StringVar(value="alphabeta")
        for val, txt in [("minimax","Minimax"), ("alphabeta","Alpha-Beta")]:
            rb = tk.Radiobutton(algo_frame, text=txt, variable=self.algo_var,
                                value=val, bg=C_FONDO, fg=TEXT,
                                selectcolor=DETT,
                                activebackground=C_FONDO,
                                activeforeground=DETT,
                                font=self.font_btn,
                                command=self._algo_changed)
            rb.pack(side="left", padx=6)

        # Botón reiniciar
        reset_btn = tk.Button(left, text="⟳  REINICIAR", bg=DETT,
                              fg=TEXT, activebackground=DETT,
                              activeforeground=C_FONDO, relief="flat",
                              font=self.font_btn, cursor="hand2",
                              command=self.reset_game, width=20)
        reset_btn.pack(pady=(6, 0))

        # Contador de nodos
        self.nodes_label = tk.Label(left, text="Nodos explorados: —",
                                    bg=C_FONDO, fg=TEXT, font=self.font_label)
        self.nodes_label.pack(pady=(8, 0))

        # Leyenda
        legend = tk.Frame(left, bg=C_FONDO)
        legend.pack(pady=(10, 0))
        for color, label in [(IA,"MAX (IA)"), (HUMAN,"MIN (humano)"),
                             ("#ff8c00","Podado  ✂")]:
            row = tk.Frame(legend, bg=C_FONDO)
            row.pack(anchor="w")
            tk.Canvas(row, width=12, height=12, bg=C_FONDO,
                      highlightthickness=0).pack(side="left")
            dot = tk.Canvas(row, width=14, height=14, bg=C_FONDO,
                            highlightthickness=0)
            dot.pack(side="left")
            dot.create_oval(2, 2, 12, 12, fill=color, outline="")
            tk.Label(row, text=label, bg=C_FONDO, fg=TEXT,
                     font=self.font_label).pack(side="left")

        # ── Panel derecho: árbol ──
        right = tk.Frame(main, bg=G_FONDO, relief="flat", bd=0)
        right.pack(side="right", fill="both", expand=True)

        tree_header = tk.Frame(right, bg=G_FONDO)
        tree_header.pack(fill="x", padx=10, pady=(8,2))
        tk.Label(tree_header, text="ÁRBOL DE DECISIÓN",
                 bg=G_FONDO, fg=TEXT, font=self.font_label).pack(side="left")

        # Canvas con scrollbars
        canvas_frame = tk.Frame(right, bg=G_FONDO)
        canvas_frame.pack(fill="both", expand=True, padx=6, pady=6)

        self.canvas = tk.Canvas(canvas_frame, bg=G_FONDO, highlightthickness=0,
                                width=480, height=500)
        vbar = tk.Scrollbar(canvas_frame, orient="vertical",
                            command=self.canvas.yview)
        hbar = tk.Scrollbar(canvas_frame, orient="horizontal",
                            command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)

        hbar.pack(side="bottom", fill="x")
        vbar.pack(side="right",  fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.bind("<MouseWheel>",
                         lambda e: self.canvas.yview_scroll(-1*(e.delta//120), "units"))

        # Placeholder inicial
        self.canvas.create_text(240, 240, text="Juega para ver el árbol",
                                fill=TEXT, font=self.font_label)

    # ── helpers ──────────────────────────────
    def _algo_changed(self):
        self.algorithm = self.algo_var.get()

    def _set_status(self, text, color=IA):
        self.status_label.config(text=text, fg=color)

    # ── fin de juego ─────────────────────────
    def _end_game(self, winner):
        self.game_over = True
        # Deshabilitar todos los botones
        for i in range(SIZE):
            for j in range(SIZE):
                self.buttons[i][j].config(state="disabled", cursor="arrow")

        if winner == PLAYER_HUMAN:
            self._set_status("¡GANASTE!", TEXT)
            self._flash_board(HUMAN)
        elif winner == PLAYER_AI:
            self._set_status("GANA LA IA", TEXT)
            self._flash_board(IA)
        else:
            self._set_status("EMPATE  —  🤝", TEXT)

        # Popup de fin de juego
        self._show_result_popup(winner)

    def _flash_board(self, color, times=6):
        """Parpadeo de color en las celdas llenas al terminar."""
        filled = [(i,j) for i in range(SIZE) for j in range(SIZE)
                  if self.board[i][j] != EMPTY]
        def toggle(n):
            if n <= 0:
                return
            bg = color if n % 2 == 0 else C_FONDO
            for i,j in filled:
                self.buttons[i][j].config(bg=bg)
            self.root.after(220, lambda: toggle(n-1))
        toggle(times)

    def _show_result_popup(self, winner):
        popup = tk.Toplevel(self.root)
        popup.configure(bg=G_FONDO)
        popup.resizable(False, False)
        popup.title("")
        popup.grab_set()

        # Centra el popup
        self.root.update_idletasks()
        rx = self.root.winfo_rootx() + self.root.winfo_width()  // 2
        ry = self.root.winfo_rooty() + self.root.winfo_height() // 2
        popup.geometry(f"320x180+{rx-160}+{ry-90}")

        if winner == PLAYER_HUMAN:
            icon, msg, color = "🏆", "¡GANASTE!", TEXT
        elif winner == PLAYER_AI:
            icon, msg, color = "🤖", "IA GANA", TEXT
        else:
            icon, msg, color = "🤝", "EMPATE", TEXT

        tk.Label(popup, text=icon, bg=G_FONDO, font=("Courier New", 36)).pack(pady=(20,4))
        tk.Label(popup, text=msg, bg=G_FONDO, fg=color,
                 font=tkfont.Font(family="Courier New", size=18, weight="bold")).pack()

        tk.Button(popup, text="JUGAR DE NUEVO", bg=DETT, fg=TEXT,
                  activebackground=DETT, activeforeground=C_FONDO,
                  relief="flat", cursor="hand2",
                  font=tkfont.Font(family="Courier New", size=10, weight="bold"),
                  command=lambda: [popup.destroy(), self.reset_game()],
                  width=18).pack(pady=16)

    # ── jugar ─────────────────────────────────
    def play(self, i, j):
        global nodes_count
        if self.game_over or self.board[i][j] != EMPTY:
            return

        # Movimiento humano
        self.board[i][j] = PLAYER_HUMAN
        self.buttons[i][j].config(text="O", fg=HUMAN,
                                  bg=C_FONDO, disabledforeground=HUMAN)

        winner = check_winner(self.board)
        if winner or not get_moves(self.board):
            self._end_game(winner)
            return

        self._set_status("Turno de la IA", TEXT)
        self.root.update()

        # Movimiento IA
        nodes_count = 0
        tree = []
        best, best_val = None, -math.inf

        for move in get_moves(self.board):
            new_board = copy.deepcopy(self.board)
            new_board[move[0]][move[1]] = PLAYER_AI

            if self.algorithm == "alphabeta":
                val = alphabeta(new_board, MAX_DEPTH, -math.inf, math.inf,
                                False, tree, -1)
            else:
                val = minimax(new_board, MAX_DEPTH, False, tree, -1)

            if val > best_val:
                best_val, best = val, move

        if best:
            self.board[best[0]][best[1]] = PLAYER_AI
            self.buttons[best[0]][best[1]].config(text="X", fg=IA,
                                                   bg=C_FONDO,
                                                   disabledforeground=IA)

        algo_name = "Alpha-Beta" if self.algorithm == "alphabeta" else "Minimax"
        self.nodes_label.config(
            text=f"Nodos explorados: {nodes_count}  ({algo_name})")

        winner = check_winner(self.board)
        if winner or not get_moves(self.board):
            self._end_game(winner)
        else:
            self._set_status("TU TURNO", TEXT)

        self.draw_tree(tree)

    # ── árbol ─────────────────────────────────
    def draw_tree(self, tree):
        self.canvas.delete("all")
        if not tree:
            return

        # Límite de nodos a mostrar para no colapsar la UI
        MAX_NODES = 300
        visible = tree[:MAX_NODES]

        # Calcular posiciones por nivel con BFS
        from collections import defaultdict
        levels = defaultdict(list)
        for idx, node in enumerate(visible):
            d = node["depth"]
            levels[d].append(idx)

        max_depth = max(levels.keys()) if levels else 0
        NODE_R = 14
        LEVEL_H = 60
        MIN_COL_W = 34

        # Ancho del nivel más poblado
        max_count = max(len(v) for v in levels.values())
        canvas_w = max(480, max_count * MIN_COL_W + 40)
        canvas_h = (max_depth + 1) * LEVEL_H + 60

        self.canvas.config(scrollregion=(0, 0, canvas_w, canvas_h))

        pos = {}
        for depth, indices in levels.items():
            n = len(indices)
            for k, idx in enumerate(indices):
                x = (k + 1) * canvas_w / (n + 1)
                y = depth * LEVEL_H + 30
                pos[idx] = (x, y)

        # Aristas
        for idx, node in enumerate(visible):
            if node["parent"] >= 0 and node["parent"] < len(visible):
                if idx in pos and node["parent"] in pos:
                    px, py = pos[node["parent"]]
                    cx, cy = pos[idx]
                    self.canvas.create_line(px, py + NODE_R, cx, cy - NODE_R,
                                            fill=TEXT, width=1)

        # Nodos
        for idx, node in enumerate(visible):
            if idx not in pos:
                continue
            x, y = pos[idx]

            if node["pruned"]:
                fill = "#ff8c00"
                txt_color = TEXT
                label = "✂"
            elif node["is_max"]:
                fill = IA
                txt_color = C_FONDO
                label = str(node["value"]) if isinstance(node["value"], int) else "?"
            else:
                fill = HUMAN
                txt_color = TEXT
                label = str(node["value"]) if isinstance(node["value"], int) else "?"

            self.canvas.create_oval(x-NODE_R, y-NODE_R, x+NODE_R, y+NODE_R,
                                    fill=fill, outline="", tags="node")
            # Texto condensado
            short = label[:4] if len(str(label)) > 4 else str(label)
            self.canvas.create_text(x, y, text=short, fill=txt_color,
                 
