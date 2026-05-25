# Práctica 4 — Clasificación con Métricas de Distancia

## Introducción

La clasificación es una de las tareas fundamentales del aprendizaje automático supervisado. Su objetivo es aprender, a partir de un conjunto de ejemplos etiquetados, una función capaz de asignar una clase a nuevas instancias no vistas. Entre los enfoques más intuitivos y bien estudiados se encuentran los clasificadores basados en métricas de distancia, cuya premisa central es que instancias similares en el espacio de características pertenecen a la misma clase.

Esta práctica explora tres familias de clasificadores de este tipo —el centroide euclidiano, el vecino más cercano (1-NN) y el algoritmo k de vecinos más cercanos (k-NN)— aplicados sobre el dataset **Iris** del repositorio UCI. Para evaluar el rendimiento de forma robusta se emplean tres esquemas de validación cruzada distintos: Leave-One-Out, 10-Fold Cross-Validation y Hold-Out 70/30. Adicionalmente, se estudia el impacto de la función de distancia elegida sobre la precisión final del modelo, comparando las métricas Euclidiana, Manhattan, Chebyshev y Coseno.

---

## Objetivo general

Implementar, evaluar y comparar clasificadores basados en métricas de distancia sobre un dataset real, analizando el efecto del clasificador, la función de distancia y el método de validación sobre la precisión obtenida.

---

## Objetivos específicos

1. Seleccionar un dataset adecuado (Kaggle o UCI) y realizar un análisis exploratorio de datos (EDA) que incluya estadísticas descriptivas y visualizaciones por clase.
2. Implementar desde cero los clasificadores Centroide Euclidiano, 1-NN y k-NN (con k = 3, 5, 7, 9 y 11) sin depender de bibliotecas de aprendizaje automático de alto nivel.
3. Incorporar al menos cuatro funciones de distancia — Euclidiana, Manhattan, Chebyshev y Coseno — y permitir su selección dinámica en tiempo de ejecución.
4. Aplicar tres métodos de validación cruzada (LOO, 10-Fold y Hold-Out 70/30) para obtener estimaciones de precisión estadísticamente confiables.
5. Construir una tabla comparativa que sistematice los resultados de todas las combinaciones clasificador × métrica × validación e identifique la configuración óptima.

---

## Ejercicios por realizar

### 1. Selección del dataset

- Seleccionar el dataset **Iris** del repositorio UCI Machine Learning Repository.
- Verificar que el archivo CSV contiene las cuatro características (`sepal_length`, `sepal_width`, `petal_length`, `petal_width`) y la columna de clase (`class`).
- Documentar el origen, número de instancias y clases del dataset.

### 2. Análisis exploratorio de datos (EDA)

- Reportar el número de filas y columnas del dataset.
- Calcular y mostrar la distribución de clases (número de instancias por clase).
- Calcular la estadística descriptiva fundamental de cada atributo:
  - Media (`μ`)
  - Desviación estándar (`σ`)
- Generar gráficas 2D que muestren pares de atributos coloreados por clase:
  - Pairplot (todas las combinaciones de pares)
  - Histogramas por atributo y clase
  - Boxplots por clase
  - Mapa de calor de correlaciones entre atributos

### 3. Implementación de los clasificadores

Implementar los siguientes clasificadores en Python puro con NumPy (sin `sklearn` para entrenamiento/predicción):

| Clasificador | Descripción |
|---|---|
| **Centroide Euclidiano** | Calcula el centroide (media) de cada clase; asigna la clase cuyo centroide está más cerca |
| **1-NN** | Retorna la clase del vecino más próximo en el conjunto de entrenamiento |
| **3-NN** | Votación mayoritaria entre los 3 vecinos más cercanos |
| **5-NN** | Votación mayoritaria entre los 5 vecinos más cercanos |
| **7-NN** | Votación mayoritaria entre los 7 vecinos más cercanos |
| **9-NN** | Votación mayoritaria entre los 9 vecinos más cercanos |
| **11-NN** | Votación mayoritaria entre los 11 vecinos más cercanos |

