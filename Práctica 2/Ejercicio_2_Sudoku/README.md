# 🧩 Sudoku Solver con A* y Recocido Simulado

## 📌 Descripción del proyecto

Este proyecto consiste en el desarrollo de una aplicación en Python con interfaz gráfica que permite resolver tableros de Sudoku utilizando dos algoritmos de inteligencia artificial:

* 🔍 **A*** (búsqueda informada)
* 🔥 **Recocido Simulado** (Simulated Annealing)

El sistema permite generar tableros de diferentes niveles de dificultad, resolverlos mediante el algoritmo seleccionado y analizar su rendimiento en términos de tiempo, memoria y efectividad.

---

## 🎯 Objetivo

Comparar el desempeño de dos enfoques de resolución de problemas:

* Un algoritmo determinista (A*)
* Un algoritmo probabilístico (Recocido Simulado)

Evaluando:

* ⏱️ Tiempo de ejecución
* 🧠 Consumo de memoria
* ✅ Capacidad para encontrar solución

---

## 🖥️ Características principales

* Generación automática de tableros de Sudoku
* Interfaz gráfica interactiva con Tkinter
* Selección de algoritmo de resolución
* Selección de nivel de dificultad
* Visualización del Sudoku antes y después de resolver
* Medición de rendimiento (tiempo y memoria)

---

## 🧠 Algoritmos implementados

### 🔍 A* (A estrella)

Algoritmo de búsqueda informada que utiliza la función:

f(n) = g(n) + h(n)

Donde:

* g(n): costo acumulado
* h(n): heurística (número de celdas vacías)

Características:

* ✔ Garantiza solución (si existe)
* ✔ Encuentra solución óptima
* ❌ Alto costo computacional
* ❌ Alto consumo de memoria en problemas grandes

---

### 🔥 Recocido Simulado

Algoritmo probabilístico inspirado en el enfriamiento de metales.

Características:

* ✔ Bajo consumo de memoria
* ✔ Rápido en comparación con A*
* ❌ No garantiza solución
* ❌ Puede quedarse en mínimos locales

---

## 🎚️ Niveles de dificultad

| Nivel      | Celdas vacías |
| ---------- | ------------- |
| Fácil      | 20            |
| Intermedio | 35            |
| Difícil    | 45            |

---

## ⚙️ Tecnologías utilizadas

* Python 3.x
* Tkinter (interfaz gráfica)
* tracemalloc (medición de memoria)
* heapq (cola de prioridad para A*)

---

## 🚀 Ejecución del programa

1. Asegúrate de tener Python instalado
2. Ejecuta el archivo:

```bash
python nombre_del_archivo.py
```

3. En la interfaz:

   * Selecciona el nivel de dificultad
   * Presiona **Generar**
   * Selecciona el algoritmo
   * Presiona **Resolver**

---

## 📊 Métricas evaluadas

El sistema mide automáticamente:

* ⏱️ Tiempo de ejecución
* 🧠 Memoria máxima utilizada (MB)
* 🔢 Número de nodos explorados (A*)
* ✅ Estado de resolución

---

## 📈 Resultados esperados

* A* es más preciso pero más costoso computacionalmente
* Recocido Simulado es más rápido pero menos confiable
* En niveles difíciles, A* puede volverse lento
* Recocido puede no encontrar solución óptima

---

## 🧠 Conclusiones

Este proyecto demuestra cómo diferentes enfoques de inteligencia artificial pueden aplicarse a un mismo problema, mostrando sus ventajas y limitaciones.

* A* es ideal cuando se requiere precisión
* Recocido Simulado es útil cuando se prioriza velocidad

---

## 📌 Autores

* **De la Cruz Velázquez Marco Uriel**

* **Sanchez Gomez Alan Ivan**

* **Solis Lugo Mayra**

**Escuela Superior de Cómputo (ESCOM)**

**Ingeniería en Sistemas Computacionales**

---

## 📎 Notas

* El generador de Sudoku utiliza backtracking para garantizar soluciones válidas
* El rendimiento puede variar dependiendo del hardware
* El recocido simulado puede producir soluciones no óptimas en algunos casos

---
