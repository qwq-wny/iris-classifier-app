# Current production model

- Model: LogisticRegression with StandardScaler (pipeline)
- Trained by: `python -m ml.train --version improved`
- Dataset: `data/iris_v2.csv` (cleaned version, tracked with DVC)
- MLflow run name: `improved-v2`
- Scores on the test set: accuracy = 0.9474, macro F1 = 0.9466
- File used by the app: `models/model.pkl`
