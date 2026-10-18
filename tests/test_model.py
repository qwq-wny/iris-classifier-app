"""Tests for the saved model and the predict helper."""

import os

import pytest

from app.predict import MODEL_FILE, load_model, predict_iris


def test_model_file_exists():
    assert os.path.exists(MODEL_FILE)


def test_model_can_be_loaded():
    model = load_model()
    assert model is not None


@pytest.mark.parametrize(
    "values,expected",
    [
        ((5.1, 3.5, 1.4, 0.2), "setosa"),
        ((5.9, 2.8, 4.3, 1.3), "versicolor"),
        ((7.2, 3.0, 5.8, 1.6), "virginica"),
    ],
)
def test_model_knows_real_flowers(values, expected):
    assert predict_iris(*values) == expected


@pytest.mark.parametrize("bad_value", [-5, 31, 1000])
def test_model_rejects_crazy_numbers(bad_value):
    with pytest.raises(ValueError):
        predict_iris(bad_value, 3.5, 1.4, 0.2)
