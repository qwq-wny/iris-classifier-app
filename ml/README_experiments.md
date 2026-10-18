# Experiments documentation

All experiments are tracked with MLflow. The runs are saved in the `mlruns/`
folder and `mlflow.db` (local backend). You can open them with `mlflow ui`.

## Run 1: baseline-v1

- Dataset: iris_v1.csv (the first version, with data problems)
- Git commit of the dataset: `0e0a9e4`
- Model: LogisticRegression
- No scaler, C = 1.0
- Result: accuracy = 0.8684, f1_macro = 0.8651

The wrong labels in the data confused the model, so the score is not great.

## Run 2: improved-v2

- Dataset: iris_v2.csv (the cleaned version)
- Git commit of the dataset: `8ec6f2f`
- Model: LogisticRegression inside a pipeline with StandardScaler
- C = 10.0 (a stronger setting, tested during tuning)
- Result: accuracy = 0.9474, f1_macro = 0.9466

Cleaning the data and scaling the numbers made the model clearly better.

## Which model is used in production

The **improved-v2** model is used in the app because it has the best scores
on the test data (accuracy 0.9474 and macro F1 0.9466, against 0.8684 and
0.8651 for the baseline). It was trained on the cleaned dataset, so wrong
labels and copies did not teach it anything bad.

## The metric we optimize and why

The main metric is **macro F1**. It shows how well the model predicts all
three flower types. If the model only predicted the easy "setosa" class and
ignored the other two classes, macro F1 would drop. So macro F1 is a fair
metric for this multi-class problem. Accuracy is also recorded because it is
easy to explain.
