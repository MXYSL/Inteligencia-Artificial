<div align="center">

# 🧪 Problema de las Jarras

Aplicación desarrollada en **Python** con interfaz gráfica utilizando **Tkinter** para analizar el comportamiento de algoritmos de búsqueda en el espacio de estados.

</div>

---

## 📌 Descripción del Proyecto

Este proyecto implementa una solución al **Problema de las Jarras de Agua**, un problema clásico de búsqueda utilizado en Inteligencia Artificial para estudiar estrategias de exploración del espacio de estados.

El programa permite comparar dos algoritmos fundamentales:

🔹 **Breadth-First Search (BFS)** – Búsqueda en Anchura
🔹 **Depth-First Search (DFS)** – Búsqueda en Profundidad

La aplicación incluye una **interfaz gráfica interactiva** que permite introducir los valores de las jarras y observar los resultados generados por cada algoritmo.

---

## 🧠 El Problema de las Jarras

Se tienen **dos jarras con capacidades distintas** y el objetivo es medir una cantidad específica de agua utilizando únicamente las siguientes operaciones:

| Operación    | Descripción                    |
| ------------ | ------------------------------ |
| Llenar jarra | Llenar completamente una jarra |
| Vaciar jarra | Vaciar completamente una jarra |
| Transferir   | Pasar agua de una jarra a otra |

El objetivo es encontrar una **secuencia de pasos** que permita obtener una cantidad específica de agua en alguna de las jarras.

---

## ⚙️ Algoritmos Implementados

### 🔵 Breadth-First Search (BFS)

La **búsqueda en anchura** explora el espacio de estados **nivel por nivel**, utilizando una **estructura de datos tipo cola (queue)**.

**Características:**

✔ Encuentra la **solución más corta**
✔ Explora los estados por niveles
✔ Puede consumir **más memoria**

---

### 🟣 Depth-First Search (DFS)

La **búsqueda en profundidad** explora primero los estados **más profundos del árbol**, utilizando una **estructura tipo pila (stack)**.

**Características:**

✔ Puede encontrar soluciones rápidamente
✔ Generalmente usa **menos memoria**
✔ No siempre encuentra la solución óptima

---

## 📊 Métricas Analizadas

El programa permite comparar el comportamiento de los algoritmos utilizando las siguientes métricas:

### ⏱ Tiempo de Ejecución

Se mide el tiempo que tarda cada algoritmo en encontrar una solución.

### 🧠 Memoria Utilizada

Se calcula la memoria máxima utilizada durante la ejecución del algoritmo.

### 🔎 Estados Explorados

Cantidad de estados visitados durante la búsqueda.

Estas métricas permiten analizar **la eficiencia y el comportamiento de cada algoritmo**.

---

## 🖥 Interfaz Gráfica

La interfaz fue desarrollada utilizando **Tkinter**, permitiendo una interacción sencilla con el usuario.

### Funcionalidades de la interfaz:

* Ingreso de **capacidad de la Jarra A**
* Ingreso de **capacidad de la Jarra B**
* Definición del **objetivo**
* Ejecución de **BFS**
* Ejecución de **DFS**
* Visualización del **camino solución**

---

## 📷 Ejemplo de Resultados

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

## 📁 Estructura del Proyecto

```
Proyecto-Jarras/
│
├── jarras.py
└── README.md
```

---

## 🧰 Tecnologías Utilizadas

| Tecnología        | Uso                   |
| ----------------- | --------------------- |
| Python            | Lenguaje principal    |
| Tkinter           | Interfaz gráfica      |
| tracemalloc       | Medición de memoria   |
| time              | Medición de tiempo    |
| collections.deque | Implementación de BFS |

---

## ▶️ Ejecución del Programa

1. Clonar el repositorio o descargar el proyecto.
2. Ejecutar el archivo principal:

```
python jarras.py
```

3. Ingresar los valores de las jarras y el objetivo.
4. Ejecutar BFS o DFS para observar los resultados.

---



## 🧑‍💼 Autor

**De la Cruz Velázquez Marco Uriel**

## 🏢 Institución

**Escuela Superior de Cómputo (ESCOM)**
**Ingeniería en Sistemas Computacionales**

