
# 8-Puzzle Solver


# Descripción del Proyecto

Este proyecto implementa un **solver visual del 8-Puzzle**, uno de los problemas clásicos utilizados en cursos de **Inteligencia Artificial y búsqueda en espacios de estados**.

El programa permite:

* Resolver automáticamente el puzzle
* Visualizar el proceso de solución
* Comparar distintos algoritmos de búsqueda
* Analizar métricas de rendimiento

La aplicación incluye una **interfaz gráfica interactiva** que permite generar estados aleatorios del puzzle y ejecutar diferentes algoritmos para encontrar la solución.

---

# El Problema del 8-Puzzle

El **8-Puzzle** consiste en un tablero de **3 × 3** que contiene:

* 8 fichas numeradas
* 1 espacio vacío

El objetivo es ordenar las fichas hasta llegar al estado final:

```text
1 2 3
4 5 6
7 8 _
```

donde el espacio vacío se representa con `0`.

---

## Movimientos permitidos

Las fichas pueden moverse intercambiándose con el espacio vacío:

| Movimiento | Descripción                    |
| ---------- | ------------------------------ |
| Arriba     | Mover ficha hacia arriba       |
| Abajo      | Mover ficha hacia abajo        |
| Izquierda  | Mover ficha hacia la izquierda |
| Derecha    | Mover ficha hacia la derecha   |

---

# Algoritmos Implementados

El programa permite comparar tres algoritmos de búsqueda.

---

## Breadth-First Search (BFS)

Explora el espacio de estados **nivel por nivel**, utilizando una **cola (queue)**.

**Ventajas**

* Garantiza encontrar la solución óptima
* Explora sistemáticamente el árbol

**Desventajas**

* Puede consumir una gran cantidad de memoria

---

## Depth-First Search (DFS)

Explora el árbol **profundizando en cada rama antes de retroceder**, utilizando una **pila (stack)**.

**Ventajas**

* Puede encontrar soluciones rápidamente
* Consume menos memoria en ciertos casos

**Desventajas**

* No garantiza encontrar la solución más corta

---

## A* (A Star)

Es un algoritmo de búsqueda informada que utiliza una función heurística para guiar la exploración.

Combina:

* costo acumulado del camino (g)
* estimación heurística del costo restante (h)

En este proyecto se utiliza la **distancia Manhattan** como función heurística.

### Heurística Manhattan

La distancia Manhattan calcula la suma de las distancias de cada ficha a su posición objetivo.

```text
|x1 - x2| + |y1 - y2|
```

Esto permite priorizar estados que se encuentran más cerca de la solución.

**Ventajas**

* Alta eficiencia en problemas de búsqueda
* Reduce el número de nodos explorados
* Garantiza encontrar la solución óptima cuando la heurística es admisible

---

# Métricas Analizadas

El sistema registra automáticamente varias métricas para comparar el comportamiento de los algoritmos.

---

## Tiempo de Ejecución

Se mide el tiempo total que tarda el algoritmo en encontrar la solución utilizando el módulo:

```text
time
```

---

## Memoria Utilizada

La memoria máxima utilizada durante la ejecución se calcula mediante el módulo:

```text
tracemalloc
```

La memoria se muestra en **kilobytes (KB)**.

---

## Nodos Explorados

Representa la cantidad de estados visitados durante la búsqueda.

Esta métrica permite analizar el tamaño del espacio de estados explorado por cada algoritmo.

---

## Profundidad

Indica el nivel del árbol de búsqueda en el que se encontró la solución.

---

# Interfaz Gráfica

La interfaz fue desarrollada utilizando **Tkinter** y está organizada en diferentes secciones.

---

## Tablero del Puzzle

Muestra visualmente el estado actual del puzzle y permite observar la animación de los movimientos durante la resolución.

---

## Panel de Algoritmos

Permite ejecutar los diferentes métodos de búsqueda:

* BFS
* DFS
* A*
* Random (generar estado inicial aleatorio)

---

## Panel de Métricas

Muestra información sobre:

* algoritmo utilizado
* número de pasos
* tiempo de ejecución
* memoria utilizada
* nodos explorados
* profundidad

---

## Árbol de Búsqueda

Incluye una representación visual simplificada del **árbol de búsqueda**, mostrando cómo se expande la exploración en función de la profundidad.

---

## Registro de Movimientos

Lista la secuencia de movimientos necesarios para llegar a la solución.

Ejemplo:

```text
Paso 0 — estado inicial
Paso 1 — derecha
Paso 2 — arriba
Paso 3 — izquierda
```

---

# Ejemplo de Resultados

```text
Algoritmo: A*
Pasos: 12
Tiempo: 0.0134 s
Memoria: 48.2 KB
Nodos explorados: 127
Profundidad: 12
```

---

# Estructura del Proyecto

```text
8-puzzle-solver/
│
├── puzzle.py
└── README.md
```

---

# Tecnologías Utilizadas

| Tecnología        | Uso                                         |
| ----------------- | ------------------------------------------- |
| Python            | Lenguaje principal                          |
| Tkinter           | Interfaz gráfica                            |
| heapq             | Implementación de cola de prioridad para A* |
| collections.deque | Implementación de BFS                       |
| tracemalloc       | Medición de memoria                         |
| threading         | Ejecución paralela del algoritmo            |

---

# Ejecución del Programa

1. Descargar o clonar el proyecto.
2. Ejecutar el archivo principal:

```text
python puzzle.py
```

3. Presionar el botón **Random** para generar un estado inicial.
4. Ejecutar alguno de los algoritmos para resolver el puzzle.

---

Autor: Solis Lugo Mayra

Institución: Escuela Superior de Cómputo (ESCOM) - Ingeniería en Sistemas Computacionales
