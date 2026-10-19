"""Train the iris model and save everything to MLflow."""

import argparse
import json
import os
import subprocess

import joblib
import mlflow
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from ml.data_pipeline import clean_data, load_data


def get_git_commit():
    """Return the current git commit (so we know which code trained the model)."""
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def get_dvc_data_hash():
    """Return the DVC hash of the data folder, read from data.dvc."""
    try:
        with open("data.dvc", encoding="utf-8") as file:
            for line in file:
                key, _, value = line.strip().removeprefix("-").strip().partition(":")
                if key == "md5":
                    return value.strip()
    except OSError:
        pass
    return "unknown"


def load_config(version):
    """Read the json config file for one experiment."""
    config_path = os.path.join(os.path.dirname(__file__), "configs", f"{version}.json")
    with open(config_path, encoding="utf-8") as file:
        return json.load(file)


def build_model(config):
    """Create the model. The improved version also scales the numbers first."""
    if config["use_scaler"]:
        return make_pipeline(
            StandardScaler(),
            LogisticRegression(C=config["C"], max_iter=config["max_iter"]),
        )
    return LogisticRegression(C=config["C"], max_iter=config["max_iter"])


def train(version):
    config = load_config(version)

    data = load_data(os.path.join("data", config["dataset"]))
    if config["clean_data"]:
        data = clean_data(data)

    x = data[["sepal_length", "sepal_width", "petal_length", "petal_width"]].to_numpy()
    y = data["species"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=y
    )

    model = build_model(config)
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    accuracy = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions, average="macro")
    matrix = confusion_matrix(y_test, predictions)

    os.makedirs("models", exist_ok=True)
    model_file = os.path.abspath(os.path.join("models", "model.pkl"))
    joblib.dump(model, model_file)

    report = (
        f"run: {config['run_name']}\n"
        f"dataset: {config['dataset']}\n"
        f"accuracy: {accuracy:.4f}\n"
        f"f1_macro: {f1:.4f}\n\n"
        f"confusion matrix:\n{matrix}\n"
    )
    report_file = os.path.abspath(os.path.join("models", "report.txt"))
    with open(report_file, "w", encoding="utf-8") as file:
        file.write(report)

    mlflow.set_experiment("iris-classifier")
    with mlflow.start_run(run_name=config["run_name"]):
        mlflow.log_param("git_commit", get_git_commit())
        mlflow.log_param("dvc_data_hash", get_dvc_data_hash())
        mlflow.log_param("dataset_version", version)
        mlflow.log_param("dataset_file", config["dataset"])
        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_param("C", config["C"])
        mlflow.log_param("max_iter", config["max_iter"])
        mlflow.log_param("use_scaler", config["use_scaler"])
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1_macro", f1)
        mlflow.log_artifact(model_file)
        mlflow.log_artifact(report_file)

    print(f"{version}: accuracy={accuracy:.4f} f1_macro={f1:.4f}")
    print(f"model saved to {model_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", choices=["baseline", "improved"], required=True)
    args = parser.parse_args()
    train(args.version)
