"""Helper that loads the model and makes predictions."""

import os

import joblib

# Path to the saved model file (models/model.pkl).
MODEL_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "models", "model.pkl")
)

# The smallest and biggest size (in cm) we accept for each measurement.
MIN_VALUE = 0
MAX_VALUE = 30

INPUT_NAMES = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
]


def load_model():
    """Load the trained model from the models folder."""
    if not os.path.exists(MODEL_FILE):
        raise FileNotFoundError("Model file is missing. Run ml/train.py first.")
    return joblib.load(MODEL_FILE)


def check_input(values):
    """Check that every number is inside a normal range for iris flowers."""
    for name, value in zip(INPUT_NAMES, values):
        if value <= MIN_VALUE or value > MAX_VALUE:
            raise ValueError(f"{name} must be between 0 and 30 cm.")


def predict_iris(sepal_length, sepal_width, petal_length, petal_width):
    """Take 4 flower measurements and return the flower name."""
    values = [sepal_length, sepal_width, petal_length, petal_width]
    check_input(values)
    model = load_model()
    flower = model.predict([values])[0]
    return flower
