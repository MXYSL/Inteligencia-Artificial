"""
main.py
-------
Punto de entrada del programa. Carga el dataset Iris, lo normaliza y evalúa
tres clasificadores (Centroid, 1-NN y k-NN) con los tres métodos de validación.

Uso:
    python main.py [--metric euclidean|manhattan|chebyshev|cosine] [--k K]
"""

import argparse
import numpy as np
from src.dataset import load_iris, normalize
from src.classifiers import EuclideanCentroidClassifier, KNNClassifier, NNClassifier
from src.validation import leave_one_out, k_fold, hold_out
from src.distances import DISTANCE_FUNCTIONS


def make_factory(clf_class, **kwargs):
    return lambda: clf_class(**kwargs)


def run(metric: str, k: int) -> None:
    X, y, classes = load_iris()
    X_norm, mu, sigma = normalize(X)

    print(f"\nDataset: {len(y)} samples, {len(classes)} classes: {classes}")
    print(f"Metric: {metric}  |  K (for KNN): {k}\n")

    experiments = [
        ("Euclidean Centroid", make_factory(EuclideanCentroidClassifier)),
        ("1-NN", make_factory(NNClassifier, metric=metric)),
        (f"{k}-NN", make_factory(KNNClassifier, k=k, metric=metric)),
    ]

    header = f"{'Classifier':<22} {'LOO':>8} {'10-Fold':>8} {'HoldOut':>8}"
    print(header)
    print("-" * len(header))

    for name, factory in experiments:
        loo = leave_one_out(X_norm, y, factory)
        fold = k_fold(X_norm, y, factory)
        ho = hold_out(X_norm, y, factory)
        print(f"{name:<22} {loo:>7.2%} {fold:>8.2%} {ho:>8.2%}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Iris classifier comparison")
    parser.add_argument(
        "--metric",
        choices=list(DISTANCE_FUNCTIONS),
        default="euclidean",
        help="Distance metric (default: euclidean)",
    )
    parser.add_argument(
        "--k",
        type=int,
        default=3,
        help="Number of neighbours for KNN (default: 3)",
    )
    args = parser.parse_args()
    run(args.metric, args.k)