Todos los clasificadores deben exponer la misma interfaz: `fit(X, y)`, `predict(X)` y `predict_one(x)`.

### 4. Implementación de las funciones de distancia

Implementar al menos las siguientes métricas y exponerlas mediante un diccionario de selección dinámica (`DISTANCE_FUNCTIONS`):

| Métrica | Familia | Fórmula |
|---|---|---|
| **Euclidiana** | Minkowski (p=2) | $\sqrt{\sum (a_i - b_i)^2}$ |
| **Manhattan** | Minkowski (p=1) | $\sum \|a_i - b_i\|$ |
| **Chebyshev** | Minkowski (p→∞) | $\max \|a_i - b_i\|$ |
| **Coseno** | No Minkowski | $1 - \dfrac{a \cdot b}{\|a\|\,\|b\|}$ |

### 5. Preprocesado: normalización z-score

- Implementar la normalización z-score: $X' = \dfrac{X - \mu}{\sigma}$
- Calcular `μ` y `σ` **exclusivamente sobre el conjunto de entrenamiento** de cada partición para evitar fuga de información (_data leakage_).
- Aplicar los mismos parámetros al conjunto de prueba de cada partición.

### 6. Implementación de los métodos de validación

Implementar los tres esquemas de validación cruzada:

| Método | Descripción | Parámetros |
|---|---|---|
| **Leave-One-Out (LOO)** | Entrena con n−1 muestras; la muestra excluida actúa como test. Repite n veces. | — |
| **10-Fold Cross-Validation** | Divide el dataset en 10 pliegues; rota el pliegue de test en cada iteración. | k = 10, semilla = 42 |
| **Hold-Out 70/30** | Partición aleatoria fija: 70 % entrenamiento, 30 % test. | ratio_test = 0.3, semilla = 42 |

Implementar mediante una función `factory: Callable[[], Clasificador]` que genere una nueva instancia del clasificador en cada iteración.

### 7. Tabla comparativa de resultados

Construir una tabla que incluya todas las combinaciones de:
- Clasificador (Centroide, 1-NN, 3-NN, 5-NN, 7-NN, 9-NN, 11-NN)
- Métrica (Euclidiana, Manhattan, Chebyshev, Coseno)
- Método de validación (LOO, 10-Fold, Hold-Out)

Reportar la precisión (accuracy) para cada combinación y calcular la media y desviación típica entre los tres esquemas de validación.

Identificar y destacar:
- La combinación con la **mejor media global**
- La combinación **más consistente** (menor desviación típica entre validaciones)
- La **mejor** y **peor métrica** de distancia
- La diferencia de rendimiento entre el Centroide y los clasificadores k-NN

### 8. Análisis y conclusiones

Redactar un análisis de los resultados que responda a las siguientes preguntas:
- ¿Qué clasificador obtiene la mayor precisión y por qué?
- ¿Qué métrica de distancia es más adecuada para este dataset?
- ¿En qué medida el número de vecinos k afecta a la precisión?
- ¿Cuál es el método de validación más confiable para este tamaño de dataset?
- ¿Qué diferencia hay entre usar distancias de tipo Minkowski frente a la distancia Coseno?

---

## Resultados

### 1. Descripción del dataset

El dataset **Iris** (UCI Machine Learning Repository) contiene **150 muestras** descritas por **4 características continuas** y una columna de clase. No contiene valores nulos ni duplicados.

| Dimensión | Valor |
|---|---|
| Filas | 150 |
| Columnas | 5 (4 características + clase) |
| Clases | 3 |
| Muestras por clase | 50 (dataset perfectamente balanceado) |

**Distribución de clases:**

| Clase | Muestras | Proporción |
|---|---:|---:|
| Iris-setosa | 50 | 33.3 % |
| Iris-versicolor | 50 | 33.3 % |
| Iris-virginica | 50 | 33.3 % |

---

### 2. Estadística descriptiva

#### Global (todas las clases)

