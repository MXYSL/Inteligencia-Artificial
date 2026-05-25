"""
validation.py
-------------
Implementa los tres métodos de validación cruzada para evaluar clasificadores:
Leave-One-Out (LOO), k-Fold y Hold-Out.
"""

import numpy as np
from typing import Callable


ClassifierFactory = Callable[[], object]


def accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calcula la precisión de las predicciones.

    Args:
        y_true: Etiquetas verdaderas.
        y_pred: Etiquetas predichas.

    Returns:
        La proporción de predicciones correctas.
    """
    # Compara elemento a elemento y calcula la proporción de aciertos
    return float(np.mean(y_true == y_pred))


def leave_one_out(X: np.ndarray, y: np.ndarray, factory: ClassifierFactory) -> float:
    """
    Realiza validación cruzada Leave-One-Out.

    Este método entrena el clasificador n veces, usando n-1 muestras para entrenar
    y 1 muestra para validar, donde n es el tamaño del conjunto de datos.

    Args:
        X: Matriz de características.
        y: Vector de etiquetas.
        factory: Función que crea una nueva instancia del clasificador.

    Returns:
        La precisión promedio del modelo usando validación LOO.
    """
    # Número total de muestras en el conjunto de datos
    n = len(y)

    # Acumulador del número de predicciones correctas a lo largo de las n iteraciones
    correct = 0

    # Itera n veces, usando cada muestra i como único ejemplo de prueba
    for i in range(n):
        # Genera una máscara booleana para seleccionar las muestras de entrenamiento
        # ------------------------------------------
        # np.arange(n): array de índices de 0 a n-1
        # != i: produce True en todas las posiciones excepto en la i
        # mask: array booleano de tamaño n con False sólo en la posición i
        # ------------------------------------------
        mask = np.arange(n) != i

        # Crea una nueva instancia del clasificador para esta iteración
        # Compatible con:
        # - KNNClassifier
        # - NNClassifier
        # - EuclideanCentroidClassifier
        # ------------------------------------------
        # factory(): llamada sin argumentos que devuelve un clasificador sin entrenar
        # ------------------------------------------
        clf = factory()

        # Entrena el clasificador con las n-1 muestras que no son la muestra i
        # ------------------------------------------
        # clf.fit: ajusta el modelo a los datos de entrenamiento
        # X[mask]: submatriz con las características de todas las muestras excepto la i
        # y[mask]: subvector con las etiquetas de todas las muestras excepto la i
        # ------------------------------------------
        clf.fit(X[mask], y[mask])

        # Predice la clase de la muestra i (la única excluida del entrenamiento)
        # Posibles clases en el conjunto Iris:
        # - 0: Iris-setosa
        # - 1: Iris-versicolor
        # - 2: Iris-virginica
        # ------------------------------------------
        # clf.predict_one: predice la etiqueta de una única muestra
        # X[i]: vector de características de la muestra i
        # ------------------------------------------
        pred = clf.predict_one(X[i])

        # Incrementa el contador si la predicción coincide con la etiqueta real
        correct += int(pred == y[i])

    # Retorna la proporción de predicciones correctas sobre el total de muestras
    return correct / n


def k_fold(
    X: np.ndarray,
    y: np.ndarray,
    factory: ClassifierFactory,
    k: int = 10,
    seed: int = 42,
) -> float:
    """
    Realiza validación cruzada k-fold.

    Divide el conjunto de datos en k pliegues y utiliza cada pliegue como conjunto
    de prueba mientras que los pliegues restantes se usan para entrenamiento.

    Args:
        X: Matriz de características.
        y: Vector de etiquetas.
        factory: Función que crea una nueva instancia del clasificador.
        k: Número de pliegues. Por defecto 10.
        seed: Semilla para reproducibilidad. Por defecto 42.

    Returns:
        La precisión promedio del modelo usando validación k-fold.
    """
    # Número total de muestras en el conjunto de datos
    n = len(y)

    # Crea un generador aleatorio con la semilla proporcionada para reproducibilidad
    rng = np.random.default_rng(seed)

    # Genera una permutación aleatoria de los índices para mezclar el conjunto de datos
    # ------------------------------------------
    # rng.permutation(n): devuelve un array de 0 a n-1 en orden aleatorio
    # indices: array de índices mezclados que se usará para dividir los pliegues
    # ------------------------------------------
    indices = rng.permutation(n)

    # Divide los índices mezclados en k subconjuntos (pliegues) de tamaño similar
    folds = np.array_split(indices, k)

    # Lista que acumula la precisión obtenida en cada uno de los k pliegues
    accs = []

    # Itera k veces; en cada iteración el pliegue i actúa como conjunto de prueba
    # y los k-1 pliegues restantes se usan para entrenamiento
    for i in range(k):
        # Índices del conjunto de prueba: los pertenecientes al pliegue i
        test_idx = folds[i]

        # Índices de entrenamiento: concatenación de todos los pliegues excepto el i
        train_idx = np.concatenate([folds[j] for j in range(k) if j != i])

        # Crea una nueva instancia del clasificador para esta iteración
        # Compatible con:
        # - KNNClassifier
        # - NNClassifier
        # - EuclideanCentroidClassifier
        # ------------------------------------------
        # factory(): llamada sin argumentos que devuelve un clasificador sin entrenar
        # ------------------------------------------
        clf = factory()

        # Entrena el clasificador con las muestras de los k-1 pliegues de entrenamiento
        # ------------------------------------------
        # clf.fit: ajusta el modelo a los datos de entrenamiento
        # X[train_idx]: submatriz con las características del conjunto de entrenamiento
        # y[train_idx]: subvector con las etiquetas del conjunto de entrenamiento
        # ------------------------------------------
        clf.fit(X[train_idx], y[train_idx])

        # Predice las clases del conjunto de prueba (el pliegue i)
        # Posibles clases en el conjunto Iris:
        # - 0: Iris-setosa
        # - 1: Iris-versicolor
        # - 2: Iris-virginica
        # ------------------------------------------
        # clf.predict: predice las etiquetas de un conjunto de muestras
        # X[test_idx]: submatriz con las características del conjunto de prueba
        # ------------------------------------------
        preds = clf.predict(X[test_idx])

        # Calcula la precisión del pliegue i y la acumula en la lista de resultados
        # ------------------------------------------
        # accuracy: compara y[test_idx] con preds y devuelve la proporción de aciertos
        # y[test_idx]: etiquetas verdaderas del conjunto de prueba
        # preds: etiquetas predichas por el clasificador para el pliegue i
        # ------------------------------------------
        accs.append(accuracy(y[test_idx], preds))

    # Retorna la media de las precisiones de los k pliegues como estimación global
    return float(np.mean(accs))


def hold_out(
    X: np.ndarray,
    y: np.ndarray,
    factory: ClassifierFactory,
    test_ratio: float = 0.3,
    seed: int = 42,
) -> float:
    """
    Realiza validación con el método hold-out.

    Divide el conjunto de datos en dos partes: una para entrenamiento y otra
    para prueba, según la razón especificada.

    Args:
        X: Matriz de características.
        y: Vector de etiquetas.
        factory: Función que crea una nueva instancia del clasificador.
        test_ratio: Proporción del conjunto de prueba. Por defecto 0.3.
        seed: Semilla para reproducibilidad. Por defecto 42.

    Returns:
        La precisión del modelo en el conjunto de prueba.
    """
    # Número total de muestras en el conjunto de datos
    n = len(y)

    # Crea un generador aleatorio con la semilla proporcionada para reproducibilidad
    rng = np.random.default_rng(seed)

    # Genera una permutación aleatoria de los índices para mezclar el conjunto de datos
    # ------------------------------------------
    # rng.permutation(n): devuelve un array de 0 a n-1 en orden aleatorio
    # indices: array de índices mezclados que se usará para dividir entrenamiento y prueba
    # ------------------------------------------
    indices = rng.permutation(n)

    # Calcula el índice de corte que separa el conjunto de entrenamiento del de prueba
    # ------------------------------------------
    # test_ratio: fracción de muestras reservadas para prueba
    # 1 - test_ratio: fracción destinada a entrenamiento
    # split: número de muestras que pertenecen al conjunto de entrenamiento
    # ------------------------------------------
    split = int(n * (1 - test_ratio))

    # Divide los índices mezclados en conjunto de entrenamiento y de prueba
    train_idx, test_idx = indices[:split], indices[split:]

    # Crea una nueva instancia del clasificador
    # Compatible con:
    # - KNNClassifier
    # - NNClassifier
    # - EuclideanCentroidClassifier
    # ------------------------------------------
    # factory(): llamada sin argumentos que devuelve un clasificador sin entrenar
    # ------------------------------------------
    clf = factory()

    # Entrena el clasificador con el subconjunto de entrenamiento
    # ------------------------------------------
    # clf.fit: ajusta el modelo a los datos de entrenamiento
    # X[train_idx]: submatriz con las características del conjunto de entrenamiento
    # y[train_idx]: subvector con las etiquetas del conjunto de entrenamiento
    # ------------------------------------------
    clf.fit(X[train_idx], y[train_idx])

    # Predice las clases del conjunto de prueba (muestras no vistas durante el entrenamiento)
    # Posibles clases en el conjunto Iris:
    # - 0: Iris-setosa
    # - 1: Iris-versicolor
    # - 2: Iris-virginica
    # ------------------------------------------
    # clf.predict: predice las etiquetas de un conjunto de muestras
    # X[test_idx]: submatriz con las características del conjunto de prueba
    # ------------------------------------------
    preds = clf.predict(X[test_idx])

    # Retorna la precisión del clasificador sobre el conjunto de prueba
    # ------------------------------------------
    # accuracy: compara y[test_idx] con preds y devuelve la proporción de aciertos
    # y[test_idx]: etiquetas verdaderas del conjunto de prueba
    # preds: etiquetas predichas por el clasificador
    # ------------------------------------------
    return accuracy(y[test_idx], preds)
