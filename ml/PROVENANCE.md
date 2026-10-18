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

- Python 3.12 (in Docker) / 3.14 (used on the student laptop)
- scikit-learn, pandas, flask, mlflow, dvc: see `requirements.txt` and
  `requirements-dev.txt`.

## Model artifacts

- `models/model.pkl` - the model used by the app (joblib format).
- `mlruns/` - the MLflow history of the two training runs.
