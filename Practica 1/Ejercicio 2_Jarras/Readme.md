# Problema de las Jarras – Comparación BFS vs DFS

## Descripción

Este proyecto implementa una solución al **Problema de las Jarras de Agua** utilizando dos algoritmos de búsqueda clásicos en Inteligencia Artificial:

* **Breadth-First Search (BFS)** – Búsqueda en Anchura
* **Depth-First Search (DFS)** – Búsqueda en Profundidad

El programa permite comparar ambos algoritmos en términos de:

* **Tiempo de ejecución**
* **Memoria utilizada**
* **Número de estados explorados**

Además, cuenta con una **interfaz gráfica desarrollada en Python utilizando Tkinter**, lo que permite al usuario ingresar las capacidades de las jarras y el objetivo de manera interactiva.

---

## Funcionamiento del Problema

El problema consiste en dos jarras con capacidades diferentes y sin marcas de medición. A partir de estas jarras se deben realizar operaciones para obtener una cantidad específica de agua.

Las operaciones permitidas son:

* Llenar una jarra completamente
* Vaciar una jarra
* Transferir agua de una jarra a otra hasta llenar o vaciar alguna

El objetivo es encontrar una secuencia de pasos que permita obtener la cantidad de agua deseada en alguna de las jarras.

---

## Algoritmos Implementados

### Breadth-First Search (BFS)

BFS explora el espacio de estados **nivel por nivel**, utilizando una **cola (queue)** para almacenar los estados pendientes de explorar.

Características:

* Garantiza encontrar la **solución más corta**
* Explora más nodos en muchos casos
* Puede consumir **más memoria**

---

### Depth-First Search (DFS)

DFS explora el espacio de estados **profundizando lo más posible en cada rama** antes de retroceder, utilizando una **pila (stack)**.

Características:

* Puede encontrar soluciones más rápido en algunos casos
* Utiliza menos memoria que BFS en ciertos escenarios
* No siempre encuentra la solución más corta

---

## Métricas Analizadas

El programa mide tres métricas importantes para cada algoritmo:

### 1. Tiempo de Ejecución

Se mide utilizando el módulo:

```
time
```

Esto permite calcular cuánto tiempo tarda cada algoritmo en encontrar la solución.

---

### 2. Memoria Utilizada

Se utiliza el módulo:

```
tracemalloc
```

para medir la memoria máxima utilizada durante la ejecución del algoritmo.

La memoria se muestra en **megabytes (MB)**.

---

### 3. Estados Explorados

Se contabiliza el número de estados visitados durante la búsqueda, lo cual permite analizar la eficiencia de cada algoritmo.

---

## Interfaz Gráfica

La interfaz está construida con **Tkinter** y permite:

* Ingresar la capacidad de la **Jarra A**
* Ingresar la capacidad de la **Jarra B**
* Ingresar el **objetivo**

Además, se incluyen botones para ejecutar:

* **BFS**
* **DFS**

Los resultados se muestran en el panel derecho con:

* Algoritmo utilizado
* Tiempo de ejecución
* Memoria utilizada
* Estados explorados
* Camino de solución

---

## Ejemplo de Salida

```
Algoritmo: BFS
Tiempo: 0.000532 segundos
Memoria usada: 0.001842 MB
Estados explorados: 17

Camino:

(0,0)
(5,0)
(5,3)
(2,3)
(2,0)
(0,2)
(5,2)
(4,3)
```

---

## Requisitos

Para ejecutar el programa se requiere:

* Python 3.8 o superior

Librerías utilizadas:

```
tkinter
collections
time
tracemalloc
```

Todas forman parte de la **biblioteca estándar de Python**, por lo que no es necesario instalar dependencias adicionales.

---

## Ejecución

Para ejecutar el programa:

```
python jarras.py
```

Se abrirá la interfaz gráfica donde se podrán ingresar los valores y ejecutar los algoritmos.


Autor: De la Cruz Velázquez Marco Uriel
Institución: Escuela Superior de Cómputo (ESCOM) - Ingeniería en Sistemas Computacionales
