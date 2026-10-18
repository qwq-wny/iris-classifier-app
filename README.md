# Iris Classifier App

A very small machine learning project for a university course.
The app predicts the type of an iris flower (setosa, versicolor or virginica)
from 4 measurements: sepal length, sepal width, petal length and petal width.

The project shows the full workflow that the course asked for:

- a trained machine learning model (scikit-learn),
- tests for the app (pytest),
- Docker,
- CI/CD with GitHub Actions,
- data versioning with DVC,
- experiment tracking with MLflow.

## How the app works

1. The user opens the web page and types 4 numbers.
2. The numbers go to a logistic regression model.
3. The model answers with one flower name.

## Project structure

```
app/                  the Flask web app
ml/                   training code, configs and MLOps docs
data/                 csv files (tracked with DVC, not with git)
models/               the saved model (model.pkl)
tests/                pytest tests
.github/workflows/    CI and CD pipelines
Dockerfile            instructions to build the app image
```

## How to run it on your computer

```bash
python -m venv .venv
.venv\Scripts\activate        # on Windows
pip install -r requirements.txt -r requirements-dev.txt
python -m ml.train --version improved
python app/main.py
```

Then open http://127.0.0.1:5000 in a browser.

## How to run the tests

```bash
pytest -v
```

## How to run it with Docker

```bash
docker build -t iris-classifier-app .
docker run -p 5000:5000 iris-classifier-app
```

## How the data is versioned (DVC)

The csv files live in `data/` but they are NOT inside git.
Git only stores a small pointer file called `data.dvc`.
The real files are stored in an Azure Storage container.

To download the data:

```bash
pip install -r requirements-dev.txt
dvc pull
```

More details: [ml/README_data.md](ml/README_data.md)

## How the experiments are tracked (MLflow)

Every training run is saved to MLflow (folder `mlruns/`).
To see the runs with a simple UI:

```bash
mlflow ui
```

Then open http://127.0.0.1:5000.

More details: [ml/README_experiments.md](ml/README_experiments.md)

## How code goes from commit to production

1. New work is done in a `feature/...` branch.
2. A pull request merges the feature branch into `dev`.
   CI runs: tests + code checks + Docker build.
   The pull request can only be merged if CI is green.
3. A pull request merges `dev` into `staging`.
   The staging pipeline creates a staging `.env` file and builds the staging image.
4. A pull request merges `staging` into `main`.
   The production pipeline creates a production `.env` file and builds the
   production image.

| Branch | What it is for | Pipeline that runs |
|---|---|---|
| feature/... | new work | CI (when a PR is opened) |
| dev | combine features, run tests | CI on every push and PR |
| staging | test the app like production | CI on PR + staging build on merge |
| main | the final version | CI on PR + production build on merge |

More details: [DEPLOYMENT.md](DEPLOYMENT.md)
