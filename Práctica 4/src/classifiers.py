"""
classifiers.py
--------------
Define los tres clasificadores utilizados en la práctica:
EuclideanCentroidClassifier, KNNClassifier y NNClassifier.
"""

import numpy as np
from collections import Counter
from .distances import euclidean, DISTANCE_FUNCTIONS


class EuclideanCentroidClassifier:
    """Clasificador basado en centroides euclideos.
    
    Realiza clasificación calculando el centroide (media) de cada clase
    y asignando nuevas muestras a la clase cuyo centroide es más cercano.
    """

    def __init__(self):
        """Inicializa el clasificador."""
        # Diccionario para almacenar los centroides de cada clase
        self.centroids: dict[int, np.ndarray] = {}

    def fit(self, X: np.ndarray, y: np.ndarray) -> "EuclideanCentroidClassifier":
        """Entrena el clasificador calculando los centroides.
        
        Args:
            X: Matriz de características de entrenamiento (n_samples, n_features).
            y: Vector de etiquetas de clase (n_samples,).
            
        Returns:
            Devuelve self para permitir encadenamiento de métodos.
        """
        # Calcula el centroide para cada clase única en los datos
        # --------------------------------------------
        # Posibles clases en el conjunto Iris:
        # 0 - Iris-setosa
        # 1 - Iris-versicolor
        # 2 - Iris-virginica
        # --------------------------------------------
        for label in np.unique(y):
            # .mean(axis=0): calcula la media aritmética de todas las muestras de la clase actual
            self.centroids[label] = X[y == label].mean(axis=0)
        return self

    def predict_one(self, x: np.ndarray) -> int:
        """Predice la clase de una única muestra.
        
        Args:
            x: Vector de características (n_features,).
            
        Returns:
            Etiqueta de clase predicha (int).
        """
        # Encuentra el centroide más cercano usando distancia euclidea
        # Por cada centroide en self.centroids, calcula la distancia euclidea a x 
        # y retorna la etiqueta del centroide más cercano.
        # -------------------------------------------
        # self.centroids: diccionario con etiquetas de clase como claves y centroides como valores
        # min(..., key=...): encuentra la clave del centroide más cercano a x
        # euclidean(x, self.centroids[c]): calcula la distancia euclidea entre x y el centroide de la clase c
        # -- ------------------------------------------
        return min(self.centroids, key=lambda c: euclidean(x, self.centroids[c]))

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predice las clases de múltiples muestras.
        
        Args:
            X: Matriz de características (n_samples, n_features).
            
        Returns:
            Array con las etiquetas predichas para cada muestra.
        """
        # Aplica la función predict_one a cada muestra en X y devuelve un array de predicciones
        return np.array([self.predict_one(x) for x in X])


class KNNClassifier:
    def __init__(self, k: int = 1, metric: str = "euclidean"):
        self.k = k                                      # número de vecinos a considerar
        self.metric = metric                            # nombre de la métrica: "euclidean", "manhattan"...
        self._dist_fn = DISTANCE_FUNCTIONS[metric]      # función de distancia correspondiente al nombre
        self.X_train: np.ndarray | None = None          # matriz de características de entrenamiento
        self.y_train: np.ndarray | None = None          # vector de etiquetas de entrenamiento

    def fit(self, X: np.ndarray, y: np.ndarray) -> "KNNClassifier":
        self.X_train = X
        self.y_train = y
        return self

    def predict_one(self, x: np.ndarray) -> int:
        # Calcula la distancia entre x y cada muestra en el conjunto de entrenamiento
        # --------------------------------------------
        # self.X_train: matriz de características del conjunto de entrenamiento
        # self._dist_fn: función de distancia seleccionada (euclidean, manhattan, etc.)
        # distances: array con la distancia de x a cada muestra en el conjunto de entrenamiento
        # --------------------------------------------
        distances = np.array([self._dist_fn(x, xi) for xi in self.X_train])
        
        # Encuentra los índices de las k muestras más cercanas
        # --------------------------------------------
        # np.argsort(distances): devuelve los índices que ordenarían el array de distancias
        # [:self.k]: toma los primeros k índices (los más cercanos)
        # indices: array con los índices de las k muestras más cercanas
        # --------------------------------------------
        indices = np.argsort(distances)[: self.k]
        
        # Realiza una votación entre las etiquetas de las k muestras más cercanas
        # --------------------------------------------
        # self.y_train[indices]: obtiene las etiquetas de las k muestras más cercanas
        # Counter(...): cuenta cuántas veces aparece cada etiqueta entre las k más cercanas
        # -- ------------------------------------------
        votes = Counter(self.y_train[indices])
        
        # Devuelve la etiqueta con más votos (la clase más común entre las k muestras más cercanas)
        # --------------------------------------------
        # votes.most_common(1): devuelve una lista con la etiqueta más común y su conteo
        # --------------------------------------------
        # votes.most_common(1)       # → [(0, 2)]   lista con 1 tupla (clase, conteo)
        # votes.most_common(1)[0]    # → (0, 2)     la tupla
        # votes.most_common(1)[0][0] # → 0          el entero de la clase
        return votes.most_common(1)[0][0]

    def predict(self, X: np.ndarray) -> np.ndarray:
        # Aplica la función predict_one a cada muestra en X y devuelve un array de predicciones
        return np.array([self.predict_one(x) for x in X])


class NNClassifier(KNNClassifier):
    """Vecino más cercano — alias de KNNClassifier con k=1."""

    # Instancia el clasificador KNN con k=1 y la métrica especificada
    def __init__(self, metric: str = "euclidean"):
        super().__init__(k=1, metric=metric)
