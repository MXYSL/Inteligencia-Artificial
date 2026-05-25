# Práctica 4 — Clasificación con Métricas de Distancia

Comparativa de clasificadores basados en distancia sobre el dataset **Iris**, evaluados con tres esquemas de validación cruzada distintos.

---

## Estructura del proyecto

```
Práctica 4/
├── data/
│   └── iris.csv                  # Dataset UCI Iris (150 muestras, 4 características, 3 clases)
├── src/
│   ├── __init__.py
│   ├── dataset.py                # Carga del CSV y normalización z-score
│   ├── distances.py              # Métricas: Euclidiana, Manhattan, Chebyshev, Coseno
│   ├── classifiers.py            # Centroide Euclidiano, KNN y 1-NN
│   └── validation.py             # LOO, 10-Fold y Hold-Out
├── notebooks/
│   └── eda_report.ipynb          # EDA + gráficas + tabla comparativa completa
├── results/
│   └── results.csv               # Resultados de todas las combinaciones
├── main.py                       # CLI: evalúa una métrica y un K concretos
├── compare.py                    # Ejecuta y compara todas las combinaciones automáticamente
└── requirements.txt
```

---

## Dataset

El dataset **Iris** contiene 150 muestras de flores divididas en 3 clases perfectamente balanceadas:

| Clase | Muestras |
|---|---|
| Iris-setosa | 50 |
| Iris-versicolor | 50 |
| Iris-virginica | 50 |

Características: `sepal_length`, `sepal_width`, `petal_length`, `petal_width` (en cm).

Preprocesado aplicado: **normalización z-score** calculada sobre el conjunto de entrenamiento y aplicada al de prueba para evitar fuga de información.

---

## Clasificadores implementados

| Clasificador | Clase | Descripción |
|---|---|---|
| **Centroide Euclidiano** | `EuclideanCentroidClassifier` | Calcula el centroide (media) de cada clase; asigna la clase cuyo centroide está más cerca |
| **1-NN** | `NNClassifier` | Alias de KNN con k=1; retorna la clase del vecino más próximo |
| **K-NN** | `KNNClassifier` | K vecinos más cercanos; decide por votación mayoritaria (`Counter`) |

Los valores de K evaluados son: **3, 5, 7, 9, 11**.

Todos los clasificadores exponen la misma interfaz:
- `fit(X, y)` — entrena el modelo
- `predict(X)` — predice un conjunto de muestras
- `predict_one(x)` — predice una única muestra

---

## Métricas de distancia

| Métrica | Función | Descripción |
|---|---|---|
| **Euclidiana** | `euclidean(a, b)` | $\sqrt{\sum (a_i - b_i)^2}$ — distancia física estándar |
| **Manhattan** | `manhattan(a, b)` | $\sum \|a_i - b_i\|$ — robusta ante valores atípicos |
| **Chebyshev** | `chebyshev(a, b)` | $\max \|a_i - b_i\|$ — sólo importa la dimensión con mayor diferencia |
| **Coseno** | `cosine(a, b)` | $1 - \dfrac{a \cdot b}{\|a\|\,\|b\|}$ — mide diferencia de ángulo, no de magnitud |

El diccionario `DISTANCE_FUNCTIONS` agrupa las cuatro funciones y permite seleccionarlas dinámicamente por nombre.

---

## Esquemas de validación

| Esquema | Función | Descripción |
|---|---|---|
| **Leave-One-Out** | `leave_one_out(X, y, factory)` | Entrena n veces con n-1 muestras; la muestra excluida actúa como test |
| **10-Fold** | `k_fold(X, y, factory, k=10, seed=42)` | Divide en 10 pliegues; rota el pliegue de test en cada iteración |
| **Hold-Out** | `hold_out(X, y, factory, test_ratio=0.3, seed=42)` | 70 % entrenamiento / 30 % test, partición aleatoria con semilla fija |

El parámetro `factory` es un callable sin argumentos que devuelve una nueva instancia del clasificador, lo que permite reutilizar las mismas funciones de validación con cualquier modelo.

---

## Resultados

### Tabla completa (todas las combinaciones)

| Clasificador | Métrica | LOO | 10-Fold | Hold-Out | Media |
|---|---|---:|---:|---:|---:|
| Centroide | Euclidiana | 85.33% | 86.00% | 88.89% | 86.74% |
| 1-NN | Euclidiana | 94.67% | 94.67% | 100.00% | **96.44%** |
| 3-NN | Euclidiana | 94.67% | 94.67% | 97.78% | 95.70% |
| 5-NN | Euclidiana | 94.67% | 94.67% | 97.78% | 95.70% |
| 7-NN | Euclidiana | 96.00% | 96.00% | 95.56% | 95.85% |
| 9-NN | Euclidiana | 95.33% | 95.33% | 97.78% | 96.15% |
| 11-NN | Euclidiana | 95.33% | 95.33% | 97.78% | 96.15% |
| 1-NN | Manhattan | 92.67% | 92.67% | 97.78% | 94.37% |
| 3-NN | Manhattan | 94.67% | 94.67% | 100.00% | **96.44%** |
| 5-NN | Manhattan | 95.33% | 95.33% | 97.78% | 96.15% |
| 7-NN | Manhattan | 94.00% | 94.00% | 97.78% | 95.26% |
| 9-NN | Manhattan | 94.67% | 94.00% | 97.78% | 95.48% |
| 11-NN | Manhattan | 94.00% | 94.00% | 97.78% | 95.26% |
| 1-NN | Chebyshev | 95.33% | 95.33% | 97.78% | 96.15% |
| 3-NN | Chebyshev | 95.33% | 95.33% | 97.78% | 96.15% |
| 5-NN | Chebyshev | 93.33% | 93.33% | 93.33% | 93.33% |
| 7-NN | Chebyshev | 95.33% | 94.67% | 95.56% | 95.19% |
| 9-NN | Chebyshev | 94.67% | 94.00% | 93.33% | 94.00% |
| 11-NN | Chebyshev | 95.33% | 94.67% | 93.33% | 94.44% |
| 1-NN | Coseno | 85.33% | 85.33% | 91.11% | 87.26% |
| 3-NN | Coseno | 88.00% | 88.00% | 86.67% | 87.56% |
| 5-NN | Coseno | 86.00% | 86.67% | 93.33% | 88.67% |
| 7-NN | Coseno | 88.00% | 86.00% | 91.11% | 88.37% |
| 9-NN | Coseno | 86.67% | 86.00% | 91.11% | 87.93% |
| 11-NN | Coseno | 85.33% | 83.33% | 93.33% | 87.33% |

