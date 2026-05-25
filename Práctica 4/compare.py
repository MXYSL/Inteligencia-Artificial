"""
compare.py
----------
Ejecuta todas las combinaciones de clasificadores, métricas de distancia y valores de K,
e imprime una tabla comparativa completa destacando la mejor combinación.

Uso:
    python compare.py

No requiere argumentos — itera todas las combinaciones automáticamente.
"""

import numpy as np
import pandas as pd

from src.dataset import load_iris, normalize
from src.classifiers import EuclideanCentroidClassifier, KNNClassifier, NNClassifier
from src.validation import leave_one_out, k_fold, hold_out
from src.distances import DISTANCE_FUNCTIONS


# Valores de K a evaluar en KNNClassifier (requeridos por la práctica)
K_VALUES = [3, 5, 7, 9, 11]

# Lista de métricas de distancia a evaluar (extraídas del diccionario DISTANCE_FUNCTIONS)
METRICS = list(DISTANCE_FUNCTIONS.keys())


def make_factory(clf_class, **kwargs):
    """Devuelve una función fábrica que crea una nueva instancia del clasificador."""
    return lambda: clf_class(**kwargs)


def build_experiments(metric: str) -> list[tuple[str, callable]]:
    """
    Construye la lista de experimentos (nombre, fábrica) para una métrica dada.

    Args:
        metric: Nombre de la métrica de distancia.

    Returns:
        Lista de tuplas (nombre_clasificador, fábrica).
    """
    # Experimentos base: Centroid ignora la métrica — siempre usa distancia euclidiana internamente
    experiments = [
        ("Centroid", make_factory(EuclideanCentroidClassifier)),
        ("1-NN",     make_factory(NNClassifier, metric=metric)),
    ]

    # Agrega una entrada por cada valor de K definido en K_VALUES
    for k in K_VALUES:
        experiments.append(
            (f"{k}-NN", make_factory(KNNClassifier, k=k, metric=metric))
        )

    return experiments


def run_all() -> pd.DataFrame:
    """
    Ejecuta todas las combinaciones y recopila los resultados en un DataFrame.

    Returns:
        DataFrame con columnas: Classifier, Metric, LOO, 10-Fold, HoldOut, Mean.
    """
    # Carga y normaliza el conjunto de datos una sola vez — reutilizado en todos los experimentos
    # ------------------------------------------
    # X: matriz de características originales
    # y: vector de etiquetas numéricas
    # classes: lista de nombres de clases
    # X_norm: características normalizadas mediante z-score
    # ------------------------------------------
    X, y, classes = load_iris()
    X_norm, _, _ = normalize(X)

    print(f"Dataset: {len(y)} muestras | Clases: {classes}\n")
    print("Ejecutando todas las combinaciones...\n")

    # Lista de diccionarios que acumulan los resultados de cada experimento
    rows = []

    # Itera sobre cada métrica de distancia disponible
    for metric in METRICS:
        # Obtiene todos los clasificadores configurados para esta métrica
        experiments = build_experiments(metric)

        for name, factory in experiments:
            # Omite variaciones de métrica para Centroid — la métrica no tiene efecto en él
            if name == "Centroid" and metric != "euclidean":
                continue

            # Evalúa el clasificador con los tres métodos de validación
            # ------------------------------------------
            # loo:  precisión Leave-One-Out
            # fold: precisión validación 10-Fold
            # ho:   precisión Hold-Out (30% prueba)
            # mean: media aritmética de los tres resultados de validación
            # ------------------------------------------
            loo  = leave_one_out(X_norm, y, factory)
            fold = k_fold(X_norm, y, factory)
            ho   = hold_out(X_norm, y, factory)
            mean = np.mean([loo, fold, ho])

            # Registra los resultados de esta combinación como una fila del DataFrame
            rows.append({
                "Classifier": name,
                "Metric":     metric,
                "LOO":        loo,
                "10-Fold":    fold,
                "HoldOut":    ho,
                "Mean":       mean,
            })

            # Muestra el progreso en tiempo real por cada combinación evaluada
            print(f"  {name:<8} | {metric:<12} | "
                  f"LOO={loo:.2%}  10-Fold={fold:.2%}  HoldOut={ho:.2%}  "
                  f"Mean={mean:.2%}")

    return pd.DataFrame(rows)


