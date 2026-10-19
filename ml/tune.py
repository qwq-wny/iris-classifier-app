"""Search LogisticRegression hyperparameters and log the best model to MLflow.

This is the third experiment ("tuned-v2"): same cleaned dataset and the same
scaler as improved-v2, but C and class_weight are chosen by a grid search
instead of by hand. The tuner never overwrites the model used by the app,
it writes `models/model_tuned.pkl` so the two can be compared.
"""

import argparse
import os

import joblib
import mlflow
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from ml.data_pipeline import clean_data, load_data
from ml.train import get_dvc_data_hash, get_git_commit

COLUMNS = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

PARAM_GRID = {
    "logisticregression__C": [0.1, 1.0, 10.0, 100.0],
    "logisticregression__class_weight": [None, "balanced"],
}


def tune(dataset):
    data = clean_data(load_data(os.path.join("data", dataset)))
    x = data[COLUMNS].to_numpy()
    y = data["species"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=y
    )

    pipeline = make_pipeline(StandardScaler(), LogisticRegression(max_iter=500))
    search = GridSearchCV(
        pipeline,
        PARAM_GRID,
        scoring="f1_macro",
        cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
        n_jobs=-1,
    )
    search.fit(x_train, y_train)

    model = search.best_estimator_
    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions, average="macro")
    matrix = confusion_matrix(y_test, predictions)
    best_c = model.named_steps["logisticregression"].C
    best_weight = model.named_steps["logisticregression"].class_weight

    os.makedirs("models", exist_ok=True)
    model_file = os.path.abspath(os.path.join("models", "model_tuned.pkl"))
    joblib.dump(model, model_file)

    report = (
        "run: tuned-v2\n"
        f"dataset: {dataset}\n"
        f"best_params: C={best_c}, class_weight={best_weight}\n"
        f"cv_best_f1_macro: {search.best_score_:.4f}\n"
        f"accuracy: {accuracy:.4f}\n"
        f"f1_macro: {f1:.4f}\n\n"
        f"confusion matrix:\n{matrix}\n"
    )
    report_file = os.path.abspath(os.path.join("models", "report_tuned.txt"))
    with open(report_file, "w", encoding="utf-8") as file:
        file.write(report)

    mlflow.set_experiment("iris-classifier")
    with mlflow.start_run(run_name="tuned-v2"):
        mlflow.set_tag("stage", "challenger")
        mlflow.log_param("git_commit", get_git_commit())
        mlflow.log_param("dvc_data_hash", get_dvc_data_hash())
        mlflow.log_param("dataset_version", "tuned")
        mlflow.log_param("dataset_file", dataset)
        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_param("search", "GridSearchCV over C and class_weight")
        mlflow.log_param("search_candidates", str(len(search.cv_results_["params"])))
        mlflow.log_param("search_cv_folds", 5)
        mlflow.log_param("C", best_c)
        mlflow.log_param("class_weight", str(best_weight))
        mlflow.log_param("max_iter", 500)
        mlflow.log_param("use_scaler", True)
        mlflow.log_metric("cv_best_f1_macro", search.best_score_)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1_macro", f1)
        mlflow.log_artifact(model_file)
        mlflow.log_artifact(report_file)

    print(f"best params: C={best_c}, class_weight={best_weight}")
    print(f"cv best f1_macro: {search.best_score_:.4f}")
    print(f"tuned-v2: accuracy={accuracy:.4f} f1_macro={f1:.4f}")
    print(f"model saved to {model_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="iris_v2.csv")
    args = parser.parse_args()
    tune(args.dataset)
