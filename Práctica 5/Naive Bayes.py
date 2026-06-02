import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris, load_wine
from sklearn.model_selection import train_test_split, KFold, LeaveOneOut, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.naive_bayes import GaussianNB


# ==========================
# CLASIFICADOR NAIVE BAYES MANUAL
# ==========================

class GaussianNaiveBayesManual:
    def fit(self, X, y):
        self.classes = np.unique(y)
        self.mean = {}
        self.std = {}
        self.priors = {}

        for c in self.classes:
            X_c = X[y == c]
            self.mean[c] = X_c.mean(axis=0)
            self.std[c] = X_c.std(axis=0) + 1e-9
            self.priors[c] = len(X_c) / len(X)

    def gaussian_pdf(self, x, mean, std):
        exponent = np.exp(-((x - mean) ** 2) / (2 * std ** 2))
        return (1 / (np.sqrt(2 * np.pi) * std)) * exponent

    def predict(self, X):
        predictions = []

        for x in X:
            posteriors = []

            for c in self.classes:
                prior = np.log(self.priors[c])
                likelihood = np.sum(np.log(self.gaussian_pdf(x, self.mean[c], self.std[c])))
                posterior = prior + likelihood
                posteriors.append(posterior)

            predictions.append(self.classes[np.argmax(posteriors)])

        return np.array(predictions)


# ==========================
# FUNCIÓN GENERAL DE ANÁLISIS
# ==========================

def analizar_dataset(nombre, dataset):
    print("\n" + "="*60)
    print(f"DATASET: {nombre}")
    print("="*60)

    X = dataset.data
    y = dataset.target
    feature_names = dataset.feature_names
    target_names = dataset.target_names

    df = pd.DataFrame(X, columns=feature_names)
    df["class"] = y
    df["class_name"] = df["class"].apply(lambda i: target_names[i])

    # ==========================
    # PROBABILIDAD A PRIORI
    # ==========================

    print("\nProbabilidades a priori por clase:")
    priors = df["class_name"].value_counts(normalize=True)

    for clase, prob in priors.items():
        print(f"P({clase}) = {prob:.4f}")

    # ==========================
    # MEDIA Y DESVIACIÓN ESTÁNDAR POR CLASE
    # ==========================

    print("\nMedia y desviación estándar por característica y clase:")

    for clase in target_names:
        print(f"\nClase: {clase}")
        subset = df[df["class_name"] == clase]

        stats = subset[feature_names].agg(["mean", "std"]).T
        print(stats)

    # ==========================
    # GRÁFICAS KDE
    # ==========================

    for feature in feature_names:
        plt.figure(figsize=(8, 5))

        for clase in target_names:
            subset = df[df["class_name"] == clase]
            sns.kdeplot(subset[feature], label=clase, fill=False)

        plt.title(f"KDE de {feature} por clase - {nombre}")
        plt.xlabel(feature)
        plt.ylabel("Densidad")
        plt.legend()
        plt.grid(True)
        plt.show()

    # ==========================
    # MATRIZ DE CORRELACIÓN POR CLASE
    # ==========================

    for clase in target_names:
        subset = df[df["class_name"] == clase]

        plt.figure(figsize=(9, 7))
        sns.heatmap(subset[feature_names].corr(), annot=True, cmap="coolwarm", fmt=".2f")
        plt.title(f"Matriz de correlación - Clase {clase} - {nombre}")
        plt.show()

    # ==========================
    # HOLD-OUT 80/20
    # ==========================

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    modelo_manual = GaussianNaiveBayesManual()
    modelo_manual.fit(X_train, y_train)
    y_pred_manual = modelo_manual.predict(X_test)

    acc_manual = accuracy_score(y_test, y_pred_manual)

    print("\nHold-Out 80/20 - Naive Bayes Manual")
    print(f"Accuracy: {acc_manual:.4f}")
    print(classification_report(y_test, y_pred_manual, target_names=target_names))

    # ==========================
    # COMPARACIÓN CON SCIKIT-LEARN
    # ==========================

    modelo_sklearn = GaussianNB()
    modelo_sklearn.fit(X_train, y_train)
    y_pred_sklearn = modelo_sklearn.predict(X_test)

    acc_sklearn = accuracy_score(y_test, y_pred_sklearn)

    print("\nHold-Out 80/20 - GaussianNB Scikit-learn")
    print(f"Accuracy: {acc_sklearn:.4f}")
    print(classification_report(y_test, y_pred_sklearn, target_names=target_names))

    # ==========================
    # 10-FOLD CROSS VALIDATION
    # ==========================

    kfold = KFold(n_splits=10, shuffle=True, random_state=42)

    scores_manual = []

    for train_index, test_index in kfold.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        modelo = GaussianNaiveBayesManual()
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)

        scores_manual.append(accuracy_score(y_test, y_pred))

    print("\n10-Fold Cross-Validation - Manual")
    print(f"Accuracy promedio: {np.mean(scores_manual):.4f}")
    print(f"Desviación estándar: {np.std(scores_manual):.4f}")

    scores_sklearn = cross_val_score(GaussianNB(), X, y, cv=kfold)

    print("\n10-Fold Cross-Validation - Scikit-learn")
    print(f"Accuracy promedio: {scores_sklearn.mean():.4f}")
    print(f"Desviación estándar: {scores_sklearn.std():.4f}")

    # ==========================
    # LEAVE-ONE-OUT
    # ==========================

    loo = LeaveOneOut()
    scores_loo_manual = []

    for train_index, test_index in loo.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        modelo = GaussianNaiveBayesManual()
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)

        scores_loo_manual.append(accuracy_score(y_test, y_pred))

    print("\nLeave-One-Out - Manual")
    print(f"Accuracy promedio: {np.mean(scores_loo_manual):.4f}")

    scores_loo_sklearn = cross_val_score(GaussianNB(), X, y, cv=loo)

    print("\nLeave-One-Out - Scikit-learn")
    print(f"Accuracy promedio: {scores_loo_sklearn.mean():.4f}")

    # ==========================
    # CONCLUSIÓN SOBRE INDEPENDENCIA
    # ==========================

    print("\nConclusión sobre independencia:")
    print("""
Naive Bayes supone que las características son independientes entre sí dentro de cada clase.
Para evaluar si esta suposición tiene sentido, se revisan las matrices de correlación por clase.
Si existen correlaciones fuertes, por ejemplo mayores a 0.70 o menores a -0.70, entonces la independencia no se cumple completamente.
Sin embargo, Naive Bayes puede seguir funcionando bien aunque la independencia no sea perfecta, porque es un clasificador robusto y sencillo.
""")


# ==========================
# EJECUCIÓN CON DOS DATASETS
# ==========================

iris = load_iris()
wine = load_wine()

analizar_dataset("Iris", iris)
analizar_dataset("Wine", wine)