| Atributo | Media (μ) | Desv. típica (σ) | Mín. | Máx. |
|---|---:|---:|---:|---:|
| sepal_length | 5.843 | 0.828 | 4.3 | 7.9 |
| sepal_width | 3.057 | 0.436 | 2.0 | 4.4 |
| petal_length | 3.758 | 1.765 | 1.0 | 6.9 |
| petal_width | 1.199 | 0.762 | 0.1 | 2.5 |

#### Por clase

| Atributo | Iris-setosa μ (σ) | Iris-versicolor μ (σ) | Iris-virginica μ (σ) |
|---|---|---|---|
| sepal_length | 5.006 (0.352) | 5.936 (0.516) | 6.588 (0.636) |
| sepal_width | 3.418 (0.381) | 2.770 (0.314) | 2.974 (0.322) |
| petal_length | 1.464 (0.174) | 4.260 (0.470) | 5.552 (0.552) |
| petal_width | 0.244 (0.107) | 1.326 (0.198) | 2.026 (0.275) |

> **Observación:** `petal_length` y `petal_width` presentan alta varianza global (σ = 1.765 y 0.762, respectivamente) y separación clara entre clases, lo que las convierte en las características más discriminantes. `sepal_width` es la menos informativa globalmente.

---

### 3. Tabla comparativa de resultados

Todas las combinaciones clasificador × métrica × validación. La precisión se expresa como porcentaje; la última columna es la media de los tres esquemas de validación.

| Clasificador | Métrica | LOO | 10-Fold | Hold-Out | Media | Desv. típica |
|---|---|---:|---:|---:|---:|---:|
| Centroide | Euclidiana | 85.33 % | 86.00 % | 88.89 % | 86.74 % | 1.89 % |
| 1-NN | Euclidiana | 94.67 % | 94.67 % | 100.00 % | **96.44 %** | 3.08 % |
| 3-NN | Euclidiana | 94.67 % | 94.67 % | 97.78 % | 95.70 % | 1.80 % |
| 5-NN | Euclidiana | 94.67 % | 94.67 % | 97.78 % | 95.70 % | 1.80 % |
| 7-NN | Euclidiana | 96.00 % | 96.00 % | 95.56 % | 95.85 % | **0.26 %** |
| 9-NN | Euclidiana | 95.33 % | 95.33 % | 97.78 % | 96.15 % | 1.41 % |
| 11-NN | Euclidiana | 95.33 % | 95.33 % | 97.78 % | 96.15 % | 1.41 % |
| 1-NN | Manhattan | 92.67 % | 92.67 % | 97.78 % | 94.37 % | 2.95 % |
| 3-NN | Manhattan | 94.67 % | 94.67 % | 100.00 % | **96.44 %** | 3.08 % |
| 5-NN | Manhattan | 95.33 % | 95.33 % | 97.78 % | 96.15 % | 1.41 % |
| 7-NN | Manhattan | 94.00 % | 94.00 % | 97.78 % | 95.26 % | 2.18 % |
| 9-NN | Manhattan | 94.67 % | 94.00 % | 97.78 % | 95.48 % | 2.02 % |
| 11-NN | Manhattan | 94.00 % | 94.00 % | 97.78 % | 95.26 % | 2.18 % |
| 1-NN | Chebyshev | 95.33 % | 95.33 % | 97.78 % | 96.15 % | 1.41 % |
| 3-NN | Chebyshev | 95.33 % | 95.33 % | 97.78 % | 96.15 % | 1.41 % |
| 5-NN | Chebyshev | 93.33 % | 93.33 % | 93.33 % | 93.33 % | ~0.00 % |
| 7-NN | Chebyshev | 95.33 % | 94.67 % | 95.56 % | 95.19 % | 0.46 % |
| 9-NN | Chebyshev | 94.67 % | 94.00 % | 93.33 % | 94.00 % | 0.67 % |
| 11-NN | Chebyshev | 95.33 % | 94.67 % | 93.33 % | 94.44 % | 1.02 % |
| 1-NN | Coseno | 85.33 % | 85.33 % | 91.11 % | 87.26 % | 3.34 % |
| 3-NN | Coseno | 88.00 % | 88.00 % | 86.67 % | 87.56 % | 0.77 % |
| 5-NN | Coseno | 86.00 % | 86.67 % | 93.33 % | 88.67 % | 4.06 % |
| 7-NN | Coseno | 88.00 % | 86.00 % | 91.11 % | 88.37 % | 2.58 % |
| 9-NN | Coseno | 86.67 % | 86.00 % | 91.11 % | 87.93 % | 2.78 % |
| 11-NN | Coseno | 85.33 % | 83.33 % | 93.33 % | 87.33 % | 5.29 % |

