# Clasificador Naive Bayes Gaussiano

## Descripción

Este proyecto implementa un clasificador **Naive Bayes Gaussiano** desarrollado manualmente en Python, además de realizar una comparación directa con la implementación oficial proporcionada por **Scikit-Learn**.

La práctica tiene como finalidad comprender el funcionamiento interno del algoritmo Naive Bayes mediante el cálculo explícito de probabilidades a priori, medias, desviaciones estándar y verosimilitudes Gaussianas, así como analizar el comportamiento del modelo utilizando dos datasets clásicos del aprendizaje automático:

* Iris
* Wine

Adicionalmente, se realiza un análisis estadístico y visual de los datos mediante gráficas de densidad (KDE), matrices de correlación y diferentes métodos de validación para evaluar el desempeño del clasificador.

---

## Integrantes

* De la Cruz Velázquez Marco Uriel
* Sánchez Gómez Alan Iván
* Solís Lugo Mayra

---

## Información 

**Instituto:** Instituto Politécnico Nacional (IPN)

**Escuela:** Escuela Superior de Cómputo (ESCOM)

**Carrera:** Ingeniería en Sistemas Computacionales

**Materia:** Inteligencia Artificial

**Profesor:** Andrés García Floriano

**Práctica:** Clasificador Naive Bayes

**Fecha:** 01 de junio de 2026

---

## Objetivos

### Objetivo General

Implementar y analizar un clasificador Naive Bayes Gaussiano utilizando datasets multiclase, evaluando sus supuestos estadísticos, desempeño predictivo y comparación con herramientas profesionales de Machine Learning.

### Objetivos Específicos

* Implementar manualmente el algoritmo Gaussian Naive Bayes.
* Calcular probabilidades a priori para cada clase.
* Obtener medias y desviaciones estándar por característica y clase.
* Analizar visualmente la distribución de los datos mediante gráficas KDE.
* Evaluar la independencia entre características utilizando matrices de correlación.
* Aplicar distintos métodos de validación para medir el desempeño del clasificador.
* Comparar los resultados obtenidos con la implementación GaussianNB de Scikit-Learn.
* Analizar el comportamiento del algoritmo en diferentes conjuntos de datos.

---

## Datasets Utilizados

### Iris

El dataset Iris es uno de los conjuntos de datos más utilizados en aprendizaje automático y reconocimiento de patrones.

#### Características

* Longitud del sépalo
* Ancho del sépalo
* Longitud del pétalo
* Ancho del pétalo

#### Clases

* Setosa
* Versicolor
* Virginica

#### Información General

* 150 muestras
* 4 características
* 3 clases

---

### Wine

El dataset Wine contiene información química obtenida a partir de diferentes variedades de vino.

#### Características

Incluye variables como:

* Alcohol
* Ácido málico
* Cenizas
* Alcalinidad de cenizas
* Magnesio
* Fenoles totales
* Flavonoides
* Proantocianinas
* Intensidad de color
* Entre otras propiedades químicas

#### Clases

* Clase 0
* Clase 1
* Clase 2

#### Información General

* 178 muestras
* 13 características
* 3 clases

---

## Tecnologías Utilizadas

* Python 3
* NumPy
* Pandas
* Matplotlib
* Seaborn
* Scikit-Learn
* Jupyter Notebook
* Visual Studio Code

---

## Funcionalidades Implementadas

### Análisis Estadístico

* Cálculo de probabilidades a priori.
* Cálculo de medias por clase.
* Cálculo de desviaciones estándar por clase.

### Visualización de Datos

* Gráficas KDE (Kernel Density Estimation).
* Matrices de correlación.
* Análisis de distribución de características.

### Implementación Manual del Clasificador

* Cálculo de probabilidades a priori.
* Cálculo de parámetros Gaussianos.
* Función de densidad de probabilidad Gaussiana.
* Cálculo de probabilidades posteriores.
* Clasificación mediante máxima verosimilitud.

### Validación del Modelo

* Hold-Out 80/20.
* 10-Fold Cross Validation.
* Leave-One-Out (LOO).

### Comparación de Resultados

* Clasificador Manual.
* GaussianNB de Scikit-Learn.

---

## Estructura del Proyecto

```text
.
├── Naive Bayes.py
├── Notebook Naive Bayes.ipynb
└── README.md
```

### Descripción de los Archivos

| Archivo                      | Descripción                                                                                                         |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `Naive Bayes.py`             | Implementación completa del clasificador Gaussian Naive Bayes y generación de resultados experimentales.            |
| `Notebook Naive Bayes.ipynb` | Documento principal de la práctica que integra teoría, desarrollo, análisis estadístico, resultados y conclusiones. |
| `README.md`                  | Documento descriptivo del proyecto e instrucciones de uso.                                                          |

---

## Instalación

### Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
```

### Crear entorno virtual

```bash
python -m venv .venv
```

### Activar entorno virtual

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / macOS

```bash
source .venv/bin/activate
```

### Instalar dependencias

```bash
pip install numpy pandas matplotlib seaborn scikit-learn
```

---

## Ejecución

Ejecutar el programa principal:

```bash
python "Naive Bayes.py"
```

El programa realizará automáticamente:

1. Carga de los datasets Iris y Wine.
2. Cálculo de probabilidades a priori.
3. Cálculo de medias y desviaciones estándar.
4. Generación de gráficas KDE.
5. Generación de matrices de correlación.
6. Implementación manual de Gaussian Naive Bayes.
7. Evaluación mediante Hold-Out.
8. Evaluación mediante 10-Fold Cross Validation.
9. Evaluación mediante Leave-One-Out.
10. Comparación contra Scikit-Learn.

---

## Métodos de Validación Utilizados

### Hold-Out 80/20

Divide el conjunto de datos en:

* 80% entrenamiento
* 20% prueba

Permite evaluar rápidamente la capacidad predictiva del modelo.

### 10-Fold Cross Validation

Divide el dataset en diez particiones.

Cada partición se utiliza como conjunto de prueba una vez, obteniendo una estimación más estable del desempeño del clasificador.

### Leave-One-Out (LOO)

Utiliza una única muestra para prueba en cada iteración y el resto para entrenamiento.

Es uno de los métodos más exhaustivos de validación.

---

## Resultados Esperados

La ejecución del programa genera:

* Probabilidades a priori por clase.
* Medias y desviaciones estándar.
* Gráficas KDE para cada característica.
* Matrices de correlación por clase.
* Accuracy para Hold-Out.
* Accuracy promedio para 10-Fold Cross Validation.
* Accuracy promedio para Leave-One-Out.
* Comparación entre la implementación manual y Scikit-Learn.

---

## Aprendizajes Obtenidos

Durante esta práctica se estudian conceptos fundamentales de aprendizaje supervisado, incluyendo:

* Clasificación probabilística.
* Teorema de Bayes.
* Distribuciones Gaussianas.
* Independencia condicional.
* Evaluación de modelos.
* Validación cruzada.
* Comparación entre implementaciones manuales y bibliotecas especializadas.

---

## Conclusión

La implementación manual del clasificador Gaussian Naive Bayes permite comprender detalladamente los fundamentos matemáticos y probabilísticos que sustentan el algoritmo. Mediante el análisis de los datasets Iris y Wine se evalúan los supuestos de distribución e independencia, además de validar experimentalmente el desempeño del modelo utilizando diferentes técnicas de validación.

La comparación con Scikit-Learn permite verificar la correcta implementación del algoritmo y demostrar que Naive Bayes continúa siendo una alternativa eficiente, interpretable y computacionalmente económica para problemas de clasificación supervisada.
