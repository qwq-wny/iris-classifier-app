# Experiments documentation

All experiments are tracked with MLflow. The runs are saved in the `mlruns/`
folder and `mlflow.db` (local backend). You can open them with `mlflow ui`.

## Traceability table

| Experiment | MLflow run ID | Git commit | DVC data hash | Accuracy | Macro F1 |
|---|---|---|---|---|---|
| baseline-v1 | `7c586a346c3945a89a25b09f13a70fec` | `0e0a9e41585facb72375944ba102bdab24979271` | `c4f884dbd8910a355ec91c2672ecaa68.dir` | 0.8684 | 0.8651 |
| improved-v2 | `6e9ceeef46394dee9af782ba3d7ebbe9` | `8ec6f2f5f0b8914894a71d0d13c860667187499d` | `0fba930d9fb57b40b64019e040011e66.dir` | 0.9474 | 0.9466 |
| tuned-v2 | `6a6b28106bf9420694ba62a64a24979d` | `2976a3f1809c53c74f76ca883be0fd62f96b097b` | `0fba930d9fb57b40b64019e040011e66.dir` | 0.9211 | 0.9195 |

Each run also carries a `stage` tag:

| run | `stage` tag | meaning |
|---|---|---|
| baseline-v1 | `baseline` | reference point, not used by the app |
| improved-v2 | `candidate` | the model in production |
| tuned-v2 | `challenger` | grid-search result, evaluated and rejected |

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

## Run 3: tuned-v2 (challenger)

- Dataset: iris_v2.csv (same cleaned data as improved-v2)
- Git commit: `2976a3f`
- DVC data hash: `0fba930d9fb57b40b64019e040011e66.dir`
- MLflow run ID: `6a6b28106bf9420694ba62a64a24979d`
- Search: `GridSearchCV` over `C` in {0.1, 1, 10, 100} and `class_weight`
  in {None, balanced}, 5-fold stratified CV, scoring macro F1 (8 candidates)
- Best parameters: `C=1.0`, `class_weight=None`
- Cross-validation: best macro F1 = 0.9715
- Hold-out test set: accuracy = 0.9211, macro F1 = 0.9195
- Artifacts: `models/model_tuned.pkl`, `models/report_tuned.txt`

**Result: the tuned model is worse than improved-v2 on the hold-out set**
(0.9211 against 0.9474). With only 149 rows, the hyperparameters that win inside
cross-validation do not automatically win on a 38-sample test set. The model is
therefore **not promoted**: the app keeps `models/model.pkl` from improved-v2.
`ml/tune.py` writes to a separate file on purpose, so a challenger can never
silently replace the production model.

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
