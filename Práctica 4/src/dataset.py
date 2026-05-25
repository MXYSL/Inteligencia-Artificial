"""
dataset.py
----------
Carga y preprocesa el dataset Iris desde un archivo CSV.
Proporciona funciones de normalización z-score para estandarizar las características.
"""

import numpy as np
import pandas as pd
from pathlib import Path


# Ruta al archivo CSV del dataset Iris
DATA_PATH = Path(__file__).parent.parent / "data" / "iris.csv"


def load_iris(path: Path = DATA_PATH) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """Carga el dataset de Iris desde un archivo CSV.
    
    Carga los datos del dataset Iris y los procesa para obtener las características
    (features) y las etiquetas (labels) mapeadas a valores numéricos.
    
    Args:
        path (Path): Ruta al archivo CSV del dataset. Por defecto utiliza DATA_PATH.
    
    Returns:
        tuple[np.ndarray, np.ndarray, list[str]]: Una tupla que contiene:
            - X (np.ndarray): Matriz de características de forma (n_muestras, n_características).
            - y (np.ndarray): Vector de etiquetas numéricas de forma (n_muestras,).
            - classes (list[str]): Lista de nombres de clases ordenadas alfabéticamente.
    """
    # Leer el archivo CSV en un dataframe de pandas
    df = pd.read_csv(path)
    
    # Seleccionar las columnas de características (todas excepto 'class')
    feature_cols = [col for col in df.columns if col != "class"]
    
    # Convertir las características a un array de numpy de tipo float
    X = df[feature_cols].values.astype(float)
    
    # Obtener las clases únicas y ordenadas
    # En nuestro ejemplo:
    # Iris-setosa, Iris-versicolor, Iris-virginica
    classes = sorted(df["class"].unique())
    
    # Crear un mapeo de clases a índices numéricos
    # Iris-setosa -> 0, Iris-versicolor -> 1, Iris-virginica -> 2
    label_map = {c: i for i, c in enumerate(classes)}
    
    # Mapear las etiquetas de texto a valores numéricos
    y = df["class"].map(label_map).values.astype(int)
    
    return X, y, classes


def normalize(X: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Normaliza las características usando estandarización (z-score).
    
    Calcula la media y desviación estándar de cada característica y aplica
    la transformación de estandarización: (X - μ) / σ.
    
    Args:
        X (np.ndarray): Matriz de características de forma (n_muestras, n_características).
    
    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray]: Una tupla que contiene:
            - X_norm (np.ndarray): Características normalizadas.
            - mu (np.ndarray): Media de cada característica.
            - sigma (np.ndarray): Desviación estándar de cada característica.
    """
    # Calcular la media de cada característica por columna
    mu = X.mean(axis=0)
    
    # Calcular la desviación estándar de cada característica por columna
    sigma = X.std(axis=0)
    
    # Evitar división por cero: si sigma es 0, establecerla a 1
    sigma[sigma == 0] = 1
    
    # Retornar datos normalizados y parámetros de normalización
    return (X - mu) / sigma, mu, sigma


def apply_normalization(X: np.ndarray, mu: np.ndarray, sigma: np.ndarray) -> np.ndarray:
    """Aplica normalización a datos nuevos usando parámetros previamente calculados.
    
    Utiliza la media y desviación estándar obtenidas durante el entrenamiento
    para normalizar nuevas muestras de forma consistente.
    
    Args:
        X (np.ndarray): Matriz de características a normalizar.
        mu (np.ndarray): Media de cada característica (del conjunto de entrenamiento).
        sigma (np.ndarray): Desviación estándar de cada característica (del conjunto de entrenamiento).
    
    Returns:
        np.ndarray: Características normalizadas de la misma forma que X.
    """
    # Aplicar la transformación de estandarización con los parámetros proporcionados
    return (X - mu) / sigma