### Conclusiones

| Categoría | Combinación | Valor |
|---|---|---|
| **Mejor media global** | 1-NN Euclidiana y 3-NN Manhattan | 96.44% |
| **Más consistente** | 7-NN Euclidiana (LOO=96%, 10-Fold=96%, HoldOut=95.56%) | Desv. típica 0.0026 |
| **Mejor métrica** | Euclidiana y Manhattan (empatadas) | Media top 96.44% |
| **Peor métrica** | Coseno | Media máx. 88.67% |
| **Centroide vs KNN** | EuclideanCentroid alcanza 86.74% frente al 96.44% de KNN | –9.7 pp |

---

## Instalación

```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate          # Linux / macOS
# .venv\Scripts\activate           # Windows

# Instalar dependencias
pip install -r requirements.txt
```

---

## Uso

### `main.py` — evaluación de una combinación concreta

```bash
python main.py --metric euclidean --k 3
```

| Argumento | Valores posibles | Por defecto |
|---|---|---|
| `--metric` | `euclidean`, `manhattan`, `chebyshev`, `cosine` | `euclidean` |
| `--k` | entero positivo | `3` |

Ejemplo de salida:

```
Dataset: 150 muestras, 3 clases: ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
Metric: euclidean  |  K (for KNN): 3

Classifier              LOO     10-Fold    HoldOut
---------------------------------------------------
Euclidean Centroid    85.33%    86.00%     88.89%
1-NN                  94.67%    94.67%    100.00%
3-NN                  94.67%    94.67%     97.78%
```

### `compare.py` — comparativa completa automática

```bash
python compare.py
```

Itera todas las combinaciones de métricas (×4) y valores de K (3, 5, 7, 9, 11), más el Centroide y el 1-NN. Muestra progreso en tiempo real, imprime la tabla completa, las mejores combinaciones por categoría y guarda los resultados en `results/results.csv`.

### Notebook EDA

```bash
jupyter notebook notebooks/eda_report.ipynb
```

El notebook incluye:
- Vista previa y estadísticas descriptivas del dataset
- Histogramas por clase y característica
- Pairplot con separación de clases
- Mapa de correlación entre características
- Boxplots por clase
- Tabla comparativa de precisión (todos los clasificadores × todas las métricas × todos los esquemas de validación)
- Gráfica de barras comparativa

---

## Módulos

### `src/dataset.py`

| Función | Descripción |
|---|---|
| `load_iris(path)` | Carga el CSV y codifica las etiquetas de texto a enteros (0, 1, 2) |
| `normalize(X)` | Normalización z-score; devuelve `(X_norm, mu, sigma)` |
| `apply_normalization(X, mu, sigma)` | Aplica parámetros ya calculados a datos nuevos |

### `src/distances.py`

| Función / Variable | Descripción |
|---|---|
| `euclidean(a, b)` | Distancia euclidiana entre dos vectores |
| `manhattan(a, b)` | Distancia Manhattan (L1) |
| `chebyshev(a, b)` | Distancia Chebyshev (L∞) |
| `cosine(a, b)` | Distancia coseno; devuelve 1.0 si algún vector es cero |
| `DISTANCE_FUNCTIONS` | Diccionario `{nombre: función}` para selección dinámica |

### `src/classifiers.py`

| Clase | Parámetros | Descripción |
|---|---|---|
| `EuclideanCentroidClassifier` | — | Centroide por clase; distancia euclidiana fija |
| `KNNClassifier` | `k`, `metric` | K vecinos; votación por `Counter.most_common` |
| `NNClassifier` | `metric` | Alias de `KNNClassifier(k=1)` |

### `src/validation.py`

| Función | Parámetros clave | Descripción |
|---|---|---|
| `leave_one_out(X, y, factory)` | — | Itera n veces, cada muestra actúa una vez como test |
| `k_fold(X, y, factory, k=10, seed=42)` | `k`, `seed` | Divide en k pliegues; rota el pliegue de test |
| `hold_out(X, y, factory, test_ratio=0.3, seed=42)` | `test_ratio`, `seed` | Partición fija entrenamiento/test |
| `accuracy(y_true, y_pred)` | — | Proporción de predicciones correctas |

---

## Dependencias

| Paquete | Versión mínima | Uso |
|---|---|---|
| `numpy` | 1.26 | Operaciones matriciales y de distancia |
| `pandas` | 2.2 | Carga del CSV y construcción de tablas |
| `matplotlib` | 3.8 | Gráficas del notebook |
| `seaborn` | 0.13 | Pairplot, boxplots y gráfica comparativa |
| `scikit-learn` | 1.4 | Utilidades del notebook (métricas auxiliares) |
| `jupyter` / `notebook` | 1.0 / 7.0 | Ejecución del notebook EDA |
