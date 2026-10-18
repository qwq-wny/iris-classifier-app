# Experiments documentation

All experiments are tracked with MLflow. The runs are saved in the `mlruns/`
folder (local file backend). You can open them with `mlflow ui`.

## Run 1: baseline-v1

- Dataset: iris_v1.csv (the first version, with small data problems)
- Model: LogisticRegression
- No scaler, C = 1.0
- Result: accuracy = 0.9474, f1_macro = 0.9478
- Saved model: `models/model.pkl` (this file was replaced by run 2)

## Run 2: improved-v2

- Dataset: iris_v2.csv (the cleaned version)
- Model: LogisticRegression inside a pipeline with StandardScaler
- C = 10.0 (tried a stronger setting)
- Result: accuracy = 0.9737, f1_macro = 0.9737

## Which model is used in production

The **improved-v2** model is used in the app because it has the best scores
on the test data (accuracy and macro F1). It was trained on the cleaned
dataset, so wrong values and copied rows did not teach it anything bad.

## The metric we optimize and why

The main metric is **macro F1**. It shows how well the model predicts all
three flower types. If the model only predicted the easy "setosa" class and
ignored the other two classes, macro F1 would drop. So macro F1 is a fair
metric for this multi-class problem. Accuracy is also recorded because it is
easy to explain.

(The exact numbers of every run can also be seen in the `mlruns/` folder or
with `mlflow ui`.)
