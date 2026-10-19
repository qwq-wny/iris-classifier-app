# Experiments documentation

All experiments are tracked with MLflow. The runs are saved in the `mlruns/`
folder and `mlflow.db` (local backend). You can open them with `mlflow ui`.

## Traceability table

| Experiment | MLflow run ID | Git commit | DVC data hash | Accuracy | Macro F1 |
|---|---|---|---|---|---|
| baseline-v1 | `7c586a346c3945a89a25b09f13a70fec` | `0e0a9e41585facb72375944ba102bdab24979271` | `c4f884dbd8910a355ec91c2672ecaa68.dir` | 0.8684 | 0.8651 |
| improved-v2 | `6e9ceeef46394dee9af782ba3d7ebbe9` | `8ec6f2f5f0b8914894a71d0d13c860667187499d` | `0fba930d9fb57b40b64019e040011e66.dir` | 0.9474 | 0.9466 |

Every run stores `git_commit` and `dvc_data_hash` as MLflow params, so a run can
be traced back to exact code and exact data. The artifact paths are relative to
the repository root (`mlruns/<experiment_id>/<run_id>/artifacts`), so the runs
open on any machine that has the repository.

## Run 1: baseline-v1

- Dataset: iris_v1.csv (the first version, with data problems)
- Git commit of the dataset: `0e0a9e4`
- DVC data hash: `c4f884dbd8910a355ec91c2672ecaa68.dir`
- MLflow run ID: `7c586a346c3945a89a25b09f13a70fec`
- Model: LogisticRegression
- No scaler, C = 1.0
- Result: accuracy = 0.8684, f1_macro = 0.8651

The wrong labels in the data confused the model, so the score is not great.

## Run 2: improved-v2

- Dataset: iris_v2.csv (the cleaned version)
- Git commit of the dataset: `8ec6f2f`
- DVC data hash: `0fba930d9fb57b40b64019e040011e66.dir`
- MLflow run ID: `6e9ceeef46394dee9af782ba3d7ebbe9`
- Model: LogisticRegression inside a pipeline with StandardScaler
- C = 10.0 (a stronger setting, tested during tuning)
- Result: accuracy = 0.9474, f1_macro = 0.9466

Cleaning the data and scaling the numbers made the model clearly better.

## Which model is used in production

The **improved-v2** model is used in the app because it has the best scores
on the test data (accuracy 0.9474 and macro F1 0.9466, against 0.8684 and
0.8651 for the baseline). It was trained on the cleaned dataset, so wrong
labels and copies did not teach it anything bad.

| Item | Value |
|---|---|
| MLflow run ID | `6e9ceeef46394dee9af782ba3d7ebbe9` |
| Git commit of the code | `8ec6f2f5f0b8914894a71d0d13c860667187499d` |
| DVC data hash | `0fba930d9fb57b40b64019e040011e66.dir` |
| Model artifact | `mlruns/1/6e9ceeef46394dee9af782ba3d7ebbe9/artifacts/model.pkl` |
| Model used by the app | `models/model.pkl` (SHA-256 `ac5498dd82fdfdac86cbffa5bf4d71bb5b3a82e50e15789dd0de7145a5cea8ee`) |
| Verification cases | `ml/registry/golden_sample.json` |

## The metric we optimize and why

The main metric is **macro F1**. It shows how well the model predicts all
three flower types. If the model only predicted the easy "setosa" class and
ignored the other two classes, macro F1 would drop. So macro F1 is a fair
metric for this multi-class problem. Accuracy is also recorded because it is
easy to explain.
