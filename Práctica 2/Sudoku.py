import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import copy
import tracemalloc

SIZE = 9
SUBGRID = 3

# ---------------- UTILIDADES ----------------
def find_empty(board):
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == 0:
                return i, j
    return None


def is_valid(board, row, col, num):
    for i in range(SIZE):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = row - row % 3, col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def count_conflicts(board):
    conflicts = 0
    for i in range(SIZE):
        row = [x for x in board[i] if x != 0]
        conflicts += len(row) - len(set(row))

        col = [board[x][i] for x in range(SIZE) if board[x][i] != 0]
        conflicts += len(col) - len(set(col))
    return conflicts


# ---------------- A* (Backtracking guiado) ----------------
# ---------------- A* PURO ----------------
import heapq

class Node:
    def __init__(self, board, g, h):
        self.board = board
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f


def heuristic(board):
    return sum(row.count(0) for row in board)


def get_successors(board):
    successors = []
    empty = find_empty(board)

    if not empty:
        return successors

    row, col = empty

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            new_board = copy.deepcopy(board)
            new_board[row][col] = num
            successors.append(new_board)

    return successors


def solve_astar(board):
    tracemalloc.start()
    start = time.time()

    open_list = []
    visited = set()

    start_node = Node(copy.deepcopy(board), 0, heuristic(board))
    heapq.heappush(open_list, start_node)

    nodes = 0

    while open_list:
        current = heapq.heappop(open_list)
        nodes += 1

        board_tuple = tuple(tuple(row) for row in current.board)
        if board_tuple in visited:
            continue

        visited.add(board_tuple)

        if find_empty(current.board) is None:
            end = time.time()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            return True, end - start, nodes, peak / (1024 * 1024), current.board

        for successor in get_successors(current.board):
            h = heuristic(successor)
            g = current.g + 1
            heapq.heappush(open_list, Node(successor, g, h))

    end = time.time()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return False, end - start, nodes, peak / (1024 * 1024), board  # MB


# ---------------- RECOCIDO SIMULADO ----------------
def simulated_annealing(board):
    tracemalloc.start()
    start = time.time()

    def fill_board(b):
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                nums = list(range(1, 10))
                random.shuffle(nums)
                for i in range(3):
                    for j in range(3):
                        if b[box_row+i][box_col+j] == 0:
                            b[box_row+i][box_col+j] = nums.pop()
        return b

    def get_neighbors(b):
        new_b = copy.deepcopy(b)
        box = random.randint(0, 8)
        r = (box // 3) * 3
        c = (box % 3) * 3

        cells = [(i, j) for i in range(r, r+3) for j in range(c, c+3)]
        a, b2 = random.sample(cells, 2)
        new_b[a[0]][a[1]], new_b[b2[0]][b2[1]] = new_b[b2[0]][b2[1]], new_b[a[0]][a[1]]
        return new_b

    current = fill_board(copy.deepcopy(board))
    current_cost = count_conflicts(current)

    T = 1.0
    cooling = 0.999

    for _ in range(10000):
        if current_cost == 0:
            break
        neighbor = get_neighbors(current)
        neighbor_cost = count_conflicts(neighbor)

        delta = neighbor_cost - current_cost

        if delta < 0 or random.random() < pow(2.71828, -delta / T):
            current = neighbor
            current_cost = neighbor_cost

        T *= cooling

    end = time.time()

    current_mem, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return current_cost == 0, current, end - start, peak / (1024 * 1024)  # MB


# ---------------- GENERADOR ----------------
def solve_fast(board):
    empty = find_empty(board)
    if not empty:
        return True

    row, col = empty

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_fast(board):
                return True
            board[row][col] = 0

    return False


def generate_board(empty_cells):
    base = [[0]*9 for _ in range(9)]
    solve_fast(base)  # 👈 IMPORTANTE

    cells = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(cells)

    for i in range(empty_cells):
        r, c = cells[i]
        base[r][c] = 0

    return base


# ---------------- GUI ----------------
class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku IA")

        self.board = None

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.entries = [[None for _ in range(9)] for _ in range(9)]

        for i in range(9):
            for j in range(9):
                e = tk.Entry(self.frame, width=2, font=('Arial', 18), justify='center')
                e.grid(row=i, column=j)
                self.entries[i][j] = e

        controls = tk.Frame(root)
        controls.pack(pady=10)

        self.alg = ttk.Combobox(controls, values=["A*", "Recocido"])
        self.alg.set("A*")
        self.alg.grid(row=0, column=0)

        self.diff = ttk.Combobox(controls, values=["Fácil", "Intermedio", "Difícil"])
        self.diff.set("Fácil")
        self.diff.grid(row=0, column=1)

        tk.Button(controls, text="Generar", command=self.generate).grid(row=0, column=2)
        tk.Button(controls, text="Resolver", command=self.solve).grid(row=0, column=3)

        self.result = tk.Label(root, text="")
        self.result.pack()

    def generate(self):
        levels = {"Fácil":20, "Intermedio":35, "Difícil":45}
        self.board = generate_board(levels[self.diff.get()])
        self.update_ui()

    def update_ui(self):
        for i in range(9):
            for j in range(9):
                val = self.board[i][j]
                self.entries[i][j].delete(0, tk.END)
                if val != 0:
                    self.entries[i][j].insert(0, str(val))

    def solve(self):
        board_copy = copy.deepcopy(self.board)
        alg = self.alg.get()

        if alg == "A*":
            solved, t, nodes, mem, solution = solve_astar(board_copy)
            if solved:
                self.board = solution
                self.update_ui()
            msg = f"A* -> Tiempo: {t:.3f}s | Nodos: {nodes} | Memoria: {mem:.2f} MB | Resuelto: {solved}"
        else:
            solved, result_board, t, mem = simulated_annealing(board_copy)
            self.board = result_board
            self.update_ui()
            msg = f"Recocido -> Tiempo: {t:.3f}s | Memoria: {mem:.2f} MB | Resuelto: {solved}"

        self.result.config(text=msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