---

### 4. Análisis de resultados

#### Mejor media global

Dos configuraciones alcanzan la mayor media: **1-NN Euclidiana** y **3-NN Manhattan**, ambas con 96.44 %. Sin embargo, ambas presentan una desviación típica de 3.08 %, motivada por el Hold-Out que reportó 100 % con la semilla fija (42), resultado no reproducible en LOO ni 10-Fold.

#### Configuración más consistente

**7-NN Euclidiana** es la más estable: LOO = 96.00 %, 10-Fold = 96.00 %, Hold-Out = 95.56 %, con una desviación típica de solo 0.26 %. Esta consistencia entre esquemas de validación indica un rendimiento genuino y no dependiente de la partición aleatoria.

#### Impacto de la métrica de distancia

| Métrica | Media máxima alcanzada | Observación |
|---|---:|---|
| Euclidiana | 96.44 % | Mejor combinación junto a Manhattan |
| Manhattan | 96.44 % | Igualmente competitiva; más robusta ante valores atípicos |
| Chebyshev | 96.15 % | Ligeramente inferior; 5-NN se estanca en 93.33 % |
| Coseno | 88.67 % | Peor de las cuatro; mide orientación, no magnitud |

La distancia Coseno obtiene los peores resultados porque Iris es un dataset donde las diferencias de **magnitud** entre los vectores de características son las que separan las clases (especialmente en `petal_length` y `petal_width`). Al normalizar los vectores, esta información se pierde.

#### Impacto del número de vecinos k

Con la métrica Euclidiana, el rendimiento se mantiene estable entre k = 1 y k = 11 (rango 94.67 %–96.44 %). No se observa sobreajuste significativo al aumentar k, lo que es consistente con el tamaño reducido del dataset (150 muestras) y la buena separabilidad de las clases.

#### Centroide vs. k-NN

El Centroide Euclidiano alcanza 86.74 % de media, frente al 96.44 % del mejor k-NN. La diferencia de **–9.7 puntos porcentuales** se explica porque el centroide asume fronteras de decisión lineales (hiperplanos de Voronoi), insuficientes para separar Iris-versicolor e Iris-virginica, cuyas regiones de solapamiento requieren fronteras no lineales.

#### Fiabilidad del método de validación

LOO y 10-Fold muestran resultados muy similares entre sí en casi todas las combinaciones, lo que indica estabilidad. Hold-Out puede producir estimaciones optimistas o pesimistas según la partición aleatoria: en este experimento (semilla 42), favoreció a 1-NN Euclidiana y 3-NN Manhattan reportando 100 %, cifra que ni LOO ni 10-Fold replican.

---

### 5. Conclusiones

| Categoría | Combinación | Valor |
|---|---|---|
| **Mejor media global** | 1-NN Euclidiana y 3-NN Manhattan (empatadas) | 96.44 % |
| **Más consistente** | 7-NN Euclidiana | Desv. típica 0.26 % |
| **Mejor métrica** | Euclidiana y Manhattan (empatadas) | Media máx. 96.44 % |
| **Peor métrica** | Coseno | Media máx. 88.67 % |
| **Centroide vs. k-NN** | Centroide 86.74 % frente a k-NN 96.44 % | −9.7 pp |
| **Validación más robusta** | LOO y 10-Fold (resultados muy similares entre sí) | Menor varianza entre esquemas |
