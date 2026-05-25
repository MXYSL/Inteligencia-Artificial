"""
distances.py
------------
Funciones de distancia para clasificación: euclidiana, Manhattan, Chebyshev y coseno.
Expone el diccionario DISTANCE_FUNCTIONS para selección dinámica de métrica en los clasificadores.
"""

import numpy as np


def euclidean(a: np.ndarray, b: np.ndarray) -> float:
    """Calcula la distancia euclidiana entre dos vectores.
    
    La distancia euclidiana es la raíz cuadrada de la suma de los cuadrados
    de las diferencias entre los elementos correspondientes de dos vectores.
    
    Args:
        a: Primer vector de entrada.
        b: Segundo vector de entrada.
    
    Returns:
        La distancia euclidiana como un número flotante.
    """
    # Calcular las diferencias entre los vectores, elevarlas al cuadrado,
    # sumarlas y obtener la raíz cuadrada del resultado
    return float(np.sqrt(np.sum((a - b) ** 2)))


def manhattan(a: np.ndarray, b: np.ndarray) -> float:
    """Calcula la distancia de Manhattan entre dos vectores.
    
    La distancia de Manhattan (también conocida como distancia L1) es la suma
    de los valores absolutos de las diferencias entre los elementos
    correspondientes de dos vectores.
    
    Args:
        a: Primer vector de entrada.
        b: Segundo vector de entrada.
    
    Returns:
        La distancia de Manhattan como un número flotante.
    """
    # Calcular los valores absolutos de las diferencias y sumarlos
    return float(np.sum(np.abs(a - b)))


def chebyshev(a: np.ndarray, b: np.ndarray) -> float:
    """Calcula la distancia de Chebyshev entre dos vectores.
    
    La distancia de Chebyshev (también conocida como distancia L∞ o del máximo)
    es el máximo de los valores absolutos de las diferencias entre los elementos
    correspondientes de dos vectores.
    
    Args:
        a: Primer vector de entrada.
        b: Segundo vector de entrada.
    
    Returns:
        La distancia de Chebyshev como un número flotante.
    """
    # Obtener el valor máximo de los valores absolutos de las diferencias
    return float(np.max(np.abs(a - b)))


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    """Calcula la distancia coseno entre dos vectores.
    
    La distancia coseno es 1 menos el coseno de la similitud. Es una medida
    que captura la diferencia de ángulos entre dos vectores, independientemente
    de sus magnitudes.
    
    Args:
        a: Primer vector de entrada.
        b: Segundo vector de entrada.
    
    Returns:
        La distancia coseno como un número flotante en rango [0, 2].
        Retorna 1.0 si alguno de los vectores es cero.
    """
    # Calcular la norma (magnitud) de cada vector
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    # Si alguno de los vectores es cero, retornar distancia máxima
    if norm_a == 0 or norm_b == 0:
        return 1.0
    
    # Calcular 1 menos el coseno de la similitud
    return float(1.0 - np.dot(a, b) / (norm_a * norm_b))


# Diccionario que mapea nombres de distancias a sus funciones correspondientes
DISTANCE_FUNCTIONS = {
    "euclidean": euclidean,
    "manhattan": manhattan,
    "chebyshev": chebyshev,
    "cosine": cosine,
}
