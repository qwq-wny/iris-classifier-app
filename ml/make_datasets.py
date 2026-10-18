"""Create the two dataset versions (v1 and v2) from the sklearn iris data.

v1 = first usable version, but it still has some small problems
     (2 copied rows, 1 impossible value, and 6 rows with a wrong label).
v2 = the cleaned version (problems fixed, only the 150 real flowers).
"""

import os

import pandas as pd
from sklearn.datasets import load_iris


def make_dataframe():
    """Turn the sklearn iris data into a simple pandas table."""
    iris = load_iris()
    data = pd.DataFrame(
        iris.data,
        columns=["sepal_length", "sepal_width", "petal_length", "petal_width"],
    )
    data["species"] = [iris.target_names[n] for n in iris.target]
    return data


def make_v1(data):
    """Add small realistic data problems to the clean data."""
    v1 = pd.concat([data, data.iloc[[0, 1]]], ignore_index=True)

    # One impossible measurement (a typing mistake).
    v1.loc[0, "sepal_width"] = 50.0

    # Six rows where somebody wrote the wrong flower name.
    for row in [10, 40, 70, 90, 120, 140]:
        correct = v1.loc[row, "species"]
        if correct == "setosa":
            v1.loc[row, "species"] = "versicolor"
        else:
            v1.loc[row, "species"] = "setosa"

    return v1


def main():
    os.makedirs("data", exist_ok=True)
    data = make_dataframe()
    v1 = make_v1(data)
    v1.to_csv(os.path.join("data", "iris_v1.csv"), index=False)
    data.to_csv(os.path.join("data", "iris_v2.csv"), index=False)
    print(f"v1 saved with {len(v1)} rows")
    print(f"v2 saved with {len(data)} rows")


if __name__ == "__main__":
    main()