def print_full_table(df: pd.DataFrame) -> None:
    """Imprime la tabla comparativa completa con formato."""
    print("\n" + "=" * 72)
    print("TABLA COMPARATIVA COMPLETA")
    print("=" * 72)

    # Convierte las columnas numéricas a cadenas de porcentaje para la visualización
    # ------------------------------------------
    # display: copia del DataFrame con los valores formateados
    # .map(lambda x: f"{x:.2%}"): convierte cada valor float a porcentaje con 2 decimales
    # ------------------------------------------
    display = df.copy()
    for col in ["LOO", "10-Fold", "HoldOut", "Mean"]:
        display[col] = display[col].map(lambda x: f"{x:.2%}")

    print(display.to_string(index=False))


def print_best(df: pd.DataFrame) -> None:
    """Encuentra e imprime la mejor combinación por categoría."""
    print("\n" + "=" * 72)
    print("MEJORES COMBINACIONES")
    print("=" * 72)

    # Mejor combinación global según la precisión media de los tres métodos de validación
    # ------------------------------------------
    # df["Mean"].idxmax(): índice de la fila con mayor precisión media
    # best_row: fila del DataFrame con los mejores resultados globales
    # ------------------------------------------
    best_row = df.loc[df["Mean"].idxmax()]
    print(f"\n{'Mejor combinación global (mayor precisión media)'}")
    print(f"  Clasificador : {best_row['Classifier']}")
    print(f"  Métrica      : {best_row['Metric']}")
    print(f"  LOO          : {best_row['LOO']:.2%}")
    print(f"  10-Fold      : {best_row['10-Fold']:.2%}")
    print(f"  HoldOut      : {best_row['HoldOut']:.2%}")
    print(f"  Media        : {best_row['Mean']:.2%}")

    # Combinación más robusta — menor desviación estándar entre los tres métodos de validación
    # ------------------------------------------
    # df["Std"]: desviación estándar de LOO, 10-Fold y HoldOut calculada por fila
    # most_robust: fila con menor varianza entre los métodos, indicando mayor consistencia
    # ------------------------------------------
    print(f"\n{'Combinación más robusta (menor varianza entre métodos de validación)'}")
    df["Std"] = df[["LOO", "10-Fold", "HoldOut"]].std(axis=1)
    most_robust = df.loc[df["Std"].idxmin()]
    print(f"  Clasificador : {most_robust['Classifier']}")
    print(f"  Métrica      : {most_robust['Metric']}")
    print(f"  Desv. típica : {most_robust['Std']:.4f}  ← menor = más consistente")

    # Mejor clasificador por métrica de distancia
    # ------------------------------------------
    # subset: subconjunto del DataFrame filtrado por cada métrica
    # best: fila con mayor precisión media dentro de ese subconjunto
    # ------------------------------------------
    print(f"\n{'Mejor clasificador por métrica'}")
    print(f"  {'Métrica':<12} {'Clasificador':<14} {'Media':>8}")
    print(f"  {'-'*36}")
    for metric in METRICS:
        subset = df[df["Metric"] == metric]
        if subset.empty:
            continue
        best = subset.loc[subset["Mean"].idxmax()]
        print(f"  {metric:<12} {best['Classifier']:<14} {best['Mean']:>8.2%}")

    # Comparación LOO vs 10-Fold — análisis del pesimismo de LOO
    # ------------------------------------------
    # df["LOO_vs_Fold"]: diferencia LOO - 10-Fold; negativa si LOO es más pesimista
    # pessimistic_count: número de combinaciones donde LOO produce menor precisión que 10-Fold
    # ------------------------------------------
    print(f"\n{'LOO vs 10-Fold (LOO tiende a ser más pesimista)'}")
    df["LOO_vs_Fold"] = df["LOO"] - df["10-Fold"]
    pessimistic_count = (df["LOO_vs_Fold"] < 0).sum()
    total = len(df)
    print(f"  LOO < 10-Fold en {pessimistic_count}/{total} combinaciones "
          f"({pessimistic_count/total:.0%} de los casos)")


def save_csv(df: pd.DataFrame, path: str = "results/results.csv") -> None:
    """Guarda la tabla completa de resultados en un archivo CSV."""
    # ------------------------------------------
    # df.to_csv: exporta el DataFrame al archivo especificado sin incluir el índice de fila
    # path: ruta del archivo de salida (por defecto "results/results.csv")
    # ------------------------------------------
    df.to_csv(path, index=False)
    print(f"\nResultados guardados en: {path}")


if __name__ == "__main__":
    df = run_all()
    print_full_table(df)
    print_best(df)
    save_csv(df)
