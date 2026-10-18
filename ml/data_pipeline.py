"""Load and clean the iris data used for training."""

import pandas as pd

# The columns our csv files must have.
COLUMNS = ["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]


def load_data(path):
    """Read one csv file and check that the columns are correct."""
    data = pd.read_csv(path)
    if list(data.columns) != COLUMNS:
        raise ValueError(f"Wrong columns in {path}: {list(data.columns)}")
    return data


def clean_data(data):
    """Remove rows that are broken: empty cells, copies, and outliers."""
    rows_before = len(data)
    data = data.dropna()
    data = data.drop_duplicates()
    data = data[data["sepal_width"] <= 10]
    rows_after = len(data)
    print(f"Cleaning: {rows_before} rows -> {rows_after} rows")
    return data
