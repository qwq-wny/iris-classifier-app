# Provenance

This file explains where everything in this project comes from, so the
project can be reproduced later.

## Data source

- Name: Iris Flower Dataset
- Source: scikit-learn built-in dataset (`sklearn.datasets.load_iris`)
- Original creator: R.A. Fisher (1936), this copy is distributed with
  scikit-learn under its BSD license.
- The script that created the csv files: `ml/make_datasets.py`

## How the csv files were made

```bash
python ml/make_datasets.py
```

- v1: the 150 original rows + 2 copied rows + 1 wrong value
  (this was done on purpose to show a "dirty" first dataset).
- v2: the 150 original rows, nothing added or changed.

## Training

```bash
python -m ml.train --version baseline
python -m ml.train --version improved
```

- Split: 75% train / 25% test, `random_state=42`, stratified by class.
- The random seed is fixed, so training gives the same result every time.

## Software versions

- Python 3.12 (base image in the Dockerfile)
- Python 3.13.15 (used to verify the project locally on macOS)
- Versions that were verified locally: scikit-learn 1.9.1, pandas 3.0.6,
  flask 3.1.3, mlflow 3.17.1, dvc 3.67.1
- The full dependency list is in `requirements.txt` and `requirements-dev.txt`.

## Model artifacts

- `models/model.pkl` - the model used by the app (joblib format).
- `mlruns/` - the MLflow history of the two training runs.

## Traceability table (Git - DVC - MLflow - model)

| Layer | baseline-v1 | improved-v2 |
|---|---|---|
| Git commit (data) | `0e0a9e4` | `8ec6f2f` |
| DVC hash | `c4f884dbd8910a355ec91c2672ecaa68.dir` | `0fba930d9fb57b40b64019e040011e66.dir` |
| MLflow run ID | `7c586a346c3945a89a25b09f13a70fec` | `6e9ceeef46394dee9af782ba3d7ebbe9` |
| Accuracy / macro F1 | 0.8684 / 0.8651 | 0.9474 / 0.9466 |
| Artifact path | `mlruns/1/7c586a346c3945a89a25b09f13a70fec/artifacts/` | `mlruns/1/6e9ceeef46394dee9af782ba3d7ebbe9/artifacts/` |
| Used by the app | no | yes (`models/model.pkl`) |

The app model `models/model.pkl` and the improved-v2 artifact have the same
SHA-256 (`ac5498dd82fdfdac86cbffa5bf4d71bb5b3a82e50e15789dd0de7145a5cea8ee`),
and `models/report.txt` is identical to the artifact report.
