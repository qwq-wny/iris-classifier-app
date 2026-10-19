# Current production model

- Model: LogisticRegression with StandardScaler (pipeline)
- Trained by: `python -m ml.train --version improved`
- Dataset: `data/iris_v2.csv` (cleaned version, tracked with DVC)
- MLflow run name: `improved-v2`
- MLflow run ID: `6e9ceeef46394dee9af782ba3d7ebbe9`
- Git commit of the training code: `8ec6f2f5f0b8914894a71d0d13c860667187499d`
- DVC data hash: `0fba930d9fb57b40b64019e040011e66.dir`
- Scores on the test set: accuracy = 0.9474, macro F1 = 0.9466
- MLflow artifact: `mlruns/1/6e9ceeef46394dee9af782ba3d7ebbe9/artifacts/model.pkl`
- File used by the app: `models/model.pkl`
- SHA-256 of `models/model.pkl`: `ac5498dd82fdfdac86cbffa5bf4d71bb5b3a82e50e15789dd0de7145a5cea8ee`
  (identical to the improved-v2 artifact, checked with `shasum -a 256`)

## Input contract

| Position | Field | Unit | Valid range |
|---|---|---|---|
| 1 | `sepal_length` | cm | 0 < x <= 30 |
| 2 | `sepal_width` | cm | 0 < x <= 30 |
| 3 | `petal_length` | cm | 0 < x <= 30 |
| 4 | `petal_width` | cm | 0 < x <= 30 |

Labels returned by the model: `setosa`, `versicolor`, `virginica`.

## Loading example

```python
import joblib

model = joblib.load("models/model.pkl")
flower = model.predict([[5.9, 2.8, 4.3, 1.3]])[0]
print(flower)  # versicolor
```

## Verification cases

`ml/registry/golden_sample.json` contains fixed inputs with the expected output,
plus the run ID, Git commit, DVC hash and model SHA-256. A quick check:

```python
import json
import joblib

sample = json.load(open("ml/registry/golden_sample.json", encoding="utf-8"))
model = joblib.load(sample["model"]["path"])
for case in sample["cases"]:
    assert model.predict([case["input"]])[0] == case["expected"], case
print(f"{len(sample['cases'])} cases passed")
```

## Challenger model (not in production)

`python -m ml.tune` trains a grid-search variant and saves it separately as
`models/model_tuned.pkl`. It is **not** loaded by the app.

| Item | Value |
|---|---|
| MLflow run ID | `6a6b28106bf9420694ba62a64a24979d` |
| Best parameters | `C=1.0`, `class_weight=None` |
| CV macro F1 (5-fold) | 0.9715 |
| Hold-out accuracy / macro F1 | 0.9211 / 0.9195 |
| Why not promoted | lower hold-out score than improved-v2 (0.9474 / 0.9466) |
